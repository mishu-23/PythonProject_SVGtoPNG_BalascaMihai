import xml.etree.ElementTree as ET

def parse_svg(file_path):
    """
    Parseaaza un fisier SVG si extrage dimensiunile si elementele sale.

    Parametri:
    - file_path (str): calea catre fisierul SVG.

    Returneaza:
    - width (int): latimea imaginii.
    - height (int): inaltimea imaginii.
    - elements (list): lista de elemente (tag, atribute) gasite in SVG.
    """
    print(f"[info] Citim fisierul SVG: {file_path}")
    tree = ET.parse(file_path)
    root = tree.getroot()

    width = int(root.attrib.get('width', 100))
    height = int(root.attrib.get('height', 100))
    print(f"[debug] Dimensiuni detectate: {width}x{height}")

    elements = []
    for elem in root:
        tag = elem.tag.split('}')[-1] #renuntam la namespace
        attributes = elem.attrib
        elements.append((tag, attributes))
        print(f"[debug] Element detectat: {tag}: {attributes}" )

    print("[info] Parsarea SVG s-a termminat cu succes")
    return width, height, elements