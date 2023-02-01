import cv2
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
ruta = os.getenv('ruta') # Cargamos la ruta desde un archivo .env

#------------------------------Definimos el formato de tiempo en el que se guardaran los archivos------------------------
dt = datetime.now()
seg = dt.strftime("%Y-%m-%d %H;%M;%S")
min = dt.strftime("%Y-%m-%d %H;%M")

#-------------------------------Función para guardar solo el rostro de las caras detectadas como conocidas---------------

def guardaRostros(frame,name, top, right, bottom, left):
    os.chdir(f"{ruta}/CV_grupo11/rostros/{name}")
    frame_cara = frame[top:bottom, left:right]
    now = datetime.now() 
    print("[INFO] Object found. Saving locally.") 
    cv2.imwrite(f'{now.year}-{now.month}-{now.day} {now.hour}.{now.minute}.{now.second}.jpg', frame_cara)

#------------Función para guardar una imagen por minuto del fotograma completo al detectar una cara conocida-------------

def guardaFotoLogin(name, img):
    os.chdir(f"{ruta}/CV_grupo11/imagenes/{name}")
    cv2.imwrite(f'{min}.jpg',img)

#--------------Función para guardar una imagen por minuto del rostro reconocido con bounding box y etiqueta---------------

def guardaBoxes(name, frame):
    os.chdir(f"{ruta}/CV_grupo11/boxes/{name}")
    cv2.imwrite(f'{min}.jpg', frame)