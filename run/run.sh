#!/usr/bin/env bash

main_dir=$HOME/Desktop/tg-bot/telegram-bot

# Check if python is installed.
if !command -v python3 &>/dev/null; then
    echo "Python3 is not installed. Please install Python3 to continue."
    exit 1
fi

# Check if pip is installed.
if !command -v pip&>/dev/null; then
    echo "pip is not installed. Installing pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
fi

# Creating a virtual environment.
VENV_DIR = "venv"
if [! -d "$VENV_DIR"]; then
    echo "Creating a virtual environment..."
    python3 -m venv $VENV_DIR
fi

source $VENV_DIR/bin/activate

# Installing modules in the requirements.txt
echo "Installing requirements..."
cd ..
chmod +x requirements.txt
pip3 install -r $main_dir/requirements.txt

# Running the main.py
echo "Running the script..."
cd $main_dir/bot
chmod +x main.py
python3 main.py

