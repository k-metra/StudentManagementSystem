from typing import List, Dict, Any, Callable, Optional
from utils.table_display import TableDisplay
from classes.UserChoiceManager import UserChoiceManager
from utils.clear_console import clear_console
from utils.misc import enter_to_continue
from termcolor import colored

def interactive_table(
    data: List[Dict[str, Any]], 
    columns: Dict[str, str], 
    title: str,
    additional_options: List[str] = None,
    on_select_item: Callable[[Dict[str, Any], int], None] = None,
    items_per_page: int = 10
) -> Optional[str]:
    """
    Display an interactive table with pagination, filtering, and search.
    
    Args:
        data: List of dictionaries containing the data
        columns: Dict with key as data field name and value as display header
        title: Title to display above the table
        additional_options: Additional menu options to show
        on_select_item: Callback function when an item is selected (item, row_id)
        items_per_page: Number of items per page
        
    Returns:
        The selected additional option label, or None if back/exit
    """
    if additional_options is None:
        additional_options = []
    
    table = TableDisplay(data, columns, items_per_page)
    choice_manager = UserChoiceManager()
    
    while True:
        # Build menu options
        clear_console()
        options = []
        
        # Add item selection option if there's data and callback
        if table.filtered_data and on_select_item:
            options.append("Select Item")
        
        # Add pagination options
        options.extend(table.get_pagination_options())
        
        # Add filter/search options
        options.extend([
            "Filter/Search Options"
        ])
        
        # Add additional options
        options.extend(additional_options)
        
        # Add back option
        options.append("Back")
        
        # Create the combined prompt with table and menu
        table_display = table.generate_table_display()
        
        combined_prompt = f"""{colored(f"<== {title} ==>", "cyan", attrs=["bold"])}

{table_display}

{colored("Available Actions:", "white", attrs=["bold"])}"""
        
        choice_manager.set_prompt(combined_prompt)
        choice_manager.set_options(options)
        
        choice = choice_manager.get_user_choice()
        choice_label = choice.label()
        
        if choice_label == "Back":
            return None
        elif choice_label == "Select Item":
            handle_item_selection(table, on_select_item)
            return True # We return a non-null value to indicate an item was selected
        elif choice_label == "Previous Page":
            table.previous_page()
        elif choice_label == "Next Page":
            table.next_page()
        elif choice_label == "Go to Page":
            handle_go_to_page(table)
        elif choice_label == "Filter/Search Options":
            handle_filter_search_menu(table)
        elif choice_label in additional_options:
            return choice_label

def handle_item_selection(table: TableDisplay, on_select_item: Callable):
    """Handle item selection from the table"""
    clear_console()
    
    # Show the table again for reference
    print(colored("<== Select Item ==>", "cyan", attrs=["bold"]))
    print()
    print(table.generate_table_display())
    print()
    
    try:
        item_id = int(input("Enter the ID of the item to select (0 to cancel): ").strip())
        
        if item_id == 0:
            return
        
        if 1 <= item_id <= len(table.filtered_data):
            # Find the item in the filtered data
            actual_index = item_id - 1
            if actual_index < len(table.filtered_data):
                selected_item = table.filtered_data[actual_index]
                on_select_item(selected_item, item_id)
                return
            else:
                print(colored("Invalid item ID.", "red"))
                enter_to_continue()
        else:
            print(colored("Invalid item ID.", "red"))
            enter_to_continue()
    except ValueError:
        print(colored(f"Invalid input. Please enter a number.", "red"))
        enter_to_continue()

def handle_go_to_page(table: TableDisplay):
    """Handle going to a specific page"""
    clear_console()
    
    # Show current pagination info
    print(colored("<== Go to Page ==>", "cyan", attrs=["bold"]))
    print()
    print(f"Current page: {table.current_page}")
    print(f"Total pages: {table.get_total_pages()}")
    print()
    
    try:
        page = input(f"Enter page number (1-{table.get_total_pages()}): ")
        page = int(page)
        
        if not table.go_to_page(page):
            print(colored(f"Invalid page number. Please enter a number between 1 and {table.get_total_pages()}.", "red"))
            enter_to_continue()
    except ValueError:
        print(colored("Invalid input. Please enter a number.", "red"))
        enter_to_continue()

