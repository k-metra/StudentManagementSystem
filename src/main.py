import os

from utils.clear_console import clear_console
from classes.UserChoiceManager import UserChoiceManager
from utils.options import options

def main():
    print("Welcome to the Student Management System!")

    options_list = options("Add Student", "View Students", "Delete Student", "Exit")
    choice_manager = UserChoiceManager(options_list, prompt="Please choose an action:")
    user_choice = choice_manager.get_user_choice()

    print(user_choice)

main()
