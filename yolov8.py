import random
import time

import torch
import cv2
import numpy as np
from ultralytics import YOLO
import ultralytics
import argparse
import os
import socket
import json
from colorama import init, Fore, Back, Style
import turtle
from ffpyplayer.player import MediaPlayer
i=1
init()

# print(os.listdir("videolar/"))

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('Using device:', device)
print()
play = MediaPlayer("br.mp3")

# Additional Info when using cuda
if device.type == 'cuda':
    print(" ")
    print(" ")
    print(" ")
    print(" ")


    print(
        f"{Fore.BLACK}{Fore.BLACK}{Back.YELLOW}{Style.DIM}{'S A R S I L M A Z'}{Style.RESET_ALL}{Fore.BLACK}".center(150, " "))
    print(" ")
    print(
        f"{Fore.RED}🚀🚀🚀{Style.RESET_ALL} {Fore.BLACK}{Back.GREEN} {Style.DIM} {' SARSILMAZ UÇUŞ İÇİN HAZIR '} {Style.RESET_ALL}{Fore.RED}🚀🚀🚀{Style.RESET_ALL}".center(
            150, " "))
    print(" ")
    print(f"{Fore.YELLOW}{ultralytics.checks()}{Style.RESET_ALL}")
    print(torch.cuda.get_device_name(0))

parser = argparse.ArgumentParser()
parser.add_argument('-w', '--weights', type=str, default="yolov8n.pt", help='modeli secmek icin')
parser.add_argument('-c', '--coco', type=str, default="coco.txt", help='coco txt´yi seçmek için')
parser.add_argument('--isim', type=str, default="video", help='video ismini seçmek için')
parser.add_argument('--socketip', type=str, default="127.0.1.1", help='modeli secmek icin')
parser.add_argument('-k', '--kaynak', type=str, default="0", help='kaynağı belirtir')
parser.add_argument('--kaydet', action='store_true', help='video olarak kaydeder')
parser.add_argument('--siniflar', action='store_true', help='Sınıfları yazdırır')
parser.add_argument('--datagonder', action='store_true', help='video olarak kaydeder')
parser.add_argument('--yazdir', action='store_true', help='bilgileri konsola yazdırır')
parser.add_argument('--oran', type=float, default=0.55, help='confidence threshold')
parser.add_argument('--sarso', action='store_true', help='Animasyonu çağırır')
args = parser.parse_args()
print(args)

path0 = f'videolar/{args.isim}{len(os.listdir("videolar/"))}.avi'

if args.sarso:
    screen = turtle.Screen()
    screen.bgpic("sars.png")
    screen.setup(width=1000, height=600)
    pen = turtle.Turtle()
    pen.speed(2)
    pen.penup()
    pen.goto(-200, -150)
    pen.pendown()
    pen2 = turtle.Turtle()
    pen2.speed(2)
    pen2.penup()
    pen2.goto(-200, -150)
    pen2.pendown()
    pen2.color("white")
    pen2.pensize(2)
    pen2.forward(450)

    pen.color("white")
    pen.write("S", font=("Verdana", 40, "italic"))
    pen.penup()
    pen.forward(50)
    pen.pendown()

    pen.color("white")
    pen.write("A", font=("Verdana", 40, "italic"))
    pen.penup()
    pen.forward(50)
    pen.pendown()
    pen.color("white")
    pen.write("R", font=("Verdana", 40, "italic"))
    pen.penup()
    pen.forward(50)
    pen.pendown()
    pen.color("white")
    pen.write("S", font=("Verdana", 40, "italic"))
    pen.penup()
    pen.forward(53)
    pen.pendown()
    pen.color("white")
    pen.write("I", font=("Verdana", 40, "italic"))
    pen.penup()
    pen.forward(47)
    pen.pendown()
    pen.color("white")
    pen.write("L", font=("Verdana", 40, "italic"))
    pen.penup()
    pen.forward(50)
    pen.pendown()
    pen.color("white")
    pen.write("M", font=("Verdana", 40, "italic"))
    pen.penup()
    pen.forward(55)
    pen.pendown()
    pen.color("white")
    pen.write("A", font=("Verdana", 40, "italic"))
    pen.penup()
    pen.forward(50)
    pen.pendown()
    pen.color("white")
    pen.write("Z", font=("Verdana", 40, "italic"))
    pen.penup()
    pen.forward(50)
    pen.pendown()
    time.sleep(2)
    turtle.bye()

