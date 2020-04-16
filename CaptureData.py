# TODO: use a central store, like GlobalConfig, instead of accessing all these modules directly.
from Libs.IO.DataCapture.DataCapturer import DataCapturer
from Libs.IO.DataCapture.Operations.Average import Average
from Libs.IO.DataCapture.Operations.BackgroundFilter import BackgroundFilter
from Libs.IO.DataCapture.Operations.Capture import Capture
from Libs.IO.DataCapture.Operations.Crop import Crop
from Libs.IO.DataCapture.Operations.ExtractByContours import ExtractByContours
from Libs.IO.DataCapture.Operations.Filter import Filter
from Libs.IO.DataCapture.Operations.Histogram import Histogram
from Libs.IO.DataCapture.Operations.Predict import Predict
from Libs.IO.DataCapture.Operations.ShiftToCenter import ShiftToCenter
import GlobalConfig
import math
import pygubu
import threading
import tkinter as tk
from tkinter import *

builder = pygubu.Builder()
builder.add_from_file('./GUI.ui') # TODO: SHould not be defined here
mainwindow = builder.get_object('tlMain')

builder.tkvariables.__getitem__('crop').set(GlobalConfig.Defaults.crop)

def on_medianFilter_toggle():
  Filter.filter_mode = 1 if builder.tkvariables.__getitem__('medianFilter').get() else 0

def on_crop_toggle():
  Crop.apply = builder.tkvariables.__getitem__('crop').get()

def on_center_toggle():
  ShiftToCenter.apply = builder.tkvariables.__getitem__('shiftToCenter').get()

def on_recordBackground_toggle():
  recordBackground = builder.tkvariables.__getitem__('recordBackground').get()
  BackgroundFilter.recording = recordBackground
  if not BackgroundFilter.recording:
    BackgroundFilter.apply = True
  else:
    BackgroundFilter.apply = False

def on_average_changed(value):
  avg = math.ceil(float(value))
  Average.Set(avg)

def on_predict_toggle():
  predict = builder.tkvariables.__getitem__('predict').get() # TODO: Refactor this to a single method isntead of going into tkvariables everywhere
  Predict.apply = predict

def on_areaSizeCutOff_changed(value):
  ExtractByContours.area_size_cut_off = float(value)

def on_capture_click():
  entry = builder.get_object('tbxSubject')
  subject = entry.get()
  Capture.SetSubject(subject)
  Capture.capture = True

def on_backgroundMargin_changed(*args):
  entry = builder.get_object('tbxBackgroundMargin')
  background_margin = entry.get()
  if background_margin != '':
    GlobalConfig.background_margin = float(background_margin)

svBackgroundMargin = builder.tkvariables.__getitem__('svBackgroundMargin')
svBackgroundMargin.trace("w", on_backgroundMargin_changed)

def on_medianFilterKernelSize_changed(*args):
  entry = builder.get_object('tbxMedialFilterKernelSize')
  medianSize = entry.get()
  if medianSize != '':
    GlobalConfig.Filtering.median_size = int(medianSize)

svMedianFilterKernelSize = builder.tkvariables.__getitem__('svMedianFilterKernelSize')
svMedianFilterKernelSize.trace('w', on_medianFilterKernelSize_changed)

svHistogram = builder.tkvariables.__getitem__('svHistogram')
svHistogram.set('None')
def on_histogram_changed(*args):
  mode = 0
  histogramValue = svHistogram.get()
  if histogramValue == 'Original':
    mode = 1
  elif histogramValue == 'Processed':
    mode = 2
  GlobalConfig.histogram_mode = mode
  print('Histogram set to ' + histogramValue)

svHistogram.trace('w', on_histogram_changed)

callbacks = {
  'on_areaSizeCutOff_changed': on_areaSizeCutOff_changed,
  'on_average_changed': on_average_changed,
  'on_capture_click': on_capture_click,
  'on_crop_toggle': on_crop_toggle,
  'on_center_toggle': on_center_toggle,
  'on_medianFilter_toggle': on_medianFilter_toggle, 
  'on_predict_toggle': on_predict_toggle,
  'on_recordBackground_toggle': on_recordBackground_toggle
}

builder.connect_callbacks(callbacks)

def start():
  dataCapturer = DataCapturer()
  dataCapturer.Capture()
threading.Thread(target=start).start()

mainwindow.mainloop()