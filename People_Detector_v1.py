from __future__ import print_function
import numpy as np
import cv2
import csv


# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
video_path = "OneLeaveShop1front.mpg"
pedestrian_cascade = cv2.CascadeClassifier("haarcascade_fullbody.xml")
vs = cv2.VideoCapture(video_path)
id = 0

def check_if_in(pedestrians, ped):
    for pedestrian in pedestrians:
        if np.abs(ped[0] - pedestrian[0]) + np.abs(ped[1] - pedestrian[1]) < 150:
            return False
    return True

def analisis_trayectorias(trayectorias):
    id = 0
    with open('person_detector.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["id_person", "hora_entrada", "hora_salida", "tramo", "movimiento"])
        for mov in trayectorias:
            tramo_izquierdo = []
            tramo_central = []
            tramo_derecho = []
            orden = []
            for tray in mov:
                centro = (210, 330)
                coor_uno = tray
                #print(coor_uno)
                if coor_uno[0] < 210:
                    ind = 0
                elif coor_uno[0] > 330:
                    ind = 1
                else:
                    ind = 2
                if ind == 0:  # la persona está a la izquierda
                    if not 0 in orden:
                     orden.append(0)
                    tramo_izquierdo.append(coor_uno)
                if ind == 1:  # la persona está a la derecha
                    if not 1 in orden:
                        orden.append(1)
                    tramo_derecho.append(coor_uno)
                if ind == 2:  # la persona está en el centro
                    if not 2 in orden:
                        orden.append(2)
                    tramo_central.append(coor_uno)

            print(id)

            for ord in orden:
                if ord == 0:
                    if len(tramo_izquierdo) > 0: #la persona está a la izquierda
                        print("La persona avanza por la izquierda")
                        aux = tramo_izquierdo[0]
                        aux1 =  tramo_izquierdo[len(tramo_izquierdo)-1]
                        if aux[1] > aux1[1]:
                            print("va de izquierda a derecha")
                            spamwriter.writerow([id, "00:00", "00:10", "izquierdo", "izqAder"])
                        else:
                            print("va de derecha a izquierda")
                            spamwriter.writerow([id, "00:00", "00:10", "izquierdo", "derAizq"])


                if ord == 1:
                    if len(tramo_derecho) > 0: #la persona está a la derecha
                        print("La persona avanza por la derecha")
                        aux = tramo_derecho[0]
                        aux1 =  tramo_derecho[len(tramo_derecho)-1]
                        if aux[1] > aux1[1]:
                            print("va de derecha a izquierda")
                            spamwriter.writerow([id, "00:00", "00:10", "derecho", "derAizq"])
                        else:
                            print("va de izquierda a derecha")
                            spamwriter.writerow([id, "00:00", "00:10", "derecho", "izqAder"])
                if ord == 2:
                    if len(tramo_central) > 0: #la persona está en el centro
                        print("La persona avanza por el centro")
                        aux = tramo_central[0]
                        aux1 = tramo_central[len(tramo_central)-1]
                        if aux[0] > aux1[0]:
                            print("la persona entra")
                            spamwriter.writerow([id, "00:00", "00:10", "central", "entra"])
                        else:
                            print("la persona sale")
                            spamwriter.writerow([id, "00:00", "00:10", "central", "sale"])

            id += 1
trackers = cv2.MultiTracker_create()
all_pedestrians = []

trayectorias = []
# trayectorias = [[(31, 105, 10, 10), (32, 106, 10, 10), (33, 109, 10, 10), (32, 106, 10, 10), (31, 106, 10, 10), (32, 107, 10, 10), (32, 106, 10, 10), (32, 105, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 105, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 105, 10, 10), (33, 108, 10, 10), (32, 106, 10, 10), (31, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (31, 107, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 107, 10, 10), (32, 106, 10, 10), (31, 107, 10, 10), (32, 106, 10, 10), (32, 107, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 107, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (31, 107, 10, 10), (32, 107, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 105, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 107, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 107, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 107, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 107, 10, 10), (32, 105, 10, 10), (32, 107, 10, 10), (32, 105, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 107, 10, 10), (32, 106, 10, 10), (32, 107, 10, 10), (32, 107, 10, 10), (32, 107, 10, 10), (32, 105, 10, 10), (32, 106, 10, 10), (32, 105, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 105, 10, 10), (32, 107, 10, 10), (32, 106, 10, 10), (32, 107, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (31, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 107, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (31, 106, 10, 10), (32, 106, 10, 10), (32, 105, 10, 10), (32, 106, 10, 10), (32, 107, 10, 10), (32, 106, 10, 10), (32, 107, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 107, 10, 10), (32, 107, 10, 10), (32, 107, 10, 10), (32, 108, 10, 10), (32, 106, 10, 10), (32, 107, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 107, 10, 10), (32, 106, 10, 10), (31, 107, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 107, 10, 10), (32, 106, 10, 10), (32, 107, 10, 10), (32, 106, 10, 10), (32, 107, 10, 10), (32, 106, 10, 10), (32, 107, 10, 10), (32, 108, 10, 10), (32, 107, 10, 10), (32, 107, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 107, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (31, 105, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 107, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 107, 10, 10), (31, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (31, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 107, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (31, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 107, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (31, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 107, 10, 10), (32, 106, 10, 10), (32, 106, 10, 10), (32, 107, 10, 10), (32, 107, 10, 10), (32, 107, 10, 10), (32, 106, 10, 10), (32, 107, 10, 10), (32, 107, 10, 10), (32, 107, 10, 10), (32, 107, 10, 10), (32, 107, 10, 10), (32, 107, 10, 10)], [(313, 93, 10, 10), (313, 95, 10, 10), (314, 94, 10, 10), (314, 94, 10, 10), (314, 95, 10, 10), (316, 94, 10, 10), (316, 95, 10, 10), (315, 96, 10, 10), (316, 96, 10, 10), (316, 96, 10, 10), (315, 97, 10, 10), (316, 98, 10, 10), (315, 97, 10, 10), (316, 98, 10, 10), (315, 98, 10, 10), (316, 98, 10, 10), (316, 97, 10, 10), (316, 98, 10, 10), (316, 98, 10, 10), (317, 97, 10, 10), (316, 99, 10, 10), (316, 99, 10, 10), (316, 100, 10, 10), (316, 101, 10, 10), (316, 100, 10, 10), (316, 101, 10, 10), (316, 101, 10, 10), (316, 101, 10, 10), (316, 102, 10, 10), (316, 101, 10, 10), (316, 101, 10, 10), (317, 102, 10, 10), (316, 101, 10, 10), (315, 101, 10, 10), (315, 101, 10, 10), (315, 102, 10, 10), (313, 102, 10, 10), (313, 103, 10, 10), (312, 103, 10, 10), (313, 103, 10, 10), (310, 104, 10, 10), (311, 105, 10, 10), (312, 105, 10, 10), (311, 105, 10, 10), (311, 106, 10, 10), (312, 106, 10, 10), (311, 105, 10, 10), (312, 105, 10, 10), (312, 105, 10, 10), (312, 106, 10, 10), (311, 106, 10, 10), (311, 106, 10, 10), (310, 108, 10, 10), (309, 108, 10, 10), (309, 108, 10, 10), (309, 108, 10, 10), (308, 109, 10, 10), (309, 109, 10, 10), (309, 109, 10, 10), (309, 109, 10, 10), (308, 109, 10, 10), (308, 109, 10, 10), (308, 109, 10, 10), (307, 110, 10, 10), (307, 110, 10, 10), (307, 110, 10, 10), (306, 110, 10, 10), (307, 111, 10, 10), (307, 112, 10, 10), (307, 112, 10, 10), (307, 113, 10, 10), (306, 113, 10, 10), (306, 114, 10, 10), (306, 115, 10, 10), (306, 114, 10, 10), (306, 114, 10, 10), (305, 115, 10, 10), (307, 114, 10, 10), (307, 115, 10, 10), (307, 114, 10, 10), (308, 115, 10, 10), (309, 116, 10, 10), (308, 116, 10, 10), (309, 117, 10, 10), (310, 117, 10, 10), (310, 118, 10, 10), (311, 118, 10, 10), (312, 119, 10, 10), (313, 118, 10, 10), (313, 119, 10, 10), (314, 119, 10, 10), (315, 119, 10, 10), (315, 119, 10, 10), (315, 119, 10, 10), (316, 119, 10, 10), (316, 120, 10, 10), (317, 121, 10, 10), (318, 121, 10, 10), (319, 121, 10, 10), (319, 123, 10, 10), (321, 123, 10, 10), (322, 123, 10, 10), (324, 123, 10, 10), (326, 124, 10, 10), (328, 124, 10, 10), (329, 124, 10, 10), (330, 123, 10, 10), (330, 124, 10, 10), (327, 123, 10, 10), (328, 123, 10, 10), (330, 124, 10, 10), (332, 124, 10, 10), (332, 124, 10, 10), (334, 125, 10, 10), (334, 125, 10, 10), (337, 125, 10, 10), (339, 127, 10, 10), (340, 126, 10, 10), (342, 126, 10, 10), (343, 126, 10, 10), (344, 127, 10, 10), (346, 126, 10, 10), (346, 127, 10, 10), (348, 126, 10, 10), (350, 126, 10, 10), (350, 127, 10, 10), (353, 127, 10, 10), (354, 128, 10, 10), (355, 128, 10, 10), (357, 129, 10, 10), (359, 130, 10, 10), (363, 132, 10, 10), (364, 132, 10, 10), (366, 131, 10, 10), (369, 130, 10, 10), (371, 130, 10, 10), (374, 130, 10, 10), (376, 130, 10, 10), (377, 130, 10, 10), (377, 130, 10, 10), (378, 130, 10, 10), (378, 131, 10, 10), (378, 132, 10, 10)]]
# analisis_trayectorias(trayectorias)
while True:
    # reads frames from a video
    ret, frames = vs.read()

    if frames is None:
        break

    img_color = frames.copy()
    # convert to gray scale of each frames
    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)

    # Detects pedestrians of different sizes in the input image
    pedestrians = pedestrian_cascade.detectMultiScale(gray, 1.1, 1)
    # To draw a rectangle in each pedestrians
    for (x,y,w,h) in pedestrians:
        r = x+30,y+30,10,10
        if check_if_in(all_pedestrians, r):
            all_pedestrians.append(r)
            trackers.add(cv2.TrackerCSRT_create(), frames, r)
            cv2.rectangle(img_color,(x,y),(x+w,y+h),(0,255,0),2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img_color, 'Person', (x + 6, y - 6), font, 0.5, (0,
            255, 0), 1)
            # Display frames in a window
    (success, cajas) = trackers.update(frames)
    cnt = 0
    if success and len(cajas) > 0:
        for box in cajas:
            (x, y, w, h) = [int(v) for v in box]
            if len(trayectorias) < len(cajas):
                trayectorias.append([])
            trayectorias[cnt].append((x, y, w, h))
            cnt+=1
            cv2.putText(img_color, str(cnt), (x + 6, y - 6), font, 0.5, (0,
                                                                         255, 0), 1)
            cv2.rectangle(img_color, (x, y), (x + w, y + h),
                          (0, 255, 0), 2)
    cv2.imshow('Pedestrian detection', img_color)
    # Wait for Enter key to stop
    if cv2.waitKey(33) == 13:
        break

analisis_trayectorias(trayectorias)
