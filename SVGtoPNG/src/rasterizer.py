import cairo
# from png_writer import create_image
# from PIL import ImageDraw

def apply_opacity(color, opacity):
    """
    Aplica opacitatea unui culoare hexadecimale si returneaza valorile RGBA.

    Args:
        color (str): Culoarea in format hexadecimale (#RRGGBB).
        opacity (float): Valoarea opacitatii (0 - complet transparent, 1 - complet opac).

    Returns:
        tuple: Tuple cu valorile RGBA normalizate in intervalul [0, 1].
    """
    if color.startswith('#'):
        r = int(color[1:3], 16) / 255.0
        g = int(color[3:5], 16) / 255.0
        b = int(color[5:7], 16) / 255.0
        return r, g, b, float(opacity)
    return 0, 0, 0, 1 #default e negru mat

def parse_path(path_data, context):
    """
    Parseaza datele unui path SVG si le deseneaza folosind contextul Cairo.

    Args:
        path_data (str): Datele path-ului in format SVG.
        context (cairo.Context): Contextul Cairo pentru desenare.
    """
    import re
    command_re = re.compile(r"([MLHVCSQTZmlhvcsqtz])|(-?[\d.]+)")

    cursor = (0, 0)
    start_point = (0, 0)
    tokens = command_re.findall(path_data)
    tokens = [t[0] or t[1] for t in tokens]
    i = 0

    while i < len(tokens):
        command = tokens[i]
        i += 1
        if command in "Mm": #move to
            x, y = float(tokens[i]), float(tokens[i + 1])
            i += 2
            if command == "m":
                x += cursor[0]
                y += cursor[1]
            cursor = (x, y)
            start_point = cursor
            context.move_to(x, y)

        elif command in "Ll": #Line to
            x, y = float(tokens[i]), float(tokens[i + 1])
            i += 2
            if command == "l":
                x += cursor[0]
                y += cursor[1]
            cursor = (x, y)
            context.line_to(x, y)

        elif command in "Cc": #cubic bezier curve
            x1, y1 = float(tokens[i]), float(tokens[i + 1])
            x2, y2 = float(tokens[i+2]), float(tokens[i + 3])
            x, y = float(tokens[i+4]), float(tokens[i + 5])
            i += 6
            if command == "c":
                x1 += cursor[0]
                y1 += cursor[1]
                x2 += cursor[0]
                y2 += cursor[1]
                x += cursor[0]
                y += cursor[1]
            cursor = (x, y)
            context.curve_to(x1, y1, x2, y2, x, y)

        elif command in "Zz": #close path
            context.close_path()
            cursor = start_point

        elif command in "Hh":  # Horizontal line to
            x = float(tokens[i])
            i += 1

            if command == "h":  # Ajustam coordonata pentru mod relativ
                x += cursor[0]

            # Desenam linia
            context.line_to(x, cursor[1])

            # Actualizam cursorul
            cursor = (x, cursor[1])

        elif command in "Vv":  # Vertical line to
            y = float(tokens[i])
            i += 1

            if command == "v":  # Ajustam coordonata pentru mod relativ
                y += cursor[1]

            # Desenam linia
            context.line_to(cursor[0], y)

            # Actualizam cursorul
            cursor = (cursor[0], y)

        elif command in "Ss":  # Smooth cubic Bezier curve
            x2, y2 = float(tokens[i]), float(tokens[i + 1])
            x, y = float(tokens[i + 2]), float(tokens[i + 3])
            i += 4

            # Determinam punctul de control ca simetric fata de ultimul punct de control sau cursor
            if "control_point" in locals():  # Daca exista un punct de control anterior
                x1 = 2 * cursor[0] - control_point[0]
                y1 = 2 * cursor[1] - control_point[1]

            else:  # Daca nu exista un punct de control anterior
                x1, y1 = cursor

            if command == "s":  # Ajustam coordonatele pentru mod relativ
                x2 += cursor[0]
                y2 += cursor[1]
                x += cursor[0]
                y += cursor[1]

            # Actualizam punctele de control si cursorul
            control_point = (x2, y2)  # Salvam punctul de control actual
            cursor = (x, y)

            # Desenam curba
            context.curve_to(x1, y1, x2, y2, x, y)

        elif command in "Qq":  # Quadratic Bezier curve
            x1, y1 = float(tokens[i]), float(tokens[i + 1])
            x, y = float(tokens[i + 2]), float(tokens[i + 3])
            i += 4

            if command == "q":  # Ajustam coordonatele pentru mod relativ
                x1 += cursor[0]
                y1 += cursor[1]
                x += cursor[0]
                y += cursor[1]

            # Desenam curba
            context.curve_to(x1, y1, x, y, x, y)

            # Actualizam punctele de control si cursorul
            quadratic_control_point = (x1, y1)
            cursor = (x, y)

        elif command in "Tt":  # Smooth quadratic Bezier curve
            x, y = float(tokens[i]), float(tokens[i + 1])
            i += 2

            # Determinam punctul de control
            if "quadratic_control_point" in locals():  # Daca exista un punct de control anterior
                x1 = 2 * cursor[0] - quadratic_control_point[0]
                y1 = 2 * cursor[1] - quadratic_control_point[1]

            else:  # Daca nu exista un punct de control anterior
                x1, y1 = cursor

            if command == "t":  # Ajustam coordonatele pentru mod relativ
                x += cursor[0]
                y += cursor[1]

            # Desenam curba
            context.curve_to(x1, y1, x, y, x, y)

            # Actualizam punctele de control si cursorul
            quadratic_control_point = (x1, y1)
            cursor = (x, y)

        else:
            raise ValueError(f"Unknown command: {command}")

def rasterize_svg(width, height, elements, png_path):
    """
    Creaza o imagine PNG dintr-un SVG si o salveaza la calea specificata.

    Args:
        width (int): Latimea imaginii in pixeli.
        height (int): Inaltimea imaginii in pixeli.
        elements (list): Lista de elemente SVG (ex. rect, circle, path, etc.).
        png_path (str): Calea la care va fi salvata imaginea PNG.
    """
    print(f"[info] Cream un canvas de dimensiuni: {width}x{height}")

    # Cream un canvas folosind cairo
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
            print(f"[info] Rasterizam o elipsa cu atribute: {attributes}")
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
                context.arc(0, 0, 1, 0, 2 * 3.14159)
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

        elif tag == "path":
            print(f"[info] Rasterizam un path cu atribute: {attributes}")
            path_data = attributes.get("d", "")
            fill = attributes.get("fill", "#000000")
            print(f"[debug] fill: {fill}")
            opacity = float(attributes.get("fill-opacity", attributes.get("opacity", 1)))
            stroke = attributes.get("stroke", None)
            stroke_width = float(attributes.get("stroke-width", 1))

            # Convertim datele din atributul "d" intr-o cale Cairo
            parse_path(path_data, context)
            path_copy = context.copy_path()

            r, g, b, a = apply_opacity(fill, opacity)
            print(f"[debug] rgba: {r}, {g}, {b}, {a}")
            context.set_source_rgba(r, g, b, a)
            context.fill()

            if stroke:
                context.append_path(path_copy)
                r, g, b, a = apply_opacity(stroke, opacity)
                context.set_source_rgba(r, g, b, a)
                context.set_line_width(stroke_width)
                context.stroke()

        # Salvam imaginea
        print(f"[info] Salvam imaginea PNG la: {png_path}")
        surface.write_to_png(png_path)
        print("[info] Rasterizarea s-a terminat cu succes.")