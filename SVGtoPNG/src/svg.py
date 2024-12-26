import argparse
from svg_parser import parse_svg
from rasterizer import rasterize_svg
import os

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("svg_path")
    args = parser.parse_args()

    svg_path = args.svg_path

    if not os.path.isfile(svg_path):
        print(f"[error] Fisierul SVG '{svg_path}' nu a fost gasit.")
        return

    png_path = os.path.splitext(svg_path)[0] + ".png"

    print("[info] Pornim parsarea fisierului SVG...")
    width, height, elements = parse_svg(svg_path)
    print(f"[debug] Dimensiuni SVG: {width}x{height}")
    print(f"[debug] Elemente: {elements}")

    print("[info] Pornim rasterizarea PNG-ului...")
    rasterize_svg(width, height, elements, png_path)
    print(f"[info] Imaginea PNG a fost salvata la {png_path}")

if __name__ == "__main__":
    main()
