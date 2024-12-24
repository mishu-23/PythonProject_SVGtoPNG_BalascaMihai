from png_writer import create_image
from PIL import ImageDraw

def rasterize_svg(width, height, elements, png_path):
    print(f"[processing] Cream un canvas de dimensiuni: {width}x{height}")

    img = create_image(width, height)
    draw = ImageDraw.Draw(img)

    for tag, attributes in elements:
        if tag == "rect":
            print(f"[processing] Cream un dreptunghi cu atribute: {attributes}")
            x = int(attributes["x"])
            y = int(attributes["y"])
            w = int(attributes["width"])
            h = int(attributes["height"])
            fill = attributes.get("fill", "black")
            draw.rectangle([x, y, x + w, y + h], fill=fill)

        elif tag == "circle":
            print(f"[processing] Cream un cerc cu atribute: {attributes}")
            cx = int(attributes["cx"])
            cy = int(attributes["cy"])
            r = int(attributes["r"])
            fill = attributes.get("fill", "black")
            draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=fill)

        elif tag == "line":
            print(f"[processing] Cream o linie cu atribute: {attributes}")
            x1 = int(attributes["x1"])
            y1 = int(attributes["y1"])
            x2 = int(attributes["x2"])
            y2 = int(attributes["y2"])
            stroke = attributes.get("stroke", "black")
            draw.line([x1, y1, x2, y2], fill=stroke)

        elif tag == "ellipse":
            print(f"[processing] Cream o elipsa cu atribute: {attributes}")
            cx = int(attributes["cx"])
            cy = int(attributes["cy"])
            rx = int(attributes["rx"])
            ry = int(attributes["ry"])
            fill = attributes.get("fill", "black")
            draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=fill)

        elif tag == "polygon":
            print(f"[processing] Cream un poligon cu atribute: {attributes}")
            points = [tuple(map(int, point.split(','))) for point in attributes["points"].split()]
            fill = attributes.get("fill", "black")
            draw.polygon(points, fill=fill)

        elif tag == "polyline":
            print(f"[processing] Cream o polilinie cu atribute: {attributes}")
            points = [tuple(map(int, point.split(','))) for point in attributes["points"].split()]
            stroke = attributes.get("stroke", "black")
            draw.line(points, fill=stroke, width=1)

    print(f"[processing] Cream un PNG la: {png_path}")
    img.save(png_path)
    print(f"[processing] Rasterizarea s-a terminat cu succes")