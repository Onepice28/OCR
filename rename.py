import os

dataset_folder = 'dataset_normalized'
subfolders = [f for f in os.listdir(dataset_folder) if os.path.isdir(os.path.join(dataset_folder, f))]

for index, subfolder in enumerate(subfolders):
    old_name = os.path.join(dataset_folder, subfolder)
    new_name = os.path.join(dataset_folder, str(index))
    os.rename(old_name, new_name)

    print(f'Renamed: {old_name} -> {new_name}')
