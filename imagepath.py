import os

image_dir = "documents/image_sample/Images1"
image_files = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]

# print paths
for image_file in image_files:
    print(image_file)