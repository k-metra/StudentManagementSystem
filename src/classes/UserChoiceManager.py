import keyboard
import termcolor

from utils.clear_console import clear_console

class UserChoiceManager:
    def __init__(self, options, prompt="Select an option:"):
        self.options = options
        self.prompt = prompt
        self.current_index = 0

    def display_options(self, clear=True):
        # Initially clear the console before showing options
        if clear:
            clear_console()
        
        print(self.prompt)

        for idx, option in enumerate(self.options):
            if idx == self.current_index:
                print(termcolor.colored(f"> {option}", "white", attrs=["bold"]))
                continue

            print(f"  {option}")
    
    def get_user_choice(self):
        while True:
            self.display_options()
            event = keyboard.read_event()

            if not event.event_type == keyboard.KEY_DOWN:
                continue

            if event.name == "up" and self.current_index > 0:
                self.current_index = (self.current_index - 1) % len(self.options)
            
            elif event.name == "down" and self.current_index < len(self.options) -  1:
                self.current_index = (self.current_index + 1) % len(self.options)
            
            elif event.name == "enter":
                return self.current_index