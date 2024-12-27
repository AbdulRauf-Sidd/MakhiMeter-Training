from PIL import Image

def change_color(image_path, output_path):
    # Open the image
    img = Image.open(image_path)
    img = img.convert('RGB')  # Ensure image is in RGB mode
    
    # Get image size
    width, height = img.size
    
    # Target and replacement color
    target_color = (105,19,105)  # RGB for #1d19b5
    replacement_color = (0, 0, 0)  # RGB for black #000000
    
    # Process each pixel
    for x in range(width):
        for y in range(height):
            current_color = img.getpixel((x, y))
            if current_color == target_color or current_color == (29,25,181):
                img.putpixel((x, y), replacement_color)
    
    # Save the modified image
    img.save(output_path)
    print(f"Image saved to {output_path}")

# Example usage
change_color('/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model v1.4/D species masked/D.bizonata_m_12.png', 'output_image3.jpg')
