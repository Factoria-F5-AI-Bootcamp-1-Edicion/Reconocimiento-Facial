import face_recognition
import os
from dotenv import load_dotenv
import cv2
from logging_config import logging

load_dotenv()
ruta = os.getenv('ruta')

# Creamos la función de codificación de las caras.
def codifica_caras_conocidas(known_face_encodings, known_face_names):
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

def codifica_caras_webcam(frame):
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convertimos el formato de color BGR (utilizado por OpenCV) a RGB (que es el que utiliza face_recognition) usando
    # "COLOR_BGR2RGB" de cv2.
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Encuentra las posiciones y codificaciones del fotograma actual
    face_locations = face_recognition.face_locations(rgb_small_frame)
    logging.info(f"guarda caras {face_locations}")
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    return face_encodings, face_locations
