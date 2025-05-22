import os
from PIL import Image
from io import BytesIO
from tkinter import Tk, filedialog

# Configs
MAX_DIM = 2000
MAX_SIZE = 2 * 1024 * 1024
SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png')

def select_folder():
    root = Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Select the Folder Containing Images")
    return folder

def resize_and_compress(input_path, output_path):
    with Image.open(input_path).convert("RGB") as img:
        img.thumbnail((MAX_DIM, MAX_DIM))
        buffer = BytesIO()

        low, high = 10, 95
        while low <= high:
            mid = (low + high) // 2
            buffer.seek(0)
            buffer.truncate()
            img.save(buffer, format='JPEG', quality=mid, optimize=True)
            if buffer.tell() <= MAX_SIZE:
                low = mid + 1
            else:
                high = mid - 1

        with open(output_path, 'wb') as f:
            f.write(buffer.getvalue())

def process_recursive(input_root):
    output_root = input_root.rstrip('/\\') + "_compressed"

    for root, _, files in os.walk(input_root):
        rel_path = os.path.relpath(root, input_root)
        output_dir = os.path.join(output_root, rel_path)
        os.makedirs(output_dir, exist_ok=True)

        for filename in files:
            if filename.lower().endswith(SUPPORTED_FORMATS):
                input_file = os.path.join(root, filename)
                output_file = os.path.join(output_dir, filename)
                try:
                    resize_and_compress(input_file, output_file)
                    print(f"Processed: {os.path.join(rel_path, filename)}")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")

    print(f"\n✅ All done! Compressed folder: {output_root}")

if __name__ == '__main__':
    folder = select_folder()
    if folder:
        process_recursive(folder)
    else:
        print("❌ No folder selected.")
