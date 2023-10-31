"""
To use as a script, for example in a shelf tool and ideally bind it to a hotkey.
Creates an object merge node for each nodes in the clipboard.
"""

import hou

network = hou.ui.curDesktop().paneTabUnderCursor()
networkPath = network.pwd().path()
pos = network.cursorPosition()

color = hou.Color((0.47, 0.81, 0.2))
clipboard = hou.ui.getTextFromClipboard()

n = 0

if clipboard:
    list = clipboard.split()
    for item in list:
        if hou.node(item) != None:
            merge = hou.node(networkPath).createNode('object_merge', 'in_' + item.split('/')[-2] + '_' + item.split('/')[-1])
            merge.parm('objpath1').set(str(item))
            merge.parm('xformtype').set(1)
            merge.setPosition(pos)
            merge.setColor(color)
            merge.move([n*2,0])
            if n == 0:
                merge.setSelected(True, True)
            else:
                merge.setSelected(True, False)
            n += 1