# geometric-perception
Classifies objects based on their geometry using a 3D camera and [Tensorflow + Keras][2] and [OpenCV][1].

See a demonstration and explanation on how this all works on YouTube.

<a href="http://www.youtube.com/watch?feature=player_embedded&v=-wlFQKV2cHc
" target="_blank"><img src="https://raw.githubusercontent.com/Devoney/geometric-perception/master/Misc/YouTubeThumbnail.PNG" alt="IMAGE ALT TEXT HERE" width="480" height="270" border="4" /></a>


# How to start
- Clone this repository
- Find yourself a 3D camera. I've used a [Occipital Structure Core][3]. Or use [a virtual depth camera from Blender][7].
  - When using the Structure Core depth camera you should [download their SDK][4].
  - You can use [this C++ code to pipe the camera data][5] to python.
    - Adjust the pipe for your operation system, as Windows pipes are used here.
  - Or alternatively, on Windows, you can use [this executable][6].
- After having setup the named pipe to transfer the camera data it is time to start the python code to capture the camera data. Run [CaptureData.py][8]. Which will show you this GUI:

![Data Capture Control][DataCaptureControl]
- By now the named pipe should be connected and images should be streaming to the GUI.

# Capturing images
- First you will want to `Record background` for a few seconds. Then turn it off.
- Then put the object into the scene.
- `Apply median filter` to reduce noise.
- You can play with the number of frames to `Average` or the `Background margin` to reduce noise further.
- Next tick `Shift to center` which will shift and normalize the data. This shows you what data will go to the neural network.
- Using the Data Capture Control you can capture images using the `Capture` button.
- It will store data in the data folder.
- When you are pleased with the captures data you need to move the data manually into a sub folder of the `data` folder. Give this the label you want to use when training the network. Like `geometric-perception\data\cube\` for instance.

[1]: http://www.opencv.org
[2]: https://www.tensorflow.org/guide/keras
[3]: https://structure.io/structure-core
[4]: https://structure.io/developers
[5]: https://github.com/Devoney/geometric-perception/blob/master/Misc/SimpleStreamer.cpp
[6]: https://github.com/Devoney/geometric-perception/blob/master/Misc/SimpleStreamer.7z
[7]: https://github.com/Devoney/geometric-perception/blob/master/Misc/VirtualDepthCam.blend
[8]: https://github.com/Devoney/geometric-perception/blob/master/CaptureData.py

[DataCaptureControl]: https://raw.githubusercontent.com/Devoney/geometric-perception/master/Misc/ControlPanel.png
[YouTubeThumbnail]: https://raw.githubusercontent.com/Devoney/geometric-perception/master/Misc/YouTubeThumbnail.PNG
