import os
import sys
import zipfile
from pathlib import Path

def normalize(input_str):
    translit_mapping = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z',
        'и': 'i', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
        'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch',
        'ш': 'sh', 'щ': 'shch', 'ь': '', 'ю': 'iu', 'я': 'ia'
    }

    normalized_str = ''
    for char in input_str:
        if char.lower() in translit_mapping:
            normalized_str += translit_mapping[char.lower()]
        elif char.isalnum():
            normalized_str += char.lower()
        else:
            normalized_str += '_'

    return normalized_str

def get_archive_name_without_extension(file_path):
    return Path(file_path).stem

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

def categorize_and_move_file(file_path, destination_folder):
    category = categorize_file(file_path)
    print(f"Категоризація файлу: {file_path}, Категорія: {category}")

    sorted_folder_path = os.path.join(os.path.abspath(destination_folder), category)
    print(f"Шлях сортованої папки: {sorted_folder_path}")

    # Створіть папку, якщо вона не існує
    Path(sorted_folder_path).mkdir(parents=True, exist_ok=True)

    if category == 'archives':
        archive_name_without_extension = get_archive_name_without_extension(file_path)
        new_extraction_path = os.path.join(sorted_folder_path, normalize(archive_name_without_extension))
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(sorted_folder_path)
        os.rename(os.path.join(sorted_folder_path, archive_name_without_extension), new_extraction_path)
        return new_extraction_path
    else:
        normalized_name = normalize(os.path.basename(file_path))
        new_file_path = os.path.join(sorted_folder_path, normalized_name)
        os.rename(file_path, new_file_path)
        return new_file_path

def process_folder(folder_path):
    print(f"Обробка папки: {folder_path}")

    # Створити папку 'sorted' в вказаній директорії
    sorted_folder_path = os.path.join(folder_path, 'sorted')
    Path(sorted_folder_path).mkdir(parents=True, exist_ok=True)

    items = os.listdir(folder_path)

    for item in items:
        item_path = os.path.join(folder_path, item)

        if os.path.isfile(item_path):
            categorize_and_move_file(item_path, sorted_folder_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Використання: python DZ.py <шлях_папки>")
    else:
        folder_path = sys.argv[1]
        process_folder(folder_path)