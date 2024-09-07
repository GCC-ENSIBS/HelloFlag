#!/bin/bash

# Define the directories to check and create if they don't exist
directories=("./codimd" "./codimd/database-data" "./codimd/upload-data")

# Loop through each directory
for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "Directory $dir does not exist. Creating it now."
        mkdir -p "$dir"
    else
        echo "Directory $dir already exists."
    fi
done

echo "All necessary directories have been checked and created if needed."

# Launch app
sudo chmod 777 ./codimd -R
docker compose up --build
