import os

def get_static_files_paths(app, *paths):
    file_paths = []

    for root, dirs, files in os.walk(os.path.join(app.root_path, "static", *paths)):
        for file in files:
            file_paths.append(os.path.join(root, file))
            
    return file_paths