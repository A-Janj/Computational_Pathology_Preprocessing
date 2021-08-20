print("Bismillah")

from histolab.slide import Slide
import glob
import os
from histolab.tiler import GridTiler

BASE_PATH = "D:\\Downloads\\WSIs"

WSI_path= "D:\\Downloads\\WSIs/*.svs"
WSI_paths = glob.glob(WSI_path)
for path in WSI_paths:

   PROCESS_PATH_TCGA = os.path.join(BASE_PATH, 'TCGA')
   breast_slide = Slide(path, processed_path=PROCESS_PATH_TCGA)

   print(f"Slide name: {breast_slide.name}")
   print(f"Levels: {breast_slide.levels}")
   print(f"Dimensions at level 0: {breast_slide.dimensions}")
   print(f"Dimensions at level 1: {breast_slide.level_dimensions(level=1)}")
   print(f"Dimensions at level 2: {breast_slide.level_dimensions(level=2)}")

   breast_slide.thumbnail
   breast_slide.show()
   slide_name = breast_slide.name


   grid_tiles_extractor = GridTiler(
      tile_size=(4096, 4096),
      level=0,
      check_tissue=True,
      tissue_percent=80.0,
      pixel_overlap=0, # default
      prefix=slide_name+"/"+slide_name, # save tiles in the "grid" subdirectory of slide's processed_path
      suffix=".png" # default
   )

   # grid_tiles_extractor.locate_tiles(
   #     slide=breast_slide,
   #     scale_factor=64,
   #     alpha=64,
   #     outline="#046C4C",
   # )

   grid_tiles_extractor.extract(breast_slide)