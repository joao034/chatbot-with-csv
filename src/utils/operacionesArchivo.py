import os 

def guardarArchivo( path, archivo ):
    with open(path, 'w', encoding='utf-8') as file: 
        file.write( archivo )

def eliminarArchivo( path ):
    if os.path.exists(path):
        os.remove(path)