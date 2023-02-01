# Instalación de las librerías necesarias: "pip install opencv-python", "pip install face_recognition".
import face_recognition
import sys
import cv2
import numpy as np

# Importamos las funciones de los otros archivos
from source.confidence import face_confidence
from source.otros_analisis import analisis_opcionales
from source.codificador import codifica_caras_conocidas, codifica_caras_webcam
from source.logging_config import logging
from source.rectangulos_cara import posicionRectangulos
from source.guarda_imagenes import guardaFotoLogin

#---------------------Clase "Facerecognition" para el reconocimiento de caras-------------------------------------------------------
class FaceRecognition:
    face_locations = []# Creamos variables para guardar las coordenadas, las codificaciones y los nombres de las caras detectadas, y los nombres y las codificaciones de las caras guardadas.
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True # Recomendación de la docu para ahorrar computación.
    emociones = False
    edades= False
    razas= False

    #----------------------------------------------- Función de inicio--------------------------------------------------------------
    def __init__(self):
        codifica_caras_conocidas(self.known_face_encodings, self.known_face_names) # Codificamos las caras de la carpeta /faces

    #------------------------------------- Función que pondrá en marcha todo el preceso---------------------------------------------
    def run_recognition(self):
        video_capture = cv2.VideoCapture(0) # Creamos la captura de video. El índice hace referencia a la cámaras del ordenador en uso. Asegurarse de que se tienen los permisos necesarios para acceder a la cámara.

        if not video_capture.isOpened():
            sys.exit('Video source not found...') # Creamos exepción por si no se inicia la captura de video.

        while True: # Creamos bucle mientras la cámara esté abierta

            ret, frame = video_capture.read() # Leemos la captura y extraemos el fotograma en "frame" y "ret" nos indicará "True" si la captura ha sido exitosa.

            if self.process_current_frame: # Añadimos para solo procesar cada dos fotogramas y ahorra poder de cómputo. Cuando 'process_current_frame' es True.
                self.face_encodings, self.face_locations = codifica_caras_webcam(frame)
                self.face_names = []
                logging.info(f"Probando {self.face_names}")

                for face_encoding in self.face_encodings: # Recorre todas las codificaciones de los fotogramas capturados por la cámara

                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding) # Comprueba si las caras que ve la cámara hacen match con las caras conocidas (carpeta 'faces')
                    name = 'Unknown' # Dejamos por defecto 'Unknow' para caras no conocidas
                    confidence = '?'
                    acceso = 'Access Denied'
                    age = ' ? '
                    emotion = '  ?  '
                    race = '  ?  '
                    color = (0, 0, 255)

                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding) # Calculamos la 'face_distance', es decir, la similitud entre la cara que ve la cámara y las caras conocidas
                    best_match_index = np.argmin(face_distances) # Con la funcion 'argmin' de numpy, obtenemos el índice de la 'face_distance' menor, y la guardamos como mejor match 'best_match_index'
                    
                    if matches[best_match_index]: # Con el índice elegido como mejor, seleccionamos el mejor match de 'matches'(en el caso de que sí haya match).
                        name = self.known_face_names[best_match_index] # Se elige el nombre y el confidence de la cara conocida con match más alto.
                        confidence = face_confidence(face_distances[best_match_index])
                        acceso = 'Access Granted'
                        img = frame                       
                        color = (0, 143, 57)
                        guardaFotoLogin(name, img)
                        age, emotion, race = analisis_opcionales(frame, self.edades, self.emociones, self.razas)

                    self.face_names.append((name, confidence, age, emotion, color, acceso, race)) # Añadimos a la lista nombre, confianza acceso, edad, emocion y raza, que luego se mostrarán en pantalla. 
                    logging.info(f"Probando {self.face_names}")
            self.process_current_frame = not self.process_current_frame # Tras analizar un fotograma, cambia 'process_current_frame' a False, de tal manera que analiza uno de cada dos fotogramas, para ahorrar memoria.
            
            posicionRectangulos(frame,self.face_locations, self.face_names) #Definimos los rectángulos para las caras.
            
            salida_camara = cv2.resize(frame, (0, 0), fx=1, fy=1)
            cv2.imshow('Reconocimiento Facial', salida_camara) # Mostramos la imagen resultante
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
            
            if cv2.waitKey(1) == ord('q'): # Fijamos la letra 'Q' del teclado, para romper el bucle y salir del reconocimiento facial.
                break
        video_capture.release()
        cv2.destroyAllWindows() # Cierra la cámara y todas las pestañas.(Tras haber pulsado Q)