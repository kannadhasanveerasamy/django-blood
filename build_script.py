import os
import shutil

# Specify the source directory where the built files are located
source_dir = "dist"

# Specify the target directory where you want to move the built files
target_dir = "build"

# Create the target directory if it doesn't exist
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# Move the built files from the source directory to the target directory
for file_name in os.listdir(source_dir):
    shutil.move(os.path.join(source_dir, file_name), os.path.join(target_dir, file_name))

print("Build process completed.")
