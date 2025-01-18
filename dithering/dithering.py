import numpy as np
from PIL import Image

def floyd_steinberg_dithering(image_path, levels, threshold=None):
    img = Image.open(image_path).convert('L')
    img_array = np.array(img, dtype=float)
    height, width = img_array.shape
    
    def find_closest_color(pixel_value):
        if len(levels) == 2:
            return 0 if pixel_value < threshold else 255
        else:
            return levels[np.abs(levels - pixel_value).argmin()]
    
    for y in range(height-1):
        for x in range(width-1):
            old_pixel = img_array[y, x]
            new_pixel = find_closest_color(old_pixel)
            img_array[y, x] = new_pixel
            
            error = old_pixel - new_pixel
            
            if x < width-1:
                img_array[y, x+1] += error * 7/16
            if y < height-1:
                if x > 0:
                    img_array[y+1, x-1] += error * 3/16
                img_array[y+1, x] += error * 5/16
                if x < width-1:
                    img_array[y+1, x+1] += error * 1/16
    
    return Image.fromarray(np.uint8(img_array))

def ordered_dithering_4x4(image_path):
    img = Image.open(image_path).convert('L')
    img_array = np.array(img, dtype=float)
    dither_matrix = np.array([
        [6, 14, 2, 8],
        [4, 0, 10, 11],
        [12, 15, 5, 1],
        [9, 3, 13, 7]
    ])
    dither_matrix = dither_matrix / 16.0
    height, width = img_array.shape
    result = np.zeros_like(img_array)
    for y in range(height):
        for x in range(width):
            threshold = dither_matrix[y % 4, x % 4] * 255
            
            if img_array[y, x] > threshold:
                result[y, x] = 255
            else:
                result[y, x] = 0
                
    return Image.fromarray(np.uint8(result))

def generate_bayer_8x8():
    bayer = np.array([
        [0,  32, 8,  40, 2,  34, 10, 42],
        [48, 16, 56, 24, 50, 18, 58, 26],
        [12, 44, 4,  36, 14, 46, 6,  38],
        [60, 28, 52, 20, 62, 30, 54, 22],
        [3,  35, 11, 43, 1,  33, 9,  41],
        [51, 19, 59, 27, 49, 17, 57, 25],
        [15, 47, 7,  39, 13, 45, 5,  37],
        [63, 31, 55, 23, 61, 29, 53, 21]
    ]) / 63.0 
    return bayer

def bayer_dithering(image_path, palette):
    img = Image.open(image_path).convert('L')
    img_array = np.array(img, dtype=float)
    height, width = img_array.shape
    
    bayer = generate_bayer_8x8()
    
    result = np.zeros_like(img_array)
    
    def find_closest_color(value):
        return palette[np.abs(palette - value).argmin()]
    
    img_array = np.clip((img_array * 1.2) - 30, 0, 255)
    
    for y in range(height):
        for x in range(width):
            pixel_value = img_array[y, x]
            threshold = bayer[y % 8, x % 8] * 255
            adjusted_value = pixel_value + (threshold - 128)
            result[y, x] = find_closest_color(adjusted_value)
            
    return Image.fromarray(np.uint8(result))

bw_palette = np.array([0, 255])
result_bw = bayer_dithering('stanczyk.png', bw_palette)
result_bw.save('stanczyk_bayer_bw.png')

gray_palette = np.array([50, 100, 150, 200])
result_gray = bayer_dithering('stanczyk.png', gray_palette)
result_gray.save('stanczyk_bayer_gray.png')

result = ordered_dithering_4x4('stanczyk.png')
result.save('stanczyk_ordered_dither.png')

result_bw = floyd_steinberg_dithering('stanczyk.png', [0, 255], threshold=69)
result_bw.save('stanczyk_dithered_bw.png')

levels = np.array([0, 64, 128, 192, 255])
result_gray = floyd_steinberg_dithering('stanczyk.png', levels)
result_gray.save('stanczyk_dithered_gray.png')