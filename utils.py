import cv2
from datetime import date, datetime
import math
import numpy as np
import pandas as pd
import os

def circle_mask(img,offset=0):
  height,width = img.shape[:2]
  r = math.floor(min(width,height)/2)
  if min(width,height) == height:
    offset_w = offset
    offset_h = 0
  elif min(width,height) == width:
    offset_w = 0
    offset_h = offset
  else:
    offset_w = offset
    offset_h = offset
  circle_img = np.zeros((height,width), np.uint8)
  cv2.circle(circle_img,(int(width/2), int(height/2)), r, 255,thickness=-1)
  if offset is not 0:
    cv2.circle(circle_img,(math.ceil((1+offset_w)*width/2), math.ceil((1+offset_h)*height/2)), r, 255,thickness=-1)
    cv2.circle(circle_img,(math.floor((1-offset_w)*width/2), math.floor((1-offset_h)*height/2)), r, 255,thickness=-1)
  return cv2.bitwise_and(img, img, mask=circle_img)

def crop(image,x,y,w,h):
  return image[y: y + h, x: x + w]

def preprocess(img,offset=0.02):
  height,width = img.shape[:2]
  r = math.ceil(height*(1+2*offset))
  x = int((width - r)/2)
  img = circle_mask(img,offset)
  img = crop(img,x,0,r,height)
  diff = img.shape[1]-img.shape[0]
  img = cv2.copyMakeBorder(img, diff//2, diff//2, 0,0, cv2.BORDER_CONSTANT, value=[0,0,0])
  return x,diff//2,img

#extract pixel - mm ratio
def getPixelLength(img, new_width=128,yCrop=0.85,xCrop=3, mm=2):
  h,w = img.shape[:2]
  y = int(round(yCrop*h))
  cropped = crop(img,0,y,w//xCrop,h-y)
  scale_gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
# adjust the second value of the next line to tune the detection
  ret, thresh = cv2.threshold(scale_gray, 210, 255, cv2.THRESH_BINARY)
  contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# filter noisy detection
  contours = [c for c in contours if cv2.contourArea(c) > 100]
# sort from by (y, x)
  contours.sort(key=lambda c: (cv2.boundingRect(c)[1], cv2.boundingRect(c)[0]))
# work on the segment
  #cv2.rectangle(cropped, cv2.boundingRect(contours[-1]), (0,255,0), 2)
  x_,y_,w_,h_ = cv2.boundingRect(contours[-1])
  return w/(new_width*w_/mm)

def calc_diameter(preds, k):
  A = preds.sum()*(k**2)  #preds_prob.sum()i da dene
  return 2*math.sqrt(A/np.pi)

def exportCSV(result_dict,folder,filename):#json lamak daha iyi gibi
  #dirrek csv dict de fena olmaz
  df = pd.DataFrame(data=result_dict)
  path = os.path.join(folder, filename + '_' + str(date.today()) + ".csv")
  df.to_csv(path, index=False)
  return path

