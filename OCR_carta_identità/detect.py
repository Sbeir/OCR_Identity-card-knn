import cv2
from PIL import Image
import numpy as np
from cv2 import boundingRect, countNonZero, cvtColor, drawContours, findContours, getStructuringElement, imread, morphologyEx, pyrDown, rectangle, threshold
import os
import glob

def crop(img_path):
    img = Image.open(img_path)
    img = img.resize((1920,1080))
    cropped_im = img.crop((620, 305, 1050, 520))
    cropped_im.save('img-process/result/ritaglio.png')
    #cropped_im.show()

#svuota cartella
def reset_folder(path):
    delete = os.listdir(path)
    for file in delete[0:]:
        os.remove(os.path.join(path, file))

def import_img(path):
    image = imread(path)
    return image



def transform_image():
    path =  'img-process/result'
    list_of_files = glob.glob('card/*.png')
    latest_file = max(list_of_files, key=os.path.getctime)
    crop(latest_file)


    image = import_img('img-process/result/ritaglio.png')
    reset_folder(path)

    # downsample and use it for processing
    rgb = pyrDown(image)

    # apply grayscale
    small = cvtColor(rgb, cv2.COLOR_BGR2GRAY)

    # morphological gradient
    morph_kernel = getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    grad = morphologyEx(small, cv2.MORPH_GRADIENT, morph_kernel)

    # binarize
    _, bw = threshold(src=grad, thresh=0, maxval=255, type=cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    morph_kernel = getStructuringElement(cv2.MORPH_RECT, (9, 1))

    # connect horizontally oriented regions
    connected = morphologyEx(bw, cv2.MORPH_CLOSE, morph_kernel)
    mask = np.zeros(bw.shape, np.uint8)

    # find contours
    contours, hierarchy = findContours(connected, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    # filter contours
    n = 0
    for idx in range(0, len(hierarchy[0])):
        rect = x, y, rect_width, rect_height = boundingRect(contours[idx])
        
        # fill the contour
        mask = drawContours(mask, contours, idx, (255, 255, 2555), cv2.FILLED)
        
        # ratio of non-zero pixels in the filled region
        r = float(countNonZero(mask)) / (rect_width * rect_height)
        if r > 0.45 and rect_height > 8 and rect_width > 8:
            rgb = rectangle(rgb, (x, y+rect_height), (x+rect_width, y), (0,255,0),1)
            roi = rgb[y:y + rect_height, x:x + rect_width]
            cv2.imwrite('img-process/result/rect' + str(n) + '.png', roi)
            n += 1
            
    # eliminiamo i rettangoli non necessari     
    num_files = len(os.listdir(path))   
    delete = os.listdir(path)
    while num_files > 4:
        for file in delete[:1]:
            os.remove(os.path.join(path, file))
            num_files -= 1
            
    #eliminiamo le etichhette "nome" e "cognome"
    delete = os.listdir(path)
    for file in delete[1::2]:
        os.remove(os.path.join(path, file))
        
    #rinominiamo i file finali nella cartella result 
    rename = os.listdir(path)
    os.rename(os.path.join(path, rename[0]), os.path.join(path, 'nome.png'))
    os.rename(os.path.join(path, rename[1]), os.path.join(path, 'cognome.png'))
        
    #visualizziamo il risultato
    #Image.fromarray(rgb).show()  
    #cv2.imshow('thresh', bw)  
    #cv2.waitKey(0)



transform_image()

