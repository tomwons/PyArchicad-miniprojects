from archicad import ACConnection

conn = ACConnection.connect()
assert conn

acc = conn.commands
act = conn.types
acu = conn.utilities

def get_main_folder_name():
    source_tree = 'LayoutBook'

    # Pobranie drzewa LayoutBook
    layoutbook_tree = acc.GetNavigatorItemTree(act.NavigatorTreeId(source_tree))

    # Funkcje do identyfikacji elementów do przeniesienia
    def find_main_folder(item: act.NavigatorItem):
        return True if item.type == 'LayoutBookRootItem' else False

    # Uzyskanie identyfikatora głównego folderu
    main_folder_items = acu.FindInNavigatorItemTree(layoutbook_tree.rootItem, lambda i: find_main_folder(i))

    if main_folder_items:
        main_folder_name = main_folder_items[0].name
        print(f"The name of the main folder in LayoutBook is: {main_folder_name}")
        return main_folder_name
    else:
        print("Main folder not found in LayoutBook.")
        return None

# Call the function to get the main folder name
main_folder_name = get_main_folder_name()