from bigtree import *

# Crear los nodos con valores 
raiz = Node("Raiz", valor=1)
nodo_1 = Node("Nodo 1", valor=6)
nodo_2 = Node("Nodo 2", valor=5)
nodo_3 = Node("Nodo 3", valor=3)
nodo_4 = Node("Nodo 4", valor=2)
nodo_5 = Node("Nodo 5", valor=8)
nodo_6 = Node("Nodo 6", valor=9)
nodo_7 = Node("Nodo 7", valor=7)
nodo_8 = Node("Nodo 8", valor=4)

# Establecer los hijos de cada nodo
raiz.children = [nodo_1, nodo_2]
nodo_1.children = [nodo_3, nodo_4]
nodo_2.children = [nodo_5, nodo_6, nodo_7]
nodo_3.children = [nodo_8]

# Mostrar el árbol 
raiz.show()

# Recorrido en preorden
print([node.node_name for node in preorder_iter(raiz)])

# Pedir un valor a buscar
busq = int(input('Ingresa el valor que deseas buscar (1-9): '))

# Buscar el nodo que tenga el valor 
nodo_encontrado = find(raiz, lambda node: node.valor == busq)

# Mostrar el nombre del nodo encontrado
print(f"Nodo que contiene ese valor: {nodo_encontrado.node_name if nodo_encontrado else 'No encontrado'}")