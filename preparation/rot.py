from PIL import Image
import os

def rotate_images(input_folder, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):  # Check for image files
            image_path = os.path.join(input_folder, filename)
            img = Image.open(image_path)

            # Rotate by 90 degrees (counter-clockwise)
            rotated_img = img.rotate(90, expand=True)

            # Save the rotated image to the output folder
            output_path = os.path.join(output_folder, filename)
            rotated_img.save(output_path)
            print(f"Rotated and saved: {output_path}")

# Example usage
rotate_images('/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model v1.4/missing segment', 'output_folder')
