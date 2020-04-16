import numpy as np
from scipy.ndimage.interpolation import shift

def ShiftToCenter2d(matrix):
  (height, width) = matrix.shape
  
  matrixHeightIndices, matrixWidthIndices = np.mgrid[0:height, 0:width]
  binaryMatrix = np.where(matrix > 0, 1, np.nan)
  
  widthResultMatrix = binaryMatrix * matrixWidthIndices
  heightResultMatrix = binaryMatrix * matrixHeightIndices
  
  centerWidthOfBlob = np.nanmean(widthResultMatrix)
  centerHeightOfBlob = np.nanmean(heightResultMatrix)
  
  centerWidthOfImage = (width - 1) / 2
  centerHeightOfImage = (height - 1) / 2

  toShiftHorizontally = centerWidthOfImage - centerWidthOfBlob
  toShiftVertically =  centerHeightOfImage - centerHeightOfBlob

  return shift(matrix, [toShiftVertically, toShiftHorizontally])