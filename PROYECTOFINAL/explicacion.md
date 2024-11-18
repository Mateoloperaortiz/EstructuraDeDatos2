# Buscador de Rutas de Vuelo

---

## Importación de Módulos

```python
import csv
from datetime import datetime
import json
from pathlib import Path
from collections import Counter
from typing import List, Tuple, Dict
```

- **csv**: Para leer archivos CSV que contienen las rutas de vuelo.
- **datetime**: Para manejar fechas y horas, especialmente al registrar el historial de búsquedas.
- **json**: Para leer y escribir archivos JSON utilizados en el historial y estadísticas.
- **pathlib.Path**: Para manejar rutas de archivos de manera más flexible.
- **collections.Counter**: Para contar y almacenar las rutas más populares.
- **typing**: Para proporcionar anotaciones de tipo que mejoran la legibilidad y mantenimiento del código.

---

## Clase `BuscadorRutas`

Esta clase encapsula toda la funcionalidad relacionada con la búsqueda de rutas, manejo del historial y estadísticas.

### Método `__init__`

```python
def __init__(self):
    self.grafo = {}
    self.historial_busquedas = []
    self.estadisticas = {'rutas_populares': Counter()}
    self.cargar_grafo("PROYECTOFINAL/rutas_vuelos.csv")
    self.cargar_historial()
```

- **`self.grafo`**: Un diccionario que representa el grafo de rutas aéreas, donde cada ciudad está conectada a otras mediante vuelos.
- **`self.historial_busquedas`**: Lista que almacena el historial de búsquedas realizadas por el usuario.
- **`self.estadisticas`**: Diccionario que almacena estadísticas, como las rutas más populares.
- **`cargar_grafo`**: Carga las rutas desde un archivo CSV y construye el grafo.
- **`cargar_historial`**: Carga el historial de búsquedas desde un archivo JSON.

---

### Método `cargar_grafo`

```python
def cargar_grafo(self, nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            next(lector)  # Salta la cabecera
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
```

- **Función**: Lee el archivo CSV de rutas y construye un grafo donde cada ciudad origen apunta a una lista de destinos con su costo y duración.
- **Manejo de Errores**: Si el archivo no existe, informa al usuario y termina el proceso de carga.

---

### Método `cargar_historial`

```python
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
```

- **Función**: Carga el historial de búsquedas y las estadísticas desde un archivo JSON.
- **Manejo de Errores**:
  - **FileNotFoundError**: Si el archivo no existe, crea uno nuevo con datos vacíos.
  - **JSONDecodeError**: Si el archivo está corrupto o mal formado, lo reemplaza por uno nuevo.

---

### Método `guardar_historial`

```python
def guardar_historial(self, nombre_archivo="PROYECTOFINAL/historial_busquedas.json"):
    data = {
        'busquedas': self.historial_busquedas,
        'rutas_populares': dict(self.estadisticas['rutas_populares'])
    }
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        json.dump(data, archivo, indent=2, ensure_ascii=False)
```

- **Función**: Guarda el historial de búsquedas y las estadísticas actuales en un archivo JSON.
- **Parámetros**:
  - **`nombre_archivo`**: Ruta donde se guardará el archivo JSON.

---

### Método `guardar_busqueda`

```python
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
```

- **Función**: Registra una nueva búsqueda en el historial.
- **Detalles**:
  - **`mejor_ruta`**: Se asume que la primera ruta en la lista es la mejor (debe estar previamente ordenada).
  - **`entrada_busqueda`**: Diccionario con detalles de la búsqueda realizada.
- **Actualización**: Agrega la entrada al historial y guarda los cambios.

---

### Método `encontrar_todas_las_rutas`

```python
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
```

- **Función**: Busca recursivamente todas las rutas desde una ciudad origen hasta una ciudad destino, respetando el precio máximo y el número máximo de escalas.
- **Parámetros**:
  - **`origen`**, **`destino`**: Ciudades entre las cuales se busca la ruta.
  - **`max_precio`**, **`max_escalas`**: Restricciones de búsqueda.
  - **`camino`**, **`costo_total`**, **`duracion_total`**: Variables utilizadas durante la recursión para acumular el camino y los costos.
- **Lógica**:
  - **Caso Base**: Si se llega al destino y el costo es aceptable, se retorna la ruta encontrada.
  - **Recursión**: Explora todas las conexiones desde la ciudad actual que no hayan sido visitadas aún.
- **Optimización**: Evita ciclos comprobando que la siguiente ciudad no esté ya en el camino actual.

---

### Método `mostrar_rutas`

```python
def mostrar_rutas(self, rutas: List[Dict], tipo_orden: str = "costo"):
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
        texto_escalas = "directa" if escalas == 0 else f"{escalas} escala{'s' if escalas > 1 else ''}"
        print(f"Tipo: Ruta {texto_escalas}")
        
        print(f"Costo total: ${ruta['costo']:.2f} USD")
        
        horas = int(ruta['duracion'])
        minutos = int((ruta['duracion'] - horas) * 60)
        print(f"Duración total: {horas}h {minutos:02d}min")
        
        print("-" * 40)
```

