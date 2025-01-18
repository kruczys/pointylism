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

result_bw = floyd_steinberg_dithering('stanczyk.png', [0, 255], threshold=39)
result_bw.save('stanczyk_dithered_bw.png')

levels = np.array([0, 64, 128, 192, 255])
result_gray = floyd_steinberg_dithering('stanczyk.png', levels)
result_gray.save('stanczyk_dithered_gray.png')