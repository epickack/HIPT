#save patch pngs

import h5py
#import numpy as np
import openslide
from openslide import open_slide
#from PIL import Image
import os
import pandas as pd

import webdataset as wds
import tqdm

main_dir = "/home/ivan/Documents/ai_models/patched_img_4096"
process_list_file = "process_list_autogen.csv"
svs_dir = "/media/ivan/external_drive/epithelioid_vascular_tumors/"
tar_savedir = "/home/ivan/Documents/ai_models/patched_img_4096/tar_patch_4096"
patch_size = 4096


def slide_to_tar(slide_id):
    sink = wds.TarWriter( os.path.join(tar_savedir, slide_id + ".tar"))

    with h5py.File( os.path.join(h5_dir, slide_id + ".h5"), "r") as f:
        # get first object name/key; may or may NOT be a group
        a_group_key = list(f.keys())[0]
    
        # this gets the object names in the group and returns as a list
        data = list(f[a_group_key])
        
    slide = open_slide( os.path.join(svs_dir, slide_id + ".svs"))
    
   
    for img_tuple in tqdm.tqdm(data):
        rep_tile = slide.read_region(img_tuple, 0, tuple([patch_size, patch_size]))
        rep_tile_rgb = rep_tile.convert("RGB")

        sink.write({
            "__key__": slide_id + "_" + str(img_tuple[0]) + "_" + str(img_tuple[1]),
            "image": rep_tile_rgb
            })
    
    sink.close()


process_list = pd.read_csv( os.path.join(main_dir, process_list_file))

slide_file_names = list(process_list["slide_id"])

h5_dir = os.path.join(main_dir, "patches")

for i in range(len(slide_file_names)):
    slide_id = slide_file_names[i].split(".")[0]
    print("\n\n" + str(i + 1) + "/" + str(len(slide_file_names)) )
    
    #check if tar file already saved in dir
    if os.path.exists(os.path.join(tar_savedir, slide_id + ".tar")):
        print(" " + slide_id + " already exists... \n")

    else:
        print(" Processing slide: " + str(slide_id) + "\n")
        slide_to_tar(slide_id)
        

    
    
    
    
    
    
    
    