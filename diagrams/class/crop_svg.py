"""
Crop a PlantUML-generated SVG into 3 equal horizontal parts with overlap.
Usage: python crop_svg.py class_diagram.svg
Adjust the 'overlap' variable to control how many pixels each part shares with its neighbour.
"""

import re
import sys

def crop_svg(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract total width and height from the SVG tag
    width_match = re.search(r'width="(\d+)px"', content)
    height_match = re.search(r'height="(\d+)px"', content)

    if not width_match or not height_match:
        print("Could not find width/height in SVG.")
        sys.exit(1)

    total_width = int(width_match.group(1))
    total_height = int(height_match.group(1))
    part_width = total_width // 3
    overlap = 100  # pixels of overlap between adjacent parts

    print(f"Total SVG size: {total_width} x {total_height}")
    print(f"Base part width: {part_width}, overlap: {overlap}px each side")

    for i in range(3):
        x_offset = max(0, i * part_width - overlap)
        end = min(total_width, (i + 1) * part_width + overlap)
        w = end - x_offset

        cropped = re.sub(
            r'width="\d+px"',
            f'width="{w}px"',
            content,
            count=1
        )
        cropped = re.sub(
            r'style="width:\d+px;height:\d+px;background:#FFFFFF;"',
            f'style="width:{w}px;height:{total_height}px;background:#FFFFFF;"',
            cropped,
            count=1
        )
        cropped = re.sub(
            r'viewBox="0 0 \d+ \d+"',
            f'viewBox="{x_offset} 0 {w} {total_height}"',
            cropped,
            count=1
        )

        output_file = input_file.replace(".svg", f"_part{i+1}.svg")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(cropped)
        print(f"Saved: {output_file}  (x={x_offset} to {x_offset + w}, width={w})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python crop_svg.py class_diagram.svg")
        sys.exit(1)
    crop_svg(sys.argv[1])
