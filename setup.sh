#!/bin/bash
set -e

# JDK
if ! java -version &>/dev/null; then
    echo "Installing OpenJDK via Homebrew..."
    brew install openjdk
    echo 'export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"' >> ~/.zshrc
    export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"
else
    echo "JDK already installed: $(java -version 2>&1 | head -1)"
fi

# Python venv
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt

echo "Setup complete. Run: source .venv/bin/activate"
