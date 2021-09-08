import cv2
import os
import numpy as np
from detect import reset_folder

#import image
def import_img(img_nome, img_cognome):
    nome = cv2.imread(img_nome)
    nome = cv2.resize(nome,(1000,160))
    cognome = cv2.imread(img_cognome)
    cognome = cv2.resize(cognome,(1000,160))
    return nome, cognome

#grayscale
def grayscale(nome, cognome):
    gray_nome = cv2.cvtColor(nome,cv2.COLOR_BGR2GRAY)
    gray_cognome = cv2.cvtColor(cognome,cv2.COLOR_BGR2GRAY)
    return gray_nome, gray_cognome

#binary
def binary(gray_nome, gray_cognome):
    ret_nome,thresh_nome = cv2.threshold(gray_nome,120,255,cv2.THRESH_BINARY_INV)
    ret_cognome,thresh_cognome = cv2.threshold(gray_cognome,110,255,cv2.THRESH_BINARY_INV)
    #cv2.imshow('cognome', thresh_cognome)
    #cv2.waitKey(0)
    return thresh_nome, thresh_cognome

#dilation
def dilation(thresh_nome, thresh_cognome):
    kernel = np.ones((1,1), np.uint8)
    dilation_nome = cv2.dilate(thresh_nome, kernel, iterations=1)
    kernel = np.ones((1,1), np.uint8)
    dilation_cognome = cv2.dilate(thresh_cognome, kernel, iterations=1)
    return(dilation_nome, dilation_cognome)

#find contours
def countours(dilation_nome, dilation_cognome):
    ctrs_nome, hier_nome = cv2.findContours(dilation_nome.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ctrs_nome = sorted(ctrs_nome, key=lambda ctr: cv2.boundingRect(ctr)[0])
    ctrs_cognome, hier_cognome = cv2.findContours(dilation_cognome.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ctrs_cognome = sorted(ctrs_cognome, key=lambda ctr: cv2.boundingRect(ctr)[0])
    return(ctrs_nome, ctrs_cognome)

#ritaglio le lettere
def rect(ctrs, bw, path):
    for i, ctr in enumerate(ctrs):
        # Get bounding box
        x, y, w, h = cv2.boundingRect(ctr)

        # Getting ROI
        roi = bw[y:y+h, x:x+w]

        # show ROI
        #cv2.imshow('segment no:'+str(i),roi)
        cv2.rectangle(bw,(x,y),( x + w, y + h ),(0,255,0),2)
        #cv2.waitKey(0)

        if w > 15 and h > 15:
            cv2.imwrite(path.format(i), np.invert(roi))


def run_letters():
    reset_folder('img-process/letters_nome')
    reset_folder('img-process/letters_cognome')

    nome, cognome = import_img('img-process/result/nome.png', 'img-process/result/cognome.png')
    gray_nome, gray_cognome = grayscale(nome, cognome)
    thresh_nome, thresh_cognome = binary(gray_nome, gray_cognome)
    dilation_nome, dilation_cognome = dilation(thresh_nome, thresh_cognome)
    ctrs_nome, ctrs_cognome = countours(dilation_nome, dilation_cognome)
    rect(ctrs_nome, thresh_nome, 'img-process/letters_nome/l_{}.png')
    rect(ctrs_cognome, thresh_cognome, 'img-process/letters_cognome/l_{}.png')
 
run_letters() 
    