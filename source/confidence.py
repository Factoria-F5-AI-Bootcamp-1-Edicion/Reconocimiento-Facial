import math

#------------Creamos la función que nos dara el porcentaje de seguridad sobre la identificación de la cara--------

def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold) # face_match_treshold" (mínimo aceptable de parecido entre la imagen capturada y la guarda en los datos).
    linear_val = (1.0 - face_distance) / (range * 2.0) # face_distance indica cuanto se parece la cara que detectamos a la cara que tenemos guardada. Mayor valor menor similitud.

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%' # Devolvemos los valores redondeaos a dos decimales y pasados a porcentaje.
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'