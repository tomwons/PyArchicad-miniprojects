from archicad import ACConnection

# Nawiązanie połączenia z ArchiCAD
conn = ACConnection.connect()
assert conn

# Przypisanie aliasów do często używanych modułów API ArchiCAD
acc = conn.commands
act = conn.types
acu = conn.utilities

# Konfiguracja skryptu
moveToFolder = True
folderName = '-- NiewykorzystaneWidoki --'
renameFolderFromPreviousRun = True
folderNameForPreviousRun = '-- Poprzednie NiewykorzystaneWidoki --'

# Funkcja sprawdzająca, czy element NavigatorItem to link
def isLinkNavigatorItem(item: act.NavigatorItem):
    return item.sourceNavigatorItemId is not None

# Pobranie drzewa elementów dla Layout Book
layoutBookTree = acc.GetNavigatorItemTree(act.NavigatorTreeId('LayoutBook'))
links = acu.FindInNavigatorItemTree(layoutBookTree.rootItem, isLinkNavigatorItem)

# Pobranie drzewa elementów dla Publisher Sets i znalezienie linków
for publisherSetName in acc.GetPublisherSetNames():
    publisherSetTree = acc.GetNavigatorItemTree(act.NavigatorTreeId('PublisherSets', publisherSetName))
    links += acu.FindInNavigatorItemTree(publisherSetTree.rootItem, isLinkNavigatorItem)

# Ustalenie źródeł linków
sourcesOfLinks = set(link.sourceNavigatorItemId.guid for link in links)

# Pobranie drzewa elementów dla View Map
viewMapTree = acc.GetNavigatorItemTree(act.NavigatorTreeId('ViewMap'))
unusedViewTreeItems = acu.FindInNavigatorItemTree(viewMapTree.rootItem,
    lambda node: node.name != folderName and node.name != folderNameForPreviousRun and
        not acu.FindInNavigatorItemTree(node, lambda i: i.navigatorItemId.guid in sourcesOfLinks)
    )

# Filtracja elementów niewykorzystanych widoków
unusedViewTreeItemsFiltered = []
for ii in unusedViewTreeItems:
    isChildOfUnused = False
    for jj in unusedViewTreeItems:
        if ii != jj and acu.FindInNavigatorItemTree(jj, lambda node: node.navigatorItemId.guid == ii.navigatorItemId.guid):
            isChildOfUnused = True
            break
    if not isChildOfUnused:
        unusedViewTreeItemsFiltered.append(ii)
unusedViewTreeItems = unusedViewTreeItemsFiltered

# Sprawdzenie istnienia foldera z poprzedniego uruchomienia i ewentualna zmiana nazwy
folderFromPreviousRun = acu.FindInNavigatorItemTree(viewMapTree.rootItem, lambda i: i.name == folderName)
if folderFromPreviousRun and renameFolderFromPreviousRun:
    acc.RenameNavigatorItem(folderFromPreviousRun[0].navigatorItemId, newName=folderNameForPreviousRun)

# Utworzenie foldera na niewykorzystane widoki
unusedViewsFolder = None
if moveToFolder:
    if not renameFolderFromPreviousRun and folderFromPreviousRun:
        unusedViewsFolder = folderFromPreviousRun[0].navigatorItemId
    else:
        unusedViewsFolder = acc.CreateViewMapFolder(act.FolderParameters(folderName))

# Przesunięcie niewykorzystanych widoków do foldera i wydruk informacji
for item in sorted(unusedViewTreeItems, key=lambda i: i.prefix + i.name):
    try:
        if moveToFolder and unusedViewsFolder:
            acc.MoveNavigatorItem(item.navigatorItemId, unusedViewsFolder)
        print(f"{item.prefix} {item.name}\n\t{item}")
    except:
        continue
