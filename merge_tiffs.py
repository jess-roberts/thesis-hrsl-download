#!/usr/bin/env python
import argparse
import os
import time
import glob 
import rasterio 
from rasterio.merge import merge


def readCommands():
  """
  Read commandline arguments
  """
  p = argparse.ArgumentParser(description=("Merging multiple tifs."))
  p.add_argument("--tifDir", dest ="tifDir", type=str, default='./', help=("Directory containing .tif files to merge"))
  p.add_argument("--out_tif", dest ="out_tif", type=str, default='./output_merged.tif', help=("Output file path and name"))
  cmdargs = p.parse_args()
  return cmdargs


class mergeTiffs(object):
    """
        Class to handle the reading
        in of multiple tiffs
        and merging them 
        into one
    """
    def __init__(self,tifDir,out_tif):
        self.multMerge(tifDir,out_tif)
    
    def multMerge(self,tifDir,out_tif):
        """
            Function to search directory
            for all relevant files
            and perform the merge
        """
        # criteria to find the tifs
        search_criteria = '*.tif'
        tifs = os.path.join(tifDir, search_criteria)

        # taking the returned files and globbing them together
        tif_fps = glob.glob(tifs)

        # opening these files and creating list of them (for merge)
        self.tifs_4_mosaic = []
        for fp in tif_fps:
            print('Taking file ',fp,' for merge.')
            src = rasterio.open(fp)
            self.tifs_4_mosaic.append(src)

        # merging them into single array 
        self.dest, self.out_trans = rasterio.merge.merge(self.tifs_4_mosaic)

        # updating metadata
        """
        out_meta = src.meta.copy()
        out_meta.update({"driver": "Gtiff",
                        "height": dest.shape[1],
                        "width": dest.shape[2],
                        "transform": out_trans})
        """
        
        # writing merged file
        """
        with rasterio.open(out_tif, "w", **out_meta) as dest_obj:
                print('--Writing out merged geotiff--')
                dest_obj.write(dest)
        """

if __name__=="__main__":
    start_time = time.time()
    cmd = readCommands()

    merged = mergeTiffs(tifDir='../../HRSL/tiff_unzip/',out_tif='../../HRSL/tiff_unzip/hrsl_global_pop_density.tif')

    print("--- %s seconds ---" % (time.time() - start_time))
