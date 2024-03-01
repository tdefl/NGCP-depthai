import supervision as sv

image_paths = sv.list_files_with_extensions(
    directory="images/",
    extensions=["png", "jpg", "jpg"])

print('image count:', len(image_paths))