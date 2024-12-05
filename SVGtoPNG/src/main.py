from svg_parser import parse_svg
from rasterizer import rasterize
from png_writer import write_png

def main(input_file, output_file, width, height):
    print(f"Parsing SVG file: {input_file}")
    shapes = parse_svg(input_file)
    print(f"Shapes parsed: {shapes}")

    print(f"Rasterizing with width={width}, height={height}")
    canvas = rasterize(shapes, width, height)
    print(f"Canvas dimensions: {canvas.shape}")

    write_png(canvas, output_file)
    print(f"PNG file saved as: {output_file}")

if __name__ == '__main__':
    main("input.svg", "output.png", 800, 600)

