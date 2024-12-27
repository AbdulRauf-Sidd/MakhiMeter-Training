from PIL import Image
import os

def process_images(folder_path, output_folder):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):  # Process image files only
            image_path = os.path.join(folder_path, filename)
            img = Image.open(image_path).convert('L')  # Convert to grayscale

            # Process each pixel
            img = img.point(lambda p: 255 if p == 255 else 0)

            # Save the processed image
            output_path = os.path.join(output_folder, filename)
            img.save(output_path)

            print(f"Processed: {filename}")

# Example usage
process_images('/home/abdulrauf/Projects/MakhiMeter-Training/data/brain/masked aug', '/home/abdulrauf/Projects/MakhiMeter-Training/data/brain/masked aug 2')
