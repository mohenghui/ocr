
from pathlib import Path
from utils import *

from tqdm import tqdm
txt=""
sorted_txt="sortfont.txt"
for line in open(sorted_txt, encoding='utf-8'):
    txt+=line.strip()
# print(txt)
common_list = txt
# print(common_list)
#
font_file = './ttf2img/ttf_save/'
image_file_train= './ttf2img/img_save'
image_file_test='./ttf2img/img_save_test'
persist_floder=["train","test"]
if os.path.exists(image_file_train):
    shutil.rmtree(image_file_train)
os.mkdir(image_file_train)
if os.path.exists(image_file_test):
    shutil.rmtree(image_file_test)
# os.mkdir(image_file_test)
fonts = os.listdir(font_file)
for idx in tqdm(range(len(fonts))):
    font_path = os.path.join(font_file, fonts[idx])
    # try:
    font2image(font_path, image_file_train, image_file_test,common_list)


    # except:
    #     print(font+' failed!!!!!!!!!!!!!!!!!!')
    # move_file(font.split(".")[0],image_file_train,image_file_test,1000)
rename_dataset(sorted_txt,os.path.join(image_file_train,"train"))
split_path=os.path.join(image_file_train,"train")
test_split(split_path,ratio=0.9)
# remove_empty_floder(image_file_train)


remove_targe_floder(image_file_train,persist_floder)