#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 15:08:47 2019

@author: wickedshaman
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 20:29:41 2019
@author: wickedshaman
"""
import random
import numpy as np
import cv2


pathName_output = "/home/wickedshaman/Desktop/Keratoconus/ECE_5554_Final_Project_Sarang_Joshi/output_keratoconus/"
pathName_input = "/home/wickedshaman/Desktop/Keratoconus/ECE_5554_Final_Project_Sarang_Joshi/sample_gray_keratoconus/"
spread_factor = None
num_ghost_imgs = 2


def saveImage(pathName, img, name):
    cv2.imwrite(pathName + name, img)
    return

def channel_transformer(img_mono, channel, mat_t):
    ht,wid = img_mono.shape[:2]    
    translated_img = cv2.warpAffine(img_mono, mat_t, (wid,ht), borderMode=cv2.BORDER_REFLECT)
    return cv2.split(translated_img)

def generate_affine_matrix(img):
    ht,wid = img.shape[:2]
    rand_y = negative_wt() * random.randint(spread_factor[0],spread_factor[1])
    rand_x = negative_wt() *random.randint(spread_factor[0],spread_factor[1])
    shift_ht = ht/rand_y
    shift_wid = wid/rand_x
    #print (str(rand_y) + "::" + str(rand_x))
    mat_t= np.float32([[1,0,shift_ht],[0,1,shift_wid]])
    return mat_t

def negative_wt():
    wt = random.randint(-1,1)
    if wt == -1:
        return -1
    else:
        return 1

def isolate_img_channel(img, channel):
    pass


def img_transformer(img):   
    mat_t = generate_affine_matrix(img)
    B,G,R = cv2.split(img)
    zeros = np.zeros(B.shape, dtype="uint8")
    
    # create a monochromatic image for the red channel and apply single channel transform to distort the image
    img_red = cv2.merge((zeros,zeros, R))
    _, _, img_red_c   = channel_transformer(img_red, "red", mat_t )

    # create a monochromatic image for the green channel and apply single channel transform to distort the image
    img_green = cv2.merge((zeros,G, zeros))
    _, img_green_c, _ = channel_transformer(img_green, "green", mat_t )
           
    # create a monochromatic image for the blue channel and apply single channel transform to distort the image
    img_blue = cv2.merge((B,zeros,zeros))
    img_blue_t, _, _  = channel_transformer(img_blue, "blue", mat_t )
    
    translated_img = cv2.merge((B,img_green_c,img_red_c ))
    return translated_img

if __name__ == "__main__":
    
    severity = input ("Enter severity of keratonus (mild, severe, extreme, custom):")
    if severity == "mild":
        spread_factor = (35,45)
        num_ghost_imgs = random.randint(2,3)
    elif severity == "severe":
        spread_factor = (15,25)
        num_ghost_imgs = random.randint(3,4)
    elif severity == "extreme":
        spread_factor = (15,25)
        num_ghost_imgs = random.randint(3,5)
    elif severity == "custom":
        num_ghost_imgs = input("enter ghost images num:")
    else:
        print ("incorrect input.... generating images with severe Keratoconus")
        spread_factor = (20,25)
    
    for i in range(2):    
        img_o = cv2.imread("./input_images/panorama.jpg")
        img_bg = cv2.imread("./input_images/panorama.jpg",0)
        saveImage(pathName_input,img_bg, "panorama.jpg" )
        img_kc = img_bg
        cv2.imshow('Keratoconus', img_bg)
        cv2.waitKey()
    
        for j in range(num_ghost_imgs):
            img_t = img_transformer(img_o)
            img_gray = cv2.cvtColor(img_t, cv2.COLOR_BGR2GRAY)
            img_kc = cv2.addWeighted(img_kc,0.73,img_gray,0.27,1)
        #img_kc = cv2.addWeighted(img_bg,0.3,img_kc,0.65,1)

            
        cv2.imshow('Keratoconus', img_kc )
        output_name = "pan_keratoconus_" + str(i) + ".jpg"
        saveImage(pathName_output,img_kc, output_name )
        output_name = "pan_keratoconus_" + str(i) + ".png"
        saveImage(pathName_output,img_kc, output_name )
        cv2.waitKey()
        cv2.destroyAllWindows()
