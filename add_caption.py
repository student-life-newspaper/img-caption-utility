import sys
import argparse
from PIL import Image, ImageDraw, ImageFont
import os

def add_caption_to_image(image_path, caption_text, output_path, font_path=None, text_color="black", font_size=30):
    # Open the original image with error handling
    try:
        image = Image.open(image_path)
    except IOError:
        print(f"Error: Unable to open image at {image_path}")
        return
    
    image = image.convert("RGBA")  # Convert to RGBA to handle transparency if needed
    width, height = image.size

    # Dynamically set font size based on the image width if not provided
    if font_size is None:
        font_size = max(20, width // 15)  # Font size scales with the width of the image
    
    margin = font_size // 4  # Dynamically adjust margin

    # Convert text color argument to RGB values
    if text_color.lower() == "white":
        rgba_color = (255, 255, 255, 255)
    else:
        rgba_color = (0, 0, 0, 255)  # Default to black

    # Try loading Times New Roman or the user-specified font
    try:
        if font_path and os.path.exists(font_path):
            font = ImageFont.truetype(font_path, font_size)
        else:
            # Load Times New Roman from system fonts
            font = ImageFont.truetype("Times New Roman.ttf", font_size)
    except IOError:
        print(f"Error: Unable to load Times New Roman or the specified font. Falling back to default.")
        return

    # Word wrapping: calculate how many lines are needed for the text
    draw = ImageDraw.Draw(image)
    lines = []
    words = caption_text.split(' ')
    current_line = ""
    
    for word in words:
        test_line = current_line + word + " "
        text_width = draw.textbbox((0, 0), test_line, font=font)[2]
        if text_width <= width - margin * 2:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    
    if current_line:
        lines.append(current_line.strip())

    # Calculate height needed for text box based on number of lines
    line_height = font_size + margin
    text_box_height = line_height * len(lines)

    # Create a new image with extra height to fit the text
    new_image = Image.new('RGBA', (width, height + text_box_height), (255, 255, 255, 0))  # Transparent background
    new_image.paste(image, (0, 0), image if image.mode == 'RGBA' else None)  # Handle transparency if necessary

    # Draw each line of text left-aligned and vertically centered in the added space
    draw = ImageDraw.Draw(new_image)
    y_offset = height + ((text_box_height - len(lines) * line_height) // 2)  # Center the text vertically in the added space

    for i, line in enumerate(lines):
        text_x = margin  # Left-align the text with a margin
        text_y = y_offset + i * line_height
        draw.text((text_x, text_y), line, fill=rgba_color, font=font)

    # Save the new image with the adjusted height
    new_image.save(output_path)
    print(f"Output image saved as {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add a caption below an image.')
    parser.add_argument('image_path', type=str, help='Path to the input image.')
    parser.add_argument('caption_text', type=str, help='Text to add as caption.')
    parser.add_argument('--output_path', type=str, default='output_image.png', help='Path to save the output image.')
    parser.add_argument('--font_path', type=str, default=None, help='Path to the font file (optional).')
    parser.add_argument('--text_color', type=str, default='black', help='Text color: black or white (default is black).')
    parser.add_argument('--font_size', type=int, default=None, help='Font size in pixels (optional).')

    args = parser.parse_args()

    add_caption_to_image(
        args.image_path,
        args.caption_text,
        args.output_path,
        args.font_path,
        args.text_color,
        args.font_size
    )
