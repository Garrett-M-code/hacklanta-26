# Update package list first
echo "Updating package list..."
sudo apt update

# Check if curl is instaled
if ! command -v curl &> /dev/null; then
  echo "curl is not installed. Installing..."
  sudo apt update && sudo apt install -y curl
fi

# check if pip3 is installed
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
  echo "pip3 is not installed. Installing..."
  sudo apt update && sudo apt install -y python3-pip
fi

# installing dependencies
echo "Checking Python dependencies..."
if pip3 list 2>/dev/null | grep -q "^keyboard "; then
    echo "✓ keyboard package is already installed"
else
    echo "Installing keyboard package..."
    if sudo pip3 install --break-system-packages keyboard; then
        echo "✓ keyboard package installed successfully"
    else
        echo "✗ Failed to install keyboard package"
        exit 1
    fi
fi

# Check if ollama binary exists
if [ -f /usr/local/bin/ollama ] || [ -f /usr/bin/ollama ]; then
    echo "✓ ollama binary found, skipping installation"
else
    echo "Installing ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
fi

# Wait for ollama to start (adds a small delay)
echo "Waiting for ollama to start..."
sleep 3


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

# Check if the model is already downloaded
echo "Checking for deepseek-r1:1.5b model..."

if ollama list | grep -q "deepseek-r1:1.5b"; then
    echo "✓ Model deepseek-r1:1.5b is already downloaded"
    echo "  Skipping download..."
else
    echo "Downloading deepseek-r1:1.5b..."
    if ollama pull deepseek-r1:1.5b; then
        echo "✓ Download completed successfully"
    else
        echo "✗ Download failed"
        exit 1
    fi
fi

echo ""
echo "========================================="
echo "✓ Setup complete! ollama is ready to use"
echo "========================================="
echo ""
