import os
import requests
import threading
import hou

# TODO: 
# Fix Naming Natural_hdriCamelCaseName
# Add $OS Karma LPE Tag
# Fix Issues with large files
# Support Short url
# Catch Errors and popup messages

def download_file(url, filename):
    response = requests.get(url, stream=True)
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            print('chunk !')
            file.write(chunk)
        print('DL !')
    return filename

clipboard = hou.ui.getTextFromClipboard()

res = '8k'
ext = 'exr'
dir = '$HIP/pic/hdri'

if clipboard and type(clipboard) is str:
    name = clipboard.replace('https://polyhaven.com/a/', '')
    
    if name != '':
        url = f"https://dl.polyhaven.org/file/ph-assets/HDRIs/{ext}/{res}/{name}_{res}.{ext}"
        filename = f"{dir}/{name}_{res}.{ext}"
        print(url, filename)
        
        if os.path.isfile(hou.text.expandString(filename)):
            os.remove(hou.text.expandString(filename))
            
        os.makedirs(hou.text.expandString(dir), exist_ok=True)
            
        #download_file(url, hou.text.expandString(filename))
        download_thread = threading.Thread(target=download_file, args=(url, hou.text.expandString(filename)))
        download_thread.start()
        
        pane = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
        if pane is not None:
            # Get the position of the mouse cursor in the network editor
            cursor_pos = pane.cursorPosition()
        
            # Get the network in which the pane is currently displaying
            network = pane.pwd()
        
            # Create a new node at the cursor position
            # Example: creating a geometry node
            new_node = network.createNode('domelight::2.0', node_name=f"Natural_hdri_{name}")
            
            # Set the position of the new node to the cursor position
            new_node.setPosition(cursor_pos)
            
            print('JOINED')
            new_node.parm('xn__inputstexturefile_r3ah').set(filename)
        
        
        

        
    