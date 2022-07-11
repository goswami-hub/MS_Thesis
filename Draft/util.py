
import os, sys, random
import xml.etree.ElementTree as ET
from glob import glob
import pandas as pd

def load_data(annotation_path):
  """
  Input parameters:
  annotation_path: Location of annotation file
  Output:
  A data frame of ground truth bounding box co-ordinates
  A list of ground truth bounding box co-ordinates
  """
  
  full_path= annotation_path + '/*.xml'
  annotations = glob(full_path)

  alldata = []
  cnt = 0
 
  for file in annotations:
    ID=int(file.split('/')[-1].split('_')[-1].split('.')[0])
    filename = file.split('\\')[-1]
    filename =filename.split('.')[0] + '.jpg'
    row = []
    parsedXML = ET.parse(file)
    for node in parsedXML.getroot().iter('object'):
      blood_cells = node.find('name').text
      xmin = int(node.find('bndbox/xmin').text)
      xmax = int(node.find('bndbox/xmax').text)
      ymin = int(node.find('bndbox/ymin').text)
      ymax = int(node.find('bndbox/ymax').text)

      row = [ID,filename, blood_cells, xmin, xmax, ymin, ymax]
      alldata.append(row)
      cnt += 1

  df = pd.DataFrame(alldata, columns=['ID','filename', 'cell_type', 'xmin', 'xmax', 'ymin', 'ymax'])
  df = df.sort_values(by=['ID'])
  return df, alldata


import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

def plot_annotation(img_path, img_ann):
  """
  Input
  img_path: Image path of input image
  img_ann: List of annotations for input image, each annotation is a 
              dictionary with xmin, ymin, xmax, ymax, cell_type
  Output
  Image with bounding boxes
  """

  im = Image.open(img_path)


  fig, ax = plt.subplots(figsize=(12,16))
  ax.imshow(im)

  for i in range(len(img_ann)):
    xmin = int(img_ann[i]['xmin'])
    ymin = int(img_ann[i]['ymin'])
    w = int(img_ann[i]['xmax']) - int(img_ann[i]['xmin'])
    h = int(img_ann[i]['ymax']) - int(img_ann[i]['ymin'])

    if img_ann[i]['cell_type']=='RBC':
      ax.annotate('RBC', xy=(xmin-40,ymin+20))
      rect = patches.Rectangle((xmin,ymin), w, h, linewidth=2, edgecolor='r', facecolor='none')
    elif img_ann[i]['cell_type']=='WBC':
      ax.annotate('WBC', xy=(xmin-40,ymin+20))
      rect = patches.Rectangle((xmin,ymin), w, h, linewidth=2, edgecolor='b', facecolor='none')
    else:
      ax.annotate('Platelets', xy=(xmin-40,ymin+20))
      rect = patches.Rectangle((xmin,ymin), w, h, linewidth=2, edgecolor='g', facecolor='none')
    ax.add_patch(rect)

  return  plt.show()