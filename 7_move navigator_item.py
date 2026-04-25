from archicad import ACConnection

conn = ACConnection.connect()
assert conn

acc = conn.commands
act = conn.types
acu = conn.utilities


# Define a list of dictionaries with folder and item information
folders_and_items = [
    {"folder_name": "HLS", "sheet_name": "0. Poziom 0", "view_name": "Poziom 0", "location_item_name": "1", "pH": "PDF"},
    {"folder_name": "HLS", "sheet_name": "1. Poziom +1", "view_name": "Poziom +1", "location_item_name": "2", "pH": "PDF"},
    # Add more dictionaries as needed
]

source_tree = 'LayoutBook'
parent = "PROJEKT"
folderSan = "SANITARNIK"

# Pobranie drzewa LayoutBook
layoutbook_tree = acc.GetNavigatorItemTree(act.NavigatorTreeId(source_tree))

# Funkcje do identyfikacji elementów do przeniesienia
def find_parent(item: act.NavigatorItem):
    return True if item.name == parent and item.type == 'LayoutBookRootItem' else False

def find_folder(item: act.NavigatorItem, folder_name):
    return True if item.name == folder_name and item.type == 'SubsetItem' else False

def find_sheet(item: act.NavigatorItem, sheet_name):
    return True if item.name == sheet_name and item.type == 'LayoutItem' else False

def find_view(item: act.NavigatorItem, view_name):
    return True if item.name == view_name and item.type == 'DrawingItem' else False

def find_folder2(item: act.NavigatorItem, folderSan):
    return True if item.name == folderSan and item.type == 'SubsetItem' else False

def find_folder3(item: act.NavigatorItem, pH):
    return True if item.name == pH and item.type == 'SubsetItem' else False

def find_location_item(item: act.NavigatorItem, location_item_name):
    return True if item.name == location_item_name and item.type == 'LayoutItem' else False
# Iterate over the list of dictionaries
# Iterate over the list of dictionaries
for folder_and_item in folders_and_items:
    # Uzyskanie identyfikatorów elementów do przeniesienia
    parent_item = acu.FindInNavigatorItemTree(layoutbook_tree.rootItem, find_parent)
    if not parent_item:
        print(f"Parent item not found for {folder_and_item['folder_name']}")
        continue

    folder_item = acu.FindInNavigatorItemTree(parent_item[0], lambda item: find_folder(item, folder_and_item["folder_name"]))
    if not folder_item:
        print(f"Folder item not found for {folder_and_item['folder_name']}")
        continue

    sheet_item = acu.FindInNavigatorItemTree(folder_item[0], lambda item: find_sheet(item, folder_and_item["sheet_name"]))
    if not sheet_item:
        print(f"Sheet item not found for {folder_and_item['folder_name']} - {folder_and_item['sheet_name']}")
        continue

    view_item = acu.FindInNavigatorItemTree(sheet_item[0], lambda item: find_view(item, folder_and_item["view_name"]))
    if not view_item:
        print(f"View item not found for {folder_and_item['folder_name']} - {folder_and_item['sheet_name']} - {folder_and_item['view_name']}")
        continue
    
    # Use a lambda function to pass the additional argument (folderSan) to find_folder2
    folderSan_item = acu.FindInNavigatorItemTree(parent_item[0], lambda item: find_folder2(item, folderSan))
    if not folderSan_item:
        print(f"FolderSan item not found for {folder_and_item['folder_name']} - {folderSan}")
        continue

    ph_item = acu.FindInNavigatorItemTree(folderSan_item[0], lambda item: find_folder3(item, folder_and_item["pH"]))
    if not ph_item:
        print(f"pH item not found for {folder_and_item['folder_name']} - {folderSan} - {folder_and_item['pH']}")
        continue

    # Uzyskanie identyfikatorów elementów do przeniesienia w lokalizacji docelowej
    location_item_item = acu.FindInNavigatorItemTree(parent_item[0], lambda item: find_location_item(item, folder_and_item["location_item_name"]))
    if not location_item_item:
        print(f"Location item not found for {folder_and_item['folder_name']} - {folder_and_item['location_item_name']}")
        continue

    acc.MoveNavigatorItem(view_item[0].navigatorItemId, location_item_item[0].navigatorItemId)
