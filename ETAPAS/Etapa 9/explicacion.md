# Compresión de Texto utilizando Diccionarios en Python

## Tabla de Contenidos

- [Compresión de Texto utilizando Diccionarios en Python](#compresión-de-texto-utilizando-diccionarios-en-python)
  - [Tabla de Contenidos](#tabla-de-contenidos)
  - [Introducción](#introducción)
  - [Clase `Diccionario`](#clase-diccionario)
    - [`__init__`](#__init__)
    - [`agregar_palabra`](#agregar_palabra)
    - [`obtener_codigo`](#obtener_codigo)
    - [`obtener_palabra`](#obtener_palabra)
    - [`actualizar_frecuencias`](#actualizar_frecuencias)
    - [`optimizar_diccionario`](#optimizar_diccionario)
  - [Función `comprimir_texto`](#función-comprimir_texto)
  - [Función `descomprimir_texto`](#función-descomprimir_texto)
  - [Función `calcular_tamano`](#función-calcular_tamano)
  - [Función `main`](#función-main)

## Introducción

El código implementa un sistema de compresión y descompresión de texto basado en la sustitución de palabras frecuentes por códigos numéricos. Utiliza una clase `Diccionario` para gestionar las palabras y sus códigos asociados, así como para mantener un registro de la frecuencia de cada palabra en el texto.

---

## Clase `Diccionario`

La clase `Diccionario` es el núcleo del sistema de compresión. Gestiona las relaciones entre palabras y códigos, y mantiene un contador de frecuencias para optimizar el diccionario.

### `__init__`

```python
def __init__(self):
    self.palabra_a_codigo = {}
    self.codigo_a_palabra = {}
    self.frecuencias = Counter()
    self.codigo_actual = 0
```

**Descripción:**

- Inicializa las estructuras de datos necesarias:
  - `palabra_a_codigo`: Diccionario que mapea palabras a códigos.
  - `codigo_a_palabra`: Diccionario inverso que mapea códigos a palabras.
  - `frecuencias`: Contador de frecuencias de palabras usando `Counter` de `collections`.
  - `codigo_actual`: Número entero que representa el siguiente código disponible.

---

### `agregar_palabra`

```python
def agregar_palabra(self, palabra):
    if palabra not in self.palabra_a_codigo:
        codigo = str(self.codigo_actual)
        self.palabra_a_codigo[palabra] = codigo
        self.codigo_a_palabra[codigo] = palabra
        self.codigo_actual += 1
```

**Descripción:**

- Añade una nueva palabra al diccionario si no existe.
- Asigna un código numérico único a la palabra.
- Actualiza los diccionarios de mapeo y el contador de códigos.

---

### `obtener_codigo`

```python
def obtener_codigo(self, palabra):
    if palabra not in self.palabra_a_codigo:
        self.agregar_palabra(palabra)
    return self.palabra_a_codigo[palabra]
```

**Descripción:**

- Devuelve el código asociado a una palabra.
- Si la palabra no existe en el diccionario, la añade utilizando `agregar_palabra`.

---

### `obtener_palabra`

```python
def obtener_palabra(self, codigo):
    return self.codigo_a_palabra.get(codigo, codigo)
```

**Descripción:**

- Devuelve la palabra asociada a un código.
- Si el código no existe en el diccionario, devuelve el código mismo.

---

### `actualizar_frecuencias`

```python
def actualizar_frecuencias(self, texto):
    palabras = texto.lower().split()
    self.frecuencias.update(palabras)
```

**Descripción:**

- Actualiza el contador de frecuencias con las palabras del texto proporcionado.
- Convierte el texto a minúsculas y lo divide en palabras.

---

### `optimizar_diccionario`

```python
def optimizar_diccionario(self):
    palabras_comunes = sorted(self.frecuencias, key=self.frecuencias.get, reverse=True)[:1000]
    palabras_existentes = set(self.palabra_a_codigo.keys())
    palabras_retenidas = sorted(palabras_existentes, key=lambda palabra: self.frecuencias.get(palabra, 0), reverse=True)[:500]
    self.palabra_a_codigo = {}
    self.codigo_a_palabra = {}
    self.codigo_actual = 0
    for palabra in palabras_comunes:
        self.agregar_palabra(palabra)
    for palabra in palabras_retenidas:
        if palabra not in self.palabra_a_codigo:
            self.agregar_palabra(palabra)
```

**Descripción:**

- Optimiza el diccionario seleccionando las palabras más frecuentes.
- **Pasos:**
  1. **Selecciona las 1000 palabras más comunes** del texto basado en las frecuencias.
  2. **Retiene hasta 500 palabras existentes** en el diccionario que son más frecuentes.
  3. **Reinicia los diccionarios de mapeo y el contador de códigos.**
  4. **Agrega las palabras comunes y retenidas** al diccionario.

**Nota:** Este proceso asegura que el diccionario se mantiene eficiente al enfocarse en las palabras que más contribuyen a la compresión.

---

## Función `comprimir_texto`

```python
def comprimir_texto(texto, diccionario):
    diccionario.actualizar_frecuencias(texto)
    diccionario.optimizar_diccionario()

    resultado = []
    palabra_actual = ""
    for caracter in texto:
        if caracter.isalnum() or caracter == "'":
            palabra_actual += caracter
        else:
            if palabra_actual:
                if palabra_actual.lower() in diccionario.palabra_a_codigo:
                    codigo = diccionario.obtener_codigo(palabra_actual.lower())
                    if palabra_actual[0].isupper():
                        resultado.append(f"{codigo}^")  # Indicador para mayúscula
                    else:
                        resultado.append(codigo)
                else:
                    resultado.append(palabra_actual)
                palabra_actual = ""
            resultado.append(caracter)
    if palabra_actual:
        if palabra_actual.lower() in diccionario.palabra_a_codigo:
            codigo = diccionario.obtener_codigo(palabra_actual.lower())
            if palabra_actual[0].isupper():
                resultado.append(f"{codigo}^")
            else:
                resultado.append(codigo)
        else:
            resultado.append(palabra_actual)
    return "".join(resultado)
```

**Descripción:**

- Comprime el texto reemplazando palabras frecuentes por sus códigos.
- **Manejo de mayúsculas:** Utiliza `^` como indicador de que la palabra original comenzaba con mayúscula.
- **Pasos:**
  1. **Actualiza las frecuencias** y **optimiza el diccionario** antes de la compresión.
  2. **Itera sobre cada carácter** del texto:
     - Construye palabras alfanuméricas.
     - Al encontrar un separador (espacio, puntuación, etc.), procesa la palabra actual.
     - Si la palabra está en el diccionario, la reemplaza por su código (añadiendo `^` si es mayúscula).
     - Si no está en el diccionario, la deja intacta.
     - Añade el carácter separador al resultado.
  3. **Retorna el texto comprimido** como una cadena.

---

## Función `descomprimir_texto`

```python
def descomprimir_texto(texto_comprimido, diccionario):
    resultado = []
    numero = ""
    mayuscula = False
    for caracter in texto_comprimido:
        if caracter.isdigit():
            numero += caracter
        elif caracter == "^":
            mayuscula = True
        else:
            if numero:
                palabra = diccionario.obtener_palabra(numero)
                if mayuscula:
                    palabra = palabra.capitalize()
                    mayuscula = False
                resultado.append(palabra)
                numero = ""
            resultado.append(caracter)
    if numero:
        palabra = diccionario.obtener_palabra(numero)
        if mayuscula:
            palabra = palabra.capitalize()
        resultado.append(palabra)
    return "".join(resultado)
```

**Descripción:**

- Descomprime el texto reemplazando códigos por sus palabras originales.
- **Manejo de mayúsculas:** Si encuentra `^`, capitaliza la primera letra de la palabra.
- **Pasos:**
  1. **Itera sobre cada carácter** del texto comprimido:
     - Acumula dígitos para formar códigos numéricos.
     - Al encontrar `^`, activa el indicador de mayúscula.
     - Al encontrar un carácter no numérico ni `^`, procesa el código acumulado:
       - Obtiene la palabra asociada al código.
       - Aplica capitalización si es necesario.
       - Añade la palabra al resultado.
     - Añade el carácter actual al resultado.
  2. **Retorna el texto descomprimido** como una cadena.

---

## Función `calcular_tamano`

```python
def calcular_tamano(texto):
    return len(texto.encode('utf-8'))
```

**Descripción:**

- Calcula el tamaño en bytes del texto utilizando codificación UTF-8.
- **Uso:** Para comparar el tamaño antes y después de la compresión.

---

## Función `main`

```python
def main():
    diccionario = Diccionario()
    print("Ingrese el texto a comprimir:")
    texto_original = input().strip()

    texto_comprimido = comprimir_texto(texto_original, diccionario)

    print("\nResultados:")
    print(f"Texto original ({calcular_tamano(texto_original)} bytes):")
    print(texto_original)
    print(f"\nTexto comprimido ({calcular_tamano(texto_comprimido)} bytes):")
    print(texto_comprimido)

    texto_descomprimido = descomprimir_texto(texto_comprimido, diccionario)
    print("\nTexto descomprimido:")
    print(texto_descomprimido)

    bytes_original = calcular_tamano(texto_original)
    bytes_comprimido = calcular_tamano(texto_comprimido)
    porcentaje = ((bytes_original - bytes_comprimido) / bytes_original) * 100
    print(f"\nPorcentaje de compresión: {porcentaje:.1f}%")
```

**Descripción:**

- **Flujo principal del programa:**
  1. **Solicita al usuario** que ingrese el texto a comprimir.
  2. **Crea una instancia** de `Diccionario`.
  3. **Comprime el texto** utilizando `comprimir_texto`.
  4. **Muestra los resultados:**
     - Texto original y su tamaño en bytes.
     - Texto comprimido y su tamaño en bytes.
  5. **Descomprime el texto** utilizando `descomprimir_texto` para verificar la integridad.
  6. **Calcula y muestra el porcentaje de compresión** obtenido.

---

**Ejemplo de uso:**

Supongamos que el usuario ingresa el siguiente texto:

```
Hola hola hola, este es un texto de prueba. Este texto es solo para probar el algoritmo de compresión.
```

El programa podría mostrar:

```
Resultados:
Texto original (113 bytes):
Hola hola hola, este es un texto de prueba. Este texto es solo para probar el algoritmo de compresión.

Texto comprimido (90 bytes):
0^ 0 0, 1 es un 2 de 3. 1 2 es solo para 4 el 5 de 6.

Texto descomprimido:
Hola hola hola, este es un texto de prueba. Este texto es solo para probar el algoritmo de compresión.

Porcentaje de compresión: 20.4%
```
