grafo = {

    'Medellin': [('Bogota', 58.85), ('Barranquilla',89.44), ('Cartagena', 96.40), ('Montreal', 498.71) , ('Toronto', 509.62)],
    'Bogota': [('Medellin', 58.85), ('Barranquilla', 80.66), ('Cartagena', 82.71), ('Montreal', 419.10),('Toronto', 428.49)],
    'Barranquilla': [('Bogota', 80.66),('Medellin', 89.44), ('Montreal', 426.44), ('Vancouver', 781.29), ('Calgary', 801.03 ),('Edmonton', 906.29)],  
    'Cartagena': [('Medellin', 96.40), ('Bogota', 82.71),('Toronto', 436.31), ('Calgary', 781.91)],
    'Montreal': [('Bogota', 419.10),('Barranquilla', 426.44 ),('Medellin', 498.71),('Toronto', 127.50), ('Vancouver',178.50)],
    'Vancouver': [('Toronto',148.44),('Montreal',178.50),('Barranquilla',781.29)],
    'Calgary': [('Cartagena', 781.91),('Barranquilla', 801.03),('Toronto', 111.33)],
    'Edmonton': [('Barranquilla', 906.29),('Toronto',135.62)],
    'Toronto': []
}

def encontrar_todas_las_rutas(grafo, inicio, fin, camino=[], costo_total=0):
    camino = camino + [inicio]
    if inicio == fin:
        return [(camino, costo_total)]
    if inicio not in grafo:
        return []
    rutas = []
    for nodo, costo in grafo[inicio]:
        if nodo not in camino:
            nuevas_rutas = encontrar_todas_las_rutas(grafo, nodo, fin, camino, costo_total + costo)
            for ruta in nuevas_rutas:
                rutas.append(ruta)
    return rutas

def ordenar_por_costo(rutas):
    for i in range(1, len(rutas)):
        clave = rutas[i]
        j = i - 1
        while j >= 0 and clave[1] < rutas[j][1]:
            rutas[j + 1] = rutas[j]
            j -= 1
        rutas[j + 1] = clave
    return rutas

def ordenar_por_giros(rutas):
    for i in range(1, len(rutas)):
        clave = rutas[i]
        j = i - 1
        while j >= 0 and len(clave[0]) < len(rutas[j][0]):
            rutas[j + 1] = rutas[j]
            j -= 1
        rutas[j + 1] = clave
    return rutas


inicio = 'Medellin'
fin = 'Toronto'
rutas = encontrar_todas_las_rutas(grafo, inicio, fin)

rutas_ordenadas_por_costo = ordenar_por_costo(rutas.copy())
print("Rutas ordenadas por costo en USD (de menor a mayor):")
for ruta, costo in rutas_ordenadas_por_costo:
    print(f"Ruta: {ruta} con costo total: {round(costo, 3)}$ USD")

rutas_ordenadas_por_giros = ordenar_por_giros(rutas.copy())
print("\nRutas ordenadas por cantidad de escalas (de menor a mayor):")
for ruta, costo in rutas_ordenadas_por_giros:
    print(f"Ruta: {ruta} con cantidad de escalas: {len(ruta)-1}")