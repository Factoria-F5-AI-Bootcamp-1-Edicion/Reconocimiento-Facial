import face_recognition
import os
from dotenv import load_dotenv
import cv2
from source.logging_config import logging

load_dotenv()
ruta = os.getenv('ruta')

#------------------------Función para codificar las caras conocidas, de la carpeta /faces-----------------------------------------

def codifica_caras_conocidas(known_face_encodings, known_face_names):
    # Hacemos referencia a las imagenes d ela carpeta "faces".
    for image in os.listdir('faces'):

        face_image = face_recognition.load_image_file(f"faces/{image}") # Cargamos la(s) imagen(es) de la carpeta "faces".
        face_encoding = face_recognition.face_encodings(face_image)[0] # Codificamos la imagen que hemos cargado antes.
        known_face_encodings.append(face_encoding)# Añadimos la codificación de la imagen a la lista "known_face_encodings"
        logging.info(f"Probando {image}")
        basename = os.path.basename(image)
        logging.info(f"Probando {basename}")
        (filename, ext) = os.path.splitext(basename) # Obtenemos solo el nombre, sin la extensión.
        logging.info(f"Probando {filename}")
        known_face_names.append(filename) # Añadimos el nombre de la cara conocida a nombres conocidos

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

    print(known_face_names)# Sacamos por consola el nombre de las imagenes que hemos añadido a las variables.

#------------------------Función para codificar las caras que detecta la webcam-----------------------------------------

def codifica_caras_webcam(frame):
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) # Disminuimos el tamaño del fotograma a 1/4
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB) # Convertimos el formato de color BGR (utilizado por OpenCV) a RGB (que es el que utiliza face_recognition)
    face_locations = face_recognition.face_locations(rgb_small_frame) # Encuentra las posiciones y codificaciones del fotograma actual
    logging.info(f"guarda caras {face_locations}")
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations) # Codifica las caras detectadas por webcam
    return face_encodings, face_locations
