from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os
from PIL import Image
import threading

def augment_images(source_folder_rgb, source_folder_mask, output_folder_rgb, output_folder_mask, size, index, resize=True):
    # Data generator for RGB images (with interpolation and rescaling)
    datagen_rgb = ImageDataGenerator(
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
        zoom_range=0.1,
        fill_mode='nearest',
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

    # Ensure output folders exist
    os.makedirs(output_folder_rgb, exist_ok=True)
    os.makedirs(output_folder_mask, exist_ok=True)

    # Get all file names from the RGB folder assuming both folders contain the same names
    files = [f for f in os.listdir(source_folder_rgb) if f.endswith('.png')]
    files = files[index[0]: index[1]]
    print(files)
    
    for file in files:
        # Construct paths
        file_path_rgb = os.path.join(source_folder_rgb, file)
        file_path_mask = os.path.join(source_folder_mask, file)
        
        # Load and resize images
        img_rgb = Image.open(file_path_rgb).convert('L').resize((size[0], size[1]))
        # img_rgb = Image.open(file_path_rgb).convert('L')256
        if resize:
            img_mask = Image.open(file_path_mask).resize((size[0], size[1]), resample=Image.NEAREST)  # Use nearest neighbor for masks
        else:
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
            Image.fromarray((batch_rgb[0, :, :, 0] * 255).astype('uint8')).save(os.path.join(output_folder_rgb, augmented_file_name))
            Image.fromarray(batch_mask[0].astype('uint8')).save(os.path.join(output_folder_mask, augmented_file_name))


def parallel_process_files(source_rgb, source_masked, output_rgb, output_masked, size, resize):
    # Get all files in the specified folder
    files = [f for f in os.listdir(source_rgb) if os.path.isfile(os.path.join(source_rgb, f))]
    total_files = len(files)
    
    # Determine the chunk size for each thread
    chunk_size = total_files // 8
    remainder = total_files % 8

    threads = []
    start_index = 0

    # Create 8 threads
    for i in range(16):
        # Calculate end index for each chunk
        end_index = start_index + chunk_size + (1 if i < remainder else 0)

        
        # Create a thread with the target function and 5 parameters
        thread = threading.Thread(target=augment_images, args=(source_rgb, source_masked, output_rgb, output_masked, size, (start_index, end_index), resize))
        threads.append(thread)
        
        # Start the thread
        thread.start()
        
        # Update start index for the next chunk
        start_index = end_index

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

# Define paths
source_folder_rgb = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model_v1.2/experiment_2/combined rgb/'
source_folder_mask = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model_v1.2/experiment_2/combined masked/'
output_folder_rgb = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model_v1.2/experiment_2/with_rotation/size 256/interpolated/augmented rgb/'
output_folder_mask = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model_v1.2/experiment_2/with_rotation/size 256/interpolated/augmented masked/'



# Run the function
# augment_images(source_folder_rgb, source_folder_mask, output_folder_rgb, output_folder_mask, (512, 512))
parallel_process_files(source_folder_rgb, source_folder_mask, output_folder_rgb, output_folder_mask, (256, 256), resize=True)