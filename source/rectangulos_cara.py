import cv2
import os
from datetime import datetime
from dotenv import load_dotenv
from source.guarda_imagenes import guardaRostros

load_dotenv()
ruta = os.getenv('ruta')

dt = datetime.now()
seg = dt.strftime("%Y-%m-%d %H;%M;%S")
min = dt.strftime("%Y-%m-%d %H;%M")

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