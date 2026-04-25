from archicad import ACConnection

# Połączenie z ArchiCAD
conn = ACConnection.connect()
assert conn

# Pobranie dostępu do komend
acc = conn.commands
act = conn.types
acu = conn.utilities


projectMapNavigatorItemId = "Poziom 0"
parentNavigatorItemId = "PROJEKT"

# which tree to checkout: 'LayoutBook', 'PublisherSets', 'ViewMap' , "ProjectMap"
root_tree_loc = 'ProjectMap'
ViewMap_tree = acc.GetNavigatorItemTree(act.NavigatorTreeId(root_tree_loc))

root_tree_locBOOK = 'ViewMap'
layoutbook_tree = acc.GetNavigatorItemTree(
    act.NavigatorTreeId(root_tree_locBOOK))


# szuka OBIEKTU 
def findprojectMapNavigatorItemId(item: act.NavigatorItem):
    return True if item.name == projectMapNavigatorItemId else False


def findparentNavigatorItemId(item: act.NavigatorItem):
    return True if item.name == parentNavigatorItemId else False

# szuka guid
list_PROJEKT = acu.FindInNavigatorItemTree(
    ViewMap_tree.rootItem, findprojectMapNavigatorItemId)
list_parent = acu.FindInNavigatorItemTree(
    layoutbook_tree.rootItem, findparentNavigatorItemId)

lPROJEKT = list_PROJEKT[0].navigatorItemId
lparent = list_parent[0].navigatorItemId

lPROJEKT_id_str = str(lPROJEKT)
lparent_id_str = str(lparent)

print(f'lPROJEKT: {lPROJEKT_id_str}')
print(f'lparent: {lparent_id_str}')

new_viewmap = acc.CloneProjectMapItemToViewMap(lPROJEKT, lparent)
