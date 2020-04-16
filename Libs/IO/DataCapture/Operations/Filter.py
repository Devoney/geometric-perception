from scipy.ndimage import gaussian_filter, median_filter
import GlobalConfig

class Filter:
  filter_mode = 0

  def __call__(self, img):
    if Filter.filter_mode == 0:
      return img

    img = self._applyFilters(img)

    return img

  def _applyFilters(self, img):
    if Filter.filter_mode > 0:
      img = median_filter(img, GlobalConfig.Filtering.median_size)

    if Filter.filter_mode > 1:
      img = gaussian_filter(img, GlobalConfig.Filtering.gaussian_sigma)

    return img