from genericpath import isfile
import os
from pathlib import Path
from re import I
from tkinter import font
import pygame
import time 
import sys
import pandas as pd
import numpy as np
import shutil
from matplotlib import cm
from collections import Counter
from PIL import Image
import random
pygame.init()
def remove_targe_floder(remove_root,persist_floder):
    remove_floder=os.listdir(Path(remove_root))
    for i in persist_floder:
        if i in remove_floder:
            remove_floder.remove(i) 
    for remove_file in remove_floder:
        shutil.rmtree(os.path.join(remove_root,remove_file))
def move_file(font_path,old_path, new_path,random_num=300):
    filelist = os.listdir(os.path.join(old_path,font_path))  # 列出该目录下的所有文件,listdir返回的文件列表是不包含路径的。
    # print(filelist)
    old_path=os.path.join(old_path,font_path)
    new_path=os.path.join(new_path,font_path)
    n=len(filelist)
    random_list=[i for i in range (n)]   ##生成300个随机数
    random.shuffle(random_list)
    random_list=random_list[:random_num]
    for i in random_list:
        src = os.path.join(old_path, filelist[i])
        dst = os.path.join(new_path, filelist[i])
        shutil.copy(src, dst)
# def mkdir_font():
def makedir(c_path,file_flag=False):
    if  file_flag:
        c_path=os.path.dirname(c_path)
    if not os.path.exists(c_path):
        father_dir=os.path.dirname(c_path)
        if not  os.path.exists(father_dir):
            makedir(father_dir)    
        os.mkdir(c_path)
def split_datasets(font_path,train_path,test_path):
    # filelist = os.listdir(os.path.join(old_path,font_path)) 
    # old_path=os.path.join(old_path,font_path)
    # new_path=os.path.join(new_path,font_path)
    # for i in filelist:
    font_dirname=os.path.splitext(os.path.split(font_path)[-1])[-2]
    train_path=os.path.join(train_path,"train",font_dirname)
    # test_path=os.path.join(test_path,"test",font_dirname)
    makedir(train_path)
    # makedir(test_path)
    train_idx=len(os.listdir(train_path))
    # test_idx=len(os.listdir(test_path))

    shutil.copyfile(font_path,os.path.join(train_path,str(train_idx)+".png"))
    # shutil.copyfile(font_path,os.path.join(test_path,test_idx+".png"))

    
def font2image(input_file, output_paths,output_paths_test,characters, size=64):
    input_file_name = input_file.split(os.sep)[-1].split('.')[0]   # get output file_name
    output_path = os.path.join(output_paths, input_file_name)

    # output_path_test=os.path.join(output_paths_test, input_file_name)
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    # if not os.path.exists(output_path_test):
    #     os.mkdir(output_path_test)
    AZ = [chr(i) for i in range(0x0041,0x005A+1)]
    # aZ=[chr(i) for i in range (u'\u0041' <= uchar <= u'\u005a') or (u'\u0061' <= uchar <= u'\u007a'):]    
    file_sizes=[]    
    for word in characters:
        font = pygame.font.Font(input_file, size)
        rtext = font.render(word, True, (0, 0, 0), (255, 255, 255))#复写
        # if (u'\u0041' <= word <= u'\u005a') or (u'\u0061' <= word <= u'\u007a'):
        #     if word in AZ:      # for uppercase letter
        #         word = word+'+'
        #     pygame.image.save(rtext, os.path.join(output_path_test,word+".png"))
        #     continue
        # print(rtext._pixels_address)
        pygame.image.save(rtext, os.path.join(output_path,word+".png"))
        # new_path=output_path.split[]
        
    # remove_duplicated_images(output_path_test)
    # process_image(output_path_test, size)
    remove_duplicated_images(output_path)
    process_image(output_path, size)
    font_list=os.listdir(output_path)
    # train_save_dir=font_list.split('.')[0]
    # os.path.join(train_save_dir,word+".png")
    for font in font_list:
        # input_data=os.path.join(,)
        split_datasets(os.path.join(output_path,font),output_paths,output_paths_test)


