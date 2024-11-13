# Recomendador de Destinos Turísticos en Python

## Tabla de Contenido

- [Recomendador de Destinos Turísticos en Python](#recomendador-de-destinos-turísticos-en-python)
  - [Tabla de Contenido](#tabla-de-contenido)
  - [Descripción General](#descripción-general)
  - [Datos de los Municipios](#datos-de-los-municipios)
    - [Ejemplo](#ejemplo)
  - [Funciones del Script](#funciones-del-script)
    - [Función `encontrar_municipio`](#función-encontrar_municipio)
    - [Función `calcular_similitud`](#función-calcular_similitud)
  - [Flujo del Programa](#flujo-del-programa)
  - [Ejemplo de Uso](#ejemplo-de-uso)

## Descripción General

El objetivo del script es recomendar al usuario un destino turístico basado en un municipio que le haya gustado previamente. Para ello, se utilizan métricas como la altitud y las distancias desde ciertos puntos de referencia para calcular la similitud entre municipios.

## Datos de los Municipios

Los datos se almacenan en una lista llamada `datos`, donde cada elemento es una lista que representa un municipio con la siguiente estructura:

```python
[
    'Municipio',
    Temperatura (°C),
    Altura sobre el nivel del mar (metros),
    'Actividades',
    Distancia desde Medellín (Km),
    Distancia desde Rionegro (Km),
    Distancia desde Santa Fe de Antioquia (Km),
    Distancia desde Barbosa (Km),
    Distancia desde Caldas (Km)
]
```

### Ejemplo

```python
datos = [
    ['Medellín', 24, 1495, 'Turismo urbano, visitas a museos y parques, recorridos gastronómicos, entre otros.', 0, 33, 83, 18, 13],
    # ... otros municipios ...
]
```

## Funciones del Script

El script utiliza dos funciones principales:

### Función `encontrar_municipio`

Busca un municipio en la lista `datos` basado en el nombre proporcionado por el usuario.

```python
def encontrar_municipio(nombre, datos):
    for municipio in datos:
        if municipio[0].lower() == nombre.lower():
            return municipio
    return None
```

**Parámetros:**

- `nombre`: Nombre del municipio que se desea buscar.
- `datos`: Lista de municipios.

**Retorna:**

- La lista que representa al municipio si se encuentra.
- `None` si no se encuentra el municipio.

### Función `calcular_similitud`

Calcula una métrica de similitud entre dos municipios basándose en la diferencia de altitud y las distancias desde puntos de referencia.

```python
def calcular_similitud(m1, m2):
    # Diferencia en altitud
    diferencia_altura = abs(m1[2] - m2[2])
    
    # Distancias desde puntos de referencia
    distancias_m1 = m1[4:9]
    distancias_m2 = m2[4:9]
    
    # Suma de las diferencias absolutas de las distancias
    diferencia_distancias = sum([abs(d1 - d2) for d1, d2 in zip(distancias_m1, distancias_m2)])
    
    # Similitud total
    similitud = diferencia_altura + diferencia_distancias
    return similitud
```

**Parámetros:**

- `m1`: Lista que representa el primer municipio.
- `m2`: Lista que representa el segundo municipio.

**Retorna:**

- Un valor numérico que representa la similitud; valores más bajos indican mayor similitud.

## Flujo del Programa

1. **Solicitud al Usuario:**

   El programa solicita al usuario que ingrese el nombre de un municipio que le haya gustado.

   ```python
   municipio_usuario = input("Ingrese el nombre de un municipio que le haya gustado: ")
   ```

2. **Búsqueda del Municipio:**

   Utiliza la función `encontrar_municipio` para buscar el municipio en los datos.

   ```python
   municipio_preferido = encontrar_municipio(municipio_usuario, datos)
   ```

   - Si no se encuentra, muestra un mensaje de error.
   - Si se encuentra, procede al siguiente paso.

3. **Cálculo de Similitudes:**

   Calcula la similitud entre el municipio preferido y todos los demás municipios utilizando la función `calcular_similitud`.

   ```python
   similitudes = []
   for municipio in datos:
       if municipio[0].lower() != municipio_preferido[0].lower():
           similitud = calcular_similitud(municipio_preferido, municipio)
           similitudes.append((similitud, municipio))
   ```

4. **Ordenamiento y Selección:**

   Ordena la lista de similitudes y selecciona el municipio con el valor más bajo (mayor similitud).

   ```python
   similitudes.sort(key=lambda x: x[0])
   municipio_recomendado = similitudes[0][1]
   ```

5. **Salida al Usuario:**

   Muestra al usuario la recomendación basada en su preferencia.

   ```python
   print("\nBasado en su preferencia por {}, le recomendamos visitar {}.".format(municipio_preferido[0], municipio_recomendado[0]))
   print("Actividades en {}: {}".format(municipio_recomendado[0], municipio_recomendado[3]))
   ```

## Ejemplo de Uso

**Entrada del Usuario:**

```less
Ingrese el nombre de un municipio que le haya gustado: Medellín
```

**Salida del Programa:**

```less
Basado en su preferencia por Medellín, le recomendamos visitar Itagüí.
Actividades en Itagüí: Turismo urbano, visitas a centros comerciales y sitios culturales, entre otros.
```
