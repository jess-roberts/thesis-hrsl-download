#!/usr/bin/env python

from zipfile import ZipFile
import os
import time
import argparse

def readCommands():
  """
  Read commandline arguments
  """
  p = argparse.ArgumentParser(description=("Extracting .zip geotiff files before merging into single tiff"))
  p.add_argument("--dataDir", dest ="dataDir", type=str, default="../../HRSL/", help=("Input file directory containing .zip files for extraction"))
  p.add_argument("--outDir", dest ="outDir", type=str, default="../../HRSL/tiff_unzip", help=("Output file directory to extract .zip files to"))
  cmdargs = p.parse_args()
  return cmdargs


class handleZip(object):
    """
        Class to unzip multiple .zip files
        present in a directory
    """
    def __init__(self,dataDir,outDir):
        self.unZip(dataDir,outDir)
    
    def unZip(self,dataDir,outDir):
        """
            Function to unzip the files
        """
        files = []
        for file in os.listdir(dataDir):
                file = str(file)
                if file.endswith("geotiff.zip"): # take the files we want
                    files.append(os.path.join(dataDir,file)) # make a list of them
        
        for zip_file in files: # extracting each file
            with ZipFile(zip_file, 'r') as zipObj:
                print('Extracting ',zip_file,' to ',outDir)
                zipObj.extractall(outDir)


if __name__=="__main__":
    start_time = time.time()

    cmd = readCommands()

    unZip = handleZip(dataDir=cmd.dataDir,outDir=cmd.outDir)
    
    print("--- %s seconds ---" % (time.time() - start_time))
