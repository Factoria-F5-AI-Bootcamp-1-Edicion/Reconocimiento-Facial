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
