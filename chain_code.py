import os
import numpy as np
from PIL import Image, ImageDraw

directions = {
    0: (1, 0),
    1: (1, -1),
    2: (0, -1),
    3: (-1, -1),
    4: (-1, 0),
    5: (-1, 1),
    6: (0, 1),
    7: (1, 1)
}

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

def scale_coordinates(coordinates, grid_size=(8, 8)):
    if not coordinates:
        return []
    min_x, min_y = np.min(coordinates, axis=0)
    max_x, max_y = np.max(coordinates, axis=0)
    
    scale_x = (grid_size[0] - 1) / (max_x - min_x) if max_x - min_x > 0 else 1
    scale_y = (grid_size[1] - 1) / (max_y - min_y) if max_y - min_y > 0 else 1
    
    scaled_coordinates = [(int((x - min_x) * scale_x), int((y - min_y) * scale_y)) for x, y in coordinates]
    return scaled_coordinates

def compute_chain_code(scaled_coordinates):
    if len(scaled_coordinates) < 2:
        return {}
    
    grid_arrows = {}
    for i in range(1, len(scaled_coordinates)):
        x1, y1 = scaled_coordinates[i - 1]
        x2, y2 = scaled_coordinates[i]
        
        dx, dy = x2 - x1, y2 - y1
        for code, (dir_x, dir_y) in directions.items():
            if (dx, dy) == (dir_x, dir_y):
                grid_arrows[(x1, y1)] = code
                break
    
    return grid_arrows

def draw_chain_code(grid_arrows, grid_size=(8, 8), img_size=(64, 64)):
    cell_w, cell_h = img_size[0] // grid_size[0], img_size[1] // grid_size[1]
    
    img = Image.new("RGB", img_size, color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    for i in range(1, grid_size[0]):
        draw.line([(i * cell_w, 0), (i * cell_w, img_size[1])], fill=(200, 200, 200))
    for j in range(1, grid_size[1]):
        draw.line([(0, j * cell_h), (img_size[0], j * cell_h)], fill=(200, 200, 200))
    
    for (x, y), direction in grid_arrows.items():
        center_x = x * cell_w + cell_w // 2
        center_y = y * cell_h + cell_h // 2
        
        dx, dy = directions[direction]
        arrow_end_x = center_x + dx * (cell_w // 3)
        arrow_end_y = center_y + dy * (cell_h // 3)
        
        draw.line([(center_x, center_y), (arrow_end_x, arrow_end_y)], fill=(0, 0, 0), width=2)
        arrow_head = [
            (arrow_end_x, arrow_end_y),
            (arrow_end_x - dx * 4 + dy * 4, arrow_end_y - dy * 4 - dx * 4),
            (arrow_end_x - dx * 4 - dy * 4, arrow_end_y - dy * 4 + dx * 4)
        ]
        draw.polygon(arrow_head, fill=(0, 0, 0))
    
    return img

def process_folder(input_folder, output_folder, grid_size=(8, 8), img_size=(64, 64)):
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
                    print(f"Skipping {file_path}, no valid coordinates.")
                    continue
                
                scaled_coordinates = scale_coordinates(coordinates, grid_size)
                grid_arrows = compute_chain_code(scaled_coordinates)
                
                img = draw_chain_code(grid_arrows, grid_size, img_size)
                
                output_path = os.path.join(output_subfolder, f"{file_count}.png")
                img.save(output_path)
                file_count += 1

def main():
    input_folder = 'dataset_normalized'
    output_folder = 'chain_code'
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    process_folder(input_folder, output_folder)

if __name__ == "__main__":
    main()
