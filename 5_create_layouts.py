from archicad import ACConnection

conn = ACConnection.connect()
assert conn

acc = conn.commands
act = conn.types
acu = conn.utilities

# which tree to checkout: 'LayoutBook', 'PublisherSets', 'ViewMap'
root_tree_loc = 'LayoutBook'

# Define a constant parent_name
parent = "PROJEKT"
# Specify the folder name
folder_name = "SANITARNIK"
# Specify the subfolder name

# Define a list of dictionaries where each dictionary contains layout parameters
layouts_to_create = [
    {"master_name": "A2 Poziomo", "lname": "1", "lpoziom": 594, "lpion": 420, "margins": 0, "subfolder_name": "PDF"},
    {"master_name": "A3 Poziomo", "lname": "2", "lpoziom": 420, "lpion": 594, "margins": 10, "subfolder_name": "PDF"},
    {"master_name": "A2 Poziomo", "lname": "3", "lpoziom": 594, "lpion": 420, "margins": 0, "subfolder_name": "HLS"},
    {"master_name": "A3 Poziomo", "lname": "4", "lpoziom": 420, "lpion": 594, "margins": 10, "subfolder_name": "HLS"},
    {"master_name": "A2 Poziomo", "lname": "5", "lpoziom": 594, "lpion": 420, "margins": 0, "subfolder_name": "HLS"},
    {"master_name": "A3 Poziomo", "lname": "6", "lpoziom": 420, "lpion": 594, "margins": 10, "subfolder_name": "HLS"},
    {"master_name": "A2 Poziomo", "lname": "7", "lpoziom": 594, "lpion": 420, "margins": 0, "subfolder_name": "HLS"},
    {"master_name": "A3 Poziomo", "lname": "8", "lpoziom": 420, "lpion": 594, "margins": 10, "subfolder_name": "HLS"},
    {"master_name": "A2 Poziomo", "lname": "9", "lpoziom": 594, "lpion": 420, "margins": 0, "subfolder_name": "HLS"},
    {"master_name": "A3 Poziomo", "lname": "10", "lpoziom": 420, "lpion": 594, "margins": 10, "subfolder_name": "HLS"},
    # Add more dictionaries as needed
]

# Retrieve the Root Item
layoutbook_tree = acc.GetNavigatorItemTree(act.NavigatorTreeId(root_tree_loc))

def findMaster(item: act.NavigatorItem, master_name: str):
    if isinstance(item, act.NavigatorItemArrayItem):
        return any(sub_item.name == master_name and sub_item.type == 'MasterLayoutItem' for sub_item in item.items)
    return item.name == master_name and item.type == 'MasterLayoutItem'

def findFolder(item: act.NavigatorItem, folder_name: str):
    return True if item.name == folder_name and item.type == 'SubsetItem' else False

def findSubfolder(item: act.NavigatorItem, subfolder_name: str):
    return True if item.name == subfolder_name and item.type == 'SubsetItem' else False

def findLayout(item: act.NavigatorItem, layout_name: str):
    return True if item.name == layout_name and item.type == 'LayoutItem' else False

# Loop through the list of layouts to create
for layout_params in reversed(layouts_to_create):
    master_name = layout_params["master_name"]
    lname = layout_params["lname"]
    lpoziom = layout_params["lpoziom"]
    lpion = layout_params["lpion"]
    lmargin_left = layout_params["margins"]
    lmargin_top = layout_params["margins"]
    lmargin_right = layout_params["margins"]
    lmargin_bottom = layout_params["margins"]
    subfolder_name = layout_params["subfolder_name"]

    # Find the parent folder directly by its name
    list_folder = acu.FindInNavigatorItemTree(layoutbook_tree.rootItem, lambda i: findFolder(i, folder_name))

    if list_folder:
        # Find the subfolder within the parent folder
        list_subfolder = acu.FindInNavigatorItemTree(list_folder[0], lambda i: findSubfolder(i, subfolder_name))
        if list_subfolder:
            lparent = list_subfolder[0].navigatorItemId

            # Check if the layout already exists in the subfolder
            list_layout = acu.FindInNavigatorItemTree(list_subfolder[0], lambda i: findLayout(i, lname))
            if list_layout:
                print(f"Layout '{lname}' already exists in subfolder '{subfolder_name}' within folder '{folder_name}'.")
            else:
                # You can use the same master layout for each entry if desired
                lmaster = acu.FindInNavigatorItemTree(layoutbook_tree.rootItem, lambda i: findMaster(i, master_name))[0].navigatorItemId

                lparam = act.LayoutParameters(lpoziom, lpion, lmargin_left, lmargin_top, lmargin_right, lmargin_bottom,
                                              "", False, False, False, 1, 1, "", "", False, False)

                new_layout = acc.CreateLayout(lname, lparam, lmaster, lparent)
                print(f"Layout '{lname}' created successfully in subfolder '{subfolder_name}' within folder '{folder_name}'.")
        else:
            print(f"Subfolder '{subfolder_name}' not found within folder '{folder_name}'.")
    else:
        print(f"Folder '{folder_name}' not found.")
