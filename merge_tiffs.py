#!/usr/bin/env python
import argparse
import os
import time
import glob
import numpy
import rasterio
from rasterio.merge import merge


def readCommands():
  """
  Read commandline arguments
  """
  p = argparse.ArgumentParser(description=("Merging multiple tifs."))
  p.add_argument("--tifDir", dest ="tifDir", type=str, default='./', help=("Directory containing .tif files to merge"))
  p.add_argument("--chunks", dest ="chunks", type=int, default=2, help=("Number of files to mosaic iteratively"))
  cmdargs = p.parse_args()
  return cmdargs


class mergeTiffs(object):
    """
        Class to handle the reading
        in of multiple tiffs
        and merging them 
        into one
    """
    def __init__(self,tifDir,chunks):
        self.takeTifs(tifDir,chunks)

    def chunkArray(self,array,chunk_size):
        """
            Using list comprehension
            to break down an array 
            into chunk sizes of choice
        """ 
        chunked_array = [array[i * chunk_size:(i + 1) * chunk_size] for i in range((len(array) + chunk_size - 1) // chunk_size )]  
        return chunked_array
    
    def takeTifs(self,tifDir,chunks):
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
            self.src = rasterio.open(fp)
            self.tifs_4_mosaic.append(self.src)

        self.tifs_4_mosaic_chunked = self.chunkArray(self.tifs_4_mosaic,chunks)

        self.mergeTifs()

    def mergeTifs(self):
        """
            Looping through chunks of tif
            list to iteratively merge them
        """
        i = 0
        for chunk in self.tifs_4_mosaic_chunked:
            # merging each file within the chunks them into single array 
            print('Completing merge of chunk #',i+1,' of .tif list')
            dest, out_trans = rasterio.merge.merge(chunk)

            # output filename
            out_tif = '../../HRSL/tiff_unzip/merged/merged_output_'+str(i)+'.tif'

            # updating metadata
            out_meta = self.src.meta.copy()
            print('Updating metadata of outfile: ',out_tif)
            out_meta.update({"driver": "Gtiff",
                            "height": dest.shape[1],
                            "width": dest.shape[2],
                            "transform": out_trans})
            
            out_tif = '../../HRSL/tiff_unzip/merged/merged_output_'+str(i)+'.tif'
            # writing merged file
            with rasterio.open(out_tif, "w", **out_meta) as dest_obj:
                    print('--Writing out merged geotiff--')
                    dest_obj.write(dest)
            i += 1
        

if __name__=="__main__":
    start_time = time.time()
    cmd = readCommands()

    merged = mergeTiffs(tifDir='../../HRSL/tiff_unzip/',chunks=cmd.chunks)

    print("--- %s seconds ---" % (time.time() - start_time))