if args.datagonder:
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind((args.socketip, 8080))
    serv.listen(5)

# video kaydedici başlatma
if args.kaydet:
    fourrcc = cv2.VideoWriter_fourcc(*'XVID')
    videoKayit = cv2.VideoWriter(path0, fourrcc, 20.0, (640, 480))

# opening the file in read mode
my_file = open(f"utils/{args.coco}", "r")
# reading the file
data = my_file.read()
# replacing end splitting the text | when newline ('\n') is seen.
class_list = data.split("\n")
my_file.close()

# print(class_list)

# Generate random colors for class list
detection_colors = []
for i in range(len(class_list)):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    detection_colors.append((b, g, r))

# load a pretrained YOLOv8n model
model = YOLO(f"weights/{args.weights}", "v8")

# Vals to resize video frames | small frame optimise the run
frame_wid = 640
frame_hyt = 480
if args.siniflar:
    print(model.names)

# cap = cv2.VideoCapture(1)
cap = cv2.VideoCapture(0 if args.kaynak == "0" else args.kaynak)

if not cap.isOpened():
    print("Cannot open camera")
    exit()


while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True



    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    #  resize the frame | small frame optimise the run
    # frame = cv2.resize(frame, (frame_wid, frame_hyt))

    # Predict on image
    detect_params = model.predict(source=[frame], conf=args.oran, save=False)
    # Convert tensor array to numpy
    DP = detect_params[0].cpu().numpy()
    # print(f"{DP} dp")

    if len(DP) != 0:

        for i in range(len(detect_params[0])):
            # print(f"{i} i")

            boxes = detect_params[0].boxes
            box = boxes[i]  # returns one box
            clsID = box.cls.cpu().numpy()[0]
            conf = box.conf.cpu().numpy()[0]
            bb = box.xyxy.cpu().numpy()[0]

            merkez_nokta = (
            int((int(bb[2]) - int(bb[0])) / 2) + int(bb[0]), int((int(bb[3]) - int(bb[1])) / 2) + int(bb[1]))
            # print(merkez_nokta)
            infos = {"p1": (int(bb[0]), int(bb[1])),
                     "p2": (int(bb[2]), int(bb[3])),
                     "merkez_nokta": merkez_nokta,
                     "oran": round(float(conf), 2),
                     "sinif": str(model.names[int(clsID)])
                     }
            if args.yazdir:
                print(infos)
            if args.datagonder:
                jsonStr = json.dumps(infos)
                clientsocket, address = serv.accept()
                print(f"Connection from {address} has been established.")
                clientsocket.send(bytes(jsonStr, "utf-8"))
                clientsocket.close()
            cv2.rectangle(
                frame,
                (int(bb[0]), int(bb[1])),
                (int(bb[2]), int(bb[3])),
                detection_colors[int(clsID)],
                3,
            )
            cv2.circle(frame, merkez_nokta, 3, detection_colors[int(clsID)], 3)

            # Display class name and confidence
            font = cv2.FONT_HERSHEY_PLAIN
            cv2.putText(
                frame,
                class_list[int(clsID)] + " " + str(round(conf, 3)) + "%",
                (int(bb[0]), int(bb[1]) - 10),
                font,
                2,
                (131, 23, 12),
                3,
            )
    # video kaydedici
    if args.kaydet:
        videoKayit.write(frame)

    # Display the resulting frame
    cv2.imshow("ObjectDetection", frame)

    # Terminate run when "Q" pressed
    if cv2.waitKey(1) == ord("q"):
        break

# When everything done, release the capture
cap.release()
if args.kaydet:
    videoKayit.release()
    print(f'{Fore.GREEN}Video Kaydedildi -> {path0}{Style.RESET_ALL}')





cv2.destroyAllWindows()