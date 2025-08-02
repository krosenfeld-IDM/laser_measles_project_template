#!/bin/bash

set -e  # Exit on any error

apt update && apt install -y gh jq

curl -LsSf https://astral.sh/uv/install.sh | sh

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
export NVM_DIR="/usr/local/share/nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
nvm install node
npm install -g @anthropic-ai/claude-code @openai/codex @google/gemini-cli 
# @qwen-code/qwen-code

# Install git-cliff via cargo
cargo install git-cliff
