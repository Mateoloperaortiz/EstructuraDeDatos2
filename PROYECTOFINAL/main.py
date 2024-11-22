import csv
from datetime import datetime
import json
from pathlib import Path
from collections import Counter
from typing import List, Tuple, Dict

class BuscadorRutas:
    def __init__(self):
        self.grafo = {}
        self.historial_busquedas = []
        self.estadisticas = {'rutas_populares': Counter()}
        self.cargar_grafo("PROYECTOFINAL/rutas_vuelos.csv")
        self.cargar_historial()

    def cargar_grafo(self, nombre_archivo):
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                lector = csv.reader(archivo)
                next(lector)
                self.grafo = {}
                
                for fila in lector:
                    origen, destino, costo, duracion = fila
                    if origen not in self.grafo:
                        self.grafo[origen] = []
                    self.grafo[origen].append({
                        'destino': destino,
                        'costo': float(costo),
                        'duracion': float(duracion)
                    })
                    
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {nombre_archivo}")
            return

    def cargar_historial(self, nombre_archivo="historial_busquedas.json"):
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                data = json.load(archivo)
                self.historial_busquedas = data['busquedas']
                self.estadisticas['rutas_populares'].update(data.get('rutas_populares', {}))
        except FileNotFoundError:
            self.historial_busquedas = []
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                json.dump({'busquedas': [], 'rutas_populares': {}}, archivo)
        except json.JSONDecodeError:
            print("Error al leer el historial. Creando uno nuevo.")
            self.historial_busquedas = []
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                json.dump({'busquedas': [], 'rutas_populares': {}}, archivo)

    def guardar_historial(self, nombre_archivo="PROYECTOFINAL/historial_busquedas.json"):
        data = {
            'busquedas': self.historial_busquedas,
            'rutas_populares': dict(self.estadisticas['rutas_populares'])
        }
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(data, archivo, indent=2, ensure_ascii=False)

    def guardar_busqueda(self, origen, destino, rutas):
        mejor_ruta = rutas[0] if rutas else None
        entrada_busqueda = {
            'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'origen': origen,
            'destino': destino,
            'rutas_encontradas': len(rutas),
            'mejor_precio': mejor_ruta['costo'] if mejor_ruta else None,
            'mejor_duracion': mejor_ruta['duracion'] if mejor_ruta else None,
            'menos_escalas': len(mejor_ruta['camino']) - 2 if mejor_ruta else None
        }
        self.historial_busquedas.append(entrada_busqueda)
        self.guardar_historial()

    def encontrar_todas_las_rutas(self, origen: str, destino: str, max_precio: float = float('inf'),
                                 max_escalas: int = float('inf'), camino=None, costo_total=0.0, duracion_total=0.0):
        if camino is None:
            camino = []
        
        camino_actual = camino + [origen]
        
        if len(camino_actual) - 1 > max_escalas + 1:
            return []
            
        if origen == destino:
            if costo_total <= max_precio:
                return [{'camino': camino_actual, 'costo': costo_total, 'duracion': duracion_total}]
            return []
            
        if origen not in self.grafo:
            return []
            
        rutas = []
        for conexion in self.grafo[origen]:
            siguiente = conexion['destino']
            if siguiente not in camino_actual:
                nuevo_costo = costo_total + conexion['costo']
                if nuevo_costo <= max_precio:
                    nuevas_rutas = self.encontrar_todas_las_rutas(
                        siguiente, destino, max_precio, max_escalas,
                        camino_actual, nuevo_costo, duracion_total + conexion['duracion']
                    )
                    rutas.extend(nuevas_rutas)
        
        return rutas

    def mostrar_rutas(self, rutas: List[Dict]):
        if not rutas:
            print("\nNo se encontraron rutas que cumplan con los criterios especificados.")
            return

        print("\n" + "="*80)
        print(f"{'RUTAS ENCONTRADAS':^80}")
        print("="*80)

        for i, ruta in enumerate(rutas, 1):
            print(f"\nRuta {i}:")
            print("-" * 40)
            
            camino = " → ".join(ruta['camino'])
            print(f"Trayecto: {camino}")
            
            escalas = len(ruta['camino']) - 2
            if escalas == 0:
                texto_escalas = "directa"
            else:
                texto_escalas = f"{escalas} escala{'s' if escalas > 1 else ''}"
            print(f"Tipo: Ruta {texto_escalas}")
            
            print(f"Costo total: ${ruta['costo']:.2f} USD")
            
            horas = int(ruta['duracion'])
            minutos = int((ruta['duracion'] - horas) * 60)
            print(f"Duración total: {horas}h {minutos:02d}min")
            
            print("-" * 40)

    def mostrar_historial(self):
        if not self.historial_busquedas:
            print("\nNo hay historial de búsquedas.")
            return

        print("\n" + "="*80)
        print(f"{'HISTORIAL DE BÚSQUEDAS':^80}")
        print("="*80)
        
        for entrada in self.historial_busquedas:
            print(f"\nFecha: {entrada['fecha']}")
            print(f"Ruta: {entrada['origen']} → {entrada['destino']}")
            print(f"Rutas encontradas: {entrada['rutas_encontradas']}")
            
            if entrada['mejor_precio']:
                print(f"Mejor precio: ${entrada['mejor_precio']:.2f} USD")
            
            if entrada['mejor_duracion']:
                horas = int(entrada['mejor_duracion'])
                minutos = int((entrada['mejor_duracion'] - horas) * 60)
                print(f"Mejor duración: {horas}h {minutos:02d}min")
            
            if entrada['menos_escalas'] is not None:
                print(f"Menor cantidad de escalas: {entrada['menos_escalas']}")
            
            print("-" * 40)

    def actualizar_estadisticas(self, origen: str, destino: str):
        ruta_key = f"{origen}-{destino}"
        self.estadisticas['rutas_populares'][ruta_key] += 1

    def mostrar_estadisticas(self):
        print("\n" + "="*80)
        print(f"{'ESTADÍSTICAS DE BÚSQUEDAS':^80}")
        print("="*80)
        
        if not self.estadisticas['rutas_populares']:
            print("\nAún no hay estadísticas disponibles.")
            return

        print("\nRutas más buscadas:")
        for ruta, cantidad in self.estadisticas['rutas_populares'].most_common(5):
            origen, destino = ruta.split('-')
            print(f"{origen} → {destino}: {cantidad} búsqueda{'s' if cantidad > 1 else ''}")

        if self.historial_busquedas:
            total_busquedas = len(self.historial_busquedas)
            suma_costos = sum(b['mejor_precio'] for b in self.historial_busquedas if b['mejor_precio'])
            promedio_costo = suma_costos / total_busquedas if total_busquedas > 0 else 0
            
            print(f"\nTotal de búsquedas realizadas: {total_busquedas}")
            print(f"Costo promedio de rutas: ${promedio_costo:.2f} USD")

