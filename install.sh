#!/bin/bash

#!/bin/bash

# Step 1: Check if Pipenv is installed
if ! command -v pipenv &> /dev/null
then
    echo "Pipenv could not be found, installing..."
    pip install pipenv
    if [ $? -ne 0 ]; then
        echo "Failed to install Pipenv. Please install it manually."
        exit 1
    fi
fi

# Check if a virtual environment already exists
if [ -d "$(pipenv --venv)" ]; then
    echo "A virtual environment already exists."
    read -p "Do you want to update/reinstall dependencies? (y/n): " -n 1 -r
    echo    # move to a new line
    if [[ ! $REPLY =~ ^[Yy]$ ]]
    then
        echo "Update cancelled."
        exit 1
    fi
fi

# Set the environment variable to create the virtual environment inside the project directory
export PIPENV_VENV_IN_PROJECT="true"

# Step 3: Navigate to the script's directory
cd "$(dirname "$0")"

# Step 4: Install dependencies using Pipenv
echo "Installing dependencies..."
pipenv install

echo "Installation completed. Run mvd.sh to get strated."
