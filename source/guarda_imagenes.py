import cv2
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
ruta = os.getenv('ruta')

dt = datetime.now()
seg = dt.strftime("%Y-%m-%d %H;%M;%S")
min = dt.strftime("%Y-%m-%d %H;%M")

def guardaRostros(frame,name, top, right, bottom, left):
    os.chdir(f"{ruta}/CV_grupo11/rostros/{name}")
    frame_cara = frame[top:bottom, left:right]
    now = datetime.now() 
    print("[INFO] Object found. Saving locally.") 
    cv2.imwrite(f'{now.year}-{now.month}-{now.day} {now.hour}.{now.minute}.{now.second}.jpg', frame_cara)

def guardaFotoLogin(name, img):
    os.chdir(f"{ruta}/CV_grupo11/imagenes/{name}")
    cv2.imwrite(f'{min}.jpg',img)