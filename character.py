import os
import numpy as np
from PIL import Image, ImageDraw

def read_coordinates(file_path):
    coordinates = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                x, y, value = line.strip().split()
                x, y, value = float(x), float(y), int(value)
                if value == 1:
                    coordinates.append((x, y))
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return coordinates

def scale_coordinates(coordinates, img_size=(64, 64), padding=5):
    min_x, min_y = np.min(coordinates, axis=0)
    max_x, max_y = np.max(coordinates, axis=0)

    scale_x = (img_size[0] - 1 - 2 * padding) / (max_x - min_x) if max_x - min_x > 0 else 1
    scale_y = (img_size[1] - 1 - 2 * padding) / (max_y - min_y) if max_y - min_y > 0 else 1

    scaled_coordinates = [
        (int((x - min_x) * scale_x) + padding, int((y - min_y) * scale_y) + padding)
        for x, y in coordinates
    ]
    return scaled_coordinates

def create_image_from_coordinates(coordinates, img_size=(64, 64), stroke_size=2):
    img = Image.new("L", img_size, color=255)
    draw = ImageDraw.Draw(img)
    
    for x, y in coordinates:
        draw.ellipse((x - stroke_size, y - stroke_size, x + stroke_size, y + stroke_size), fill=0)
    
    return img

def save_image(img, output_path):
    img.save(output_path)

def process_folder(input_folder, output_folder, img_size=(64, 64), stroke_size=2, padding=5):
    for subfolder in os.listdir(input_folder):
        input_subfolder = os.path.join(input_folder, subfolder)
        output_subfolder = os.path.join(output_folder, subfolder)
        
        if not os.path.exists(output_subfolder):
            os.makedirs(output_subfolder)
        
        file_count = 0
        for file_name in os.listdir(input_subfolder):
            if file_name.endswith('.txt'):
                file_path = os.path.join(input_subfolder, file_name)
                coordinates = read_coordinates(file_path)
                
                if not coordinates:
                    print(f"Skipping file {file_path} due to missing coordinates.")
                    continue
                
                scaled_coordinates = scale_coordinates(coordinates, img_size, padding)
                    
                img = create_image_from_coordinates(scaled_coordinates, img_size, stroke_size)
                    
                output_path = os.path.join(output_subfolder, f"{file_count}.png")
                save_image(img, output_path)
                file_count += 1

def main():
    input_folder = 'dataset_normalized'
    output_folder = 'character'
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    process_folder(input_folder, output_folder)

if __name__ == "__main__":
    main()
