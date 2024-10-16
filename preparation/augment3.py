from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os
from PIL import Image

def augment_images(source_folder_rgb, source_folder_mask, output_folder_rgb, output_folder_mask):
    # Data generator for RGB images (with interpolation and rescaling)
    datagen_rgb = ImageDataGenerator(
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        zoom_range=0.2,
        fill_mode='constant',
        cval=0,
        rescale=1./255  # Rescaling only applies to RGB images
    )
    
    # Data generator for mask images (without interpolation and no rescaling)
    datagen_mask = ImageDataGenerator(
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        zoom_range=0.2,
        fill_mode='constant',
        cval=0  # No interpolation to keep class values intact
    )

    # Ensure output folders exist
    os.makedirs(output_folder_rgb, exist_ok=True)
    os.makedirs(output_folder_mask, exist_ok=True)

    # Get all file names from the RGB folder assuming both folders contain the same names
    files = [f for f in os.listdir(source_folder_rgb) if f.endswith('.png')]
    print(files)
    
    for file in files:
        # Construct paths
        file_path_rgb = os.path.join(source_folder_rgb, file)
        file_path_mask = os.path.join(source_folder_mask, file)
        
        # Load and resize images
        img_rgb = Image.open(file_path_rgb).resize((256, 256))
        img_mask = Image.open(file_path_mask).resize((256, 256), resample=Image.NEAREST)  # Use nearest neighbor for masks
        
        # Convert images to arrays
        img_rgb = np.array(img_rgb)
        img_mask = np.array(img_mask)
        
        # Reshape for data generator
        img_rgb = img_rgb.reshape((1,) + img_rgb.shape)
        img_mask = img_mask.reshape((1,) + img_mask.shape)
        print(img_rgb.shape, img_mask.shape)
        # Generate augmented images
        rgb_gen = datagen_rgb.flow(img_rgb, batch_size=1, seed=42)
        mask_gen = datagen_mask.flow(img_mask, batch_size=1, seed=42)

        for i in range(10):  # Generate 10 augmented images per input image
            batch_rgb = rgb_gen.__next__()
            batch_mask = mask_gen.__next__()

            # Save augmented images with consistent naming
            augmented_file_name = f'aug_{i}_{file}'
            Image.fromarray((batch_rgb[0] * 255).astype('uint8')).save(os.path.join(output_folder_rgb, augmented_file_name))
            Image.fromarray(batch_mask[0].astype('uint8')).save(os.path.join(output_folder_mask, augmented_file_name))

# Define paths
source_folder_rgb = 'version/training/defected'
source_folder_mask = 'version/training/defected masked'
output_folder_rgb = 'version/training/defected (256)'
output_folder_mask = 'version/training/defected masked (256)'

# Run the function
augment_images(source_folder_rgb, source_folder_mask, output_folder_rgb, output_folder_mask)
