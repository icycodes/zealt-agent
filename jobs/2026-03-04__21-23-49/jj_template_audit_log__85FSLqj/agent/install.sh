#!/bin/bash
set -euo pipefail

apt-get update
apt-get install -y curl ripgrep

# Install Pochi

curl -v -fsSL https://getpochi.com/install.sh | bash


ln -s ~/.pochi/bin/pochi /usr/local/bin/pochi

pochi --version