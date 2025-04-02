# Bangla Character Recognition

## Project Overview
This project focuses on recognizing handwritten Bangla characters using a deep learning model. The model preprocesses images, augments data, and trains a Convolutional Neural Network (CNN) for classification.

## Dataset Preparation
- The dataset is stored in the `dataset_normalized` folder.
- The script renames subfolders in the dataset for better organization.
- Images are resized to (32,32,3) dimensions.

## Preprocessing
- Converts images to grayscale.
- Applies thresholding and histogram equalization.
- Normalizes pixel values between 0 and 1.

## Data Augmentation
- Uses `ImageDataGenerator` to apply:
  - Width and height shifts
  - Zooming
  - Shearing
  - Rotation

## Model Architecture
The model is a CNN with:
- 2 convolutional layers (filters: 60, kernel size: 5x5)
- 2 additional convolutional layers (filters: 30, kernel size: 3x3)
- Max pooling layers
- Dropout for regularization
- Fully connected layers
- Softmax activation for classification

## Training
- Uses categorical cross-entropy loss.
- Optimized using Adam.
- Trains for 50 epochs with batch size 50.
- Saves the trained model as `BanglaModel.h5`.

## Dependencies
- Python
- OpenCV
- NumPy
- Matplotlib
- Keras
- TensorFlow

## How to Run
1. Ensure all dependencies are installed.
2. Place dataset in the `character` folder.
3. Run the script to train the model.
4. The trained model will be saved as `BanglaModel.h5` for future use.

