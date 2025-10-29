from typing import List, Dict, Any, Callable, Optional 
import math

from termcolor import colored

class TableDisplay:
    def __init__(self, data: List[Dict[str, Any]], columns: List[str], items_per_page: int = 10):
        self.original_data = data 
        self.filtered_data = data.copy()
        self.columns = columns 
        self.items_per_page = items_per_page
        self.current_page = 1
        self.filters = {}
        self.search_term = ""
        self.search_column = None 

    
    def set_data(self, data: List[Dict[str, Any]]):
        self.original_data = data 
        
        self.current_page = 1
    
    def apply_filters_and_search(self):
        self.filtered_data = self.original_data.copy()

        # apply column filters
        for column, filter_value in self.filters.items():
            if filter_value:
                self.filtered_data = [
                    item for item in self.filtered_data
                    if str(item.get(column, "")).lower() == str(filter_value).lower()
                ]

        # Apply search
        if self.search_term and self.search_column:
            self.filtered_data = [
                item for item in self.filtered_data
                if self.search_term.lower() in str(item.get(self.search_column, "")).lower()
            ]
        elif self.search_term: # Search for all columns
            self.filtered_data = [
                item for item in self.filtered_data
                if any(self.search_term.lower() in str(value).lower() 
                       for value in item.values())
            ]
    
    def set_filter(self, column: str, value: str):
        if value:
            self.filters[column] = value 
        elif column in self.filters:
            del self.filters[column]
        
        self.apply_filters_and_search()
        self.current_page = 1
    
    def set_search(self, term: str, column: Optional[str] = None):
        self.search_term = term 
        self.search_column = column 
        self.apply_filters_and_search()
        self.current_page = 1
    
    def clear_filters(self):
        self.filters = {}
        self.search_term = ""
        self.search_column = None 
        self.apply_filters_and_search()
        self.current_page = 1
    
    def get_total_pages(self):
        # Calculate the total number of pages based off of 
        # how much data there is divided by the allowed amount of items
        # per page
        return math.ceil(len(self.filtered_data) / self.items_per_page)
    

    def get_current_page_data(self):
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        
        return self.filtered_data[start_index:end_index]

    def next_page(self) -> bool:
        # Returns true if successful in going to the next page
        if self.current_page < self.get_total_pages():
            self.current_page += 1
            return True 

        return False 
    
    def previous_page(self) -> bool:
        if self.current_page > 1:
            self.current_page -= 1
            return True 
        return False

    def go_to_page(self, page: int) -> bool:
        total_pages = self.get_total_pages()

        if 1 <= page <= total_pages:
            self.current_page = page 
            return True 
        return False 
    
    def generate_table_display(self, show_id: bool = True):
        if not self.filtered_data:
            return colored("No data to display.", "yellow")
        
        column_widths = {}
        headers = {}

        if show_id:
            headers["row_id"] = "ID"
            column_widths["row_id"] = max(3, len("ID"))
        
        for field, header in self.columns.items():
            headers[field] = header 

            # Calculate width based on header and data

            max_data_width = max(
                (len(str(item.get(field, ""))) for item in self.get_current_page_data()),
                default = 0 
            )

            column_widths[field] = max(len(header), max_data_width, 10)

        
        # Generate table
        result = []

        # Header row
        header_row = ""
        for field, header in headers.items():
            header_row += header.ljust(column_widths[field] + 2)
            
        result.append(colored(header_row, "white", attrs=["bold"]))

        # Separator line
        separator = ""
        for field in headers.keys():
            separator += "-" * (column_widths[field] + 2)
        result.append(separator)

        # data rows
        current_data = self.get_current_page_data()
        start_idx = (self.current_page - 1) * self.items_per_page

        for idx, item in enumerate(current_data):
            row = ""

            if show_id:
                row_id = str(start_idx + idx + 1)
                row += row_id.ljust(column_widths["row_id"] + 2)
            
            for field in self.columns.keys():
                value = str(item.get(field, ""))
                row += value.ljust(column_widths[field] + 2)
            result.append(row)
        
        # Pagination information
        total_items = len(self.filtered_data)
        start_item = start_idx + 1 if total_items > 0 else 0
        end_item = min(start_idx + len(current_data), total_items)

        pagination_info = f"\nShowing {start_item}-{end_item} of {total_items} items"
        if self.get_total_pages() > 1:
            pagination_info += f"\t(Page {self.current_page} of {self.get_total_pages()})"

        result.append(colored(pagination_info, "cyan"))

        # Active filters info
        if self.filters or self.search_term:
            filter_info = "\nActive filters: "
            filter_parts = []

            search_info = ""
            if self.search_term:
                search_info += f"Search: '{self.search_term}'"

                if self.search_column:
                    search_info += f" in {self.columns.get(self.search_column, self.search_column)}"
                
                filter_parts.append(search_info)
            
            for column, value in self.filters.items():
                column_name = self.columns.get(column, column)
                filter_parts.append(f"{column_name}: '{value}'")
            
            filter_info += ", ".join(filter_parts)
            result.append(colored(filter_info, "yellow"))
        
        return "\n".join(result)            
    
    def get_pagination_options(self) -> List[str]:
        options = []

        if self.current_page > 1:
            options.append("Previous Page")

        if self.current_page < self.get_total_pages():
            options.append("Next Page")

        if self.get_total_pages() > 1:
            options.append("Go to Page")
        
        return options 

    def get_filter_options(self) -> List[str]:
        filter_options = []

        for field, header in self.columns.items():
            filter_options.append(f"Filter by {header}")

        filter_options.extend([
            "Search All Columns",
            "Search Specific Column",
            "Clear All Filters",
        ])

        return filter_options