def handle_filter_search_menu(table: TableDisplay):
    """Handle the filter and search submenu"""
    choice_manager = UserChoiceManager()
    
    while True:
        # Build filter menu prompt
        filter_prompt_parts = [
            colored("<== Filter & Search Options ==>", "cyan", attrs=["bold"]),
            ""
        ]
        
        # Show current filters
        if table.filters or table.search_term:
            filter_prompt_parts.append(colored("Current Filters:", "yellow", attrs=["bold"]))
            if table.search_term:
                search_info = f"  Search: '{table.search_term}'"
                if table.search_column:
                    column_name = table.columns.get(table.search_column, table.search_column)
                    search_info += f" in {column_name}"
                filter_prompt_parts.append(search_info)
            
            for column, value in table.filters.items():
                column_name = table.columns.get(column, column)
                filter_prompt_parts.append(f"  {column_name}: '{value}'")
            filter_prompt_parts.append("")
        
        filter_prompt_parts.append(colored("Filter & Search Options:", "white", attrs=["bold"]))
        
        filter_prompt = "\n".join(filter_prompt_parts)
        
        options = []
        
        # Filter options
        for field, header in table.columns.items():
            options.append(f"Filter by {header}")
        
        # Search options
        options.extend([
            "Search All Columns",
            "Search Specific Column"
        ])
        
        # Clear options
        if table.filters or table.search_term:
            options.append("Clear All Filters")
        
        options.append("Back to Table")
        
        choice_manager.set_prompt(filter_prompt)
        choice_manager.set_options(options)
        
        choice = choice_manager.get_user_choice()
        choice_label = choice.label()
        
        if choice_label == "Back to Table":
            break
        elif choice_label == "Search All Columns":
            clear_console()
            print(colored("<== Search All Columns ==>", "cyan", attrs=["bold"]))
            print()
            term = input("Enter search term: ").strip()
            table.set_search(term)
            print(colored(f"Search applied: '{term}' in all columns", "green"))
            enter_to_continue()
            break
        elif choice_label == "Search Specific Column":
            handle_specific_column_search(table)
            break
        elif choice_label == "Clear All Filters":
            table.clear_filters()
            print(colored("All filters cleared.", "green"))
            enter_to_continue()
            break
        elif choice_label.startswith("Filter by "):
            column_header = choice_label[10:]  # Remove "Filter by "
            # Find the field name from header
            field = None
            for f, h in table.columns.items():
                if h == column_header:
                    field = f
                    break
            
            if field:
                clear_console()
                print(colored(f"<== Filter by {column_header} ==>", "cyan", attrs=["bold"]))
                print()
                value = input(f"Enter value to filter by {column_header}: ").strip()
                table.set_filter(field, value)
                if value:
                    print(colored(f"Filter applied: {column_header} = '{value}'", "green"))
                else:
                    print(colored(f"Filter removed for {column_header}", "green"))
                enter_to_continue()
                break

def handle_specific_column_search(table: TableDisplay):
    """Handle searching in a specific column"""
    choice_manager = UserChoiceManager()
    
    search_prompt = f"""{colored("<== Select Column to Search ==>", "cyan", attrs=["bold"])}

{colored("Select which column to search in:", "white", attrs=["bold"])}"""
    
    column_options = []
    for field, header in table.columns.items():
        column_options.append(header)
    column_options.append("Cancel")
    
    choice_manager.set_prompt(search_prompt)
    choice_manager.set_options(column_options)
    
    choice = choice_manager.get_user_choice()
    choice_label = choice.label()
    
    if choice_label != "Cancel":
        # Find the field name
        field = None
        for f, h in table.columns.items():
            if h == choice_label:
                field = f
                break
        
        if field:
            clear_console()
            print(colored(f"<== Search in {choice_label} ==>", "cyan", attrs=["bold"]))
            print()
            term = input(f"Enter search term for {choice_label}: ").strip()
            table.set_search(term, field)
            print(colored(f"Search applied: '{term}' in {choice_label}", "green"))
            enter_to_continue()