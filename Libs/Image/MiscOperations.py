import numpy as np
import scipy.ndimage

def NormalizeFor8Bit(img):
  minimum = np.amin(img)
  img = img - minimum

  max = np.amax(img)
  
  if max == 0:
    return img

  factor = 255 / max
  return img * factor

def GetBoundingBox2d(image):
  (height, width) = image.shape
  
  yGrid, xGrid = np.mgrid[:height,:width]

  binaryImage = np.where(image > 0, 1, 0)

  yGridMasked = np.where(binaryImage == 1, yGrid, np.nan)
  xGridMasked = np.where(binaryImage == 1, xGrid, np.nan)

  yMin = int(np.nanmin(yGridMasked))
  yMax = int(np.nanmax(yGridMasked))
  
  xMin = int(np.nanmin(xGridMasked))
  xMax = int(np.nanmax(xGridMasked))

  return ((xMin, xMax), (yMin, yMax))

def pad(array, reference_shape, offsets): # TODO: Capital letter
  # Create an array of zeros with the reference shape
  result = np.zeros(reference_shape)
  # Create a list of slices from offset to offset + shape in each dimension
  insertHere = [slice(offsets[dim], offsets[dim] + array.shape[dim]) for dim in range(array.ndim)]
  # Insert the array in the result at the specified offsets
  result[insertHere] = array
  return result

def CropToBoundingBox(img):
  ((xMin, xMax), (yMin, yMax)) = GetBoundingBox2d(img)
  return img[yMin:yMax, xMin:xMax]

def ScaleToSize(img, height, width, depth):
  
  if img.shape[0] == 0 or img.shape[1] == 0:
    return np.zeros(shape=(height, width))

  yScaleRatio = height / img.shape[0]
  xScaleRatio = width / img.shape[1]
  
  maxDepth = np.amax(img) 
  zeroExcludedImage = np.where(img == 0, np.nan, img)
  minDepth = np.nanmin(zeroExcludedImage)
  zeroExcludedImage = np.where(np.isnan(zeroExcludedImage), minDepth - 1, zeroExcludedImage)
  img = zeroExcludedImage - (minDepth - 1)
  maxDepth -= minDepth
  minDepth = 0
  depthRange = maxDepth - minDepth
  zScaleRatio = depth / depthRange

  scaleFactor = min(yScaleRatio, xScaleRatio, zScaleRatio)
  img = img * scaleFactor
  
  matrix2dScaled = scipy.ndimage.zoom(img, scaleFactor, order=0)

  matrix2dScaled = (matrix2dScaled * scaleFactor).astype(np.uint16)
  
  heightOffset = int((height - matrix2dScaled.shape[0]) / 2)
  widthOffset = int((width - matrix2dScaled.shape[1]) / 2)
  matrix2dPadded = pad(
    matrix2dScaled, 
    (height, width), 
    (heightOffset, widthOffset)
  ).astype(np.uint16)

  return matrix2dPadded