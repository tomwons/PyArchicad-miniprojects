from archicad import ACConnection

conn = ACConnection.connect()
assert conn

acc = conn.commands
act = conn.types
acu = conn.utilities

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
    subfolders_to_create = ["PDF", "HLS"]  # Specify the subfolder names

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
