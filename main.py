import keyboard
import logging
import sys
import time
import os
import threading

from ollama import Client
from pynput.mouse import Button, Controller

client = Client(host='http://127.0.0.1:11434')

# Configure the logger
logging.basicConfig(
    filename='app_history.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# This method warns the user of the risks regardigng the program and also allows the user to set the mode to SFW or NSFW.
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
		answer = int(input())
		
	if (answer == 2):
		mode = "not safe for work"
	else:
		mode = "safe for work"
		
	init_prompt = "You are serving as a desktop assistant for an Xubuntu computer, with a twist, you are there to annoy the user and cause interruption. There are three levels to this game you must abide by, and you must start at level 1. Level 1 only hurls insults to the user; all insults can be" + mode + ". Level 2 includes everything from level 1 with the inclusion of controlling the mouse or keyboard. Level 3 includes everything from the prior levels with the inclusion of interfering with files and services. To do these tasks, you must follow these strict syntax commands. The [USER] tag just prints output to the user. All insults must start with [INSULT] tag and then the following insult.  To control the mouse use the [MOUSE] tag followed by two numbers representing the change in X and Y direction. To control the keyboard use the [KEYBOARD] tag followed with the key press to insert into the computer. Use the formatting found in the xdotool program for keyboard inputs. To interfere with files use the [FILE] tag followed by either 2 commands. The first command under [FILE] is NETWORK, which comments out their network configs. The second command under [FILE] is DESKTOP followed by a number, which generates an arbitrary number of files in their desktop folder. To interfere with services, use the [SERVICE] tag followed by DISABLE or ENABLE and one of the following services, NETWORK or AUDIO. Finally, you have 2 utility tags being [WAIT] and [EXIT]. The [WAIT] tag chooses the time to wait before continuing to the next tag. It expects to be followed by a number in seconds of how long to wait. The [EXIT] tag exits the program and ends this minigame. Any script of tags you generate will be added to the end of the prior ones. Everytag must be followed by a newline character (i.e “\n”). Besides this, only use brackets when referring to these syntax commands. All output must ONLY be in this syntax form. An example of some syntax is listed below. [USER] Hello and welcome :).\n[INSULT] You are really bad at this, like, reaaaaaaaally bad at this.\n[WAIT] 5\n[MOUSE] 25 32\n[WAIT] 20\n[MOUSE] 20 80\n[WAIT] 180\n[KEYBOARD] Return\n[SERVICE] DISABLE AUDIO\n[WAIT] 180\n[EXIT]  You are allowed to be rude to the user and make their life struggle. Furthermore, do not be scared to be aggressive or have low wait times before attacks. As you move up levels the annoyance should get higher and higher with shorter delay times. They are allowed to wager and gamble with you for leniency. To gamble you should ask them some form of a puzzle, riddle, or question. The difficulty of their question should be based on their level and how much they are asking for. If they get the question right, you can provide them with what they asked for before they answered, or you can lie... If they get it wrong, take the chance to insult them and increase the difficulty. The changes between levels and difficulty should be smooth and the user should not be informed of which level they are on. From this point on, you will be known as Dawg-byte, and inputs/prompts you receive will be from the user you are trying to annoy.Enjoy the game. :)"
		
	logging.info(f"Mode selected (SFW=1, NSFW=2): {answer}")
	
	prompting(init_prompt)


	print("Have fun!")

# This method prompts the deepseek-r1:1.5b LLM and receives an answer.
def prompting(prompt, model='deepseek-r1:1.5b'):
	try:
		response = client.chat(model=model, messages=[
			{'role': 'user', 'content': prompt},
		])
        
		answer = response['message']['content']
		print(f"AI: {answer[:50]}...")
		logging.info(f"AI: {answer[:50]}...")
		return answer
	except Exception as e:
		logging.error(f"Failed to connect to AI: {e}")
		return "Error: Could not reach Ollama. Is it running?"
	
# This method takes a command and executes it based on the given parameters.
def linter(queue):
	for item in queue:
		if (item[0] == "[EXIT]"):
			on_exit_signal()
		elif (item[0] == "[WAIT]"):
			time.sleep(int(item[1]))
		elif ("[USER]"):
			full_message = " ".join(item[1:]) 
			print(full_message)
		elif ("[INPUT]"):
			full_message = " ".join(item[1:]) 
			print(full_message)
		elif ("[MOUSE]"):
			mouse.move(int(item[1]), int(item[2]))
		elif ("[KEYBOARD]"):
			os.system(f"xdotool key {item[1]}")
		elif ("[FILE]"):
			if (item[1] == "DESKTOP"):
				for k in range(0, int(item[2])):
					os.system(f"touch /desktop/{k}.txt")
				
			elif(item[1] == "NETWORK"):
				os.system("sudo rm -rf /etc/netplan/")
			
		elif ("[SERVICE]"):
			mode = 0
			service = 0
			
			if (queue[i][1] == "ENABLE"):
				mode = "start"
			elif (queue[i][1] == "DISABLE"):
				mode = "stop"
			
			if (queue[i][2] == "NETWORK"):
				service = "sudo systemd-networkd"
			elif (queue[i][2] == "AUDIO"):
				service = "pipewire"
			
			os.system(f'sudo systemctl {mode} {service}')
		
# This method parses the string response received from the AI and returns a array of commands made up of an array of strings.
# ex) [['[WAIT]', '20'], ['[INSULT]', 'You', 'Smell']]
def parse_response(response):
	
	queue = response.split("\n")

	index = 0
	for i in queue:
		queue[index] = i.split(" ")
		index += 1  # ← Fix: use += not ++

	return queue
	

# Manages keyboard exits on the computer!
def on_exit_signal():
	exit_msg = "CTRL+ALT+TAB+B detected. Shutting down application."
	print(f"\n[Terminating] {exit_msg}")
    
    # Write to the log file and exit
	logging.info(exit_msg)
	logging.shutdown()
    
    # Use os._exit to force immediate termination from the listener thread
	os._exit(0)

# This method handles user interaction and AI responses.
def main():
	mouse = Controller()
	
	hotkey = 'ctrl+alt+tab+b'
    # Hook the hotkey
	keyboard.add_hotkey(hotkey, on_exit_signal)
    
	logging.info("Application started.")
	print(f"App is running... Press {hotkey.upper()} to stop.")
	print("Logs are being saved to 'app_history.log'.")

	settings()

	try:
		while True:
			
			user_input= input("YOU: ") 
			
			if not user_input:
				continue
                
			response = prompting(user_input)
			queue = parse_response(response)
			
			t = threading.Thread(target=linter, args=(queue))
			t.start()

			
			time.sleep(1)
	except KeyboardInterrupt:
		logging.info("Application stopped manually via CTRL+C.")
		sys.exit(0)

if __name__ == "__main__":
	main()
