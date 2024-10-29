# Análisis Detallado del Código para Grafo de Autores

---

## Tabla de Contenidos

- [Análisis Detallado del Código para Grafo de Autores](#análisis-detallado-del-código-para-grafo-de-autores)
  - [Tabla de Contenidos](#tabla-de-contenidos)
  - [1. Importación de Módulos](#1-importación-de-módulos)
  - [2. Clase `AutorGraph`](#2-clase-autorgraph)
    - [Definición de la Clase](#definición-de-la-clase)
    - [Método `__init__`](#método-__init__)
    - [Método `add_paper`](#método-add_paper)
    - [Método `find_connection_level`](#método-find_connection_level)
    - [Método `find_path`](#método-find_path)
    - [Método `find_max_connection_level`](#método-find_max_connection_level)
  - [3. Función `load_and_process_excel`](#3-función-load_and_process_excel)
  - [4. Función `main`](#4-función-main)
  - [5. Ejecución del Script](#5-ejecución-del-script)

---

## 1. Importación de Módulos

```python
import pandas as pd
from collections import defaultdict, deque
```

- **`pandas`**: Biblioteca utilizada para manipular y analizar datos, especialmente para leer archivos Excel.
- **`defaultdict` y `deque`**: Estructuras de datos del módulo `collections` que facilitan la implementación de grafos y algoritmos de recorrido.

---

## 2. Clase `AutorGraph`

Esta clase representa el grafo de autores, donde los nodos son autores y las aristas representan colaboraciones entre ellos.

### Definición de la Clase

```python
class AutorGraph:
    def __init__(self):
        self.graph = defaultdict(set)
        self.all_authors = set()
    ...
```

- **`self.graph`**: Un diccionario donde cada clave es un autor y su valor es un conjunto de coautores.
- **`self.all_authors`**: Un conjunto que contiene todos los autores presentes en el grafo.

### Método `__init__`

Inicializa el grafo y el conjunto de autores.

```python
def __init__(self):
    self.graph = defaultdict(set)
    self.all_authors = set()
```

- Utiliza `defaultdict(set)` para facilitar la adición de coautores sin necesidad de verificar si la clave existe.
- Inicializa `all_authors` como un conjunto vacío para almacenar todos los autores únicos.

### Método `add_paper`

Agrega un paper al grafo, estableciendo conexiones entre los autores que colaboraron en él.

```python
def add_paper(self, authors):
    for i in range(len(authors)):
        for j in range(len(authors)):
            if i != j and authors[i] and authors[j]:
                self.graph[authors[i]].add(authors[j])
                self.all_authors.add(authors[i])
                self.all_authors.add(authors[j])
```

- **Parámetros**: `authors` - Lista de autores que colaboraron en un paper.
- **Funcionalidad**:
  - Itera sobre todos los pares de autores para crear conexiones bidireccionales.
  - Evita agregar conexiones de un autor consigo mismo (`i != j`).
  - Verifica que los nombres de los autores no sean nulos (`authors[i]` y `authors[j]`).
  - Actualiza el grafo y el conjunto de todos los autores.

### Método `find_connection_level`

Encuentra el nivel de conexión (distancia mínima) entre dos autores.

```python
def find_connection_level(self, author1, author2):
    if author1 not in self.graph or author2 not in self.graph:
        return -1
    
    if author1 == author2:
        return 0

    visited = set()
    queue = deque([(author1, 0)])
    visited.add(author1)
    
    while queue:
        current_author, level = queue.popleft()

        for coauthor in self.graph[current_author]:
            if coauthor == author2:
                return level + 1
                
            if coauthor not in visited:
                visited.add(coauthor)
                queue.append((coauthor, level + 1))
    
    return -1
```

- **Parámetros**: `author1`, `author2` - Nombres de los autores.
- **Funcionalidad**:
  - Verifica que ambos autores existan en el grafo.
  - Si los autores son iguales, el nivel de conexión es 0.
  - Utiliza una búsqueda en anchura (BFS) para encontrar la distancia mínima.
  - Si encuentra al autor objetivo, devuelve el nivel de conexión.
  - Si no hay conexión, devuelve -1.

### Método `find_path`

Encuentra el camino (ruta de colaboración) entre dos autores.

```python
def find_path(self, author1, author2):
    if author1 not in self.graph or author2 not in self.graph:
        return None
    
    if author1 == author2:
        return [author1]

    visited = {author1: None}
    queue = deque([author1])
    
    while queue:
        current_author = queue.popleft()
        
        for coauthor in self.graph[current_author]:
            if coauthor not in visited:
                visited[coauthor] = current_author
                queue.append(coauthor)
                
                if coauthor == author2:
                    # Reconstruir el camino
                    path = []
                    current = author2
                    while current is not None:
                        path.append(current)
                        current = visited[current]
                    return path[::-1]
    
    return None
```

- **Parámetros**: `author1`, `author2` - Nombres de los autores.
- **Funcionalidad**:
  - Verifica que ambos autores existan en el grafo.
  - Si los autores son iguales, devuelve una lista con ese autor.
  - Utiliza BFS para encontrar el camino.
  - Mantiene un diccionario `visited` para reconstruir el camino.
  - Si encuentra al autor objetivo, reconstruye y devuelve el camino.
  - Si no hay camino, devuelve `None`.

### Método `find_max_connection_level`

Encuentra el nivel máximo de conexión en toda la red y los autores involucrados.

```python
def find_max_connection_level(self):
    max_level = 0
    max_pair = (None, None)
    all_authors = list(self.all_authors)

    for i in range(len(all_authors)):
        for j in range(i + 1, len(all_authors)):
            level = self.find_connection_level(all_authors[i], all_authors[j])
            if level > max_level and level != -1:
                max_level = level
                max_pair = (all_authors[i], all_authors[j])
                
    return max_level, max_pair
```

- **Funcionalidad**:
  - Inicializa el nivel máximo y la pareja de autores.
  - Itera sobre todos los pares de autores únicos.
  - Calcula el nivel de conexión entre cada par.
  - Actualiza el nivel máximo y los autores si encuentra un nivel mayor.
  - Devuelve el nivel máximo y la pareja de autores asociada.

---

## 3. Función `load_and_process_excel`

Carga y procesa el archivo Excel para construir el grafo de autores.

```python
def load_and_process_excel(filepath):
    df = pd.read_excel(filepath)

    graph = AutorGraph()

    for _, row in df.iterrows():
        authors = [row['Autor 1'], row['Autor 2'], row['Autor 3']]
        graph.add_paper(authors)
        
    return graph
```

- **Parámetros**: `filepath` - Ruta del archivo Excel.
- **Funcionalidad**:
  - Lee el archivo Excel usando `pandas`.
  - Crea una instancia de `AutorGraph`.
  - Itera sobre cada fila del DataFrame.
  - Extrae los autores y los agrega al grafo mediante `add_paper`.
  - Devuelve el grafo construido.

---

## 4. Función `main`

Función principal que interactúa con el usuario y proporciona el menú de opciones.

```python
def main(excel_path):
    # Crear el grafo desde el archivo Excel
    print("Cargando y procesando el archivo Excel...")
    graph = load_and_process_excel(excel_path)
    
    while True:
        print("\nMenú:")
        print("1. Encontrar nivel de conexión entre dos autores")
        print("2. Encontrar el nivel máximo de conexión en toda la red")
        print("3. Ver el camino entre dos autores")
        print("4. Salir")
        
        opcion = input("\nSeleccione una opción (1-4): ")
        
        if opcion == '1':
            autor1 = input("Ingrese el nombre del primer autor: ")
            autor2 = input("Ingrese el nombre del segundo autor: ")
            
            nivel = graph.find_connection_level(autor1, autor2)
            if nivel != -1:
                print(f"\nEl nivel de conexión entre {autor1} y {autor2} es: {nivel}")
            else:
                print(f"\nNo existe conexión entre {autor1} y {autor2}")
                
        elif opcion == '2':
            max_nivel, (autor1, autor2) = graph.find_max_connection_level()
            print(f"\nEl nivel máximo de conexión en el grafo es: {max_nivel}")
            print(f"Entre los autores: {autor1} y {autor2}")
            
        elif opcion == '3':
            autor1 = input("Ingrese el nombre del primer autor: ")
            autor2 = input("Ingrese el nombre del segundo autor: ")
            
            path = graph.find_path(autor1, autor2)
            if path:
                print("\nCamino encontrado:")
                print(" -> ".join(path))
            else:
                print("\nNo existe un camino entre estos autores")
                
        elif opcion == '4':
            print("\n¡Hasta luego!")
            break
            
        else:
            print("\nOpción no válida. Por favor, seleccione una opción válida.")
```

- **Parámetros**: `excel_path` - Ruta del archivo Excel.
- **Funcionalidad**:
  - Carga y procesa el archivo Excel para crear el grafo.
  - Muestra un menú interactivo al usuario con cuatro opciones:
    1. Encontrar el nivel de conexión entre dos autores.
    2. Encontrar el nivel máximo de conexión en la red.
    3. Ver el camino entre dos autores.
    4. Salir del programa.
  - Procesa la entrada del usuario y ejecuta la opción seleccionada.
  - Maneja casos en los que no existe conexión o camino entre autores.
  - Permite al usuario realizar múltiples consultas hasta que decida salir.

---

## 5. Ejecución del Script

El bloque final del código verifica si el script se está ejecutando directamente y, en ese caso, llama a la función `main` con la ruta del archivo Excel.

```python
if __name__ == "__main__":
    excel_path = "F:\\EstructuraDeDatos2\\ETAPAS\\Etapa 10\\referencias.xlsx"
    main(excel_path)
```

- **Funcionalidad**:
  - Comprueba si el archivo se está ejecutando como programa principal.
  - Define la ruta al archivo Excel con los datos de autores.
  - Llama a `main(excel_path)` para iniciar el programa.