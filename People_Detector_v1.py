import numpy as np
import cv2
import csv


class Person:
    """Clase persona, utilizada para identificar a cada individuo que aparece en el campo de visión"""
    trayectoria = None
    id = 0

    def __init__(self, id):
        self.id = id
        self.trayectoria = []

    """Añade un nuevo movimiento de la persona en el campo de visión"""
    def add_state(self, position):
        self.trayectoria.append(position)

    def getId(self):
        return self.id

    def get_states(self):
        return self.trayectoria


class DetectSystem:
    """Clase DetectSystem encargada de realizar todo el proceso de detección y seguimiento de las personas en la escena"""
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    #Se usará el cascadeClassifier de opencv usando un modelo de detección de personas
    pedestrian_cascade = cv2.CascadeClassifier("haarcascade_fullbody.xml")

    all_pedestrians = [] #Se guardan todas las detecciones para verificar que no se detecta dos veces a la misma persona
    personas = []
    cnt_personas = 0

    trackers = cv2.MultiTracker_create() #Se usará el multitracker de opencv para seguir a las personas identificadas

    def __get_frame(self, buffer):
        ret, frame = buffer.read()
        return ret, frame

    def __detect_pedestrian(self, frames, gray):
        """Dada una imagen detecta si hay personas en ella e inicia/continua el seguimiento de estas"""

        # Detecta personas en la escena
        pedestrians = self.pedestrian_cascade.detectMultiScale(gray, 1.1, 1)

        for (x, y, w, h) in pedestrians:
            r = x + 30, y + 30, 10, 10
            #Se comprueba que no se estudie la misma persona
            if self.__check_pedestrian_already_exist(self.all_pedestrians, r):
                self.all_pedestrians.append(r)
                self.personas.append(Person(self.cnt_personas))
                self.cnt_personas = self.cnt_personas + 1
                #Se inicializa el seguimiento
                self.trackers.add(cv2.TrackerCSRT_create(), frames, r)

        (success, cajas) = self.trackers.update(frames)
        cnt = 0
        if success and len(cajas) > 0:
            for box in cajas:
                (x, y, w, h) = [int(v) for v in box]
                #Se añade el nuevo movimiento al historial de cada persona
                self.personas[cnt].add_state((x, y, w, h))
                cnt += 1

    def __check_pedestrian_already_exist(self, pedestrians, ped):
        """Para evitar multiples detecciones de la misma persona, se verifica que las nuevas detecciones estén a cierta distancia de las demás"""
        for pedestrian in pedestrians:
            if np.abs(ped[0] - pedestrian[0]) + np.abs(ped[1] - pedestrian[1]) < 150:
                return False
        return True

    def __save_results(self):
        """Se analizan los datos obtenidos de los movimientos de las personas en la escena y se guardan los resultados en formato csv"""
        with open('person_detector.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(["id_person", "hora_entrada", "hora_salida", "tramo", "movimiento"])
            for persona in self.personas:
                tramo_izquierdo = []
                tramo_central = []
                tramo_derecho = []
                orden = []

                for tray in persona.get_states():
                    coor_uno = tray
                    if coor_uno[0] < 210:
                        ind = 0
                    elif coor_uno[0] > 330:
                        ind = 1
                    else:
                        ind = 2
                    if ind == 0:  # la persona está a la izquierda de la escena
                        if not 0 in orden:
                            orden.append(0)
                        tramo_izquierdo.append(coor_uno)
                    if ind == 1:  # la persona está a la derecha de la escena
                        if not 1 in orden:
                            orden.append(1)
                        tramo_derecho.append(coor_uno)
                    if ind == 2:  # la persona está en la puerta del establecimiento
                        if not 2 in orden:
                            orden.append(2)
                        tramo_central.append(coor_uno)

                for ord in orden: #Guardamos en orden de ocurrencia
                    if ord == 0: 
                        if len(tramo_izquierdo) > 0:

                            aux = tramo_izquierdo[0]
                            aux1 = tramo_izquierdo[len(tramo_izquierdo) - 1]
                            if aux[1] > aux1[1]:
                                spamwriter.writerow([persona.id, "00:00", "00:10", "izquierdo", "izqAder"])
                            else:
                                spamwriter.writerow([persona.id, "00:00", "00:10", "izquierdo", "derAizq"])

                    if ord == 1:
                        if len(tramo_derecho) > 0:

                            aux = tramo_derecho[0]
                            aux1 = tramo_derecho[len(tramo_derecho) - 1]
                            if aux[1] > aux1[1]:
                                spamwriter.writerow([persona.id, "00:00", "00:10", "derecho", "derAizq"])
                            else:
                                spamwriter.writerow([persona.id, "00:00", "00:10", "derecho", "izqAder"])
                    if ord == 2:
                        if len(tramo_central) > 0:

                            aux = tramo_central[0]
                            aux1 = tramo_central[len(tramo_central) - 1]
                            if aux[0] > aux1[0]:
                                spamwriter.writerow([persona.id, "00:00", "00:10", "central", "entra"])
                            else:
                                spamwriter.writerow([persona.id, "00:00", "00:10", "central", "sale"])

    def run(self, path):
        vs = cv2.VideoCapture(path)
        while True:
            ret, frames = self.__get_frame(vs)
            if frames is None:
                break
            gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
            self.__detect_pedestrian(frames, gray)

        self.__save_results()


def main():
    a = DetectSystem()
    a.run("Videos/OneLeaveShop1front.mpg")


main()
