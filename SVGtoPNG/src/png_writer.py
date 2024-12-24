from PIL import Image

def create_image(width, height):
    print(f"[processing] Cream un canvas gol cu dimensiunile {width}x{height}")
    return Image.new("RGB", (width, height), "white")