- **Función**: Muestra en consola las rutas encontradas de manera formateada y legible.
- **Detalles**:
  - **Ordenamiento**: Asume que las rutas ya están ordenadas según algún criterio (por defecto, costo).
  - **Formato de Salida**: Incluye información sobre el trayecto, tipo de ruta (directa o con escalas), costo y duración.

---

### Método `mostrar_historial`

```python
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
```

- **Función**: Muestra el historial de búsquedas realizadas por el usuario.
- **Detalles**:
  - Presenta cada búsqueda con su fecha, ruta, número de rutas encontradas y detalles de la mejor ruta.

---

### Método `actualizar_estadisticas`

```python
def actualizar_estadisticas(self, origen: str, destino: str, ruta_elegida: Dict):
    ruta_key = f"{origen}-{destino}"
    self.estadisticas['rutas_populares'][ruta_key] += 1
```

- **Función**: Actualiza el contador de rutas populares cada vez que se realiza una búsqueda.
- **Detalles**:
  - **`ruta_key`**: Clave que representa una ruta específica entre dos ciudades.
  - Incrementa en uno el contador para esa ruta.

---

### Método `mostrar_estadisticas`

```python
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
```

- **Función**: Muestra estadísticas generales sobre las búsquedas realizadas.
- **Detalles**:
  - Lista las rutas más populares basándose en el historial.
  - Calcula y muestra el total de búsquedas y el costo promedio de las rutas encontradas.

---

## Función `main`

Esta función es el punto de entrada de la aplicación y gestiona la interacción con el usuario.

```python
def main():
    buscador = BuscadorRutas()
    
    while True:
        print("\n" + "="*40)
        print(f"{'BUSCADOR DE RUTAS DE VUELO':^40}")
        print("="*40)
        print("1. Buscar rutas")
        print("2. Ver historial de búsquedas")
        print("3. Ver estadísticas")
        print("4. Salir")
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            # Solicita datos al usuario
            ciudad_origen = input("Ciudad de origen: ").strip().title()
            ciudad_destino = input("Ciudad destino: ").strip().title()
            
            # Verifica si la ciudad de origen existe en el grafo
            if ciudad_origen not in buscador.grafo:
                print(f"\nError: {ciudad_origen} no está en nuestra red de rutas")
                print("Ciudades disponibles:", ", ".join(sorted(buscador.grafo.keys())))
                continue

            # Solicita criterios de búsqueda
            try:
                precio_input = input("Precio máximo (Enter para sin límite): ").strip()
                max_precio = float(precio_input) if precio_input else float('inf')
                
                escalas_input = input("Número máximo de escalas (Enter para sin límite): ").strip()
                max_escalas = int(escalas_input) if escalas_input else 999
            except ValueError:
                print("Valor inválido. Usando sin límites.")
                max_precio = float('inf')
                max_escalas = 999

            # Busca rutas que cumplan con los criterios
            rutas = buscador.encontrar_todas_las_rutas(
                ciudad_origen, ciudad_destino,
                max_precio=max_precio,
                max_escalas=max_escalas
            )

            # Muestra las rutas encontradas
            if rutas:
                rutas_ordenadas = sorted(rutas, key=lambda x: x['costo'])
                buscador.mostrar_rutas(rutas_ordenadas[:10])
                buscador.actualizar_estadisticas(ciudad_origen, ciudad_destino, rutas_ordenadas[0])
                buscador.guardar_busqueda(ciudad_origen, ciudad_destino, rutas_ordenadas)
            else:
                print(f"\nNo se encontraron rutas entre {ciudad_origen} y {ciudad_destino}")
                print("que cumplan con los criterios especificados.")
                
        elif opcion == "2":
            buscador.mostrar_historial()
            
        elif opcion == "3":
            buscador.mostrar_estadisticas()
            
        elif opcion == "4":
            print("\n¡Gracias por usar el buscador de rutas!")
            break
            
        else:
            print("\nOpción no válida. Por favor, intente de nuevo.")
```

- **Interfaz de Usuario**:
  - Muestra un menú con opciones para buscar rutas, ver historial, ver estadísticas o salir.
- **Gestión de Opciones**:
  - **Opción 1**: Solicita información para buscar rutas y muestra los resultados.
  - **Opción 2**: Muestra el historial de búsquedas.
  - **Opción 3**: Muestra las estadísticas de búsquedas.
  - **Opción 4**: Termina la aplicación.
  - **Opción Inválida**: Informa al usuario y vuelve a mostrar el menú.

---

## Ejecución del Programa

```python
if __name__ == "__main__":
    main()
```

- **Función**: Indica que, si el script se ejecuta directamente, se llame a la función `main` para iniciar la aplicación.

---
