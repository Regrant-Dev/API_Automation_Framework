import os
import shutil


def handle_file_transfer(env_config):
    try:
        test_folder = 'TEST_FOLDER'

        # Check if the test_list is provided and not empty
        if not env_config.get('test_list'):
            return

        if not os.path.exists(test_folder):
            os.makedirs(test_folder)

        for item in env_config['test_list']:
            if os.path.exists(item):
                dest_path = os.path.join(test_folder, os.path.basename(item))
                if os.path.isdir(item):
                    # Handle directories
                    if env_config['transfer_method'] == 'copy':
                        shutil.copytree(item, dest_path)
                    elif env_config['transfer_method'] == 'move':
                        shutil.move(item, dest_path)
                else:
                    # Handle files
                    if env_config['transfer_method'] == 'copy':
                        shutil.copy(item, test_folder)
                    elif env_config['transfer_method'] == 'move':
                        shutil.move(item, test_folder)
            else:
                print(f"Path not found: {item}")
    except Exception as e:
        handle_file_transfer_cleanup(env_config)
        raise Exception(str(e))


def handle_file_transfer_cleanup(env_config):
    test_folder = 'TEST_FOLDER'

    # Check if the test_list is provided and not empty
    if not env_config.get('test_list'):
        return

    if env_config['transfer_method'] == 'move':
        for item in env_config['test_list']:
            # Construct the move path
            moved_item_path = os.path.join(test_folder, os.path.basename(item))

            # Delete __pycache__ directories in the moved path item
            if os.path.isdir(moved_item_path):
                for root, dirs, files in os.walk(moved_item_path):
                    if '__pycache__' in dirs:
                        shutil.rmtree(os.path.join(root, '__pycache__'))

            # Move the item back
            if os.path.exists(moved_item_path):
                target_path = item if os.path.isfile(item) else os.path.join(
                    os.path.dirname(item), os.path.basename(moved_item_path))
                shutil.move(moved_item_path, target_path)
            else:
                print(f"Path not found for cleanup: {moved_item_path}")

    # Remove the TEST_FOLDER
    if os.path.exists(test_folder):
        shutil.rmtree(test_folder)
    else:
        print(f"{test_folder} not found for cleanup")
