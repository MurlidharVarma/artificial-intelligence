# Traffic
An AI to identify which traffic sign appears in a photograph
```
$ python traffic.py gtsrb
Epoch 1/10
500/500 [==============================] - 5s 9ms/step - loss: 3.7139 - accuracy: 0.1545
Epoch 2/10
500/500 [==============================] - 6s 11ms/step - loss: 2.0086 - accuracy: 0.4082
Epoch 3/10
500/500 [==============================] - 6s 12ms/step - loss: 1.3055 - accuracy: 0.5917
Epoch 4/10
500/500 [==============================] - 5s 11ms/step - loss: 0.9181 - accuracy: 0.7171
Epoch 5/10
500/500 [==============================] - 7s 13ms/step - loss: 0.6560 - accuracy: 0.7974
Epoch 6/10
500/500 [==============================] - 9s 18ms/step - loss: 0.5078 - accuracy: 0.8470
Epoch 7/10
500/500 [==============================] - 9s 18ms/step - loss: 0.4216 - accuracy: 0.8754
Epoch 8/10
500/500 [==============================] - 10s 20ms/step - loss: 0.3526 - accuracy: 0.8946
Epoch 9/10
500/500 [==============================] - 10s 21ms/step - loss: 0.3016 - accuracy: 0.9086
Epoch 10/10
500/500 [==============================] - 10s 20ms/step - loss: 0.2497 - accuracy: 0.9256
333/333 - 5s - loss: 0.1616 - accuracy: 0.9535
```
## Screencast
[![Project 5: Traffic](https://img.youtube.com/vi/VN7Di-Wdig0/0.jpg)](https://youtu.be/VN7Di-Wdig0)

## Background
As research continues in the development of self-driving cars, one of the key challenges is computer vision, allowing these cars to develop an understanding of their environment from digital images. In particular, this involves the ability to recognize and distinguish road signs – stop signs, speed limit signs, yield signs, and more.

This project uses TensorFlow to build a neural network to classify road signs based on an image of those signs. To do so, we used a labeled dataset: a collection of images that have already been categorized by the road sign represented in them.

Several such data sets exist, but for this project, we have used the [German Traffic Sign Recognition Benchmark (GTSRB)](http://benchmark.ini.rub.de/?section=gtsrb&subsection=news) dataset, which contains thousands of images of 43 different kinds of road signs.

## Understanding
In the data set (gtsrb directory), there are 43 subdirectories, numbered 0 through 42. Each numbered subdirectory represents a different category (a different type of road sign). Within each traffic sign’s directory is a collection of images of that type of traffic sign.

In `traffic.py`, the main function, accepts as command-line arguments a directory containing the data and (optionally) a filename to which to save the trained model. The data and corresponding labels are then loaded from the data directory (via the `load_data` function) and split into training and testing sets. After that, the `get_model` function is called to obtain a compiled neural network that is then fitted on the training data. The model is then evaluated on the testing data. Finally, if a model filename was provided, the trained model is saved to disk.

The `load_data` function accepts as an argument `data_dir`, representing the path to a directory where the data is stored, and return image arrays and labels for each image in the data set.

The `get_model` function returns a compiled neural network model.

## My Experimentation Process
1. For Traffic sign image classification, a highlevel model creation approach taken was to feed the input (of fixed size) to convolution layer for feature extraction, then to Max Pooling layer for size reduction, followed by Flattening and feeding to Dense (fully connected) layers, and then finally to output layer (based on unique category size)
1. Tried different kernel sizes (3x3, 5x5, 7x7, 9x9, 11x11) on convolution layer, and observed that smaller the kernel size more accurately it was able to extract features from the image. Accuracy was fairly higher around 3x3 and 5x5; 3x3 had minimal loss. 
1. Adding addition convolution and max pooling layer, got me better results. The second convolution layer had increased filters.
1. Tried with different filter counts (2, 4, 8, 16, 32, 64) on convolution layer, and observed that greater the filter count, more was the accuracy with less loss. 
1. Experimented with different Max Pooling size (10x10, 8x8, 6x6, 4x4, 2x2), and observed that lower the max pool size better were the results with accuracy and losses.
1. Dropout technique is used to prevent over-fitting. Observed results with different dropout percentages, and found that results were fairly stable between drop-out percentage of 20 to 30