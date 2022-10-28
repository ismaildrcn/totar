import string
import time
import cv2
import os
import sqlite3 as sql
from tqdm import tqdm
from Process.process import FileManager, CharacterFilter, OCR, DataBase
import serial
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import threading


start_time = time.time()
# <--- Serial Communication Start --->
with open('web/coordinateText.txt','r') as file:
    coordinates = file.readline()
    file.close
#coordinates="39.000000, 34.000000"
SerialObj = serial.Serial('/dev/ttyUSB0',9600)
def gps():
    global coordinates,SerialObj
    while 1:
        ReciveString = SerialObj.readline()
        ReciveString = ReciveString.decode()
        print(ReciveString)
        if ReciveString[:5]  == 'Konum':
            print("Sensor Musait Degil Anten Veri Alamiyor")
        else:
            Latitude = ReciveString[:9]                         # Enlem
            Longitude = ReciveString[10:18]                     # Boylam
            Satellite = ReciveString[19:21]                     # Uydu Sayisi
            coordinates2 = "{}, {}".format(str(Latitude), str(Longitude))
            if len(coordinates2) > 15:
                coordinates=str(coordinates2)
            time.sleep(12)

def Address():
    global coordinates
    locator = Nominatim(user_agent = "openmapquest") #openmapquest
    location = locator.reverse(coordinates)
    return location.address

def timer(t):
    global start_time
    if time.time() - start_time >t:

        print(time.time()-start_time)
        start_time = time.time()

        address = Address()
        print(address)
        return address
    

def main():
    global coordinates
    Latitude = coordinates[:9]                         # Enlem
    Longitude = coordinates[11:20]
    print(Latitude,Longitude)
    number_files = len( os.listdir('/home/totar/Totar/Images'))
    print(number_files)


    if number_files<=0:
        time.sleep(0.5)
    x,y = 0,0
    time.sleep(3)
    StartTime = int(time.time())
    while True:
        if x < number_files:
            os.chdir("/home/totar/Totar/Images/")
            
            # <---- Deleting faulty files ---->
            for RemovePath in os.listdir("/home/totar/Totar/Images/"):
                status = os.stat(RemovePath).st_size
                if status == 0: 
                    os.remove(RemovePath)
            # <---- Deleting faulty files ---->

            try:
                
                img, ImgPath = FileManager(x)
                
                data = CharacterFilter(OCR(img))
                print(data) #None

                Latitude = coordinates[:9]                         # Enlem
                Longitude = coordinates[11:21]                     # Boylam
                if y ==0:
                    print("\n\nTOTAR ACILIYOR")
                    for i in tqdm(range(60)):
                        time.sleep(1)
                y += 1

                addr = timer(60)
                if not addr == None:
                    address = addr

                if not data == None:
                    DataBase(
                        data,
                        time.strftime('%x'),
                        time.strftime('%X'),
                        Latitude,
                        Longitude,
                        coordinates,
                        address
                    )

                x +=1
            except cv2.error:
                print("\nError: Gorsel yolu hatali, dosya bulunamadi!\n")
                x +=1
                continue
                
        number_files = len( os.listdir('/home/totar/Totar/Images'))
t1=threading.Thread(target=gps)
t1.start()

main()
t1.join()
