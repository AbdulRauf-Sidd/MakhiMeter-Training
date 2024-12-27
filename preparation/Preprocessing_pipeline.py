import os
import cv2
import PIL
import os
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
import threading
from rembg import remove
from PIL import Image
import numpy as np
import io
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import time




class preprocess:
    def __init__(self, train_dir, mask_dir, out_train_dir, out_mask_dir, size, no_augment, resize):
        self.train_dir = train_dir;
        self.mask_dir = mask_dir;
        self.out_train_dir = out_train_dir;
        self.out_mask_dir = out_mask_dir;
        self.size = size;
        self.no_augment = no_augment;
        self.resize = resize;
    
        os.makedirs(self.out_train_dir, exist_ok=True);
        os.makedirs(self.out_mask_dir, exist_ok=True);

    def background_removal(self, replace):
        files = [f for f in os.listdir(self.train_dir) if f.endswith('.png') or f.endswith('.jpg')];
        
        print(f"Removing background from training dataset...");

        for file in files:
            # Construct paths (input and output paths will have the same name)
            input_path = os.path.join(self.train_dir, file);
            if replace:
                output_path = os.path.join(self.train_dir, file);
            else:
                output_path = os.path.join(self.out_train_dir + '_temp1', file);

            with open(input_path, 'rb') as input_file:
                input_image = input_file.read()
            # Remove background
            output_image = remove(input_image)

            # Convert the result to a grayscale image (removes alpha channel)
            if self.resize:
                img = Image.open(io.BytesIO(output_image)).convert('L').resize((self.size[0], self.size[1]))
            else:
                img = Image.open(io.BytesIO(output_image)).convert('L')
            # Save the processed image with the same name as input
            img.save(output_path)

        print(f"Background from training dataset removed.")


    def flip(self, replace):
        if replace:
            path = self.train_dir
        else:
            path = self.out_train_dir + '_temp1'

        files = [f for f in os.listdir(path) if f.endswith('.png') or f.endswith('.jpg') or f.endswith('.tiff')]
    
        for file in files:
            # Construct paths
            file_path_rgb = os.path.join(path, file)
            file_path_mask = os.path.join(self.mask_dir, file)

            # Load images without resizing or converting to grayscale
            img_rgb = Image.open(file_path_rgb)
            if self.resize:
                img_mask = Image.open(file_path_mask).resize((self.size[0], self.size[1]), resample=Image.NEAREST)
            else:
                img_mask = Image.open(file_path_mask)

            # Convert images to arrays
            img_rgb = np.array(img_rgb)
            img_mask = np.array(img_mask)

            # Define rotation angles
            angles = [90, 180, 270]

            for angle in angles:
                # Rotate RGB and mask images by the specified angle
                rotated_rgb = np.rot90(img_rgb, k=angle // 90)  # Rotate by 90, 180, or 270 degrees
                rotated_mask = np.rot90(img_mask, k=angle // 90)

                # Convert rotated arrays back to images
                rotated_rgb_image = Image.fromarray(rotated_rgb)
                rotated_mask_image = Image.fromarray(rotated_mask)

                # Save rotated images with consistent naming
                rotated_rgb_image.save(os.path.join(self.out_train_dir, f'rot_{angle}_{file}'))
                rotated_mask_image.save(os.path.join(self.out_mask_dir, f'rot_{angle}_{file}'))


    def augmentation(self, replace):
        datagen_rgb = ImageDataGenerator(
            rotation_range=15,
            width_shift_range=0.1,
            height_shift_range=0.1,
            zoom_range=0.1,
            fill_mode='constant',
            cval=0,
            rescale=1./255  # Rescaling only applies to RGB images
        )

        # Data generator for mask images (without interpolation and no rescaling)
        datagen_mask = ImageDataGenerator(
            rotation_range=15,
            width_shift_range=0.1,
            height_shift_range=0.1,
            zoom_range=0.1,
            fill_mode='constant',
            cval=0  # No interpolation to keep class values intact
        )

        # Get all file names from the RGB folder assuming both folders contain the same names
        files = [f for f in os.listdir(self.out_train_dir) if f.endswith('.png')]

        print('Augmenting dataset...')

        for file in files:
            # Construct paths
            file_path_rgb = os.path.join(self.out_train_dir, file)
            file_path_mask = os.path.join(self.out_mask_dir, file)

            # Load and resize images
            img_rgb = Image.open(file_path_rgb)
            # img_rgb = Image.open(file_path_rgb).convert('L')256
            img_mask = Image.open(file_path_mask)

            # Convert images to arrays
            img_rgb = np.array(img_rgb)
            img_mask = np.array(img_mask)

            # Reshape for data generator
            img_rgb = img_rgb.reshape((1,) + img_rgb.shape + (1,))  # Adding channel dimension for grayscale
            img_mask = img_mask.reshape((1,) + img_mask.shape)  # Adding channel dimension for grayscale mask

            print(img_rgb.shape, img_mask.shape)
            # Generate augmented images
            rgb_gen = datagen_rgb.flow(img_rgb, batch_size=1, seed=42)
            mask_gen = datagen_mask.flow(img_mask, batch_size=1, seed=42)

            for i in range(10):  # Generate 10 augmented images per input image
                batch_rgb = rgb_gen.__next__()
                batch_mask = mask_gen.__next__()

                # Save augmented images with consistent naming
                augmented_file_name = f'aug_{i}_{file}'
                Image.fromarray((batch_rgb[0, :, :, 0] * 255).astype('uint8')).save(os.path.join(self.out_train_dir, augmented_file_name))
                Image.fromarray(batch_mask[0].astype('uint8')).save(os.path.join(self.out_mask_dir, augmented_file_name))


    def classes_only(self, replace):
        hex_colors = ['00ff00', 'ff0000', '0000ff', '1d19b5', 'ffff00', 'ff00ff', '00ffff',
              '691369']  # Example hex colors
        
        print('reducing masks to classes only...');

        allowed_colors = [tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) for hex_color in hex_colors]
        # Loop through all files in the directory
        for filename in os.listdir(self.out_mask_dir):
            if filename.endswith(".png"):  # Check if the file is an image, adjust as needed for other formats
                print("hi")
                file_path = os.path.join(self.out_mask_dir, filename)
                image = Image.open(file_path)
                pixels = image.load()


                # Process each pixel
                for i in range(image.width):
                    for j in range(image.height):
                        if pixels[i, j][:3] not in allowed_colors:  # Check if the pixel color is not allowed
                            pixels[i, j] = (0, 0, 0)  # Set non-matching pixels to black

                # Save the modified image
                image.save(file_path)  # Overwrite the original image

        print('masks reduced to classes only');


    def label_encode(self, replace):
        print('encoding images...');

        label_mapping = {
            0: 0,
            43: 1,
            54: 2,
            76: 3,
            105: 4,
            149: 5,
            178: 6,
            225: 7,
        }

        # Path to the folder containing the images

        # Get all image file names in the folder
        files = [f for f in os.listdir(self.out_mask_dir) if f.endswith('.png')]

        # Function to apply label encoding to each image
        def label_encode_image(image, label_mapping):
            # unique_pixel_values = set()
            # image_array = np.array(image)

            #     # Get unique pixel values and update the set
            # unique_values = np.unique(image_array)
            # unique_pixel_values.update(unique_values)
            # print(unique_pixel_values)
            # Create a copy of the image to modify
            encoded_image = image.copy()

            # Loop over the label mapping and replace the original pixel values
            for original_value, encoded_value in label_mapping.items():
                encoded_image[image == original_value] = encoded_value

            return encoded_image

        # Process each image
        for file in files:
            file_path = os.path.join(self.out_mask_dir, file)

            # Read the image in grayscale
            image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

            # Apply label encoding
            encoded_image = label_encode_image(image, label_mapping)

            # Save the encoded image, replacing the original one
            Image.fromarray(encoded_image).save(file_path)

        print("Label encoding completed")

    def unique_values(self):
        unique_pixel_values = set()
    
        # Get all image file names in the folder
        files = [f for f in os.listdir(self.out_mask_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]

        for file in files:
            # Construct the full file path
            file_path = os.path.join(self.out_mask_dir, file)

            # Read the image using OpenCV and convert it to grayscale
            image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

            # Get unique pixel values and update the set
            unique_values = np.unique(image)
            unique_pixel_values.update(unique_values)

        # Print the combined set of unique pixel values
        print(f"Unique pixel values across all images: {unique_pixel_values}")

    
    def run(self, replace):
        self.background_removal(replace)
        self.flip(replace)
        self.augmentation(replace)
        self.classes_only(replace)
        self.label_encode(replace)
        self.unique_values()

source_folder_rgb = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model_v1.2/experiment_2/combined rgb/'
source_folder_mask = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model_v1.2/experiment_2/combined masked/'
output_folder_rgb = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model_v1.2/experiment_2/test_augmented rgb/'
output_folder_mask = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model_v1.2/experiment_2/test_augmented masked/'


obj = preprocess(source_folder_rgb, source_folder_mask, output_folder_rgb, output_folder_mask, (256, 256), 10, True)
# Start the timer
start_time = time.time()
obj.run(True)
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time
print(f"The code took {elapsed_time:.6f} seconds to run.")