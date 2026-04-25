from archicad import ACConnection

conn = ACConnection.connect()
assert conn

acc = conn.commands
act = conn.types
acu = conn.utilities


def kociara():
     # Określenie drzewa do sprawdzenia: 'LayoutBook', 'PublisherSets', 'ViewMap'
    source_tree = 'ViewMap'
    # Define a list of folders to delete
    folders_to_delete = ["SW", "C.O", "WENT", "PDF", "HLS"]  # Add more folders as needed

    # Pobranie drzewa LayoutBook
    layoutbook_tree = acc.GetNavigatorItemTree(act.NavigatorTreeId(source_tree))

    # Funkcje do identyfikacji elementów do usunięcia
    def find_folder(item: act.NavigatorItem, folder_name: str):
        return True if item.name == folder_name else False

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
                except Exception as e:
                    print(f"Error deleting folder '{folder_name}': {e}")
            else:
                print(f"Folder '{folder_name}' not found.")
        except Exception as ex:
            print(f"An error occurred while processing folder '{folder_name}': {ex}")


            
kociara()