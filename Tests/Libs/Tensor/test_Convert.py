import unittest
import os
import sys
import numpy as np

modulePath = os.getcwd() + '\\Libs\Tensor\\'
sys.path.insert(0, modulePath)
from Convert import From2dDepthImageTo3dMatrix

class test_Convert(unittest.TestCase):
  def test_From2dDepthImageTo3dMatrix(self):
    # Given
    img = np.matrix(
      '1 4 ;' +
      '2 3 ;' +
      '1 8  '
    )
    rangeMin = 1
    rangeMax = 12
    expectedDepthRange = rangeMax - rangeMin
    expectedMatrix = np.zeros(shape=(3, 2, expectedDepthRange))
    expectedMatrix[0, 0, 1 - rangeMin] = 1
    expectedMatrix[0, 1, 4 - rangeMin] = 1
    expectedMatrix[1, 0, 2 - rangeMin] = 1
    expectedMatrix[1, 1, 3 - rangeMin] = 1
    expectedMatrix[2, 0, 1 - rangeMin] = 1
    expectedMatrix[2, 1, 8 - rangeMin] = 1
    
    # When
    actualMatrix = From2dDepthImageTo3dMatrix(img, rangeMin, rangeMax)

    # Then
    truthMatrix = actualMatrix == expectedMatrix
    allTrue = np.alltrue(truthMatrix)
    self.assertTrue(allTrue, 'Actual and expected matrix do not equal')

if __name__ == '__main__':
  unittest.main()