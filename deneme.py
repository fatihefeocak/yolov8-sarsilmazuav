import cv2
import base64
import json
import numpy as np

import turtle

# Pencereyi oluştur
pencere = turtle.Screen()
pencere.title("SARSILMAZ")

# Kalemimizi oluştur ve özelliklerini ayarla
kalem = turtle.Turtle()
kalem.speed(1)  # Kalem hızını ayarla
kalem.pensize(4)  # Kalem kalınlığını ayarla

# "SARSILMAZ" kelimesini yazdır
kalem.penup()
kalem.goto(-100, 0) # Başlangıç konumunu ayarla
kalem.pendown()
kalem.color("blue") # Yazı rengini ayarla
kalem.write("SARSILMAZ", font=("Arial", 30, "normal"))

# Çizimleri ekranda tut
turtle.done()





