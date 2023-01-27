# Instalación de las librerías necesarias: "pip install opencv-python", "pip install face_recognition".
import face_recognition
import os, sys
import cv2
import numpy as np
import math
import logging
from datetime import datetime


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

    # Creamos una función para que se inicien las codificaciones de las caras.
    def __init__(self):
        self.encode_faces()

    # Creamos la función de codificación de las caras.
    def encode_faces(self):
        # Hacemos referencia a las imagenes d ela carpeta "faces".
        for image in os.listdir('faces'):
            # Cargamos la imagen de la carpeta "faces".
            face_image = face_recognition.load_image_file(f"faces/{image}")
            # Codificamos la imagen que hemos cargado antes.
            face_encoding = face_recognition.face_encodings(face_image)[0]

            # Añadimos la codificación de la imagen a la variable "known_face_encodings" y el nombre a "known_face_names".
            self.known_face_encodings.append(face_encoding)
            logging.info(f"Probando {image}")
            # Obtenemos solo el nombre, sin la extensión.
            basename = os.path.basename(image)
            logging.info(f"Probando {basename}")
            (filename, ext) = os.path.splitext(basename)
            logging.info(f"Probando {filename}")
            # Añadimos el nombre de la cara conocida a nombres conocidos
            self.known_face_names.append(filename)
        # Sacamos por consola el nombre de las imagenes que hemos añadido a las variables.
        print(self.known_face_names)

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
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

                self.face_names = []
                # Recorre todas las codificaciones de los fotogramas capturados por la cámara
                for face_encoding in self.face_encodings:
                    # Comprueba si las caras que ve la cámara hacen match con las caras conocidas (carpeta 'faces')
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    # Dejamos por defecto 'Unknow' para caras no conocidas
                    name = "Acceso No Autorizado"
                    confidence = "?"

                    # Calculamos la 'face_distance', es decir, la similitud entre la cara que ve la cámara y las caras conocidas
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                    # Con la funcion 'argmin' de numpy, obtenemos el índice de la 'face_distance' menor, y la guardamos como mejor match 'best_match_index'
                    best_match_index = np.argmin(face_distances)
                    # Con el índice elegido como mejor, seleccionamos el mejor match de 'matches'(en el caso de que sí haya match).
                    if matches[best_match_index]:
                        # Se elige el nombre y el confidence de la cara conocida con match más alto.
                        name = self.known_face_names[best_match_index]
                        confidence = face_confidence(face_distances[best_match_index]) + ".Acceso Autorizado"
                        img = frame
                        now = datetime.now()
                        logging.info(now)
                        os.chdir("/Users/Pablo/Factoria F5/CV_grupo11/imagenes")
                        filename = f'{name}, {now.year}-{now.month}-{now.day} {now.hour}.{now.minute}.{now.second}.jpg'
                        logging.info(filename)
                        cv2.imwrite(filename,img)
                        

                    # Añadimos a la lista de nombres el name y la confidence, que luego se mostrarán en pantalla.
                    self.face_names.append(f'{name} ({confidence})')          
            # Tras analizar un fotograma, cambia 'process_current_frame' a False, de tal manera que analiza uno de cada dos fotogramas, para ahorrar memoria.
            self.process_current_frame = not self.process_current_frame

            # Creamos el cuadrado que enmarca la cara reconocida.
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                # Reescalamos la posición de la cara, ya que antes la habíamos reducido a 1/4.
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                (name_por, autori) = os.path.splitext(name)

                # Creamos el marco con el nombre
                # Indicamos el frame, la posición, el color del marco (0,0,255)=Rojo, y el grosor del marco (2 en este caso).
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                # Hacemos el rectángulo para el nombre y la confidence
                # Indicamos el frame, la posicion, que será mas abajo que el cuadro de la cara, y con la función cv2.FILLED rellenamos el rectángulo.
                cv2.rectangle(frame, (left, bottom - 60), (right, bottom), (0, 0, 255), cv2.FILLED)
                # Colocamos el texto y el acceso, más abajo y más a la derecha de la posición de la cara, elegimos la fuente, el tamaño de fuente, color y grosor.
                cv2.putText(frame, name_por, (left + 6, bottom - 36), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
                cv2.putText(frame, autori, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)





            # Mostramos la imagen resultante
            salida_camara = cv2.resize(frame, (0, 0), fx=1, fy=1)
            cv2.imshow('Reconocimiento Facial', salida_camara)

            # Fijamos la letra 'Q' del teclado, para romper el bucle y salir del reconocimiento facial.
            if cv2.waitKey(1) == ord('q'):
                break

        # Cierra la cámara y todas las pestañas.(Tras haber pulsado Q)
        video_capture.release()
        cv2.destroyAllWindows()