# Instalación de las librerías necesarias: "pip install opencv-python", "pip install face_recognition".
import face_recognition
import os, sys
import cv2
import numpy as np
import math
import logging
from datetime import datetime
from deepface import DeepFace
from dotenv import load_dotenv

load_dotenv()
ruta = os.getenv('ruta')

dt = datetime.now()
seg = dt.strftime("%Y-%m-%d %H;%M;%S")
min = dt.strftime("%Y-%m-%d %H;%M")

# Creamos una configuración de log para ir añadiéndolos
logging.basicConfig(
    level= logging.INFO,
    filename="logs/logging_record.log", 
    filemode="w", #Cambiar a "a" cuando no se quiera sobreescribir los logs
    format="%(asctime)s - %(levelname)s - %(message)s")

# Creamos la función que nos dara el porcentaje de seguridad sobre la identificación de la cara, para ello usamos la "face_distance" (que
# indica cuanto se parece la cara que detectamos a la cara que tenemos guardada en nuestros datos, a mayor valor menor similaritud), 
# y "face_match_treshold" (mínimo aceptable de parecido entre la imagen capturada y la guarda en los datos).
def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        # Devolvemos los valores redondeaos a dos decimales y pasados a porcentaje.
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'

# Creamos la función de codificación de las caras.
def encode_faces(known_face_encodings, known_face_names):
    # Hacemos referencia a las imagenes d ela carpeta "faces".
    for image in os.listdir('faces'):

        # Cargamos la imagen de la carpeta "faces".
        face_image = face_recognition.load_image_file(f"faces/{image}")
        # Codificamos la imagen que hemos cargado antes.
        face_encoding = face_recognition.face_encodings(face_image)[0]

        # Añadimos la codificación de la imagen a la variable "known_face_encodings" y el nombre a "known_face_names".
        known_face_encodings.append(face_encoding)
        logging.info(f"Probando {image}")
        # Obtenemos solo el nombre, sin la extensión.
        basename = os.path.basename(image)
        logging.info(f"Probando {basename}")
        (filename, ext) = os.path.splitext(basename)
        logging.info(f"Probando {filename}")
        # Añadimos el nombre de la cara conocida a nombres conocidos
        known_face_names.append(filename)

        directory = filename
        parent_dir = f"{ruta}/CV_grupo11/imagenes"
        path = os.path.join(parent_dir, directory)
        os.makedirs(path, exist_ok = True)

        parent_dir2 = f"{ruta}/CV_grupo11/rostros"
        path2 = os.path.join(parent_dir2, directory)
        os.makedirs(path2, exist_ok = True)

        parent_dir2 = f"{ruta}/CV_grupo11/boxes"
        path3 = os.path.join(parent_dir2, directory)
        os.makedirs(path3, exist_ok = True)

    # Sacamos por consola el nombre de las imagenes que hemos añadido a las variables.
    print(known_face_names)

def guardaRostros(frame,name, top, right, bottom, left):
    os.chdir(f"{ruta}/CV_grupo11/rostros/{name}")
    frame_cara = frame[top:bottom, left:right]
    now = datetime.now() 
    print("[INFO] Object found. Saving locally.") 
    cv2.imwrite(f'{now.year}-{now.month}-{now.day} {now.hour}.{now.minute}.{now.second}.jpg', frame_cara)

