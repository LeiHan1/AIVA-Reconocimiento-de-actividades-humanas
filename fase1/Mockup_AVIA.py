#Mockup del proyecto de reconocimiento de actividades humanas

import cv2
import numpy
import pandas
import sklearn

#Leer un video
def read_video(self):
    cap = cv2.VideoCapture("Vídeos/ShopAssistant2front.mpg")

    while (cap.isOpened()):
        ret, frame = cap.read()

    cap.release()

#Preprocesar las imágenes, para eliminar ruido y dejar solo las características importantes
def preprocessing_images(self, frame):
    return 0

#A partir de las imágenes preprocesadas buscar zonas de interes a traves de la extracción de contornos
def get_contours(self, image):
    return 0

#Cargar un modelo entrenado para la detección de personas

def load_pedestrian_detector(self):
    return 0

#Se tiene un contador del número de personas que hay en la escena y cuando este número varie se sabrá si ha entrado o salido alguien
people_in_scene = 0

#Dadas las areas de interes dadas por los contornos, clasificar estos para encontrar personas
def classify_contours(self, detector, contours, image, infor_image):
    return 0

#Dados los resultados guardarlos en formato csv
def save_results(self, results):
    return 0
