#!/usr/bin/env python
import argparse 
import time
import itertools

from hdx.utilities.easy_logging import setup_logging
from hdx.hdx_configuration import Configuration
from hdx.data.dataset import Dataset

setup_logging()

def readCommands():
    """
        Read command line arguments
    """     
    p = argparse.ArgumentParser(description=("Downloading data from HDX"))
    p.add_argument("--source", dest ="source", type=str, default="Facebook", help=("Data source organisation"))
    p.add_argument("--dest", dest ="dest", type=str, default='./', help=("Destination folder for download"))
    p.add_argument("--keyword", dest ="keyword", type=str, default='population', help=("Data keyword"))
    p.add_argument("--fformat", dest ="fformat", type=str, default='geotiff', help=("Desired file format"))
    cmdargs = p.parse_args()
    return cmdargs

class HDX_Download(object):
    """
        HDX data handler
    """ 
    def __init__(self,source):
        """
            Initialising the object and 
            HDX Configuration Connection if necessary
        """ 
        try:
            # Connect to HDX
            Configuration.create(hdx_site='prod', user_agent='Dataset_Download', hdx_read_only=True)
        except:
            print('There is already a HDX Configuration.')
        
        # Start HDX search based on desired data source
        self.SourceSearch(source)
    
    def SourceSearch(self,source):
        """
            Searching the HDX database for 
            desired data source and validating
            that the data returned is created by
            the desired organisation
        """ 
        # Search the database
        self.datasets = Dataset.search_in_hdx(source)

        # Loop to check that the datasets returned were actually created
        # by the desired organisation
        self.valid_datasets = []
        for i in range(len(self.datasets)):
            try:
                if source in self.datasets[i].data['dataset_source']:
                    # Create list of valid datasets
                    self.valid_datasets.append(self.datasets[i])
                    print('Valid Dataset: ', self.datasets[i].data['title'])
                else:
                    print('Invalid Dataset: ', self.datasets[i].data['title'])
            except:
                print('Search validation did not work.')
    
    def Download2Comp(self,keyword,fformat,dest):
        """
            Checking the metadata of the datasets
            returned to see if they are the data
            that we desire, by checking against
            two keywords
        """ 
        # Get the data information attached to each dataset
        self.resources = Dataset.get_all_resources(self.valid_datasets)
        
        # Getting the relevant data attached to each dataset
        get_data = ''
        for i in range(len(self.valid_datasets)):
            # Check all data attached to each dataset
            all_data = self.valid_datasets[i].get_resources()
            
            for j in range(len(all_data)):
                # Take data if it matches the keyword and format desired
                if keyword in all_data[j]['name'] and fformat in all_data[j]['format']:
                    get_data = self.valid_datasets[i].get_resource(index=j)
                    try:
                        # Download it
                        get_data['format'] = '' 
                        url, path = get_data.download(folder=dest)
                        print('Resource URL %s downloaded to %s' % (url, path))
                        get_data = '' # Clear variable to avoid duplicate downloads in the event of failure
                    
                    except:                        
                        print('Data not valid for download.')

if __name__=="__main__":
    # Creating data objects for download
    
    start_time = time.time()
    
    cmd = readCommands()
    
    data = HDX_Download(source=cmd.source)
    data.Download2Comp(keyword=cmd.keyword,fformat=cmd.fformat,dest='../../HRSL/')
    
    print("--- %s seconds ---" % (time.time() - start_time))