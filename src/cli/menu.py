"""Console menu loop and I/O handlers."""

import sys
from src.services.todo_service import TodoService

MENU = """\
===== Todo CLI =====
1. Add item
2. List items
3. Update item
4. Delete item
5. Filter by category
6. Filter by status
7. Quit
===================="""


def run_menu(service: TodoService) -> None:
    try:
        while True:
            print(MENU)
            choice = input("Choose an option: ")
            if choice == "1":
                _handle_add(service)
            elif choice == "2":
                _handle_list(service.list_items())
            elif choice == "3":
                _handle_update(service)
            elif choice == "4":
                _handle_delete(service)
            elif choice == "5":
                _handle_filter_category(service)
            elif choice == "6":
                _handle_filter_status(service)
            elif choice == "7":
                print("Goodbye!")
                return
            else:
                print("Error: Invalid option. Please choose 1-7.", file=sys.stderr)
    except KeyboardInterrupt:
        print("\nGoodbye!")


def _handle_add(service: TodoService) -> None:
    title = input("Title: ")
    if not title.strip():
        print("Error: Title cannot be empty.", file=sys.stderr)
        return
    description = input("Description (press Enter to skip): ")
    category = input('Category (press Enter for "General"): ')
    if not category.strip():
        category = "General"
    item = service.add_item(title, description=description, category=category)
    print(f"Item added successfully (ID: {item.id})")


def _handle_list(items) -> None:
    if not items:
        print("No items found.")
        return
    _print_table(items)


def _handle_update(service: TodoService) -> None:
    raw_id = input("Enter item ID: ")
    try:
        item_id = int(raw_id)
    except ValueError:
        print(f"Error: Item with ID {raw_id} not found.", file=sys.stderr)
        return
    try:
        current = service._find_by_id(item_id)
    except ValueError:
        print(f"Error: Item with ID {item_id} not found.", file=sys.stderr)
        return

    new_title = input(f'New title (press Enter to keep "{current.title}"): ')
    new_desc = input("New description (press Enter to keep current): ")
    new_cat = input(f'New category (press Enter to keep "{current.category}"): ')
    new_status = input(f'New status - pending/complete (press Enter to keep "{current.status}"): ')

    fields = {}
    if new_title.strip():
        fields["title"] = new_title
    if new_desc:
        fields["description"] = new_desc
    if new_cat.strip():
        fields["category"] = new_cat
    if new_status.strip():
        fields["status"] = new_status

    try:
        service.update_item(item_id, **fields)
        print(f"Item {item_id} updated successfully.")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)


def _handle_delete(service: TodoService) -> None:
    raw_id = input("Enter item ID: ")
    try:
        item_id = int(raw_id)
    except ValueError:
        print(f"Error: Item with ID {raw_id} not found.", file=sys.stderr)
        return
    try:
        item = service._find_by_id(item_id)
    except ValueError:
        print(f"Error: Item with ID {item_id} not found.", file=sys.stderr)
        return

    confirm = input(f'Delete "{item.title}"? (yes/no): ')
    if confirm.lower() == "yes":
        service.delete_item(item_id)
        print(f"Item {item_id} deleted successfully.")
    else:
        print("Deletion cancelled.")


def _handle_filter_category(service: TodoService) -> None:
    category = input("Enter category: ")
    items = service.filter_by_category(category)
    if not items:
        print(f'No items found in category "{category}".')
        return
    _print_table(items)


def _handle_filter_status(service: TodoService) -> None:
    status = input("Enter status (pending/complete): ")
    try:
        items = service.filter_by_status(status)
    except ValueError:
        print('Error: Invalid status. Use "pending" or "complete".', file=sys.stderr)
        return
    if not items:
        print(f'No items with status "{status}".')
        return
    _print_table(items)


def _print_table(items) -> None:
    print(f"{'ID':<4}| {'Title':<17}| {'Category':<10}| Status")
    print(f"{'-'*4}|{'-'*18}|{'-'*11}|{'-'*8}")
    for item in items:
        print(f"{item.id:<4}| {item.title:<17}| {item.category:<10}| {item.status}")
