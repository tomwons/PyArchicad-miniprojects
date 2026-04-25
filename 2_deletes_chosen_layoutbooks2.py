from archicad import ACConnection

conn = ACConnection.connect()
assert conn

acc = conn.commands
act = conn.types
acu = conn.utilities

# Określenie drzewa do sprawdzenia: 'LayoutBook', 'PublisherSets', 'ViewMap'
source_tree = 'LayoutBook'

# Define a list of dictionaries where each dictionary contains 'folder' and 'items'
folders_and_items = [
    {"folder": "SW", "items": ["-1. Poziom -1", "2. Poziom +2"]},
    {"folder": "C.O", "items": ["-1. Poziom -1", "2. Poziom +2"]},
    {"folder": "WENT", "items": ["-1. Poziom -1", "2. Poziom +2"]},
    {"folder": "PDF", "items": ["-1. Poziom -1", "2. Poziom +2"]},
    {"folder": "HLS", "items": ["-1. Poziom -1", "2. Poziom +2"]},
    # Add more dictionaries as needed
]

# Pobranie drzewa LayoutBook
layoutbook_tree = acc.GetNavigatorItemTree(act.NavigatorTreeId(source_tree))

# Funkcje do identyfikacji elementów do usunięcia
def find_folder(item: act.NavigatorItem, folder_name: str):
    return True if item.name == folder_name and item.type == 'SubsetItem' else False

def find_item(item: act.NavigatorItem, item_name: str):
    return True if item.name == item_name and item.type == 'LayoutItem' else False

# Loop through the list of folders and items
for folder_and_items in folders_and_items:
    folder_name = folder_and_items["folder"]
    items_to_delete = folder_and_items["items"]

    # Uzyskanie identyfikatora folderu
    folder_items = acu.FindInNavigatorItemTree(layoutbook_tree.rootItem, lambda i: find_folder(i, folder_name))
    
    if folder_items:
        folder_item = folder_items[0]
        for item_name in items_to_delete:
            # Uzyskanie identyfikatora elementu do usunięcia
            item_items = acu.FindInNavigatorItemTree(folder_item, lambda i: find_item(i, item_name))
            if item_items:
                try:
                    item_item = item_items[0]
                    # Usunięcie elementu
                    acc.DeleteNavigatorItems([act.NavigatorItemIdWrapper(item_item.navigatorItemId)])
                    print(f"Item '{item_name}' in folder '{folder_name}' deleted successfully.")
                except Exception as e:
                    print(f"Error deleting item '{item_name}': {e}")
            else:
                print(f"Item '{item_name}' not found in folder '{folder_name}'.")
    else:
        print(f"Folder '{folder_name}' not found.")
