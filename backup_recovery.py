import os
import shutil
import hashlib
from cryptography.fernet import Fernet

def encrypt_file(key, file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)

def decrypt_file(key, file_path):
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data)
    with open(file_path, 'wb') as file:
        file.write(decrypted_data)

def backup_data(source_dir, destination_dir, encryption_key):
    # Create a temporary directory to store encrypted backup files
    temp_dir = os.path.join(destination_dir, "temp")
    os.makedirs(temp_dir, exist_ok=True)
    
    # Iterate through files in the source directory
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            source_file = os.path.join(root, file)

            # Encrypt the source file and copy it to the temporary directory
            encrypted_file = os.path.join(temp_dir, file)
            encrypt_file(encryption_key, source_file)
            shutil.copy2(source_file, encrypted_file)
    
    # Move the encrypted backup files to the destination directory
    for file in os.listdir(temp_dir):
        shutil.move(os.path.join(temp_dir, file), os.path.join(destination_dir, file))
    
    # Delete the temporary directory
    shutil.rmtree(temp_dir)

def verify_integrity(source_dir, destination_dir, encryption_key):
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            source_file = os.path.join(root, file)
            destination_file = os.path.join(destination_dir, file)
            
            # Decrypt the backup file for integrity check
            decrypt_file(encryption_key, destination_file)
            
            # Calculate hash of the source file
            with open(source_file, 'rb') as file:
                source_hash = hashlib.sha256(file.read()).hexdigest()
            
            # Calculate hash of the decrypted destination file
            with open(destination_file, 'rb') as file:
                destination_hash = hashlib.sha256(file.read()).hexdigest()
            
            # Compare the hashes
            if source_hash != destination_hash:
                print(f"Integrity check failed for {destination_file}")
        
            # Encrypt the destination file again
            encrypt_file(encryption_key, destination_file)

encryption_key = Fernet.generate_key()

source_dir = '/home/user/Documents/important_files'
destination_dir = '/mnt/backup_drive'

# Backup data
backup_data(source_dir, destination_dir, encryption_key)

# Verify integrity
verify_integrity(source_dir, destination_dir, encryption_key
