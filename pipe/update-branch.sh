#!/usr/bin/env bash

display_usage() {
    echo "Usage: $0 [branch_name] [project_path]"
    echo "    [branch_name]  The name of the branch to checkout and pull."
    echo "    [project_path]  The path to your MagicMirror project directory."
}

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Error: Insufficient arguments provided."
    display_usage
    exit 1
fi

BRANCH=$1
PROJECT_PATH=$2

# Stop pm2
echo "Stopping MagicMirror pm2 process..."
pm2 stop magicmirror

# Check if dir exists
if [ ! -d "$PROJECT_PATH" ]; then
    echo "Error: Project directory not found at $PROJECT_PATH."
    display_usage
    exit 1
fi

cd "$PROJECT_PATH"

# update
echo "Updating repository and checking out branch $BRANCH..."
git fetch origin
git checkout "$BRANCH"
git pull origin "$BRANCH"

# hotfix electron sometimes not working. remove for production
if [ -d "node_modules/electron" ]; then
    rm -rf node_modules/electron
    echo "Removed node_modules/electron directory."
fi

# modules
MODULES_PATH="$PROJECT_PATH/modules"

# Check if the modules directory exists
if [ ! -d "$MODULES_PATH" ]; then
    echo "Error: Modules directory not found at $MODULES_PATH."
    display_usage
    exit 1
fi

# Loop through each module and install dependencies
echo "Installing dependencies for all modules..."
cd "$MODULES_PATH"

for MODULE in */; do
    if [ -d "$MODULE" ]; then
        echo "Installing dependencies for module: $MODULE"
        if [ -f "$MODULE/package.json" ]; then
            cd "$MODULE" && npm install && cd ..
            echo "Successfully installed dependencies for $MODULE"
        else
            echo "No package.json found in $MODULE. Skipping..."
        fi
    fi
done

# Set the DISPLAY environment variable
export DISPLAY=:0

# start pm2 
echo "Starting MagicMirror pm2 process..."
pm2 start magicmirror

echo "Process completed successfully."
