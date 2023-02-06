import cv2
import os
from datetime import datetime
from dotenv import load_dotenv
from source.guarda_imagenes import guardaRostros, guardaBoxes

load_dotenv()
ruta = os.getenv('ruta')

dt = datetime.now()
seg = dt.strftime("%Y-%m-%d %H;%M;%S")
min = dt.strftime("%Y-%m-%d %H;%M")

#---------------------Función para dibujar el rectángulo y teto alrededor de la(s) cara(s) detectada(s)------------------------------------
def posicionRectangulos(frame,face_locations, face_names):
    for (top, right, bottom, left), (name, confidence, age, emotion, color, acceso, race) in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4 # Reescalamos la posición de la cara, ya que antes la habíamos reducido a 1/4.

        if acceso == 'Access Granted':
            guardaRostros(frame,name, top, right, bottom, left)
        else:
            pass
        
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2) # Indicamos el frame, la posición, el color del marco (0,0,255)=Rojo, y el grosor del marco (2 en este caso).
        cv2.rectangle(frame, (left, bottom + 60), (right + 90, bottom), color, cv2.FILLED) # Hacemos el rectángulo para el nombre y la confidence. Con v2.FILLED rellenamos el rectángulo.
        cv2.putText(frame, acceso , (left + 6, bottom + 20), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
        cv2.putText(frame, name+" "+"Trust:"+confidence, (left + 6, bottom + 50), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
        DesIzq = 0
        DesAba = 0
        if age != '  ?  ': 
            cv2.rectangle(frame, (left, bottom + 90), (right + 30, bottom + 60), color, cv2.FILLED)
            cv2.putText(frame, "Age:"+str(age)[1:-1], (left + 6, bottom + 80), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
            DesIzq = 110
            DesAba = 30
        if emotion != '  ?  ': 
            cv2.rectangle(frame, (left + DesIzq, bottom + 90), (right + DesIzq + 90, bottom + 60), color, cv2.FILLED)
            cv2.putText(frame, "Emotion:"+str(emotion)[2:-2] , (left + DesIzq + 6, bottom + 80), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
            DesAba = 30
        if race != '  ?  ':
            cv2.rectangle(frame, (left, bottom + DesAba + 90), (right + 90, bottom + DesAba + 60), color, cv2.FILLED) 
            cv2.putText(frame, "Race:"+str(race)[2:-2] , (left + 6, bottom + DesAba + 80), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1) # Colocamos el texto (acceso, nombre, confianza, edad, emocion, raza)

        if acceso == 'Access Granted':
            guardaBoxes(name, frame)
        else:
            pass