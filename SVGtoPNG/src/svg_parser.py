import xml.etree.ElementTree as ET

def parse_svg(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    shapes = []
    for element in root:
        if element.tag.endswith('rect'):
            shapes.append({
                'type': 'rect',
                'x': float(element.attrib['x']),
                'y': float(element.attrib['y']),
                'width': float(element.attrib['width']),
                'height': float(element.attrib['height']),
                'fill': element.attrib.get('fill', '#000000')
            })
    return shapes