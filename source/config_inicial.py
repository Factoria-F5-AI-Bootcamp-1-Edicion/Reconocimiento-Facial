#----------------Función para configurar los fucniones opcionales a utilizar----------------

def configuracion_inicial():
    print('Le doy la bienvenida a la APP de login facial.')
    print('Antes configuremos algunas cosas.')
    print('Desea utilizar el reconocimiento de edad?')
    respuesta1 = input('s/n')
    if respuesta1 == 's':
        edades = True
    else:
        edades = False
    print('Desea utilizar el reconocimiento de emociones?')
    respuesta2 = input('s/n')
    if respuesta2 == 's':
        emociones = True
    else:
        emociones = False
    print('Desea utilizar el reconocimiento de raza?')
    respuesta3 = input('s/n')
    if respuesta3 == 's':
        razas = True
    else:
        razas = False
    print('Configuración finalizada.')
    return edades, emociones, razas