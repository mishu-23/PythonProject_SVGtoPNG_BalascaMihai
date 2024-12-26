import cairo
from png_writer import create_image
from PIL import ImageDraw

def apply_opacity(color, opacity):
    if color.startswith('#'):
        r = int(color[1:3], 16) / 255.0
        g = int(color[3:5], 16) / 255.0
        b = int(color[5:7], 16) / 255.0
        return r, g, b, float(opacity)
    return 0, 0, 0, 1 #default e negru mat

def rasterize_svg(width, height, elements, png_path):
    print(f"[info] Cream un canvas de dimensiuni: {width}x{height}")

    # Creăm un canvas folosind cairo
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    context = cairo.Context(surface)

    # Fundal alb
    context.set_source_rgba(1, 1, 1, 0)
    context.paint()

    for tag, attributes in elements:
        if tag == "rect":
            print(f"[info] Rasterizam un dreptunghi cu atribute: {attributes}")
            x = float(attributes["x"])
            y = float(attributes["y"])
            w = float(attributes["width"])
            h = float(attributes["height"])
            fill = attributes.get("fill", "#000000")
            opacity = float(attributes.get("fill-opacity", attributes.get("opacity", 1)))
            r, g, b, a = apply_opacity(fill, opacity)
            context.set_source_rgba(r, g, b, a)
            context.rectangle(x, y, w, h)
            context.fill()

            if "stroke" in attributes:
                stroke = attributes["stroke"]
                stroke_width = float(attributes.get("stroke-width", 1))
                r, g, b, a = apply_opacity(stroke, opacity)
                context.set_source_rgba(r, g, b, a)
                context.set_line_width(stroke_width)
                context.stroke()

        elif tag == "circle":
            print(f"[info] Rasterizam un cerc cu atribute: {attributes}")
            cx = float(attributes["cx"])
            cy = float(attributes["cy"])
            radius = float(attributes["r"])
            fill = attributes.get("fill", "#000000")
            opacity = float(attributes.get("fill-opacity", attributes.get("opacity", 1)))
            r, g, b, a = apply_opacity(fill, opacity)
            context.set_source_rgba(r, g, b, a)
            context.arc(cx, cy, radius, 0, 2 * 3.14159)
            context.fill()

            if "stroke" in attributes:
                stroke = attributes["stroke"]
                stroke_width = float(attributes.get("stroke-width", 1))
                r, g, b, a = apply_opacity(stroke, opacity)
                context.set_source_rgba(r, g, b, a)
                context.set_line_width(stroke_width)
                context.stroke()

        elif tag == "line":
            print(f"[info] Rasterizam o linie cu atribute: {attributes}")
            x1 = float(attributes["x1"])
            y1 = float(attributes["y1"])
            x2 = float(attributes["x2"])
            y2 = float(attributes["y2"])
            stroke = attributes.get("stroke", "#000000")
            stroke_width = float(attributes.get("stroke-width", 1))
            opacity = float(attributes.get("opacity", 1))
            r, g, b, a = apply_opacity(stroke, opacity)
            context.set_source_rgba(r, g, b, a)
            context.set_line_width(stroke_width)
            context.move_to(x1, y1)
            context.line_to(x2, y2)
            context.stroke()

        elif tag == "ellipse":
            print(f"[info] Rasterizam o elipsă cu atribute: {attributes}")
            cx = float(attributes["cx"])
            cy = float(attributes["cy"])
            rx = float(attributes["rx"])
            ry = float(attributes["ry"])
            fill = attributes.get("fill", "#000000")
            opacity = float(attributes.get("fill-opacity", attributes.get("opacity", 1)))
            r, g, b, a = apply_opacity(fill, opacity)
            context.set_source_rgba(r, g, b, a)
            context.save()
            context.translate(cx, cy)
            context.scale(rx, ry)
            context.arc(0, 0, 1, 0, 2 * 3.14159)
            context.restore()
            context.fill()

            if "stroke" in attributes:
                stroke = attributes["stroke"]
                stroke_width = float(attributes.get("stroke-width", 1))
                r, g, b, a = apply_opacity(stroke, opacity)
                context.set_source_rgba(r, g, b, a)
                context.set_line_width(stroke_width)
                context.stroke()

        elif tag == "polygon":
            print(f"[info] Rasterizam un poligon cu atribute: {attributes}")
            points = [tuple(map(float, point.split(','))) for point in attributes["points"].split()]
            fill = attributes.get("fill", "#000000")
            opacity = float(attributes.get("fill-opacity", attributes.get("opacity", 1)))
            r, g, b, a = apply_opacity(fill, opacity)
            context.set_source_rgba(r, g, b, a)

            context.move_to(*points[0])
            for point in points[1:]:
                context.line_to(*point)
            context.close_path()
            context.fill()

            if "stroke" in attributes:
                stroke = attributes["stroke"]
                stroke_width = float(attributes.get("stroke-width", 1))
                r, g, b, a = apply_opacity(stroke, opacity)
                context.set_source_rgba(r, g, b, a)
                context.set_line_width(stroke_width)
                context.stroke()

        elif tag == "polyline":
            print(f"[info] Rasterizam o polilinie cu atribute: {attributes}")
            points = [tuple(map(float, point.split(','))) for point in attributes["points"].split()]
            stroke = attributes.get("stroke", "#000000")
            stroke_width = float(attributes.get("stroke-width", 1))
            opacity = float(attributes.get("opacity", 1))
            r, g, b, a = apply_opacity(stroke, opacity)
            context.set_source_rgba(r, g, b, a)
            context.set_line_width(stroke_width)

            context.move_to(*points[0])
            for point in points[1:]:
                context.line_to(*point)
            context.stroke()

    # Salvăm imaginea
    print(f"[info] Salvam imaginea PNG la: {png_path}")
    surface.write_to_png(png_path)
    print("[info] Rasterizarea s-a terminat cu succes.")