import csv
from datetime import datetime
import json
from pathlib import Path

class BuscadorRutas:
    def __init__(self):
        self.grafo = {}
        self.historial_busquedas = []
        self.cargar_grafo()
        self.cargar_historial()

    def cargar_grafo(self, nombre_archivo="rutas.csv"):
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                lector = csv.reader(archivo)
                next(lector)
                self.grafo = {}
                
                for fila in lector:
                    origen, destino, costo = fila
                    costo = float(costo)
                    
                    if origen not in self.grafo:
                        self.grafo[origen] = []
                    self.grafo[origen].append((destino, costo))
                    
            print(f"Datos cargados exitosamente de {nombre_archivo}")
        except FileNotFoundError:
            print(f"No se encontró el archivo {nombre_archivo}. Creando uno nuevo...")
            self._crear_datos_ejemplo(nombre_archivo)

    def _crear_datos_ejemplo(self, nombre_archivo):
        datos_ejemplo = [
            ['origen', 'destino', 'costo'],
            ['Medellin', 'Bogota', '58.85'],
            ['Medellin', 'Barranquilla', '89.44'],
            ['Medellin', 'Cartagena', '96.40'],
            ['Medellin', 'Montreal', '498.71'],
            ['Medellin', 'Toronto', '509.62'],
            ['Bogota', 'Medellin', '58.85'],
            ['Bogota', 'Barranquilla', '80.66'],
            ['Bogota', 'Cartagena', '82.71'],
            ['Bogota', 'Montreal', '419.10'],
            ['Bogota', 'Toronto', '428.49']
        ]
        
        with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerows(datos_ejemplo)

    def cargar_historial(self, nombre_archivo="historial_busquedas.json"):
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                self.historial_busquedas = json.load(archivo)
        except FileNotFoundError:
            self.historial_busquedas = []

    def guardar_historial(self, nombre_archivo="historial_busquedas.json"):
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(self.historial_busquedas, archivo, indent=2, ensure_ascii=False)

    def guardar_busqueda(self, origen, destino, rutas):
        entrada_busqueda = {
            'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'origen': origen,
            'destino': destino,
            'rutas_encontradas': len(rutas),
            'mejor_precio': min(costo for _, costo in rutas) if rutas else None,
            'menos_escalas': min(len(camino) - 1 for camino, _ in rutas) if rutas else None
        }
        self.historial_busquedas.append(entrada_busqueda)
        self.guardar_historial()

    def encontrar_todas_las_rutas(self, origen, destino, camino=None, costo_total=0):
        if camino is None:
            camino = []
        
        camino_actual = camino + [origen]
        
        if origen == destino:
            return [(camino_actual, costo_total)]
            
        if origen not in self.grafo:
            return []
            
        rutas = []
        for siguiente_ciudad, costo in self.grafo[origen]:
            if siguiente_ciudad not in camino_actual:
                nuevas_rutas = self.encontrar_todas_las_rutas(
                    siguiente_ciudad, destino, camino_actual, costo_total + costo
                )
                rutas.extend(nuevas_rutas)
        
        return rutas

    def obtener_mejores_rutas(self, rutas, limite=10, ordenar_por="costo"):
        if ordenar_por == "costo":
            rutas_ordenadas = self.ordenar_por_costo(rutas.copy())
        else:
            rutas_ordenadas = self.ordenar_por_escalas(rutas.copy())
        
        return rutas_ordenadas[:limite]

    def ordenar_por_costo(self, rutas):
        for i in range(1, len(rutas)):
            clave = rutas[i]
            j = i - 1
            while j >= 0 and clave[1] < rutas[j][1]:
                rutas[j + 1] = rutas[j]
                j -= 1
            rutas[j + 1] = clave
        return rutas

    def ordenar_por_escalas(self, rutas):
        for i in range(1, len(rutas)):
            clave = rutas[i]
            j = i - 1
            while j >= 0 and len(clave[0]) < len(rutas[j][0]):
                rutas[j + 1] = rutas[j]
                j -= 1
            rutas[j + 1] = clave
        return rutas

    def mostrar_rutas(self, rutas, tipo_orden="costo"):
        if not rutas:
            print("No se encontraron rutas.")
            return

        if tipo_orden == "costo":
            print("\nTOP 10 RUTAS POR COSTO EN USD (DE MENOR A MAYOR):")
            for camino, costo in rutas:
                print(f"Ruta: {' → '.join(camino)}")
                print(f"Costo total: ${costo:.2f} USD\n")
        else:
            print("\nTOP 10 RUTAS POR CANTIDAD DE ESCALAS (DE MENOR A MAYOR):")
            for camino, costo in rutas:
                escalas = len(camino) - 2
                print(f"Ruta: {' → '.join(camino)}")
                print(f"Cantidad de escalas: {escalas}\n")

    def mostrar_historial(self):
        if not self.historial_busquedas:
            print("\nNo hay historial de búsquedas.")
            return

        print("\nHISTORIAL DE BÚSQUEDAS:")
        print("-" * 80)
        for entrada in self.historial_busquedas:
            print(f"Fecha: {entrada['fecha']}")
            print(f"Origen: {entrada['origen']}")
            print(f"Destino: {entrada['destino']}")
            print(f"Rutas encontradas: {entrada['rutas_encontradas']}")
            if entrada['mejor_precio']:
                print(f"Mejor precio: ${entrada['mejor_precio']:.2f} USD")
            if entrada['menos_escalas'] is not None:
                print(f"Menor cantidad de escalas: {entrada['menos_escalas']}")
            print("-" * 80)

def main():
    buscador = BuscadorRutas()
    
    while True:
        print("\n=== BUSCADOR DE RUTAS DE VUELO ===")
        print("1. Buscar rutas")
        print("2. Ver historial de búsquedas")
        print("3. Salir")
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            ciudad_origen = input("Ingrese su ciudad de origen: ").strip().title()
            ciudad_destino = input("Ingrese su ciudad destino: ").strip().title()
            
            rutas = buscador.encontrar_todas_las_rutas(ciudad_origen, ciudad_destino)
            if rutas:
                mejores_rutas_costo = buscador.obtener_mejores_rutas(rutas, limite=10, ordenar_por="costo")
                buscador.mostrar_rutas(mejores_rutas_costo, "costo")
                
                mejores_rutas_escalas = buscador.obtener_mejores_rutas(rutas, limite=10, ordenar_por="escalas")
                buscador.mostrar_rutas(mejores_rutas_escalas, "escalas")
                
                buscador.guardar_busqueda(ciudad_origen, ciudad_destino, rutas)
            else:
                print(f"\nNo se encontraron rutas entre {ciudad_origen} y {ciudad_destino}")
        
        elif opcion == "2":
            buscador.mostrar_historial()
        
        elif opcion == "3":
            print("\n¡Gracias por usar el buscador de rutas!")
            break
        
        else:
            print("\nOpción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()