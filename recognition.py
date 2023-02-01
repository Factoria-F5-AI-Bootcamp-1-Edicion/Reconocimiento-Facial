# Instalación de las librerías necesarias: "pip install opencv-python", "pip install face_recognition".
import face_recognition
import sys
import cv2
import numpy as np

# Importamos las funciones de los otros archivos
from confidence import face_confidence
from otros_analisis import analisis_opcionales
from codificador import codifica_caras_conocidas, codifica_caras_webcam
from logging_config import logging
from rectangulos_cara import posicionRectangulos
from guarda_imagenes import guardaFotoLogin

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
        codifica_caras_conocidas(self.known_face_encodings, self.known_face_names)

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
                self.face_encodings, self.face_locations = codifica_caras_webcam(frame)
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
                        color = (0, 143, 57)
                        guardaFotoLogin(name, img)
                        age, emotion, race = analisis_opcionales(frame, self.edades, self.emociones, self.razas)

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