from Libs.IO.DataCapture.Operations.Average import Average
from Libs.IO.DataCapture.Operations.BackgroundFilter import BackgroundFilter
from Libs.IO.DataCapture.Operations.Capture import Capture
from Libs.IO.DataCapture.Operations.Crop import Crop
from Libs.IO.DataCapture.Operations.Display import Display
from Libs.IO.DataCapture.Operations.ExtractByContours import ExtractByContours
from Libs.IO.DataCapture.Operations.Filter import Filter
from Libs.IO.DataCapture.Operations.Histogram import Histogram
from Libs.IO.DataCapture.Operations.Normalize import Normalize
from Libs.IO.DataCapture.Operations.Predict import Predict
from Libs.IO.DataCapture.Operations.ShiftToCenter import ShiftToCenter
from Libs.IO.Input import TakeNumericInput
from Libs.IO.StructureCoreClient import StructureCoreClient
from Libs.Image.MiscOperations import GetBoundingBox2d

import cv2
import GlobalConfig
import math
import matplotlib.pyplot as plt
import numpy as np
import signal
import sys

class DataCapturer:

  def __init__(self):
    self.average = Average()
    self.backgroundFilter = BackgroundFilter()
    self.capture = Capture()
    self.crop = Crop()
    self.display = Display()
    self.extractByContours = ExtractByContours()
    self.filter = Filter()
    self.histogram = Histogram()
    self.normalize = Normalize()
    self.predict = Predict()
    self.shiftToCenter = ShiftToCenter()
    
    self.client = None
    self.exit = False

  def Acquire(self):
    img = self.client.ReadImage();  
    img = self.crop(img)

    img_original = img[:]
    img_with_background = img[:]

    img = self.backgroundFilter(img)
    img = self.filter(img)
    self.histogram(img_original, img if BackgroundFilter.apply else None)
    return (img, img_original, img_with_background)

  def Capture(self):  
    self.client = StructureCoreClient(
      pipe_name=GlobalConfig.pipe_name,
      width=GlobalConfig.Img.width,
      height=GlobalConfig.Img.height,
      bytes_per_pixel=GlobalConfig.Img.bytes_per_pixel  
    )
    self.client.Connect()

    kbh = GlobalConfig.Defaults.KeyboardHelper()
    def setExit():
      self.exit = True
    kbh.OnRelease(GlobalConfig.ShortKeys.Quit, setExit)
    
    histo_img = None
    while True:
      if self.exit:
        break

      img = None
      img_with_background = None
      img_original = None
      while img is None:
        if self.exit:
          break
        (img, img_original, img_with_background) = self.Acquire()
        img = self.average(img)

      if self.exit:
        return

      img_before_normalizing = img[:]

      img = self.shiftToCenter(img)
      (img, img_original) = self.normalize(img, img_original)

      self.capture(img_before_normalizing, img, img_with_background)
      
      img_original = cv2.cvtColor(img_original.astype(np.uint8), cv2.COLOR_GRAY2RGB)
      if Predict.apply: # TODO: This if should not be here
        imgs = self.extractByContours(img_before_normalizing)
        for imgToPredict in imgs:
          boundingBox = GetBoundingBox2d(imgToPredict)
          imgToPredict = self.shiftToCenter(imgToPredict)
          img_original = self.predict(imgToPredict, boundingBox, img_original)

      self.display(img.astype(np.uint8), img_original)      
    
    self.client.Disconnect()