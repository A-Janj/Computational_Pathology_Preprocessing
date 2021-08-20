print("Bismillah")

import glob
import cv2
import numpy as np
from tiatoolbox.wsicore import wsireader
from tqdm import tqdm


# %load_ext autotime

mask_path = "E:\\MyPipeline\\WSI_masks\\pahla folder\\10H21651_A1H_E_1/*.png"
sample_wsi_path = "E:\\MyPipeline\\WSIs/10H21651_A1H_E_1.jp2"

WSI_name = "10H21651_A1H_E_1"
class_selected = "Lymphocytes"

classes_per_WSI = glob.glob(mask_path)
print(classes_per_WSI)
class_sel = classes_per_WSI[0]
print(class_sel)
mask_img = cv2.imread(class_sel, 0)
# plt.imshow(mask_img)
# plt.show()

print(mask_img.shape)
row = mask_img.shape[1]
col = mask_img.shape[0]

patch_size = 16 # 16 * (2**level = 8) = 128 hi resolution patch
overlap_percent = 50
overlap = overlap_percent/100

# print(mask_img[0, 0])
# print(np.any(mask_img))
# print(np.unique(mask_img))

list_indices = []
stride = int(patch_size * overlap)
for x in tqdm(range(0, row, stride)):
    for y in range(0, col, stride):
        non_zero_patch = np.any(mask_img[x:x+patch_size, y:y+patch_size])
        # print(non_zero_patch)
        if non_zero_patch:
            cord = [x, y]
            list_indices.append(cord)
        # print(x,y)
else:
    print("Patch indices extracted from mask image!")
    print("Number of patches", len(list_indices))

# print(np.any(mask_img[22000:100, 50:100]))

low_res = 1.25
high_res = 40
objective_level = 0

wsi_reader_v1 = wsireader.get_wsireader(
                input_img=sample_wsi_path)

multiply_by = int(wsi_reader_v1.slide_dimensions(resolution=high_res, units='power')[0] / row)
print("rows of wsi", wsi_reader_v1.slide_dimensions(resolution=high_res, units='power')[0])
print("rows of mask", mask_img.shape[1])
print("multiply by", multiply_by)

hires_patch_size = patch_size * multiply_by
list_indices = np.array(list_indices) * multiply_by

startAT = 0
for i, index in tqdm(enumerate(list_indices[startAT:])):
    # coord = np.array(index) * multiply_by
    # print(index)
    # print(coord)
    image_patch = wsi_reader_v1.read_region(
                location=index[::-1],
                level=objective_level, size=hires_patch_size)
    filename= "E:/MyPipeline/single_WSI/patchesChk/"+WSI_name+"_class_"+class_selected+"_level"+str(objective_level)+"_x"+str(index[0])+"_y"+str(index[1])+"_numb"+str(i)+".png"
    cv2.imwrite(filename=filename, img=image_patch)
else:
    print("Images written.")

# print(type(hi))
# plt.imshow(hi)
# plt.show()
