from Libs.Image.MiscOperations import CropToBoundingBox, ScaleToSize
from Libs.Image.ShiftToCenter import ShiftToCenter2d
from PIL import Image
from scipy.ndimage import gaussian_filter, median_filter
import cv2
import GlobalConfig
import Libs.DataHelper as DataHelper
import math
import matplotlib.pyplot as plt
import numpy as np

def ConvertToNetworkInput(dataset):
  nr_of_imgs = 0
  for data in dataset:
    nr_of_imgs += len(data[1])

  first_img = dataset[0][1][0]
  (width, height) = DataHelper.GetWidthHeight(first_img)
  channels = 1

  input_data = np.zeros(shape=(nr_of_imgs, GlobalConfig.TargetImg.width, GlobalConfig.TargetImg.height))
  nr_distinct_labels = len(dataset)
  labels = np.zeros(shape=(nr_of_imgs, nr_distinct_labels)).astype(int)

  label_counter = 0
  for i in range(nr_distinct_labels):
    (label, depth_frames) = dataset[i]
    for depth_frame in depth_frames:
      # plt.imshow(depth_frame)
      # plt.show()
      # src = depth_frame[..., np.newaxis] # Add additional dimension for channels, as Conv2D expects 4D input
      src = depth_frame

      (height, width) = src.shape
      if height != GlobalConfig.TargetImg.height or width != GlobalConfig.TargetImg.width:
        src = CropToBoundingBox(src)

        src = ScaleToSize(
          src,
          GlobalConfig.TargetImg.height,
          GlobalConfig.TargetImg.width,
          GlobalConfig.TargetImg.depth
        )

      np.copyto(dst=input_data[label_counter], src=src)
      bit_index = label[0]
      labels[label_counter][bit_index] = 1
      label_counter += 1

  # Now convert to 8-bit gray scale otherwise the ImageDataGenerator does not now
  # how to handle this
  rgb_input_data = None
  for i in range(len(input_data)):
    img = ConvertImg(input_data[i])
    if rgb_input_data is None:
      (height, width, channels) = img.shape
      rgb_input_data = np.zeros(shape=(nr_of_imgs, height, width, channels))
    rgb_input_data[i] = img

  # Shows the images loaded
  if False:
    for i in range(len(input_data)):
      plt.imshow(rgb_input_data[i])
      plt.show()

  return (rgb_input_data, labels)  

def ConvertImg(img):
  img = (img).astype(np.uint8)
  img = Image.fromarray(img)
  
  if GlobalConfig.resize_factor != 1:
    new_width = int(img.width * GlobalConfig.resize_factor)
    new_height = int(img.height * GlobalConfig.resize_factor)
    img = img.resize((new_width, new_height))

  img = img.convert('RGB')

  return np.array(img)