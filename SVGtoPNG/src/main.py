from svg_parser import parse_svg
from rasterizer import rasterize_svg

if __name__ == "__main__":
    svg_path = "input.svg"
    png_path = "output.png"

    print("[processing] Pornim parsarea fisierului SVG...")
    width, height, elements = parse_svg(svg_path)
    print(f"[debug] Dimensiuni SVG: {width}x{height}")
    print(f"[debug] Elemente: {elements}")

    print("[processing] Pornim rasterizarea PNG-ului")
    rasterize_svg(width, height, elements, png_path)
    print(f"[processing] Imaginea PNG a fost salvata la {png_path}")