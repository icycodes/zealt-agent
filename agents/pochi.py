import os
import json
import shlex
import shutil

from harbor.models.agent.context import AgentContext
from harbor.models.trial.paths import EnvironmentPaths
from harbor.agents.installed.base import BaseInstalledAgent, ExecInput
from pydantic import BaseModel
from pathlib import Path

from harbor.models.trajectories import (
    Trajectory,
    Step,
    ToolCall,
    Observation,
    ObservationResult,
    FinalMetrics,
    Agent,
)


class ExecInput(BaseModel):
    command: str
    cwd: str | None = None
    env: dict[str, str] | None = None
    timeout_sec: int | None = None

class Pochi(BaseInstalledAgent):
    @staticmethod
    def name() -> str:
        return "pochi"

    @property
    def _install_agent_template_path(self) -> Path:
        return Path(__file__).parent / "install-pochi.sh.j2"

    def create_run_agent_commands(self, instruction: str) -> list[ExecInput]:
        escaped_instruction = shlex.quote(instruction)

        model = self.model_name if self.model_name else "google/gemini-3.1-pro"

        env = {
            "POCHI_API_KEY": os.environ.get("POCHI_API_KEY", "")
        }

        return [
            ExecInput(
                command=(
                    "pochi "
                    f"--model {model} "
                    f"--prompt {escaped_instruction} "
                    "--stream-json "
                    f"--output-result > >(tee /logs/agent/pochi-stdout.log) 2> >(tee /logs/agent/pochi-stderr.log >&2) "
                ),
                env=env,
            ),
        ]

    def _convert_pochi_to_atif(
        self, log_lines: list[str]
    ) -> Trajectory | None:
        """Convert Pochi trajectory format to ATIF format."""
        if not log_lines:
            return None

        steps: list[Step] = []
        step_id = 1

        total_input_tokens = 0
        total_output_tokens = 0
        total_cached_tokens = 0
        session_id = "unknown"

        for line in log_lines:
            if not line.strip():
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue

            msg_id = msg.get("id", "unknown")
            if session_id == "unknown" and msg_id != "unknown":
                session_id = msg_id

            role = msg.get("role")

            if role == "user":
                text_parts = [p.get("text", "") for p in msg.get("parts", []) if p.get("type") == "text"]
                content = "\n".join(text_parts)
                steps.append(
                    Step(
                        step_id=step_id,
                        source="user",
                        message=content,
                    )
                )
                step_id += 1
            elif role == "assistant":
                metadata = msg.get("metadata", {})
                tokens = metadata.get("totalTokens", 0)
                total_output_tokens += tokens

                parts = msg.get("parts", [])

                current_reasoning = []
                current_tools = []
                current_observations = []
                current_text = []

                def _flush_step():
                    nonlocal step_id, current_reasoning, current_tools, current_observations, current_text
                    if current_tools or current_reasoning or current_observations or current_text:
                        reasoning_content = "\n".join(current_reasoning) if current_reasoning else None
                        obs = Observation(results=list(current_observations)) if current_observations else None
                        message_content = "\n".join(current_text) if current_text else (reasoning_content or "")

                        steps.append(
                            Step(
                                step_id=step_id,
                                source="agent",
                                message=message_content,
                                reasoning_content=reasoning_content,
                                tool_calls=list(current_tools) if current_tools else None,
                                observation=obs,
                                model_name=self.model_name or "google/gemini-3.1-pro"
                            )
                        )
                        step_id += 1
                        current_reasoning.clear()
                        current_tools.clear()
                        current_observations.clear()
                        current_text.clear()

                for part in parts:
                    ptype = part.get("type")
                    if ptype == "step-start":
                        _flush_step()
                    elif ptype == "reasoning":
                        current_reasoning.append(part.get("text", ""))
                    elif ptype == "text":
                        current_text.append(part.get("text", ""))
                    elif ptype and ptype.startswith("tool-"):
                        tool_name = ptype[5:]  # remove "tool-"
                        tool_call_id = part.get("toolCallId", "")
                        args = part.get("input", {})
                        current_tools.append(
                            ToolCall(
                                tool_call_id=tool_call_id,
                                function_name=tool_name,
                                arguments=args,
                            )
                        )
                        output_data = part.get("output")
                        if output_data is not None:
                            if isinstance(output_data, dict) and "output" in output_data:
                                obs_content = output_data["output"]
                            else:
                                obs_content = str(output_data)
                            current_observations.append(
                                ObservationResult(
                                    source_call_id=tool_call_id,
                                    content=obs_content,
                                )
                            )

                _flush_step()

        if not steps:
            return None

        final_metrics = FinalMetrics(
            total_prompt_tokens=total_input_tokens,
            total_completion_tokens=total_output_tokens,
            total_cached_tokens=total_cached_tokens,
            total_steps=len(steps),
        )

        trajectory = Trajectory(
            schema_version="ATIF-v1.6",
            session_id=session_id,
            agent=Agent(
                name="pochi",
                version="unknown",
                model_name=self.model_name or "google/gemini-3.1-pro",
            ),
            steps=steps,
            final_metrics=final_metrics,
        )
        return trajectory

    def populate_context_post_run(self, context: AgentContext) -> None:
        pochi_log_path = self.logs_dir / "pochi-stdout.log"
        if not pochi_log_path.exists():
            print(f"Pochi log not found at {pochi_log_path}")
            return

        try:
            log_lines = pochi_log_path.read_text().splitlines()
        except Exception as e:
            print(f"Error loading Pochi log: {e}")
            return

        # Calculate token counts for context
        n_input_tokens = 0
        n_output_tokens = 0
        n_cache_tokens = 0

        for line in log_lines:
            if not line.strip():
                continue
            try:
                msg = json.loads(line)
                if msg.get("role") == "assistant":
                    metadata = msg.get("metadata", {})
                    # Pochi log only has totalTokens in metadata currently
                    n_output_tokens += metadata.get("totalTokens", 0)
            except Exception:
                continue

        context.n_input_tokens = n_input_tokens
        context.n_output_tokens = n_output_tokens
        context.n_cache_tokens = n_cache_tokens

        try:
            atif_trajectory = self._convert_pochi_to_atif(log_lines)
            if atif_trajectory:
                atif_path = self.logs_dir / "trajectory.json"
                with open(atif_path, "w") as f:
                    json.dump(atif_trajectory.to_json_dict(), f, indent=2)
        except Exception as e:
            print(f"Error converting Pochi trajectory to ATIF: {e}")

        print(f"done saving logs to dir {self.logs_dir}")