def posicionRectangulos(frame,face_locations, face_names):
    for (top, right, bottom, left), (name, confidence, age, emotion, color, acceso, race) in zip(face_locations, face_names):
        # Reescalamos la posición de la cara, ya que antes la habíamos reducido a 1/4.
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        if acceso == 'Access Granted':
            guardaRostros(frame,name, top, right, bottom, left)
        else:
            pass

        # Creamos el marco con el nombre
        # Indicamos el frame, la posición, el color del marco (0,0,255)=Rojo, y el grosor del marco (2 en este caso).
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        # Hacemos el rectángulo para el nombre y la confidence
        # Indicamos el frame, la posicion, que será mas abajo que el cuadro de la cara, y con la función cv2.FILLED rellenamos el rectángulo.
        cv2.rectangle(frame, (left, bottom + 120), (right + 90, bottom), color, cv2.FILLED)
        # Colocamos el texto y el acceso, más abajo y más a la derecha de la posición de la cara, elegimos la fuente, el tamaño de fuente, color y grosor.
        cv2.putText(frame, acceso , (left + 6, bottom + 20), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
        cv2.putText(frame, name+" "+"Trust:"+confidence, (left + 6, bottom + 50), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
        cv2.putText(frame, "Age:"+str(age)[1:-1]+" Emotion:"+str(emotion)[2:-2] , (left + 6, bottom + 80), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
        cv2.putText(frame, "Race:"+str(race)[2:-2] , (left + 6, bottom + 110), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

        if acceso == 'Access Granted':
            os.chdir(f"{ruta}/CV_grupo11/boxes/{name}")
            cv2.imwrite(f'{min}.jpg', frame)
        else:
            pass

def detectaEdades(frame):
    face_analysis = DeepFace.analyze(img_path = frame, actions = ["age"], enforce_detection = False)
    age = [ sub['age'] for sub in face_analysis ]
    return age
def detectaEmociones(frame):
    face_analysis = DeepFace.analyze(img_path = frame, actions = ["emotion"], enforce_detection = False)
    emotion = [ sub['dominant_emotion'] for sub in face_analysis ]
    return emotion
def detectaRazas(frame):
    face_analysis = DeepFace.analyze(img_path = frame, actions = ["race"], enforce_detection = False)
    race = [ sub['dominant_race'] for sub in face_analysis ]
    return race

# Creamos la clase "Facerecognition" para el reconocimiento de caras.
class FaceRecognition:
    # Creamos variables para guardar las coordenadas, las codificaciones y los nombres de las caras detectadas, y los nombres y las
    # codificaciones de las caras guardadas.
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    # Recomendación de la docu para ahorrar computación.
    process_current_frame = True
    emociones = False
    edades= False
    razas= False

    # Creamos una función para que se inicien las codificaciones de las caras.
    def __init__(self):
        encode_faces(self.known_face_encodings, self.known_face_names)

    # Creamos la función que pondrá en marcha todo el preceso.
    def run_recognition(self):
        # Creamos la captura de video con "cv2" usando el indice de las camaras del ordenador para hacer referencia a que 
        # cámara usamos y hace falta asegurarse de que se tienen los permisos necesarios para acceder a la cámara.
        video_capture = cv2.VideoCapture(0)

        # Creamos exepción por si no se inicia la captura de video.
        if not video_capture.isOpened():
            sys.exit('Video source not found...')
    # Creamos buqle para seguir con el proceso.
        while True:
            # Leemos la captura y extraemos el fotograma en "frame" y "ret" nos indicará "True" si la captura ha sido exitosa.
            ret, frame = video_capture.read()
            # Añadimos para solo precesar cada dos fotogramas y ahorra poder de cómputo. Cuando 'process_current_frame' es True.
            if self.process_current_frame:
                # Reescalar el frame del video a un cuarto de su tamaño para agilizar el reconocimiento.
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # Convertimos el formato de color BGR (utilizado por OpenCV) a RGB (que es el que utiliza face_recognition) usando
                # "COLOR_BGR2RGB" de cv2.
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

                # Encuentra las posiciones y codificaciones del fotograma actual
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                logging.info(f"guarda caras {self.face_locations}")
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

                self.face_names = []
                logging.info(f"Probando {self.face_names}")

                # Recorre todas las codificaciones de los fotogramas capturados por la cámara
                for face_encoding in self.face_encodings:
                    # Comprueba si las caras que ve la cámara hacen match con las caras conocidas (carpeta 'faces')
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)

                    # Dejamos por defecto 'Unknow' para caras no conocidas
                    name = 'Unknown'
                    confidence = '?'
                    acceso = 'Access Denied'
                    age = ' ? '
                    emotion = '  ?  '
                    race = '  ?  '
                    color = (0, 0, 255)

                    # Calculamos la 'face_distance', es decir, la similitud entre la cara que ve la cámara y las caras conocidas
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                    # Con la funcion 'argmin' de numpy, obtenemos el índice de la 'face_distance' menor, y la guardamos como mejor match 'best_match_index'
                    best_match_index = np.argmin(face_distances)
                    
                    # Con el índice elegido como mejor, seleccionamos el mejor match de 'matches'(en el caso de que sí haya match).
                    if matches[best_match_index]:
                        # Se elige el nombre y el confidence de la cara conocida con match más alto.
                        name = self.known_face_names[best_match_index]
                        confidence = face_confidence(face_distances[best_match_index])
                        acceso = 'Access Granted'
                        img = frame
                        now = datetime.now()                        
                        color = (0, 143, 57)
                        logging.info(seg)
                        os.chdir(f"{ruta}/CV_grupo11/imagenes/{name}")
                        cv2.imwrite(f'{min}.jpg',img)
                        if self.edades == True: age = detectaEdades(frame)
                        if self.emociones == True: emotion = detectaEmociones(frame)
                        if self.razas == True: race = detectaRazas(frame)

                    self.face_names.append((name, confidence, age, emotion, color, acceso, race))
                    logging.info(f"Probando {self.face_names}")
                    # Añadimos a la lista de nombres el name y la confidence, que luego se mostrarán en pantalla.       
            # Tras analizar un fotograma, cambia 'process_current_frame' a False, de tal manera que analiza uno de cada dos fotogramas, para ahorrar memoria.
            self.process_current_frame = not self.process_current_frame
            
            posicionRectangulos(frame,self.face_locations, self.face_names)
            
            # Mostramos la imagen resultante
            salida_camara = cv2.resize(frame, (0, 0), fx=1, fy=1)
            cv2.imshow('Reconocimiento Facial', salida_camara)
            if cv2.waitKey(1) == ord('e'):
                self.edades = True
            if cv2.waitKey(1) == ord('r'):
                self.edades = False
            if cv2.waitKey(1) == ord('n'):
                self.emociones = True
            if cv2.waitKey(1) == ord('m'):
                self.emociones = False
            if cv2.waitKey(1) == ord('z'):
                self.razas = True
            if cv2.waitKey(1) == ord('x'):
                self.razas = False
            
            # Fijamos la letra 'Q' del teclado, para romper el bucle y salir del reconocimiento facial.
            if cv2.waitKey(1) == ord('q'):
                break

        # Cierra la cámara y todas las pestañas.(Tras haber pulsado Q)
        video_capture.release()
        cv2.destroyAllWindows()