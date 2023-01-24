# Instalación de las librerías necesarias: "pip install opencv-python", "pip install face_recognition".
import face_recognition
import os, sys
import cv2
import numpy as np
import math

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
            self.known_face_names.append(image)
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

            # Añadimos para solo precesar cada dos fotogramas y ahorra poder de cómputo.
            if self.process_current_frame:
                # Reescalar el frame del video a un cuarto de su tamaño para agilizar el reconocimiento.
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # Convertimos el formato de color BGR (utilizado por OpenCV) a RGB (que es el que utiliza face_recognition) usando
                # "COLOR_BGR2RGB" de cv2.
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

-----------------------------

                # Find all the faces and face encodings in the current frame of video
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

                self.face_names = []
                for face_encoding in self.face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"
                    confidence = '???'

                    # Calculate the shortest distance to face
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        confidence = face_confidence(face_distances[best_match_index])

                    self.face_names.append(f'{name} ({confidence})')

            self.process_current_frame = not self.process_current_frame

            # Display the results
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Create the frame with the name
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

            # Display the resulting image
            cv2.imshow('Face Recognition', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    fr = FaceRecognition()
    fr.run_recognition()