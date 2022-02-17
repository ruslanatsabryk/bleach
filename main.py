import cv2 as cv
import os
import numpy as np
from multiprocessing import Pool
 

def read_img(file_name):
    # Read the image with the file_name if it contains non-ascii characters
    # to avoid errors in cv.imread(file_name) 
    img = cv.imdecode(np.fromfile(file_name, dtype=np.uint8), cv.IMREAD_UNCHANGED)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    return img


def bleach_img(img):
    result = cv.adaptiveThreshold(img, 255, 
        cv.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv.THRESH_BINARY, 27, 4)
    return result


def save_img(img, file_name):
    is_success, nd_arr = cv.imencode(".jpg", img)
    if is_success:
        nd_arr.tofile(file_name)


def process_img(source_file_name, dest_file_name):
    print("process_img" , source_file_name, dest_file_name)
    img = read_img(source_file_name)
    result = bleach_img(img)
    save_img(result, dest_file_name)
    return "Success!"


def user_input():
    folder = input("\nInput path to the source folder with images \
        \n(destination folder with name '/bleached' will be created inside it): \n\nSource folder> ")

    source_folder = folder.replace("\\", "/")
    print(f"Source folder: \n{source_folder}")
    dest_folder = source_folder + "/bleached"
    print(f"Destination folder: \n{dest_folder}")

    if not os.path.isdir(source_folder):
        print(f"Source folder {source_folder} does not exist!")
        os.exit()
    
    return source_folder, dest_folder


def create_dest_folder(dest_folder):
        try: 
            os.mkdir(dest_folder)
        except FileExistsError:
            pass
        except Exception as e:
            print("An error occurred while creating the destination directory: \n{e}")
            os.exit()

def map_file_names(source_folder, dest_folder):
    for file_name in os.listdir(source_folder):
        source_file_name = source_folder + "/" + file_name
        if not os.path.isfile(source_file_name):
                continue
        
        dest_file_name = dest_folder + "/" + file_name
        yield (source_file_name, dest_file_name)
    



if __name__ == "__main__":

    source_folder, dest_folder = user_input()
    create_dest_folder(dest_folder)

    with Pool() as pool:
        pool.starmap(process_img, map_file_names(source_folder, dest_folder))
        

        
