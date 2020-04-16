import cv2
import numpy as np
from Libs.Image.MiscOperations import pad
import scipy

class Display:
  
  def __init__(self):
    self.kernel = np.ones((3,3),np.uint8)

  def __call__(self, img, img_original):

    if img.shape[0] != img_original.shape[0] or img.shape[1] != img_original.shape[1]:
      heightRatio = img_original.shape[0] / img.shape[0]
      widthRatio = img_original.shape[1] / img.shape[1]
      smallestRatio = min(heightRatio, widthRatio)
      img = scipy.ndimage.zoom(img, smallestRatio, order=0).astype(np.uint8)

    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    img_to_show = self._concat(img_original, img)
    cv2.imshow('Left: Original   Right: Processed', img_to_show)
    cv2.waitKey(1)

  def _concat(self, imgL, imgR):
    return np.concatenate([imgL, imgR], axis=1)