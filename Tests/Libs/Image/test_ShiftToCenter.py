import unittest
import os
import sys
import numpy as np

modulePath =os.getcwd() + '\\Libs\Image\\'
sys.path.insert(0, modulePath)
from ShiftToCenter import ShiftToCenter2d

class test_ShiftToCenter(unittest.TestCase):
  def test_ImageIsCentered(self):
    # Given
    matrix = np.matrix(
      '0 0 0 0 0 0 0;' +
      '0 0 0 0 0 0 0;' +
      '1 1 1 0 0 0 0;' +
      '1 1 1 0 0 0 0;' +
      '1 1 1 0 0 0 0'
    )
    
    expectedMatrix = np.matrix(
      '0 0 0 0 0 0 0;' +
      '0 0 1 1 1 0 0;' +
      '0 0 1 1 1 0 0;' +
      '0 0 1 1 1 0 0;' +
      '0 0 0 0 0 0 0'
    )

    # When
    actualMatrix = ShiftToCenter2d(matrix)
    
    # Then
    truthMatrix = actualMatrix == expectedMatrix
    matricesAreEqual = np.all(truthMatrix)
    self.assertTrue(matricesAreEqual, 'Image was not shifted correctly to the center')

if __name__ == '__main__':
  unittest.main()