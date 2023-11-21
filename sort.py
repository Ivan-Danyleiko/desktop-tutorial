import os
import sys
import shutil

def normalize(input_str):
    translit_mapping = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z',
        'и': 'i', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
        'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch',
        'ш': 'sh', 'щ': 'shch', 'ь': '', 'ю': 'iu', 'я': 'ia'
    }

    name, extension = os.path.splitext(input_str)
    normalized_name = ''
    for char in name:
        if char.lower() in translit_mapping:
            normalized_name += translit_mapping[char.lower()]
        elif char.isalnum():
            normalized_name += char.lower()
        else:
            normalized_name += '_'

    return f"{normalized_name}{extension}"

def categorize_file(file_path):
    extension = file_path.split('.')[-1].upper()
    if extension in ('JPEG', 'PNG', 'JPG', 'SVG'):
        return 'images'
    elif extension in ('AVI', 'MP4', 'MOV', 'MKV'):
        return 'video'
    elif extension in ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'):
        return 'documents'
    elif extension in ('MP3', 'OGG', 'WAV', 'AMR'):
        return 'audio'
    elif extension in ('ZIP', 'GZ', 'TAR'):
        return 'archives'
    else:
        return 'unknown'

def process_folder(folder_path, destination_folder, empty_folders):
    print(f"Обробка папки: {folder_path}")

    items = os.listdir(folder_path)

    for item in items:
        item_path = os.path.join(folder_path, item)

        if os.path.isfile(item_path):
            destination = categorize_file(item_path)
            normalized_name = normalize(os.path.basename(item_path))

            if destination == 'unknown':
                extension = os.path.splitext(item)[1].lstrip('.').lower()
                normalized_name += f'.{extension}'

            new_file_path = os.path.join(destination_folder, destination, normalized_name)
            os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
            shutil.move(item_path, new_file_path)

        elif os.path.isdir(item_path):
            process_folder(item_path, destination_folder, empty_folders)

    # Перевірте, чи папка порожня після обробки файлів
    if not os.listdir(folder_path):
        empty_folders.append(folder_path)

def create_category_folders(root_folder, destination_folder):
    categories = ['images', 'video', 'documents', 'audio', 'archives', 'unknown']
    for category in categories:
        if category not in ['archives', 'video', 'audio', 'documents', 'images']:
            category_path = os.path.join(destination_folder, category)
            os.makedirs(category_path, exist_ok=True)

def remove_empty_folders(folder):
    for root, dirs, files in os.walk(folder, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                try:
                    os.rmdir(dir_path)
                    print(f"Порожню папку видалено: {dir_path}")
                except OSError as e:
                    print(f"Не вдалося видалити порожню папку {dir_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Використання: python <шлях_скрипта> <шлях_папки>")
    else:
        folder_path = sys.argv[1]
        destination_folder = folder_path  # Папка призначення - це головна директорія
        create_category_folders(folder_path, destination_folder)
        empty_folders = []  # Список порожніх папок для видалення
        process_folder(folder_path, destination_folder, empty_folders)
        remove_empty_folders(folder_path)
        remove_empty_folders(destination_folder)
