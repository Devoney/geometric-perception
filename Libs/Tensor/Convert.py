import numpy as np

def From2dDepthImageTo3dMatrix(img, range_min, range_max):
  height = np.size(img, 0)
  width = np.size(img, 1)
  
  depth = int(range_max - range_min)
  pointCloud = np.zeros(shape=(height, width, depth+2)) # Point cloud will be binary 0 and 1
  
  for r in range(height):
    for c in range(width):
      depthValue = img[r, c]
      if depthValue == 0: # No depth is measured at 0
        continue
      pointCloudIndex = int(round(depthValue - range_min))
      pointCloud[r, c, pointCloudIndex] = 1
  
  return pointCloud

def From3dMatrixToXyzArray(matrix):
  height, width, depth = matrix.shape
  nrOfElements = int(np.sum(matrix))
  arr = np.zeros(shape=(nrOfElements, 3))
  indexCounter = 0
  for r in range(height):
    for c in range(width):
      for d in range(depth):
        depthValue = matrix[r, c, d]
        if depthValue == 1:
          arr[indexCounter] = [r, c, d]
          indexCounter += 1

  return arr

  # Aankoop	Verkoop	Verschil	
  # 373,55	399,4	25,85	
  # 366,53	377,73	11,2	
  # 1085,5	1120	34,5	
  # 441,12	516,27	75,15	
  # 11550	11548,62	-1,38	
  # 1172,47	1184,02	11,55	
  # 1170	1189,2	19,2	
  #     176,07	Totaal
