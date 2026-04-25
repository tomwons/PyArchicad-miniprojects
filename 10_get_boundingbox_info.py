from archicad import ACConnection

# Establish connection to ArchiCAD
conn = ACConnection.connect()
assert conn

# Access necessary modules
acc = conn.commands
act = conn.types

# GUID of the element you want to retrieve
element_guid = '27283429-5581-4BDF-9198-376D264225CA'

# Construct the JSON-like structure for the command
element_data = {
    "elementId": {
        "guid": element_guid
    }
}

# Call the Get3DBoundingBoxes command with the element data
bounding_boxes = acc.Get3DBoundingBoxes([element_data])

# Check if any bounding boxes were found
if bounding_boxes:
    # Extract bounding box information
    bounding_box_info = bounding_boxes[0]
    
    # Print the result
    print(f"Bounding Box Information for Element with GUID {element_guid}:\n{bounding_box_info}")
else:
    print(f"No bounding box information found for Element with GUID: {element_guid}")
