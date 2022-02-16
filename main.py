import cv2 as cv
import os

def processing(file_name):
    img = cv.imread(file_name)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    result = cv.adaptiveThreshold(img, 255, 
        cv.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv.THRESH_BINARY, 27, 4)
    return result


if __name__ == "__main__":

    source_path = "source"
    result_path = "result"
 
    for file_name in os.listdir(source_path):
        try:
            result = processing(source_path + "/" + file_name)
            cv.imwrite(result_path + "/" + file_name, result, (cv.IMWRITE_JPEG_QUALITY, 30))
        except os.error:
            print(f"File {file_name} can not be processed.")
    