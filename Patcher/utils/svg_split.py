import base64
import copy
import io
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Tuple
from xml.etree.ElementTree import Element

import cairosvg
from PIL import Image

from utils.exceptions import ArgumentException


def recolor_element(element: Element, color: str = "#FFFFFF"):
    style = element.get('style', None)
    if style is not None:
        pairs = [p.split(":") for p in style.split(";") if ":" in p]
        styles = {k.strip(): v.strip() for k, v in pairs}

        if "fill" in styles.keys():
            if styles["fill"] != "none":
                styles["fill"] = color

        if "stroke" in styles.keys():
            styles["stroke"] = color

        new_style_str = ";".join([f"{k}:{v}" for k, v in styles.items()])
        element.set("style", new_style_str)


def get_image(root_element: Element) -> Image.Image:
    svg_bytes = ET.tostring(root_element)
    png_buffer = io.BytesIO()
    cairosvg.svg2png(bytestring=svg_bytes, write_to=png_buffer)
    png_buffer.seek(0)
    return Image.open(png_buffer).copy()


def new_svg(size: Tuple[int, int], bg_color: str) -> Element:
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}
    ET.register_namespace('', namespaces['svg'])

    root = ET.Element(
        "svg",
        width=str(size[0]),
        height=str(size[1]),
        viewbox=f"0 0 {size[0]} {size[1]}"
    )

    root.append(
        ET.Element(
            "rect",
            width=str(size[0]),
            height=str(size[1]),
            style=f"fill:{bg_color};"
        )
    )

    return root


def split_svg(svg_path: Path):
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}
    ET.register_namespace('', namespaces['svg'])

    ignored_tags = [
        '{http://www.w3.org/2000/svg}defs',
        '{http://www.w3.org/2000/svg}desc',
        '{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}namedview'
    ]

    valid_tags = [
        '{http://www.w3.org/2000/svg}rect',
        '{http://www.w3.org/2000/svg}path',
        '{http://www.w3.org/2000/svg}circle',
        '{http://www.w3.org/2000/svg}ellipse',
        '{http://www.w3.org/2000/svg}text',
        '{http://www.w3.org/2000/svg}image',
    ]

    try:
        tree = ET.parse(svg_path)
        root = tree.getroot()
    except ET.ParseError:
        root = ET.fromstring(str(svg_path))

    width = root.attrib.get('width', '100%')
    height = root.attrib.get('height', '100%')
    viewbox = root.attrib.get('viewBox', f'0 0 {width} {height}')

    masks_output: dict[str, Element] = {}
    images_output: dict[str, Image.Image] = {}
    paths = [child for child in root]

    for i, path_el in enumerate(paths):
        if path_el.tag in ignored_tags:
            continue

        if path_el.tag not in valid_tags:
            raise ArgumentException(f"Unsupported tag {path_el.tag} found in svg file at path: \n{svg_path}")

        path_id = path_el.attrib.get('id', None)
        if path_id is None:
            raise ArgumentException(f"Missing id for one or more top level elements in svg file: \n{svg_path}")

        if path_el.tag == "{http://www.w3.org/2000/svg}image":
            data = path_el.get("{http://www.w3.org/1999/xlink}href")
            if data is None:
                raise ArgumentException("No data for image")

            if not data.startswith("data:image/png;base64,"):
                raise ArgumentException("Image must be embeded")

            img_data = base64.b64decode(data[22:-1])
            img = Image.open(io.BytesIO(img_data))
            images_output[path_id] = img

        else:
            masks_output[path_id] = path_el

    if len(masks_output) == 0 and len(images_output) == 0:
        raise ArgumentException(f"No masks or fill images found in svg file: \n{svg_path}")

    return masks_output, images_output
