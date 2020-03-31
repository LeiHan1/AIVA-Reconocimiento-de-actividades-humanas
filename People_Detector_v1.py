import numpy as np
import cv2
import csv



#Verifica que la nueva persona detectada nno está ya en el sistema
def check_if_in(pedestrians, ped):
    for pedestrian in pedestrians:
        if np.abs(ped[0] - pedestrian[0]) + np.abs(ped[1] - pedestrian[1]) < 150:
            return False
    return True
#Analiza las trayectorias de las personas detectadas y genera el csv de salida
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

            
            
# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
video_path = "Videos/OneLeaveShop1front.mpg"
pedestrian_cascade = cv2.CascadeClassifier("haarcascade_fullbody.xml")
trackers = cv2.MultiTracker_create()

vs = cv2.VideoCapture(video_path)

id = 0
all_pedestrians = []
trayectorias = []
font = cv2.FONT_HERSHEY_DUPLEX
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
