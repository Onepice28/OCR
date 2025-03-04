from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

chain_code_arrows = {
    0: "→",
    1: "↗",
    2: "↑",
    3: "↖",
    4: "←",
    5: "↙",
    6: "↓",
    7: "↘",
}

def calculate_chain_code(contour):
    chain_code = []
    for i in range(1, len(contour)):
        x1, y1 = contour[i - 1]
        x2, y2 = contour[i]
        
        dx = x2 - x1
        dy = y2 - y1
        
        if dx == 1 and dy == 0:
            chain_code.append(0)
        elif dx == 1 and dy == -1:
            chain_code.append(1)
        elif dx == 0 and dy == -1:
            chain_code.append(2)
        elif dx == -1 and dy == -1:
            chain_code.append(3)
        elif dx == -1 and dy == 0:
            chain_code.append(4)
        elif dx == -1 and dy == 1:
            chain_code.append(5)
        elif dx == 0 and dy == 1:
            chain_code.append(6)
        elif dx == 1 and dy == 1:
            chain_code.append(7)

    return chain_code

def get_bounding_box(coordinates):
    min_x = min(coordinates, key=lambda x: x[0])[0]
    min_y = min(coordinates, key=lambda x: x[1])[1]
    max_x = max(coordinates, key=lambda x: x[0])[0]
    max_y = max(coordinates, key=lambda x: x[1])[1]
    return min_x, min_y, max_x, max_y

def downsample_and_draw_grid(coordinates, img_size=(64, 64), padding=5):
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
    
    chain_code = calculate_chain_code(scaled_coordinates)
    
    grid_size = 4
    cell_width = img_size[0] // grid_size
    cell_height = img_size[1] // grid_size
    for i in range(grid_size + 1):
        draw.line((0, i * cell_height, img_size[0], i * cell_height), fill=0)
        draw.line((i * cell_width, 0, i * cell_width, img_size[1]), fill=0)
    
    font = ImageFont.load_default()
    for (x, y), direction in zip(scaled_coordinates, chain_code):
        row = y // (img_size[1] // grid_size)
        col = x // (img_size[0] // grid_size)
        if 0 <= row < grid_size and 0 <= col < grid_size:
            center_x = col * cell_width + cell_width // 2
            center_y = row * cell_height + cell_height // 2
            draw.text((center_x, center_y), chain_code_arrows[direction], fill=0, font=font, anchor="mm")
    
    return img

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

def save_image(img, output_path):
    img.save(output_path)

def process_folder(input_folder, output_folder, img_size=(64, 64), padding=5):
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
                
                img = downsample_and_draw_grid(coordinates, img_size, padding)
                
                output_path = os.path.join(output_subfolder, f"{file_count}.png")
                save_image(img, output_path)
                file_count += 1

def main():
    input_folder = 'dataset_normalized'
    output_folder = 'downsampled'
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    process_folder(input_folder, output_folder)

if __name__ == "__main__":
    main()
