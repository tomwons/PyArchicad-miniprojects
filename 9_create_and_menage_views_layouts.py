from archicad import ACConnection

conn = ACConnection.connect()
assert conn

acc = conn.commands
act = conn.types
acu = conn.utilities

#----------------------------------------------------------------------------------
#------------------------------------ TWORZY FOLDERY-------------------------------
#----------------------------------------------------------------------------------
def twórzfolderekkappa():
    def create_subset(subset_name, parent_navigator_item_id):
        subset_parameters = act.Subset(
            name=subset_name,
            includeToIDSequence=True,
            customNumbering=False,
            continueNumbering=False,
            useUpperPrefix=False,
            addOwnPrefix=False,
            customNumber="",
            autoNumber="",
            numberingStyle="ABC",  # Set a valid numbering style
            startAt=0,
            ownPrefix=""
        )

        try:
            new_subset_item = acc.CreateLayoutSubset(subset_parameters, parent_navigator_item_id)
            print(f"Subset '{subset_name}' created successfully.")
            return new_subset_item
        except Exception as e:
            print(f"Error creating subset '{subset_name}': {e}")
            return None

    def create_folder1():
        source_tree = 'LayoutBook'
        parent = "PROJEKT"
        subset_name = "SANITARNIK"  # Specify the subset name

        # Pobranie drzewa LayoutBook
        layoutbook_tree = acc.GetNavigatorItemTree(act.NavigatorTreeId(source_tree))

        # Funkcje do identyfikacji elementów do przeniesienia
        def find_parent(item: act.NavigatorItem):
            return True if item.name == parent else False

        # Uzyskanie identyfikatorów elementów do przeniesienia
        parent_item = acu.FindInNavigatorItemTree(layoutbook_tree.rootItem, find_parent)[0]
        # Check if the "SANITARNIK" subset already exists
        existing_subset_items = acu.FindInNavigatorItemTree(parent_item, lambda item: item.name == subset_name and item.type == 'SubsetItem')
        if existing_subset_items:
            print(f"Subset '{subset_name}' already exists.")
        else:
            # Create the "SANITARNIK" subset
            create_subset(subset_name, parent_item.navigatorItemId)

    def create_folder2():
        source_tree = 'LayoutBook'
        parent = "PROJEKT"
        subset_name = "SANITARNIK"  # Specify the subset name
        subfolders_to_create = ["PDF druk", "HLS druk"]  # Specify the subfolder names

        layoutbook_tree = acc.GetNavigatorItemTree(act.NavigatorTreeId(source_tree))

        def find_parent(item: act.NavigatorItem):
            return True if item.name == parent else False

        def find_subset(item: act.NavigatorItem):
            return True if item.name == subset_name else False

        parent_item = acu.FindInNavigatorItemTree(layoutbook_tree.rootItem, find_parent)[0]
        subset_item = acu.FindInNavigatorItemTree(parent_item, find_subset)[0]

        for subfolder_name in subfolders_to_create:
            existing_subset_items = acu.FindInNavigatorItemTree(subset_item, lambda item: item.name == subfolder_name and item.type == 'SubsetItem')

            if existing_subset_items:
                print(f"Subset '{subfolder_name}' already exists.")
            else:
                # Create the subset
                create_subset(subfolder_name, subset_item.navigatorItemId)
    create_folder1()
    create_folder2()

