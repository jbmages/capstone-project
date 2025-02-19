def dataset_download():
    # Download dataset from kagglehub
    path = kagglehub.dataset_download("tunguz/big-five-personality-test")
    print(path)
    print("Dataset path:", path)

    # Specify target directory for data
    target_folder = 'Data/'
    os.makedirs(target_folder, exist_ok=True)

    # Check the contents of the dataset path
    print("Files in the dataset:", os.listdir(path))

    for file_name in os.listdir(path):
        source = os.path.join(path, file_name)
        destination = os.path.join(target_folder, file_name)
        
        # Check if the file exists
        if os.path.exists(source):
            shutil.move(source, destination)
            print(f"Moved {file_name} to {target_folder}")
        else:
            print(f"File does not exist: {source}")

    print("Dataset moved to:", target_folder)
    return