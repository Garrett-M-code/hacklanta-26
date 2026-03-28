# installing dependencies
pip install keyboard

# Installing ollama 
curl -fsSL https://ollama.com/install.sh | sh

# Wait for ollama to start (adds a small delay)
echo "Waiting for ollama to start..."
sleep 3

# Checking ollama is running
STATUS=$(curl -o /dev/null -s -w "%{http_code}\n" "http://localhost:11434")

if [ "$STATUS" -eq 200 ] || [ "$STATUS" -eq 301 ] || [ "$STATUS" -eq 302 ]; then
  # continue with intall script if ollama is running
  echo "ollama is running (Status: $STATUS)"
  
  echo "Downloading deepseek-r1:1.5b..."
  if ollama pull deepseek-r1:1.5b; then
    echo "✓ Download completed successfully"
  else
    echo "✗ Download failed"
    exit 1
  fi
else  
  # stop install script if ollama is not running
  echo "ollama is not running (Status: $STATUS)"
  exit 1
fi