#----------------------------------------------------------------------------------
#------------------------------------ TWORZY LAYOUTY-------------------------------
#----------------------------------------------------------------------------------
def layoucik():
    # which tree to checkout: 'LayoutBook', 'PublisherSets', 'ViewMap'
    root_tree_loc = 'LayoutBook'

    # Define a constant parent_name
    parent = "PROJEKT"
    # Specify the folder name
    folder_name = "SANITARNIK"
    # Specify the subfolder name

    # Define a list of dictionaries where each dictionary contains layout parameters
    layouts_to_create = [
        {"master_name": "A2 Poziomo", "lname": "1", "lpoziom": 594, "lpion": 420, "margins": 0, "subfolder_name": "PDF druk"},
        {"master_name": "A3 Poziomo", "lname": "2", "lpoziom": 420, "lpion": 594, "margins": 10, "subfolder_name": "PDF druk"},
        {"master_name": "A2 Poziomo", "lname": "3", "lpoziom": 594, "lpion": 420, "margins": 0, "subfolder_name": "HLS druk"},
        {"master_name": "A3 Poziomo", "lname": "4", "lpoziom": 420, "lpion": 594, "margins": 10, "subfolder_name": "HLS druk"},
        {"master_name": "A2 Poziomo", "lname": "5", "lpoziom": 594, "lpion": 420, "margins": 0, "subfolder_name": "HLS druk"},
        {"master_name": "A3 Poziomo", "lname": "6", "lpoziom": 420, "lpion": 594, "margins": 10, "subfolder_name": "HLS druk"},
        {"master_name": "A2 Poziomo", "lname": "7", "lpoziom": 594, "lpion": 420, "margins": 0, "subfolder_name": "HLS druk"},
        {"master_name": "A3 Poziomo", "lname": "8", "lpoziom": 420, "lpion": 594, "margins": 10, "subfolder_name": "HLS druk"},
        {"master_name": "A2 Poziomo", "lname": "9", "lpoziom": 594, "lpion": 420, "margins": 0, "subfolder_name": "HLS druk"},
        {"master_name": "A3 Poziomo", "lname": "10", "lpoziom": 420, "lpion": 594, "margins": 10, "subfolder_name": "HLS druk"},
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

#----------------------------------------------------------------------------------
#------------------------------------ Segreguje odpowiednio------------------------
#----------------------------------------------------------------------------------
def segregs():
    # Define a list of dictionaries with folder and item information
    folders_and_items = [
        {"folder_name": "HLS", "sheet_name": "0. Poziom 0", "view_name": "Poziom 0", "location_item_name": "1", "pH": "HLS druk"},
        {"folder_name": "HLS", "sheet_name": "1. Poziom +1", "view_name": "Poziom +1", "location_item_name": "2", "pH": "HLS druk"},
        {"folder_name": "WENT", "sheet_name": "0. Poziom 0", "view_name": "Poziom 0", "location_item_name": "3", "pH": "HLS druk"},
        {"folder_name": "WENT", "sheet_name": "1. Poziom +1", "view_name": "Poziom +1", "location_item_name": "4", "pH": "HLS druk"},
        {"folder_name": "C.O", "sheet_name": "0. Poziom 0", "view_name": "Poziom 0", "location_item_name": "5", "pH": "HLS druk"},
        {"folder_name": "C.O", "sheet_name": "1. Poziom +1", "view_name": "Poziom +1", "location_item_name": "6", "pH": "HLS druk"},
        {"folder_name": "SW", "sheet_name": "0. Poziom 0", "view_name": "Poziom 0", "location_item_name": "7", "pH": "HLS druk"},
        {"folder_name": "SW", "sheet_name": "1. Poziom +1", "view_name": "Poziom +1", "location_item_name": "8", "pH": "HLS druk"},
        {"folder_name": "PDF", "sheet_name": "0. Poziom 0", "view_name": "Poziom 0", "location_item_name": "9", "pH": "PDF druk"},
        {"folder_name": "PDF", "sheet_name": "1. Poziom +1", "view_name": "Poziom +1", "location_item_name": "10", "pH": "PDF druk"},
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


#----------------------------------------------------------------------------------
#------------------------------------ laybookcleans----------------------------------
#----------------------------------------------------------------------------------
def laybookcleans():
    try:
        # Określenie drzewa do sprawdzenia: 'LayoutBook', 'PublisherSets', 'ViewMap'
        source_tree = 'LayoutBook'

        # Define a list of folders to delete
        folders_to_delete = ["SANITARNIK"]  # Add more folders as needed

        # Pobranie drzewa LayoutBook
        layoutbook_tree = acc.GetNavigatorItemTree(act.NavigatorTreeId(source_tree))

        # Funkcje do identyfikacji elementów do usunięcia
        def find_folder(item: act.NavigatorItem, folder_name: str):
            return True if item.name == folder_name and item.type == 'SubsetItem' else False

        # Loop through the list of folders to delete
        for folder_name in folders_to_delete:
            try:
                # Uzyskanie identyfikatora folderu
                folder_items = acu.FindInNavigatorItemTree(layoutbook_tree.rootItem, lambda i: find_folder(i, folder_name))

                if folder_items:
                    folder_item = folder_items[0]
                    try:
                        # Usunięcie folderu (i jego zawartości)
                        acc.DeleteNavigatorItems([act.NavigatorItemIdWrapper(folder_item.navigatorItemId)])
                        print(f"Folder '{folder_name}' deleted successfully.")
                    except acc.CommandError as ce:
                        print(f"Error deleting folder '{folder_name}': {ce}")
                else:
                    print(f"Folder '{folder_name}' not found.")
            except acc.CommandError as ce:
                print(f"An error occurred while processing folder '{folder_name}': {ce}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

#----------------------------------------------------------------------------------
#------------------------------------ LAYOUTBOOKCLEANUP----------------------------
#----------------------------------------------------------------------------------
def Layoutbookcleanup():
    # Określenie drzewa do sprawdzenia: 'LayoutBook', 'PublisherSets', 'ViewMap'
    source_tree = 'LayoutBook'

    # Define the parent folder (PROJEKT) and the list of folders to delete under it
    parent_folder_name = "PROJEKT"
    folders_to_delete = ["SW", "C.O", "WENT", "PDF", "HLS"]  # Add more folders as needed

    # Pobranie drzewa LayoutBook
    layoutbook_tree = acc.GetNavigatorItemTree(act.NavigatorTreeId(source_tree))

    # Funkcje do identyfikacji elementów do usunięcia
    def find_parent_folder(item: act.NavigatorItem):
        return True if item.name == parent_folder_name and item.type == 'LayoutBookRootItem' else False

    def find_folder(item: act.NavigatorItem, folder_name: str):
        return True if item.name == folder_name and item.type == 'SubsetItem' and item.children else False

    # Uzyskanie identyfikatora folderu "PROJEKT"
    parent_folder_items = acu.FindInNavigatorItemTree(layoutbook_tree.rootItem, lambda i: find_parent_folder(i))

    if parent_folder_items:
        parent_folder_item = parent_folder_items[0]

        # Loop through the list of folders to delete under "PROJEKT"
        for folder_name in folders_to_delete:
            try:
                # Uzyskanie identyfikatora folderu do usunięcia
                folder_items = acu.FindInNavigatorItemTree(parent_folder_item, lambda i: find_folder(i, folder_name))

                if folder_items:
                    folder_item = folder_items[0]
                    try:
                        # Usunięcie folderu (i jego zawartości)
                        acc.DeleteNavigatorItems([act.NavigatorItemIdWrapper(folder_item.navigatorItemId)])
                        print(f"Folder '{folder_name}' under '{parent_folder_name}' deleted successfully.")
                    except Exception as e:
                        print(f"Error deleting folder '{folder_name}': {e}")
                else:
                    print(f"Folder '{folder_name}' not found under '{parent_folder_name}'.")
            except Exception as ex:
                print(f"An error occurred while processing folder '{folder_name}': {ex}")
    else:
        print(f"Parent folder '{parent_folder_name}' not found.")



#----------------------------------------------------------------------------------
#------------------------------------ SIEMA HENIU----------------------------------
#----------------------------------------------------------------------------------
laybookcleans()
twórzfolderekkappa()
layoucik()
segregs()
Layoutbookcleanup()