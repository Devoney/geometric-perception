import numpy as np
import cv2

class ExtractByContours:
  area_size_cut_off = 50

  def __init__(self):
    self.color = (255)
    self.kernel = np.full(shape=(3,3), fill_value=255).astype(np.uint8)

  def __call__(self, img):
    imgs = []
    
    img8Bit = (img * (255 / np.amax(img))).astype(np.uint8)
    img8Bit = cv2.morphologyEx(img8Bit, cv2.MORPH_CLOSE, self.kernel)
    img8Bit = cv2.morphologyEx(img8Bit, cv2.MORPH_OPEN, self.kernel)
    contours, hierarchy = cv2.findContours(img8Bit, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    if len(contours) > 8:  # TODO: Arbritrary number here.
      imgs.append(img)
      return imgs # Too many objects to predict
    
    for contourIndex in range(len(contours)):
      contourArea = cv2.contourArea(contours[contourIndex])
      if contourArea < ExtractByContours.area_size_cut_off:
        continue
      contourMask = np.zeros(img.shape)
      cv2.drawContours(contourMask, contours, contourIndex, self.color, cv2.FILLED)
      
      debugContours = False
      # debugContours = True
      if debugContours:
        contourShape = np.zeros(img.shape)
        cv2.drawContours(contourShape, contours, contourIndex, self.color)
        cv2.imshow('contour shape ' + str(contourIndex), contourShape)
      
      newImg = np.where(contourMask == 255, img, 0)
      imgs.append(newImg)

    return imgs
