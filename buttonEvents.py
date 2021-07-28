import cv2
from datetime import date
import os
import numpy as np
import utils
#from keras.models import load_model
from tensorflow.keras import models
import webbrowser
import pandas as pd
import PySimpleGUI as sg

IMG_HEIGHT = 128
IMG_WIDTH = 128
model = models.load_model('./models/unet.h5',compile=False)
via_path = "./via.html"


def predict(folder):
    coordinates = {'filename':[],'file_size':[],'file_attributes':[],'region_count':[],'region_id':[],'region_shape_attributes':[],'region_attributes':[]}
    for basename in os.listdir(folder):
        if basename.endswith('.png') or basename.endswith('.jpg') or basename.endswith('.tif'):
            path_to_image = os.path.join(folder,basename)
            img = cv2.imread(path_to_image)
            original_height = img.shape[1]
            _x,_diff2,img = utils.preprocess(img)
            size = img.shape
            img = cv2.resize(img, (IMG_HEIGHT, IMG_WIDTH), interpolation = cv2.INTER_AREA) 
            inp = img.reshape((-1, IMG_HEIGHT, IMG_WIDTH, 3))
            preds_prob = model.predict(inp, verbose=1)
            preds = (preds_prob > 0.95).astype(np.uint8)
            mask = np.squeeze(preds) * 255
            mask = cv2.resize(mask, (size[0],size[1]), interpolation = cv2.INTER_AREA) 
            mask = utils.crop(mask,0,_diff2,original_height,mask.shape[0]-_diff2*2)
            mask = cv2.copyMakeBorder(mask, 0, 0, _x,_x, cv2.BORDER_CONSTANT, value=[0,0,0])
            edged = cv2.Canny(mask, 30, 200) 
            cv2.waitKey(0) 
            contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1) 
            polygon = {"name":"polygon","all_points_x":[],"all_points_y":[]} 
            for point in np.squeeze(contours):
                polygon["all_points_x"].append(point[0])
                polygon["all_points_y"].append(point[1])
            coordinates["filename"].append(str(path_to_image)) #this might cause trouble check the path in csv file
            coordinates["file_size"].append(0)
            coordinates["file_attributes"].append("{}")
            coordinates["region_count"].append(1)
            coordinates["region_id"].append(0)
            coordinates["region_shape_attributes"].append(str(polygon).replace("'",'"'))
            coordinates["region_attributes"].append("{}")
        else:
            break
    return utils.exportCSV(coordinates,folder,"Predictions")

def openVIA():
    webbrowser.open(os.path.realpath(via_path))
    
def my_popup(window):
    layout = [
        [sg.Text("Do you want to open the VGG Image Annotator to check the predictions?")],
        [sg.Button("YES"), sg.Button("NO")]
    ]
    win = sg.Window("Ueberpruefung", layout, modal=True,
        grab_anywhere=True, enable_close_attempted_event=True,element_justification='center')
    event, value = win.read()
    if event == "YES":
        openVIA()
        sg.WINDOW_CLOSE_ATTEMPTED_EVENT
    elif event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT:
        event = "NO"
    win.close()
    
def sendToDB(IMG_ORDNER,annotations):
  diameter = {'Filename':[],'Diameter[mm]':[],'Date':[]}
  images = {}
  for basename in os.listdir(IMG_ORDNER):
    if basename.endswith('.png') or basename.endswith('.jpg') or basename.endswith('.tif'):
      images[basename] = cv2.imread(os.path.join(IMG_ORDNER,basename))
  #img_size = (1598,1598,3)
  df = pd.read_csv(annotations)
  filenames = df.filename.unique()

  for filename in filenames:      
      temp_df = df.loc[df['filename'] == filename]
      data = {}
      basename = os.path.basename(filename)
      
      for index, row in temp_df.iterrows():
          polygon_string = row["region_shape_attributes"]
          label_string = row["region_attributes"]
          xy_points_string = polygon_string[polygon_string.find('"all_points_x"'):polygon_string.find('}')]
          xy_points_string = xy_points_string.split('],')
          x_points = xy_points_string[0]
          ##print(x_points)
          x_points = x_points[x_points.find('[')+1:]
          y_points = xy_points_string[1]
          y_points = y_points[y_points.find('[')+1:y_points.find(']')]
          ##print(x_points)
          x_points_int = [int(x) for x in x_points.split(',')]
          y_points_int = [int(x) for x in y_points.split(',')]
          class_label = str(index) #label_string.split(':')[1][1:-2]
          #print(x_points_int,y_points_int,class_label)
          xy_pairs = []
          for xy in zip(x_points_int,y_points_int):
              xy_pairs.append(xy)
          #print(xy_pairs)
          if class_label not in data:
              data[class_label] = []
          data[class_label].append(xy_pairs)  
      h,w = images[basename].shape[:2]
      mask = np.zeros((h, w, 1))
      index = -1
      for key in data.keys():
          index += 1
          list_of_points = data[key]
          for points in list_of_points:
              pts = np.array(points)
              cv2.fillPoly(mask, [pts], 255)
      mask = (mask >= 255).astype(np.uint8)
      k = utils.getPixelLength(images[basename], new_width=w)
      diameter["Filename"].append(basename) #for diameter calculation
      diameter["Diameter[mm]"].append(utils.calc_diameter(mask,k)) 
      diameter["Date"].append(str(date.today()))

      mask = mask * 255
      edged = cv2.Canny(mask, 30, 200) 
      cv2.waitKey(0) 
      contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
      cv2.drawContours(images[basename], contours, -1, (0, 255, 0), 2) 
      cv2.imwrite(""+ IMG_ORDNER + '/' + "DRW_" + basename, images[basename])

      cv2.imwrite(""+ IMG_ORDNER + '/' + "Mask_" + basename, mask)
      
      df = df[df['filename']!=filename]

  return utils.exportCSV(diameter,IMG_ORDNER,"Database")
