# Bangali Handwritten Character Recognition

## Overview
This project focuses on recognizing handwritten Bangla characters using a deep learning model. The model preprocesses images, augments data, and trains a Convolutional Neural Network (CNN) for classification.

## How To Run
### Clone the Repository:
bash
  git clone repo-url

### Features Extraction:
- Characters:
bash
  python characte.py

- Bounding Box:
bash
  python bounding_box.py

- Chain Code:
bash
  python chain_code.py

- Contour:
bash
  python contour.py

- Downsampling:
bash
  python downsampling.py

## Model Architecture
The model is a CNN with:
- 2 convolutional layers (filters: 60, kernel size: 5x5)
- 2 additional convolutional layers (filters: 30, kernel size: 3x3)
- Max pooling layers
- Dropout for regularization
- Fully connected layers
- Softmax activation for classification

## Training
- cnn.ipynb
- Trains for 50 epochs
- Saves the trained model as BanglaModel.h5

## Dependencies
- Python
- OpenCV
- NumPy
- Matplotlib
- Keras
- TensorFlow
