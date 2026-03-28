import keyboard
import logging
import sys
import time
import os

# Configure the logger
logging.basicConfig(
    filename='app_history.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def settings():
	print("WARNING: This program is very destructive.")
	print("WARNING: The makers of said program are not liable for any damadges.")
	print("WARNING: Use at your own risk, preferably in virutal environments.")
	print("WARNING: This program requires administrative privliages.")
	print("WARNING: Do you understand these terms? (y/n) ")
	agreement = input()
	if (agreement.upper() != 'Y'):
		print("EXITING")
		logging.info("Agreement Denied")
		on_exit_signal()
	
	logging.info("Agreement Accpeted")

	print("Starting at level one. There are three levels possible.")
	
	answer = -1
	while ((answer != 1) and (answer != 2)):
		print("Do you want prompts to be SFW (1) or NSFW (2)?\n")
		answer = input()
		
	logging.info(f"Mode selected (SFW=1, NSFW=2): {answer}")
	
	print("Have fun!")

def prompting(prompt, model='llama3'):
	try:
        response = ollama.chat(model=model, messages=[
            {'role': 'user', 'content': prompt},
        ])
        
        answer = response['message']['content']
        print(f"AI: {answer[:50]}...")
        logging.info(f"AI: {answer[:50]}...")
        return answer
    except Exception as e:
        logging.error(f"Failed to connect to AI: {e}")
        return "Error: Could not reach Ollama. Is it running?"
	


# Manages keyboard exits on the computer!
def on_exit_signal():
    exit_msg = "CTRL+ALT+TAB+B detected. Shutting down application."
    print(f"\n[Terminating] {exit_msg}")
    
    # Write to the log file and exit
    logging.info(exit_msg)
    logging.shutdown()
    
    # Use os._exit to force immediate termination from the listener thread
    os._exit(0)

def main():
    hotkey = 'ctrl+alt+tab+b'
    
    logging.info("Application started.")
    print(f"App is running... Press {hotkey.upper()} to stop.")
    print("Logs are being saved to 'app_history.log'.")
    
    # Hook the hotkey
    keyboard.add_hotkey(hotkey, on_exit_signal)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Application stopped manually via CTRL+C.")
        sys.exit(0)

if __name__ == "__main__":
    main()
