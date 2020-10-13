from thrifty.location import scrape_locations as scrape_locations_for_thrifty
from budget.location import scrape_locations as scrape_locations_for_budget
from gorentals.location import (
    scrape_locations as scrape_locations_for_gorentals,
)
from db.location import save_scraped_locations
from db.quote import get_rental_duration_operations
from utils.ui import (
    is_quit_command,
    is_empty_string,
    is_valid_db_entity_id,
    create_option,
    create_warning,
)


def scrape_locations(*args):
    company_id = args[0]
    scrape_locations_func = SCRAPE_LOCATIONS_FUNCS[company_id]
    scraped_location_names = scrape_locations_func()
    save_scraped_locations(int(company_id), scraped_location_names)


def create_quote_scraping_task(created_by, rental_duration_operation_id):
    print(created_by + ", " + str(rental_duration_operation_id))
    pass


def scrape_quotes(*args):
    pass


MAIN_MENU_COMMANDS = {
    "1": scrape_locations,
    "2": create_quote_scraping_task,
    "3": scrape_quotes,
}

SCRAPE_LOCATIONS_FUNCS = {
    "1": scrape_locations_for_thrifty,
    "2": scrape_locations_for_budget,
    "3": scrape_locations_for_gorentals,
}


def execute_command(command):
    command_id = command[0]
    command_args = command[1 : len(command)]
    command_func = MAIN_MENU_COMMANDS[command_id]
    command_func(*command_args)


def prompt_locations_scraping():
    print("The following companies provide rental locations:")
    print(create_option("[1] Thrifty"))
    print(create_option("[2] Budget"))
    print(create_option("[3] GO Rentals"))
    choice = input("Please input the company ID: ")
    if is_quit_command(choice):
        return
    elif choice in (
        "1",
        "2",
        "3",
    ):
        execute_command(["1", choice])
        return


def prompt_quote_scraping_task_creation():
    created_by = None
    rental_duration_operation_id = None
    valid_rental_duration_operation_ids = []

    while is_empty_string(created_by):
        created_by = input("Please input your name: ")
        if is_quit_command(created_by):
            return
        elif is_empty_string(created_by):
            print(create_warning("Name is invalid."))

    while not is_valid_db_entity_id(
        rental_duration_operation_id, valid_rental_duration_operation_ids
    ):
        print("The available rental duration operations are:")
        rental_duration_operations = get_rental_duration_operations()
        valid_rental_duration_operation_ids = []
        for rental_duration_operation in rental_duration_operations:
            id = rental_duration_operation["id"]
            description = rental_duration_operation["description"]
            valid_rental_duration_operation_ids.append(id)
            print(create_option("[" + str(id) + "] " + description))

        rental_duration_operation_id = input(
            "Please input the rental duration operation ID: "
        )
        if is_quit_command(rental_duration_operation_id):
            return
        elif not is_valid_db_entity_id(
            rental_duration_operation_id, valid_rental_duration_operation_ids
        ):
            print(create_warning("Rental duration operation ID is invalid."))

    create_quote_scraping_task(created_by, int(rental_duration_operation_id))


def prompt_quotes_scraping():
    pass


while True:
    print("Welcome to RentalsScraping!")
    print("Anytime you want to quit the current operation, please input 'q'.")
    print(create_option("[1] Scrape rental locations"))
    print(create_option("[2] Create a rental quote scraping task"))
    print(create_option("[3] Scrape rental quotes"))
    choice = input("Please input the command ID: ")
    if choice == "q":
        break
    elif choice == "1":
        prompt_locations_scraping()
    elif choice == "2":
        prompt_quote_scraping_task_creation()
    elif choice == "3":
        prompt_quotes_scraping()
