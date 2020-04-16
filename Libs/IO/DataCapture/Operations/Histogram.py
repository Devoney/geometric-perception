import cv2
import GlobalConfig
import matplotlib.pyplot as plt
import numpy as np

class Histogram:
  fig = None

  def _toggle(self):
    GlobalConfig.histogram_mode = GlobalConfig.histogram_mode + 1
    if GlobalConfig.histogram_mode > 2:
      GlobalConfig.histogram_mode = 0
    GlobalConfig.histogram_mode = GlobalConfig.histogram_mode
    if GlobalConfig.histogram_mode > 0:
      print('Showing histogram type ' + str(GlobalConfig.histogram_mode))

  def __call__(self, img_with_background, img_no_background):
    if GlobalConfig.histogram_mode == 0:
      return

    img_to_show = img_with_background
    if GlobalConfig.histogram_mode == 2 and not img_no_background is None:
      img_to_show = img_no_background

    self._showHistogram(img_to_show)

  # TODO: This method does not belong here, move to a Libs class of some sort
  def _showHistogram(self, histo_img):
    if self.fig is None:
      self.fig = plt.figure()

    fig = self.fig
    fig.add_subplot(111)
    # Divides by 10 to show cm instead of mm in a range of 5cm to 250cm
    n, bins, patches = plt.hist(
      (histo_img.flatten() / 10),
      64,
      density=False,
      range=(1,250),
      facecolor='g',
      alpha=0.75
    )
    plt.xlabel('Value')
    plt.ylabel('Number')
    plt.title('Histogram')
    plt.xlim(1, 250)
    plt.grid(True)
    plt.autoscale(enable=True, axis='y', tight=None)
    fig.canvas.draw()
    data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    plt.clf()

    cv2.imshow('Histogram', data)