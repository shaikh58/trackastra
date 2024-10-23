# import os
# import tifffile
# import shutil

# base_dir = '/root/vast/mustafa/trackastra/data/lysosomes'

# for dir_name in os.listdir(base_dir):
#     dir_path = os.path.join(base_dir, dir_name)
    
#     # Check if it's a directory
#     if not os.path.isdir(dir_path):
#         continue
    
#     # Get all .tiff files in the directory
#     tiff_files = [f for f in os.listdir(dir_path) if f.endswith('.tiff') or f.endswith('.tif')]
    
#     # If there's only one .tiff file
#     if len(tiff_files) == 1:
#         tiff_file = tiff_files[0]
#         tiff_path = os.path.join(dir_path, tiff_file)
        
#         print(f"Processing {tiff_path}")
        
#         # Read the TIFF file
#         with tifffile.TiffFile(tiff_path) as tif:
#             for i, page in enumerate(tif.pages):
#                 # Create a new filename for each frame
#                 new_filename = f"{os.path.splitext(tiff_file)[0]}_frame_{i:04d}.tiff"
#                 new_filepath = os.path.join(dir_path, new_filename)
                
#                 # Save each frame as a separate TIFF file
#                 tifffile.imwrite(new_filepath, page.asarray())
                
#                 print(f"Created {new_filename}")
        
#         # Delete the original file
#         # os.remove(tiff_path)
#         print(f"Deleted original file: {tiff_file}")
    
#     else:
#         print(f"Skipping {dir_path}: Found {len(tiff_files)} .tiff files")

# print("Processing complete.")

import os
import glob

# Set the base directory
base_dir = '/root/vast/mustafa/trackastra/data/lysosomes'

# Loop through all directories ending with '_tiffs'
for dir_path in glob.glob(os.path.join(base_dir, '*_tiffs')):
    if os.path.isdir(dir_path):
        print(f"Processing directory: {dir_path}")
        
        # Find all .tif files in the directory
        tif_files = glob.glob(os.path.join(dir_path, '*.tif'))
        
        # Delete each .tif file
        for tif_file in tif_files:
            try:
                os.remove(tif_file)
                print(f"Deleted: {tif_file}")
            except Exception as e:
                print(f"Error deleting {tif_file}: {str(e)}")
        
        print(f"Finished processing {dir_path}")
        print("------------------------")

print("All directories processed.")