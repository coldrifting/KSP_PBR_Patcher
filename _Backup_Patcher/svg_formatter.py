import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from utils.exceptions import ArgumentException


def reformat_svg(svg_path):
    ignored_tags = [
        '{http://www.w3.org/2000/svg}defs',
        '{http://www.w3.org/2000/svg}desc',
        '{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}namedview'
    ]

    valid_tags = [
        '{http://www.w3.org/2000/svg}path',
        '{http://www.w3.org/2000/svg}rect',
        '{http://www.w3.org/2000/svg}circle',
        '{http://www.w3.org/2000/svg}ellipse',
        '{http://www.w3.org/2000/svg}image',
        '{http://www.w3.org/2000/svg}text',
    ]

    file = Path(svg_path)

    if not file.exists():
        exit(1)

    namespaces = {'svg': 'http://www.w3.org/2000/svg'}
    ET.register_namespace('', namespaces['svg'])

    try:
        tree = ET.parse(file)
        root = tree.getroot()
    except ET.ParseError:
        root = ET.fromstring(str(file))

    width = root.attrib.get('width', '100%')
    height = root.attrib.get('height', '100%')

    output = (f"<svg width=\"{width}\"\n"
              f"     height=\"{height}\"\n"
              f"     viewBox=\"0 0 {width} {height}\"\n"
               "     xmlns=\"http://www.w3.org/2000/svg\"\n"
               "     xmlns:xlink=\"http://www.w3.org/1999/xlink\">\n")

    paths = [child for child in root]
    for path_el in paths:
        if path_el.tag in ignored_tags:
            continue

        if path_el.tag not in valid_tags:
            raise ArgumentException(f"Unsupported tag {path_el.tag} found in svg file at path: \n{svg_path}")

        path_id = path_el.attrib.get('id', None)
        if path_id is None:
            raise ArgumentException(f"Element without id found in svg file at path: \n{svg_path}")

        tag_short_name = str(path_el.tag).removeprefix('{http://www.w3.org/2000/svg}')
        tag_output = f"    <{tag_short_name} id=\"{path_id}\"\n"
        indent = (len(tag_short_name) * " " + " " * 6)
        match tag_short_name:
            case 'path' | 'rect' | 'circle' | 'ellipse':
                style = path_el.get('style', None)
                if style is not None:
                    pairs = [p.split(":") for p in style.split(";") if ":" in p]
                    styles = {k.strip(): v.strip() for k, v in pairs}

                    if "fill" in styles.keys():
                        if "fill-opacity" in styles.keys():
                            if styles["fill-opacity"] == "1":
                                del styles["fill-opacity"]

                        if "stroke" not in styles.keys():
                            if 'stroke-linecap' in styles.keys():
                                del styles['stroke-linecap']

                    if "stroke" in styles.keys():
                        if "stroke-opacity" in styles.keys():
                            if styles["stroke-opacity"] == "1":
                                del styles["stroke-opacity"]

                    new_style_str = ";".join([f"{k}:{v}" for k, v in styles.items()])
                    tag_output += f"{indent}style=\"{new_style_str}\"\n"

                    match tag_short_name:
                        case 'path':
                            d = path_el.attrib['d']
                            if d.endswith(" "):
                                d = d[:-1]
                            tag_output += f"{indent}d=\"{d}\"\n"
                        case 'rect':
                            tag_output += f"{indent}width=\"{path_el.attrib['width']}\"\n"
                            tag_output += f"{indent}height=\"{path_el.attrib['height']}\"\n"
                            tag_output += f"{indent}x=\"{path_el.attrib['x']}\"\n"
                            tag_output += f"{indent}y=\"{path_el.attrib['y']}\"\n"
                        case 'circle':
                            tag_output += f"{indent}r=\"{path_el.attrib['r']}\"\n"
                            tag_output += f"{indent}cx=\"{path_el.attrib['cx']}\"\n"
                            tag_output += f"{indent}cy=\"{path_el.attrib['cy']}\"\n"
                        case 'ellipse':
                            tag_output += f"{indent}rx=\"{path_el.attrib['rx']}\"\n"
                            tag_output += f"{indent}ry=\"{path_el.attrib['ry']}\"\n"
                            tag_output += f"{indent}cx=\"{path_el.attrib['cx']}\"\n"
                            tag_output += f"{indent}cy=\"{path_el.attrib['cy']}\"\n"

            case 'image':
                tag_output += f"{indent}style=\"image-rendering:pixelated\"\n"
                tag_output += f"{indent}preserveAspectRatio=\"none\"\n"
                tag_output += f"{indent}width=\"{path_el.attrib['width']}\"\n"
                tag_output += f"{indent}height=\"{path_el.attrib['height']}\"\n"
                tag_output += f"{indent}x=\"{path_el.attrib['x']}\"\n"
                tag_output += f"{indent}y=\"{path_el.attrib['y']}\"\n"

                image_data = path_el.attrib['{http://www.w3.org/1999/xlink}href']
                if not image_data.startswith("data:image/png;base64,"):
                    continue

                image_data = image_data.replace("\n", "&#10;")

                tag_output += f"{indent}xlink:href=\"{image_data}\"\n"

            case '{http://www.w3.org/2000/svg}text':
                tag_output += ET.tostring(path_el, encoding='utf-8')  # Give up for text tags, too complicated
                tag_output += "\n"

        tag_output += f"    />\n"
        output += tag_output

    output += "</svg>"

    file.write_text(output)


reformat_svg(sys.argv[1])
