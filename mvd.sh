#!/bin/bash

# Function to resolve the actual directory of the script
function get_script_dir {
    local SOURCE="${BASH_SOURCE[0]}"
    while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
        local DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
        SOURCE="$(readlink "$SOURCE")"
        [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
    done
    DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
    echo "$DIR"
}

# Determine the directory where the script resides
SCRIPT_DIR=$(get_script_dir)

# Activate the virtual environment
source "$SCRIPT_DIR/.venv/bin/activate"

# Run the Python script
python "$SCRIPT_DIR/mvd.py"

# Deactivate the environment
deactivate