import logging

logging.basicConfig(
    level= logging.INFO,
    filename="logs/logging_record.log", 
    filemode="w", #Cambiar a "a" cuando no se quiera sobreescribir los logs
    format="%(asctime)s - %(levelname)s - %(message)s")