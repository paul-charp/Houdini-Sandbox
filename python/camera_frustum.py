"""
To use as a script, for example in a shelf tool. 
Works on cameras and lopimportcam in the /obj context.
Display the camera frustum in the viewport. 

Adds a "Show Frustum" checkbox to the camera. 
"""

import hou

SUPPORTED_TYPES = [
    'cam', 'lopimportcam'
]


# Get the selected nodes in the current pane
selected_nodes = hou.selectedNodes()

cameras = []

# Filter out only camera nodes
for node in selected_nodes:
    type_name = node.type().name()
    if type_name in SUPPORTED_TYPES:
        cameras.append(node)

# Deselect all nodes
for node in selected_nodes:
    node.setSelected(False)


for camera in cameras:

    # Create Nodes
    vdb = camera.createNode(node_type_name='vdb', node_name='frustum')
    switch = camera.createNode(node_type_name='switch', node_name='t_frustum')
    merge = camera.createNode(node_type_name='merge', node_name='merge_frustum')
    
    # Get Xform node
    xform = hou.node(camera.path() + '/xform1')

    # Connect nodes
    switch.setInput(0, xform)
    switch.setInput(1, merge)

    merge.setInput(0, xform)
    merge.setInput(1, vdb)


    # Set Parms
    vdb.parm('camera').set('..')
    vdb.parm('samplediv').set(1)
    vdb.parm('zmin').setExpression('ch("../near")')
    vdb.parm('zmax').setExpression('ch("../far")')
    vdb.parm('source1').set(2)

    switch.parm('input').setExpression('ch("../t_frustum")')
    switch.setDisplayFlag(True)   
    
    # Add checkbox
    toggle_param = hou.ToggleParmTemplate('t_frustum', 'Show Frustum', default_value=True)
    camera.addSpareParmTuple(toggle_param, in_folder=('View',))


    camera.layoutChildren()
    camera.setSelected(True)