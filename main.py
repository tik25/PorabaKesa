# Program se uporablja za pomoc pri analizi porabe denarja.
# Program spremlja excel datoteka z podatki. ("Data.xlsx")

# Avtor: Yap Ploj
# https://github.com/tik25

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import date

# img
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\yap\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'

# pdf
from fpdf import FPDF


# ------------------------------------------------------

def GetData():
    data = pd.read_excel('../Data.xlsx')
    return data


def GetImageData():
    img = cv2.imread("../DataSlike/realtest2.jpg")
    # edit image with openCV
    ##kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    ##img = cv2.filter2D(img, -1, kernel)
    #
    txt = pytesseract.image_to_data(img)
    txt2 = pytesseract.image_to_string(img)
    print(txt)
    print("##")
    print(txt2)
    data = 0

    return data


if __name__ == '__main__':
    # ---get data from excel
    data = GetData()
    # ---analize
    N = len(data["Cena"])
    # print("st vnosov:", N)
    # print("od {} do {}".format(data["Datum"][0], data["Datum"][N-1]))
    # calculate total
    skupaj = sum(data["Cena"])
    # kolk je avg na dan
    mesci = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    prvi = data["Datum"][0]
    # zadni = data["Datum"][N - 1]
    prvidan, prvimesc, prvileto = prvi.split(".")
    zadnileto, zadnimesc, zadnidan = str(date.today()).split("-")
    prvi = date(int(prvileto), int(prvimesc), int(prvidan))
    zadni = date(int(zadnileto), int(zadnimesc), int(zadnidan))
    delta = zadni - prvi
    naDan = skupaj / delta.days

    SumKategorije = {i: 0 for i in data["Kategorije"]}
    SumKategorije.pop(np.nan)  # remove nepotrebn nan key
    for i in range(N):
        SumKategorije[data["Kategorija"][i]] += data["Cena"][i]
    # print(SumKategorije)

    # remove kategorije z ceno 0
    temp = []
    for key in SumKategorije.keys():
        if SumKategorije[key] == 0:
            temp.append(key)
    for i in temp:
        SumKategorije.pop(i)
    # ---make pie chart za kategorije
    plt.rcParams.update({'font.size': 7})  # update label font
    fig = plt.figure(figsize=(4, 3))
    y = SumKategorije.values()
    labels = ["{} = {:.2f}".format(ime1, SumKategorije[ime1]) for ime1 in SumKategorije.keys()]

    plt.title("skupaj = {:.2f}".format(skupaj, data["Datum"][0], ",".join([zadnidan, zadnimesc, zadnileto])))
    plt.pie(y, labels=labels)
    plt.tight_layout()
    plt.savefig("pie.png")
    # plt.show()

    # ---izpise artikle za vsako kategorijo
    ItemsKategorije = {}
    for kategorija in data["Kategorije"]:
        templist = []
        for i, item in enumerate(data["Kategorija"]):
            if item == kategorija:
                if data["Produkt"][i] not in templist:
                    templist.append(data["Produkt"][i])
        ItemsKategorije[kategorija] = templist
    ItemsKategorije.pop(np.nan)  # remove nepotrebn nan key


    # ---makepdf
    # fronpage
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=24)
    pdf.cell(200, 10, txt="Poraba Denarja", ln=1, align='C')
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="\nYap Ploj", ln=1, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="\n", ln=1, align='C')
    txt = "avtomatsko generiran report za podatke od {} do {}".format(data["Datum"][0], data["Datum"][N - 1])
    pdf.cell(200, 10, txt=txt, ln=2, align='C')
    pdf.cell(200, 10, txt="izvorna koda: https://github.com/tik25/PorabaKesa", ln=2, align='C',
             link="https://github.com/tik25")
    # 2nd
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="Artikli vsake kategorije:", ln=1, align='C')
    for i in ItemsKategorije:
        pdf.set_font("Arial", size=14, style="B")
        pdf.cell(200, 10, txt=i, ln=1, align='L')
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(200, 10, txt=", ".join(ItemsKategorije[i]), align='L')
        pdf.cell(200, 10, txt="", ln=1, align='L')
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="Stats:", ln=1, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="* na dan povp. = {:.2f}".format(naDan), ln=1, align='L')
    # tuki se kake statse dodas z > pdf.cell(200, 10, txt= "***" , ln=1, align='L')

    # slike
    pdf.cell(200, 10, txt="\n", ln=1, align='C')
    pdf.cell(200, 10, txt="===================================================================", ln=1, align='C')
    pdf.cell(200, 10, txt="\n", ln=1, align='C')
    pdf.image("pie.png", 1)

    # ---save pdf
    pdf.output("out.pdf")
