import pandas as pd
from collections import defaultdict, deque

class AutorGraph:
    def __init__(self):
        self.graph = defaultdict(set)
        self.all_authors = set()
        
    def add_paper(self, authors):
        for i in range(len(authors)):
            for j in range(len(authors)):
                if i != j and authors[i] and authors[j]:
                    self.graph[authors[i]].add(authors[j])
                    self.all_authors.add(authors[i])
                    self.all_authors.add(authors[j])
                    
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

def load_and_process_excel(filepath):
    df = pd.read_excel(filepath)

    graph = AutorGraph()

    for _, row in df.iterrows():
        authors = [row['Autor 1'], row['Autor 2'], row['Autor 3']]
        graph.add_paper(authors)
        
    return graph

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

if __name__ == "__main__":
    excel_path = "F:\\EstructuraDeDatos2\\ETAPAS\Etapa 10\\referencias.xlsx"
    main(excel_path)