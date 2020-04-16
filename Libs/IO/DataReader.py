import os
from PIL import ImageOps, Image
import numpy as np
from numpy import load as np_load
import Libs.DataHelper as DataHelper

left = 300
right = 1280 - left
upper = 40
lower = 960 - upper

width_unit = 17
height_unit = 22
unit_scale = 4
r_width = width_unit * unit_scale
r_height = height_unit * unit_scale

def ReadData(data_dir):
  labelfolders = [f for f in os.scandir(data_dir) if f.is_dir()]
  
  counter = -1
  dataset = []
  img_counter = 0
  for labelfolder in labelfolders:
    counter += 1
    label = (counter, labelfolder.name)
    
    files = [f.path for f in os.scandir(labelfolder.path) if not f.is_dir() and f.name.endswith('depth.npy')]
    depth_frames = []
    for f in files:
      depth_frame = np_load(f).astype(np.float)
      depth_frames.append(depth_frame)
      img_counter += 1
    
    dataset.append((label, depth_frames))

  t_min, t_max = DetermineMinMaxDistance(dataset)
  print('Range in data: min=' + str(t_min) + "mm max=" + str(t_max) + "mm")

  return (img_counter, dataset)

def DetermineMinMaxDistance(datasets):
  t_min = 65535.
  t_max = 0.

  for dataset in datasets:
    (label, depth_frames) = dataset
    for depth_frame in depth_frames:
      # Filter out 0 value is this means undetermined distance really
      depth_frame_nan = np.where(depth_frame == 0, np.nan, depth_frame)
      frame_min = np.nanmin(depth_frame_nan)
      t_min = min(frame_min, t_min)
      frame_max = np.amax(depth_frame)
      t_max = max(frame_max, t_max)
  
  return (t_min, t_max)