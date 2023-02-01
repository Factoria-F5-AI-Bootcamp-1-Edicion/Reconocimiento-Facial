#----------------Función para configurar los fucniones opcionales a utilizar----------------

def configuracion_inicial():
    print('Le doy la bienvenida a la APP de login facial.')
    print('Antes configuremos algunas cosas.')
    print('Desea utilizar el reconocimiento de edad? [s/n]')
    respuesta1 = input()
    if respuesta1 == 's':
        edades = True
    else:
        edades = False
    print('Desea utilizar el reconocimiento de emociones? [s/n]')
    respuesta2 = input()
    if respuesta2 == 's':
        emociones = True
    else:
        emociones = False
    print('Desea utilizar el reconocimiento de raza? [s/n]')
    respuesta3 = input()
    if respuesta3 == 's':
        razas = True
    else:
        razas = False
    print('Configuración finalizada.')
    return edades, emociones, razas