def main():
    buscador = BuscadorRutas()
    
    while True:
        mostrar_menu()
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            opcion_buscar_rutas(buscador)
        elif opcion == "2":
            buscador.mostrar_historial()
        elif opcion == "3":
            buscador.mostrar_estadisticas()
        elif opcion == "4":
            print("\n¡Gracias por usar el buscador de rutas!")
            break
        else:
            print("\nOpción no válida. Por favor, intente de nuevo.")

def mostrar_menu():
    print("\n" + "="*40)
    print(f"{'BUSCADOR DE RUTAS DE VUELO':^40}")
    print("="*40)
    print("1. Buscar rutas")
    print("2. Ver historial de búsquedas")
    print("3. Ver estadísticas")
    print("4. Salir")

def opcion_buscar_rutas(buscador):
    ciudad_origen = input("Ciudad de origen: ").strip().title()
    ciudad_destino = input("Ciudad destino: ").strip().title()
    
    if ciudad_origen not in buscador.grafo:
        print(f"\nError: {ciudad_origen} no está en nuestra red de rutas")
        print("Ciudades disponibles:", ", ".join(sorted(buscador.grafo.keys())))
        return

    try:
        precio_input = input("Precio máximo (Enter para sin límite): ").strip()
        max_precio = float(precio_input) if precio_input else float('inf')
        
        escalas_input = input("Número máximo de escalas (Enter para sin límite): ").strip()
        max_escalas = int(escalas_input) if escalas_input else 999
    except ValueError:
        print("Valor inválido. Usando sin límites.")
        max_precio = float('inf')
        max_escalas = 999

    rutas = buscador.encontrar_todas_las_rutas(
        ciudad_origen, ciudad_destino,
        max_precio=max_precio,
        max_escalas=max_escalas
    )

    if rutas:
        rutas_ordenadas = sorted(rutas, key=lambda x: x['costo'])
        buscador.mostrar_rutas(rutas_ordenadas[:10])
        buscador.actualizar_estadisticas(ciudad_origen, ciudad_destino)
        buscador.guardar_busqueda(ciudad_origen, ciudad_destino, rutas_ordenadas)
    else:
        print(f"\nNo se encontraron rutas entre {ciudad_origen} y {ciudad_destino}")
        print("que cumplan con los criterios especificados.")

if __name__ == "__main__":
    main()