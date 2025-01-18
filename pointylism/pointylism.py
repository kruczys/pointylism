import numpy as np
from PIL import Image, ImageDraw
import random

def pointillism_dots(image_path, num_points=1000, dot_size_range=(3, 8)):
    img = Image.open(image_path)
    img = img.convert('RGB')
    width, height = img.size
    
    result = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(result)
    
    for _ in range(num_points):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        color = img.getpixel((x, y))
        dot_size = random.randint(dot_size_range[0], dot_size_range[1])
        draw.ellipse([x-dot_size, y-dot_size, x+dot_size, y+dot_size], 
                    fill=color)
    
    return result

def pointillism_lines(image_path, num_lines=1000, line_length_range=(5, 15)):
    img = Image.open(image_path)
    img = img.convert('RGB')
    width, height = img.size
    
    result = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(result)
    
    for _ in range(num_lines):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        length = random.randint(line_length_range[0], line_length_range[1])
        angle = random.uniform(0, 2 * np.pi)
        x2 = x + length * np.cos(angle)
        y2 = y + length * np.sin(angle)
        color = img.getpixel((x, y))
        draw.line([(x, y), (x2, y2)], fill=color, width=2)
    
    return result

if __name__ == "__main__":
    image = pointillism_lines("garfild.jpg", num_lines=320000, line_length_range=(5, 10))
    image.save("efekt_puentylizmu_linie.png")
    image = pointillism_dots("garfild.jpg", num_points=200000, dot_size_range=(1, 3))
    image.save("efekt_puentylizmu_kropki.png")