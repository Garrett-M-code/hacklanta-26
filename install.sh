# Update package list first
echo "Updating package list..."
sudo apt update

# Check if curl is instaled
if ! command -v curl &> /dev/null; then
  echo "curl is not installed. Installing..."
  sudo apt update && sudo apt install -y curl
fi

# Check if pip3 is installed
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
  echo "pip3 is not installed. Installing..."
  sudo apt update && sudo apt install -y python3-pip
fi

# Install system Python packages
echo "Installing system Python packages..."
sudo apt-get install -y python3-tk python3-dev

# Installing dependencies
# Check and install keyboard
echo "Checking Python dependencies..."
if pip3 list 2>/dev/null | grep -q "^keyboard "; then
    echo "✓ keyboard package is already installed"
else
    echo "Installing keyboard package..."
    if pip3 install --break-system-packages keyboard; then
        echo "✓ keyboard package installed successfully"
    else
        echo "✗ Failed to install keyboard package"
        exit 1
    fi
fi

# Check and install pynput
if pip3 list 2>/dev/null | grep -q "^pynput "; then
    echo "✓ pynput package is already installed"
else
    echo "Installing pynput package..."
    # Try user installation first
    if pip3 install --user pynput 2>/dev/null; then
        echo "✓ pynput package installed successfully (user mode)"
    # If user install fails, try with --break-system-packages (for newer Ubuntu)
    elif pip3 install --break-system-packages pynput 2>/dev/null; then
        echo "✓ pynput package installed successfully (system override)"
    # Last resort: try with sudo
    elif sudo pip3 install pynput 2>/dev/null; then
        echo "✓ pynput package installed successfully (system-wide)"
    else
        echo "✗ Failed to install pynput package"
        exit 1
    fi
fi

# Check and Install xdotool for X11 automation
echo "Installing xdotool..."
if ! command_exists xdotool; then
    sudo apt-get install -y xdotool
    echo "✓ xdotool installed successfully"
else
    echo "✓ xdotool is already installed"
fi

# Check if ollama binary exists
if [ -f /usr/local/bin/ollama ] || [ -f /usr/bin/ollama ]; then
    echo "✓ ollama binary found, skipping installation"
else
    echo "Installing ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
fi

# Install python3-ollama for Python Ollama bindings
echo "Installing python3-ollama..."
if apt list --installed 2>/dev/null | grep -q "python3-ollama"; then
    echo "✓ python3-ollama is already installed"
else
    sudo apt-get install -y python3-ollama
    echo "✓ python3-ollama installed successfully"
fi

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
