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
        self.files = []
        for file in os.listdir(dataDir):
                file = str(file)
                if file.endswith(".zip"): # Take the .zip files we want
                    self.files.append(os.path.join(dataDir,file)) # Make a list of them
        
        for zip_file in self.files: # Extracting each file
            with ZipFile(zip_file, 'r') as zipObj:
                listOfFileNames = zipObj.namelist()
                # Iterate over the file names
                for fileName in listOfFileNames:
                    # Check filename endswith .tif
                    if fileName.endswith('.tif'):
                        # Extract a single (.tif) file from zip
                        print('Extracting ',fileName,' to ',outDir)
                        zipObj.extract(fileName, outDir)


if __name__=="__main__":
    start_time = time.time()

    cmd = readCommands()

    unZip = handleZip(dataDir=cmd.dataDir,outDir=cmd.outDir)
    
    print("--- %s seconds ---" % (time.time() - start_time))
