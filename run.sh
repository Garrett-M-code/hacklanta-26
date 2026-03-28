# Check if ollama is running and start if needed
echo "Checking if ollama is running..."

# Try to connect to ollama
if curl -s "http://localhost:11434" >/dev/null 2>&1; then
    echo "✓ ollama is already running"
else
    echo "ollama is not running, attempting to start..."
    
    # Try to start via systemd first (if installed as service)
    if systemctl list-units --full -all | grep -q ollama.service; then
        echo "Starting ollama service..."
        sudo systemctl start ollama
        sleep 3
    else
        # Start manually
        echo "Starting ollama manually..."
        ollama serve > /tmp/ollama.log 2>&1 &
        sleep 3
    fi
    
    # Verify it started
    if curl -s "http://localhost:11434" >/dev/null 2>&1; then
        echo "✓ ollama started successfully"
    else
        echo "✗ Failed to start ollama"
        exit 1
    fi
fi

# pull the model
ollama pull deepseek-r1:1.5b

# run the python script 
sudo Python main.py 



