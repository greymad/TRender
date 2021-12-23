import glob
from io import FileIO
import numpy as np
import sys
import argparse
from PIL import Image
import os 

  

def list_jpeg_files(target_folder):
    target = target_folder + "**/*.jpg"
    print(target)
    jpgFilenamesList = glob.glob(target,recursive=True);
    return jpgFilenamesList

def merge_images(file_list):
    # Opening the primary image (used in background)
    
  
    for m in file_list:
        img1 = Image.open("background.png")
        img2 = Image.open(m)
        img1.paste(img2, (10,10))
        
        fname = os.path.dirname(m) +"/"+ os.path.basename(m)[0:-3] +"png";
        print("saving " + fname)
        img1.save(fname);
        os.remove(m);
        
        

def main(target_folder,width,height):
    files = list_jpeg_files(target_folder);
    merge_images(files);

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('targetfolder', metavar='Target Folder', type=str, help='top folder of images')
    parser.add_argument('width', type =int,help='Target Width ')
    parser.add_argument('height', type =int,help='Target height')

    args = parser.parse_args()
           
    main(sys.argv[1],sys.argv[2],sys.argv[3])



