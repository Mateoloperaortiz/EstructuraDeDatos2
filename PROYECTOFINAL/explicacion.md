# Documentación del Buscador de Rutas de Vuelo

## Descripción General

Este programa implementa un sistema de búsqueda de rutas de vuelo utilizando grafos y algoritmos de ordenamiento. Permite encontrar todas las rutas posibles entre dos ciudades, ordenarlas por costo o número de escalas, y mantener un historial de búsquedas.

## Estructura del Proyecto

### Archivos del Sistema

- **buscador_rutas.py**: Archivo principal con el código del programa
- **rutas.csv**: Base de datos de rutas y costos
- **historial_busquedas.json**: Almacenamiento del historial de búsquedas

### Clase Principal: BuscadorRutas

#### Atributos

- `grafo`: Diccionario que almacena el grafo de rutas
- `historial_busquedas`: Lista que almacena el historial de búsquedas realizadas

#### Métodos Principales

##### Gestión de Datos

1. `cargar_grafo()`
   - Carga las rutas desde el archivo CSV
   - Crea la estructura del grafo en memoria
   - Si no existe el archivo, crea uno con datos de ejemplo

2. `cargar_historial()` y `guardar_historial()`
   - Manejan la persistencia del historial de búsquedas
   - Utilizan formato JSON para almacenamiento

##### Algoritmos de Búsqueda

1. `encontrar_todas_las_rutas(origen, destino)`
   - Implementa búsqueda en profundidad (DFS)
   - Encuentra todos los caminos posibles entre dos ciudades
   - Calcula el costo total de cada ruta
   - Evita ciclos en las rutas

##### Algoritmos de Ordenamiento

1. `ordenar_por_costo(rutas)`
   - Implementa ordenamiento por inserción
   - Ordena las rutas de menor a mayor costo

2. `ordenar_por_escalas(rutas)`
   - Implementa ordenamiento por inserción
   - Ordena las rutas por número de escalas

##### Visualización

1. `mostrar_rutas(rutas, tipo_orden)`
   - Muestra las mejores 10 rutas encontradas
   - Formatea la salida según el tipo de ordenamiento
   - Incluye detalles de costo y escalas

2. `mostrar_historial()`
   - Muestra el historial de búsquedas realizadas
   - Incluye estadísticas de cada búsqueda

## Estructuras de Datos Utilizadas

### 1. Grafo

- **Implementación**: Diccionario de listas de adyacencia
- **Estructura**:

```python
{
    'ciudad_origen': [('ciudad_destino', costo), ...]
}
```

### 2. Rutas

- **Implementación**: Lista de tuplas
- **Estructura**:

```python
[
    ([ciudad1, ciudad2, ..., ciudadN], costo_total),
    ...
]
```

### 3. Historial

- **Implementación**: Lista de diccionarios
- **Estructura**:

```python
[
    {
        'fecha': timestamp,
        'origen': ciudad,
        'destino': ciudad,
        'rutas_encontradas': cantidad,
        'mejor_precio': valor,
        'menos_escalas': valor
    },
    ...
]
```

## Algoritmos Implementados

### 1. Búsqueda en Profundidad (DFS)

- Utilizado para encontrar todas las rutas posibles
- Complejidad temporal: O(V + E) donde V son vértices y E aristas
- Implementado de forma recursiva
- Incluye control de ciclos

### 2. Ordenamiento por Inserción

- Utilizado para ordenar rutas por costo y escalas
- Complejidad temporal: O(n²)
- Ventajas:
  - Simple de implementar
  - Eficiente para conjuntos pequeños
  - Estable (mantiene el orden relativo)

## Uso del Programa

### Requisitos

- Python 3.x
- Archivos necesarios en el mismo directorio

### Ejecución

1. Preparar el archivo CSV con las rutas
2. Ejecutar el programa:

```bash
python buscador_rutas.py
```

### Opciones del Menú

1. **Buscar rutas**
   - Ingresa ciudad de origen y destino
   - Muestra top 10 rutas por costo y escalas
   - Guarda automáticamente en el historial

2. **Ver historial de búsquedas**
   - Muestra búsquedas anteriores
   - Incluye estadísticas de cada búsqueda

3. **Salir**
   - Termina la ejecución del programa

## Ejemplo de Uso

```python
=== BUSCADOR DE RUTAS DE VUELO ===
1. Buscar rutas
2. Ver historial de búsquedas
3. Salir

Seleccione una opción: 1
Ingrese su ciudad de origen: Medellin
Ingrese su ciudad destino: Toronto

TOP 10 RUTAS POR COSTO EN USD (DE MENOR A MAYOR):
Ruta: Medellin → Toronto
Costo total: $509.62 USD
...
```
