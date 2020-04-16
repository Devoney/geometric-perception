import numpy as np
from scipy.ndimage.interpolation import shift

def ShiftToCenter3d(matrix, x=True, y=True, z=True):
  (height, width, depth) = matrix.shape
  
  heightGrid, widthGrid, depthGrid = np.mgrid[0:height, 0:width, 0:depth]
  binaryMatrix = np.where(matrix > 0, 1, np.nan)
  
  toShiftVertically = 0
  toShiftHorizontally = 0
  toShiftDepth = 0

  if y:
    heightResultMatrix = binaryMatrix * heightGrid
    centerHeightOfBlob = np.nanmean(heightResultMatrix)
    centerHeightOfImage = (height - 1) / 2
    toShiftVertically =  centerHeightOfImage - centerHeightOfBlob
  if x:
    widthResultMatrix = binaryMatrix * widthGrid
    centerWidthOfBlob = np.nanmean(widthResultMatrix)
    centerWidthOfImage = (width - 1) / 2
    toShiftHorizontally = centerWidthOfImage - centerWidthOfBlob
  if z:
    depthResultMatrix = binaryMatrix * depthGrid
    centerDepthOfBlob = np.nanmean(depthResultMatrix)
    centerDepthOfImage = (depth - 1) / 2
    toShiftDepth = centerDepthOfImage - centerDepthOfBlob

  shiftedMatrix = shift(matrix, [toShiftVertically, toShiftHorizontally, toShiftDepth])
  shiftedMatrix = np.round(shiftedMatrix)
  return shiftedMatrix.astype(np.int)