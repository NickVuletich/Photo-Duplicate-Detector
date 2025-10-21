# Date: 10-3-25
# File: main_v2.py
# Programmer: Nicholas M. Vuletich

import os
import json
import datetime
import hashlib
import time

"""
    I am going to take each folder and all files in it and put it in a list of of the filenames.
    Each list has all of the files in the main folder and all subfolders.

    I want to add where it can show how much storage you can save.

    I need to clean up the functions and see if i can simplify them.

    Maybe try and see if I can use this on my Iphone 
"""

#---------------helper functions---------------

def file_binary(file):
    with open (file, "rb") as bf:
        hash = bf.read()
        return hash
    
def write_json(target_list):
    with open("store.json", "w") as f:
        json.dump(target_list, f, indent=4)

#---------------Test functions---------------

def test_make_list(path):
    print("testing file_info.")
    file = path
    images, folders = sub_dir_files(file)
    
    for i in range(len(images)):
        print()
        print(images[i]["name"])  
        print(images[i]["path"])  
        print(images[i]["size"])  
        print(images[i]["hash"])
        print()  

    for i in range(len(folders)):
        print(folders[i]["dir"])
        print(folders[i]["dir_path"])

    print("done testing make_list!!")

#---------------Main functions---------------
        
# Finds files in base dir
def make_list(folder_path):
    """
    At the End make it take in a list fo files at the peramater not search 
    """
    processed = 0
    image_files = []
    folders = []
    for entry in os.scandir(folder_path):
        if entry.name.startswith('.'):
            continue
        if entry.is_file() and entry.name.lower().endswith(('.mp4', '.mov')):
        #if entry.is_file() and entry.name.lower().endswith(('.jpg', '.png' , 'jpeg', '.heic', '.heif', '.arw', '.dng', '.nef', '.tiff', '.tif', '.webp', '.gif', '.bmp', '.cr2', '.cr3', '.orf', '.rw2', '.raf')):
            path = os.path.normpath(entry)
            size_mb = entry.stat().st_size / (1024 * 1024)
            hash_obj = hashlib.md5(file_binary(entry))
            hash = hash_obj.hexdigest()
            image_files.append({
                "name": entry.name,
                "path": path,
                "size": size_mb,
                "hash": hash

            })
        
        if entry.is_dir():
            dir_path = os.path.normpath(entry)
            folders.append({
                "dir": entry,
                "dir_path": dir_path
            })

    return image_files, folders
    

def sub_dir_files(folder):
    master_images = []
    master_folders = []
    image_files, folders= make_list(folder)
    master_images.extend(image_files)
    master_folders.extend(folders)
    for subdir in master_folders:
        sub_images, sub_folders= make_list(subdir["dir_path"])
        master_images.extend(sub_images)
        master_folders.extend(sub_folders)
    
    return master_images, master_folders

def compare(path):
    print("Running Compare...")
    master_list, _ = sub_dir_files(path)
    seen_hashs = set()
    duplicates = []
    total_size = 0

    for item in master_list:
        if item["hash"] in seen_hashs:
            total_size += item["size"]
            duplicates.append(item)
        else:
            seen_hashs.add(item["hash"])
    #print(seen_hashs)
    print(f"Total size that can be freed is {total_size:.2f} Mb.")
    write_json(duplicates)



#----------main----------
if __name__ == "__main__":
    start_time = time.time()
    compare("/Volumes/2TB SSD")
    elapsed = time.time() - start_time
    print(f"Total time elapsed {elapsed:.2f}.")
    print("Done running!!!")

#----------List of Folders to test----------
"""
    "/Users/nickv/Desktop/Files"
    "/Users/nickv/Desktop/untitled folder"
"""