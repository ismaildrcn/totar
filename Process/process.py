from unittest import result
import cv2
import time
import string
import sqlite3 as sql
import pytesseract as pytes


def FileManager(x):
    ImgPath = '/home/totar/Totar/Images/PlateImage-{}.jpg'.format(x)
    img = cv2.imread(ImgPath)

    return img, ImgPath

def DataBase(data, date, time, latitude, longitude, coordinate, address):
    db = sql.connect("/home/totar/Totar/web/database/TotarData.db")
    im = db.cursor()
    
    CreateTable = """CREATE TABLE IF NOT EXISTS Plates (plate,date,time,latitude,longitude,coordinate,address)"""
    EnterValue = """INSERT INTO Plates(plate, date, time, latitude, longitude, coordinate, address) values ('{}','{}','{}','{}','{}','{}','{}')""".format(
        data,
        date,
        time,
        latitude,
        longitude,
        coordinate,
        address
    )
    im.execute(CreateTable)
    im.execute("""SELECT plate FROM Plates WHERE plate=?""" ,[data])
    result = im.fetchone()
    if result:
        #gec
        print("Ayni plaka daha once yazildi.")
        pass
    else:
        im.execute(EnterValue)
        db.commit()
    
def OCR(img):
    # <---- remove noise from image ---->
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening
    # <---- remove noise from image ---->

    # <---- OCR ---->
    data = pytes.image_to_string(gray, lang='eng', config='--psm 7 --oem 1')
    data = list(data)
    return data

def CharacterFilter(data):
    characters = list(string.ascii_uppercase)
    digits = list(string.digits)
    lists = characters + digits
    new = list()

    # <---- Append data to list ---->
    for i in data:
        for j in lists:
            if i == j:
                new.append(i)
    # <---- Append data to list ---->

    # <---- Removing fake characters ---->
    if len(new)>6:
        for k in characters:
            if new[0] == k:
                new.pop(0)
            elif new[-1] == k:
                new.pop(-1)
        

        for digit0 in digits:
            for digit1 in digits:
                for digit2 in digits:
                    if new[0] == digit0 and new[1] == digit1 and new[2] ==digit2:
                        new.pop(0)
        if len(new)>6:                   
            new = ''.join(new)
            #print("Plaka:   {}".format(new))
            return new
    # <---- Removing fake characters ---->            
        
    if not (lists):
        data = data.replace('')
        """return data"""
