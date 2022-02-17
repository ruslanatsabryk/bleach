import cv2 as cv
import os
import numpy as np

def process_img(file_name):

    # Read the image with the file_name if it contains non-ascii characters
    # to avoid errors in cv.imread(file_name) 
    img = cv.imdecode(np.fromfile(file_name, dtype=np.uint8), cv.IMREAD_UNCHANGED)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    result = cv.adaptiveThreshold(img, 255, 
        cv.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv.THRESH_BINARY, 27, 4)
    return result

def save_img(img, file_name):
    is_success, nd_arr = cv.imencode(".jpg", img)
    if is_success:
        nd_arr.tofile(file_name)
    # cv.imwrite(file_name, img, (cv.IMWRITE_JPEG_QUALITY, 80))


if __name__ == "__main__":

    source_path = input("\nInput path to the source folder with images \n(destination folder with name '/bleached' will be created inside it): \n\nSource folder> ")
    # norm_path = os.path.normcase(source_path)
    norm_path = source_path.replace("\\", "/")
    print(norm_path)
    dest_path = norm_path + "/bleached"
    print(dest_path)

    if os.path.isdir(norm_path):
        
        try: 
            os.mkdir(dest_path)
        except FileExistsError:
            pass
        except Exception as e:
            print("An error occurred while creating the destination directory: \n{e}")
    
    else:
        print(f"Source folder {source_path} does not exist!")
        os.exit()
    
    for file_name in os.listdir(norm_path):
        source_file_name = norm_path + "/" + file_name
        
        if not os.path.isfile(source_file_name):
                continue
        
        dest_file_name = dest_path + "/" + file_name
        print(f"{dest_file_name}")
        
        result_img = process_img(source_file_name)
        save_img(result_img, dest_file_name)
        
        

    