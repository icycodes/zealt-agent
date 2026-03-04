import os
import json
import shlex
import shutil

from harbor.models.agent.context import AgentContext
from harbor.models.trial.paths import EnvironmentPaths
from harbor.agents.installed.base import BaseInstalledAgent, ExecInput
from pydantic import BaseModel
from pathlib import Path


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

    def populate_context_post_run(self, context: AgentContext) -> None:
        trajectory_path = self.logs_dir / "trajectory.json"
        if trajectory_path.exists():
            with open(trajectory_path, "r") as f:
                trajectory = json.load(f)
            context.trajectory = trajectory

        # copy trajectory to /logs/artifacts/
        if trajectory_path.exists():
            shutil.copy(trajectory_path, self.artifacts_dir / "trajectory.json")
        print(f"log dir {self.logs_dir}")