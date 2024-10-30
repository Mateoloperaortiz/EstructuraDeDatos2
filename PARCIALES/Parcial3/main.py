datos = [
    ['Medellín', 24, 1495, 'Turismo urbano, visitas a museos y parques, recorridos gastronómicos, entre otros.', 0, 33, 83, 18, 13],
    ['Guatapé', 24, 2135, 'Visitar la Piedra del Peñol, paseos en bote por el embalse, disfrutar de la gastronomía local, entre otros.', 79, 43, 144, 71, 53],
    ['Santa Fe de Antioquia', 24, 537, 'Turismo histórico, visitas a museos y sitios arqueológicos, paseos en bote por el río Cauca, entre otros.', 63, 92, 0, 67, 23],
    ['Rionegro', 24, 2125, 'Turismo religioso, visitas a sitios históricos, recorridos gastronómicos, entre otros.', 28, 0, 92, 50, 23],
    ['Barbosa', 24, 1525, 'Turismo de naturaleza, visitas a sitios históricos, recorridos gastronómicos, entre otros.', 18, 50, 67, 0, 30],
    ['Itagüí', 24, 1556, 'Turismo urbano, visitas a centros comerciales y sitios culturales, entre otros.', 9, 38, 97, 22, 17],
    ['Envigado', 24, 1670, 'Turismo urbano, visitas a parques y sitios culturales, entre otros.', 10, 43, 93, 26, 19],
    ['Cocorná', 24, 640, 'Turismo de naturaleza, visitas a cascadas y sitios históricos, entre otros.', 65, 25, 133, 80, 67],
    ['El Peñol', 24, 2150, 'Turismo de naturaleza, visita al Peñol de Guatapé, paseos en bote por la represa, entre otros.', 79, 42, 149, 104, 58],
    ['Sonsón', 24, 1525, 'Turismo de naturaleza, visitas a sitios históricos y culturales, entre otros.', 86, 57, 130, 112, 41]
]

def encontrar_municipio(nombre, datos):
    for municipio in datos:
        if municipio[0].lower() == nombre.lower():
            return municipio
    return None

def calcular_similitud(m1, m2):
    diferencia_altura = abs(m1[2] - m2[2])
    distancias_m1 = m1[4:9]
    distancias_m2 = m2[4:9]
    diferencia_distancias = sum([abs(d1 - d2) for d1, d2 in zip(distancias_m1, distancias_m2)])
    similitud = diferencia_altura + diferencia_distancias
    return similitud

municipio_usuario = input("Ingrese el nombre de un municipio que le haya gustado: ")

municipio_preferido = encontrar_municipio(municipio_usuario, datos)

if municipio_preferido is None:
    print("Lo siento, el municipio ingresado no se encuentra en la base de datos.")
else:
    similitudes = []
    for municipio in datos:
        if municipio[0].lower() != municipio_preferido[0].lower():
            similitud = calcular_similitud(municipio_preferido, municipio)
            similitudes.append((similitud, municipio))
    similitudes.sort(key=lambda x: x[0])
    municipio_recomendado = similitudes[0][1]
    print("\nBasado en su preferencia por {}, le recomendamos visitar {}.".format(municipio_preferido[0], municipio_recomendado[0]))
    print("Actividades en {}: {}".format(municipio_recomendado[0], municipio_recomendado[3]))