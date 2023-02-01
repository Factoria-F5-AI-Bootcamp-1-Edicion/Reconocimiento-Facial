from deepface import DeepFace

#---------------------Función para analizar la edad de la cara reconocida------------------------------------
def detectaEdades(frame):
    face_analysis = DeepFace.analyze(img_path = frame, actions = ["age"], enforce_detection = False)
    age = [ sub['age'] for sub in face_analysis ]
    return age

#---------------------Función para analizar la emoción de la cara reconocida---------------------------------
def detectaEmociones(frame):
    face_analysis = DeepFace.analyze(img_path = frame, actions = ["emotion"], enforce_detection = False)
    emotion = [ sub['dominant_emotion'] for sub in face_analysis ]
    return emotion

#---------------------Función para analizar la raza de la cara reconocida------------------------------------
def detectaRazas(frame):
    face_analysis = DeepFace.analyze(img_path = frame, actions = ["race"], enforce_detection = False)
    race = [ sub['dominant_race'] for sub in face_analysis ]
    return race

#----------Función para activar los valores de edad, emocion y raza en el caso de necesitarlos---------------
def analisis_opcionales(frame, edades, emociones, razas):
    age = ' ? '
    emotion = ' ? '
    race = ' ? '
    if edades == True: age = detectaEdades(frame)
    if emociones == True: emotion = detectaEmociones(frame)
    if razas == True: race = detectaRazas(frame)
    return age, emotion, race 