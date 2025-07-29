#!/bin/bash

set -e  # Exit on any error

apt update && apt install -y gh jq

curl -LsSf https://astral.sh/uv/install.sh | sh

curl -qL https://www.npmjs.com/install.sh | sh
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm install node
npm install -g @anthropic-ai/claude-code @openai/codex @google/gemini-cli 
# @qwen-code/qwen-code
