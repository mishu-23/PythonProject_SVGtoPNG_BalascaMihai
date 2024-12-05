import numpy as np

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) #RRGGBB

def rasterize(shapes, width, height):
    print(f"Creating canvas with dimensions ({height}, {width})")
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    for shape in shapes:
        if shape['type'] == 'rect':
            x, y, w, h = int(shape['x']), int(shape['y']), int(shape['width']), int(shape['height'])
            color = hex_to_rgb(shape['fill'])
            print(f"Rasterizing rectangle: {shape} at ({x}, {y}), size ({w}, {h}), color {color}")
            canvas[y:y+h, x:x+w] = color
    return canvas