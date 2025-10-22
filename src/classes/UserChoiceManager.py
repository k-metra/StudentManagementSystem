import keyboard
import termcolor
import time 

from utils.clear_console import clear_console
from utils.misc import clear_input_buffer

class Option:
    def __init__(self, label: str, index: int):
        self._label = label
        self._index = index 

    def label(self):
        return self._label
    
    def index(self):
        return self._index
    

    def __str__(self):
        return self.label 
    
    def __int__(self):
        return self.index

class UserChoiceManager:

    # The 'prompt' parameter is what will appear above the options
    # every re-rendering of the menu.
    def __init__(self, options=[], prompt="Select an option:"):
        self.options = options
        self.prompt = prompt
        self.current_index = 0 # Initial index is 0

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
    
    def set_prompt(self, new_prompt=""):
        self.prompt = new_prompt

    def set_options(self, new_options=[]):
        if len(new_options) <= 1:
            raise ValueError("Options list cannot have less than two options.")
        self.options = new_options
    
    def reset_selection(self):
        self.current_index = 0
    
    def set_selection(self, selection_index=0):
        if selection_index < 0 or selection_index >= len(self.options):
            raise IndexError("Selection index is out of range.")
        self.current_index = selection_index


    # NOTE **IMPORTANT**: get_user_choice will return an OPTION object (see the class above). 
    # To access the index, use int(option),
    # to access the label/text use str(option).
    def get_user_choice(self, clear=True, options=None, prompt=None) -> Option:

        # NOTE: The selected index will NOT reset when options are changed. Call the method "reset_selection()" to reset it.

        # Override options and prompt if provided
        # This allows the same UserChoiceManager to be re-used.
        # You can call get_user_choice multiple times with different
        # options and prompts.
        self.prompt = prompt if prompt is not None else self.prompt
        self.options = options if options is not None else self.options

        time.sleep(0.1)  # Small delay to ensure previous inputs are cleared
        clear_input_buffer()

        while True:
            self.display_options(clear=clear)
            event = keyboard.read_event()

            if not event.event_type == keyboard.KEY_UP:
                continue

            if event.name == "up" and self.current_index > 0:
                self.current_index = (self.current_index - 1) % len(self.options)
            
            elif event.name == "down" and self.current_index < len(self.options) -  1:
                self.current_index = (self.current_index + 1) % len(self.options)
            
            elif event.name == "enter":
                if self.current_index < 0 or self.current_index >= len(self.options):
                    raise IndexError("Current index is out of range.")

                return Option(index=self.current_index, label=self.options[self.current_index])