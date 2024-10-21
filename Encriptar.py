import networkx as nx
from cryptography.fernet import Fernet

# Función para generar una clave de encriptación
def generar_clave():
    return Fernet.generate_key()

# Función para guardar la clave en un archivo
def guardar_clave(archivo_clave, llave_fernet):
    with open(archivo_clave, 'wb') as archivo:
        archivo.write(llave_fernet)

# Función para cargar la clave desde un archivo
def cargar_clave(archivo_clave):
    with open(archivo_clave, 'rb') as archivo:
        return archivo.read()

# Función para encriptar una clave usando Fernet y teoría de grafos
def encriptar_clave(clave, llave_fernet):
    fernet = Fernet(llave_fernet)
    
    # Creamos un grafo para transformar los caracteres de la clave
    G = nx.DiGraph()
    for i, char in enumerate(clave):
        if i < len(clave) - 1:
            G.add_edge(char, clave[i + 1])
    
    # Convertimos el grafo en una cadena de texto
    grafo_texto = ','.join([f"{nodo}-{destino}" for nodo, destino in G.edges()])
    
    # Encriptamos la representación del grafo
    clave_encriptada = fernet.encrypt(grafo_texto.encode())
    
    return clave_encriptada

# Función para desencriptar la clave
def desencriptar_clave(clave_encriptada, llave_fernet):
    fernet = Fernet(llave_fernet)
    
    # Desencriptamos la representación del grafo
    grafo_texto = fernet.decrypt(clave_encriptada).decode()
    
    # Reconstruimos el grafo desde el texto desencriptado
    G = nx.DiGraph()
    for edge in grafo_texto.split(','):
        nodo, destino = edge.split('-')
        G.add_edge(nodo, destino)
    
    # Reconstruimos la clave a partir del grafo
    clave_desencriptada = ''.join(nx.topological_sort(G))
    
    return clave_desencriptada

# Solicitar la clave del usuario
clave_original = input("Introduce la clave que deseas encriptar: ")

# Generar la llave para Fernet y guardarla en un archivo
llave_fernet = generar_clave()
guardar_clave('clave_fernet.key', llave_fernet)
print(f"Clave Fernet generada y guardada en 'clave_fernet.key': {llave_fernet.decode()}")

# Encriptar la clave
clave_encriptada = encriptar_clave(clave_original, llave_fernet)
print(f"Clave encriptada: {clave_encriptada}")

# Leer la clave Fernet desde el archivo y usarla para desencriptar
llave_cargada = cargar_clave('clave_fernet.key')

# Desencriptar la clave
clave_desencriptada = desencriptar_clave(clave_encriptada, llave_cargada)
print(f"Clave desencriptada: {clave_desencriptada}")
