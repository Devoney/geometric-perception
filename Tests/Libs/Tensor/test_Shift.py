import unittest
import os
import sys
import numpy as np

modulePath = os.getcwd() + '\\Libs\\Tensor\\'
sys.path.insert(0, modulePath)
from Shift import ShiftToCenter3d

class test_Shift(unittest.TestCase):
  def test_ShiftToCenter3d(self):
    # Given
    matrix = np.zeros(shape=(5,7,9))
    submatrix = np.ones(shape=(3,3,3))
    s0,s1,s2 = submatrix.shape
    matrix[0:s0, 0:s1, 0:s2] = submatrix

    expectedMatrix = np.zeros(shape=(5,7,9)).astype(np.int)
    t0, t1, t2 = (((np.array(matrix.shape) - 1) / 2)-1).astype(np.int)

    expectedMatrix[t0:t0+s0, t1:t1+s1, t2:t2+s2] = submatrix

    # When
    actualMatrix = ShiftToCenter3d(matrix)

    # Then
    truthMatrix = actualMatrix == expectedMatrix
    areEqual = np.alltrue(truthMatrix)
    self.assertTrue(areEqual, 'Actual matrix is not equivalent to expected matrix.')

if __name__ == "__main__":
  unittest.main()