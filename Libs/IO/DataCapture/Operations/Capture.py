from Libs.Image.MiscOperations import NormalizeFor8Bit
from numpy import save as np_save
import cv2
import GlobalConfig

class Capture:
  capture = False
  subject = GlobalConfig.Defaults.capture_subject
  subject_counter = 0

  def SetSubject(newSubject):
    if newSubject == Capture.subject:
      return
    Capture.subject_counter = 0
    Capture.subject = newSubject

  def __call__(self, img_processed, img_normalized, img_with_background=None):
    if not Capture.capture:
      return
    Capture.capture = False

    # When files are listed they will be sorted by subject, then capture number, then capture type
    filename_basis = GlobalConfig.Paths.data_dir + Capture.subject + '_' + str(Capture.subject_counter).zfill(4)

    np_save(filename_basis + '_depth.npy', img_processed)
    cv2.imwrite(filename_basis + '_depth_normalized.png', img_normalized)

    if not img_with_background is None:
      np_save(filename_basis + '_depth_withbg.npy', img_with_background)
      img_with_background = NormalizeFor8Bit(img_with_background)
      cv2.imwrite(filename_basis + '_depth_withbg.png', img_with_background)

    Capture.subject_counter += 1
    print('Captured "' + filename_basis + '"')
