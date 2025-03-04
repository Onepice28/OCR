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

def get_bounding_box(coordinates):
    min_x = min(coordinates, key=lambda x: x[0])[0]
    max_x = max(coordinates, key=lambda x: x[0])[0]
    min_y = min(coordinates, key=lambda x: x[1])[1]
    max_y = max(coordinates, key=lambda x: x[1])[1]
    
    return min_x, min_y, max_x, max_y

def create_image_with_bounding_box(coordinates, img_size=(64, 64), padding=5):
    img = Image.new("L", img_size, color=255)
    draw = ImageDraw.Draw(img)
    
    if len(coordinates) == 0:
        return img

    min_x, min_y, max_x, max_y = get_bounding_box(coordinates)
    
    if max_x == min_x or max_y == min_y:
        return img
    
    scale_x = (img_size[0] - 2 * padding) / (max_x - min_x) if max_x - min_x > 0 else 1
    scale_y = (img_size[1] - 2 * padding) / (max_y - min_y) if max_y - min_y > 0 else 1
    
    scaled_coordinates = [
        (int((x - min_x) * scale_x) + padding, int((y - min_y) * scale_y) + padding)
        for x, y in coordinates
    ]
    
    left = min(scaled_coordinates, key=lambda x: x[0])[0]
    top = min(scaled_coordinates, key=lambda x: x[1])[1]
    right = max(scaled_coordinates, key=lambda x: x[0])[0]
    bottom = max(scaled_coordinates, key=lambda x: x[1])[1]

    draw.rectangle([left, top, right, bottom], outline=0)
    
    for x, y in scaled_coordinates:
        draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill=0)
    
    return img

def save_image(img, output_path):
    img.save(output_path)

def process_folder(input_folder, output_folder, img_size=(64, 64)):
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
                    continue
                
                img = create_image_with_bounding_box(coordinates, img_size)
                output_path = os.path.join(output_subfolder, f"{file_count}_bbox.png")
                save_image(img, output_path)
                file_count += 1

def main():
    input_folder = 'dataset_normalized'
    output_folder = 'bounding_box'
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    process_folder(input_folder, output_folder)

if __name__ == "__main__":
    main()
