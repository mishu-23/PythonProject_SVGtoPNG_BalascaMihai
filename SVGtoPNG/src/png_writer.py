from PIL import Image

def create_image(width, height):
    print(f"[info] Cream un canvas gol cu dimensiunile {width}x{height}")
    return Image.new("RGB", (width, height), "white")