def rename_dataset(sortfontlist,find_dir,targetpath=None):
    target_img=""
    target_path = find_dir if not  targetpath else targetpath
    # makedir(copy_dir)
    for line in open(sortfontlist, encoding='utf-8'):
        target_img+=line.strip()
    source_list=os.listdir(find_dir)
    for idx,i in enumerate(target_img):
        source_font=i
        new_name=str(idx)
        if  source_font in source_list:
            src = os.path.join(find_dir,source_font )
            dst = os.path.join(target_path, new_name)
            os.rename(src, dst)

def test_split(splitpath,testpath=None,ratio=0.8):
    if testpath:
        test_path=testpath
    else:
        test_path=os.path.join(os.path.dirname(splitpath),'test')
    for font_list in os.listdir(splitpath):
        tmp_font=os.listdir(os.path.join(splitpath,font_list))
        random.shuffle(tmp_font)
        total_num=len(tmp_font)*(1-ratio)
        for idx in range(int((total_num))):
            og_name=os.path.join(splitpath,font_list,tmp_font[idx])
            new_name=os.path.join(test_path,font_list,tmp_font[idx])
            makedir(new_name,file_flag=True)
            os.rename(og_name,new_name)
def remove_duplicated_images(path):
    while True:
        files = os.listdir(path)
        if len(files)==0:
            print('!!!!!!!!!!!!!!!!!!error:{}'.format(path))
            break
        file_sizes = []
        for file in files:
            file_size = os.path.getsize(os.path.join(path,file))
            file_sizes.append(file_size)
        counter = Counter(file_sizes)
        most_common_number = counter.most_common(1)[0][1]
        if most_common_number<=10:
            break
        most_common = counter.most_common(1)[0][0]
        for file in files:                                        # remove empty images
            file_path = os.path.join(path, file)
            if os.path.getsize(file_path)==most_common:
                os.remove(file_path)  
                
def load_image(path):
    image = Image.open(path).convert('L')
    image = np.array(image)
    return image

def cut_image(image):
    (h, w) = image.shape
    h_value = 255*h
    w_value = 255*w
    left = 0
    right = w
    upper = 0
    bottom = h
    for r in range(w):
        value = image[:, r].sum()
        if value==h_value:
            left += 1
        else:
            break
    for r in range(w-1, -1, -1):
        value = image[:,r].sum()
        if value==h_value:
            right -= 1
        else:
            break
    for c in range(h):
        value = image[c, :].sum()
        if value==w_value:
            upper += 1
        else:
            break
    for c in range(h-1, -1, -1):
        value = image[c, :].sum()
        if value==w_value:
            bottom -= 1
        else:
            break
    if left==w or right==0 or upper==h or bottom==0:
        left = 0
        right = w
        upper = 0
        bottom = h
    image_cut = image[upper:bottom, left:right]
    return image_cut

def resize_image(image_cut, size):
    (h, w) = image_cut.shape
    image_p = Image.fromarray(np.uint8(cm.gray(image_cut)*255))
    image_resized = image_p
    if h>w:
        if h>size:
            ratio = h/size
            adjust = int(w/ratio)
            if adjust<1:
                adjust=1
            image_resized = image_p.resize((adjust, size))
    else:
        if w>size:
            ratio = w/size
            adjust = int(h/ratio)
            if adjust<1:
                adjust=1
            image_resized = image_p.resize((size, adjust))
    return image_resized

def pad_image(image_resized, size):
    back = Image.new('L', (size, size), color=255)
    h_r, v_r = image_resized.size
    h = int((size-h_r)/2)
    v = int((size-v_r)/2)
    back.paste(image_resized,(h, v))
    return back

def process_image(path, size):
    files = os.listdir(path)
    for file in files:
        file_path = os.path.join(path, file)
        image = load_image(file_path)
        image = cut_image(image)
        image = resize_image(image, size)
        image = pad_image(image, size)
        image.save(file_path)
        
def remove_empty_floder(path):
    #清空没有文件的文件夹
    files = os.listdir(path)
    for file in files:
        if not os.listdir(os.path.join(path,file)):
            os.rmdir(os.path.join(path,file))
            print(file,' |removed')
    print("done!")
    
# check current font exists the given characters or not 
def check_image_exists(path, characters):
    AZ = [chr(i) for i in range(0x0041,0x005A+1)]  
    for word in characters:
        if word in AZ:      
            word = word+'+'
        image = word+'.png'
        image_path = os.path.join(path, image)
        if not os.path.exists(image_path):
            print('no ', word)
    print('done!')
