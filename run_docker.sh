#!/bin/bash

# Check if .env file exists or has placeholder
if [ ! -f .env ] || grep -q "your_api_key_here" .env; then
    if [ -f src/.env.local ]; then
        echo "Found src/.env.local, updating .env for Docker..."
        cp src/.env.local .env
    elif [ -f .env.local ]; then
        echo "Found .env.local, updating .env for Docker..."
        cp .env.local .env
    fi
fi

# Final check to ensure GEMINI_API_KEY is set
if [ ! -f .env ] || grep -q "your_api_key_here" .env; then
    echo "Error: .env file is missing or contains the placeholder API key."
    echo "Please edit the .env file in the root directory and add your GEMINI_API_KEY."
    [ ! -f .env ] && echo "GEMINI_API_KEY=your_api_key_here" > .env
    exit 1
fi

# Ensure GEMINI_MODEL is also exported if it exists in .env
export $(grep -v '^#' .env | xargs)


# Build and start the containers
echo "Building and starting the Docker containers..."
docker compose up --build -d

echo "------------------------------------------------"
echo "Application is starting up!"
echo "API will be available at: http://localhost:8000"
echo "Interactive docs: http://localhost:8000/docs"
echo "------------------------------------------------"
echo "To view logs, run: docker compose logs -f"
echo "To stop the application, run: docker compose down"
