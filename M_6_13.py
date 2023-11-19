import shutil

def create_backup(path, file_name, employee_residence):
    file_path = path + '/' + file_name
    with open(file_path, 'wb') as file:
        for name, country in employee_residence.items():
            line = f"{name} {country}\n"
            file.write(line.encode('utf-8'))

    backup_folder_path = 'backup_folder'
    shutil.make_archive(backup_folder_path, 'zip', path)
    
    return path + '/' + 'backup_folder.zip'
        
            
    