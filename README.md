# HRSL Processing

This repository contains scripts to batchprocess geotiff data downloaded from the [Humanitarian Data Exchange](https://data.humdata.org) (HDX) using the HDX Python Api. The scripts are as follows: ```hrsl_downld.py``` controls the batchdownload of data with some user controls (detailed below), ```zip2tiff_merged.py``` unzips the files downloaded (if in .ZIP format, as many are) and merges these geotiffs into one single standardised dataset in a resolution and projection of the user's choosing. This script assumes that the user has some knowledge of the dataset(s) they wish to download. In this use case, the default settings download Facebook's [High Resolution Settlement Layer](https://research.fb.com/downloads/high-resolution-settlement-layer-hrsl/) (HRSL) population data, and merge these to create a global geotiff. 

```hrsl_dwnld.py```
-
This script uses an object initialised in ```HDX_Download``` to search for and download data from the HDX database. 
### Data Search

During initialisation of this object, a HDX configuration is set up for the data exchange (using the HDX Python API ```hdx.hdx_configuration.Configuration```) unless one already exists, before then beginning the search of the database using ```hdx.data.dataset.Dataset```'s function:
```python
self.SourceSearch(source)
```
This function is referring to the source of the data required (i.e. the organisation that uploaded it), defined by the user at the command line or in-script. Within this function, a check takes place for each dataset returned to ensure that the data source searched for within the database actually did upload it (by checking the standardised metadata using ```hdx.data.dataset.Dataset.data```), as opposed to simply being mentioned in the dataset's description: 
```python
if source in self.datasets[i].data['dataset_source']:
      # Create list of valid datasets
      self.valid_datasets.append(self.datasets[i])
```

### Data Selection and Download
Once the data has been validated as attributed to the desired data source, the next function can then be called if the user wishes to download that data:
```python
def Download2Comp(self,keyword,fformat,dest):
```
This function also performs a metadata check against a keyword(s) (i.e. to extract the data the user is searching for) and the desired file type (fformat). If the dataset('s metadata) meets the criteria of the user, its data information is then extracted through the HDX Python API's ```hdx.data.dataset.Dataset``` function ```.get_resource()```.
```python
if keyword in all_data[j]['name'] and fformat in all_data[j]['format']:
      get_data = self.valid_datasets[i].get_resource(index=j)
```
The datasets' data resource information is then used for download by using the HDX Python API's ```hdx.data.dataset.Dataset.resource``` function ```.download()``` which returns the URL used for download and the destination pathway. 

The following command line arguments are available:

```--source default:Facebook```
>The dataset's source organisation 

```--dest default:'./'```
>The folder destination for download

```--keyword default:'population'```
>The keyword(s) to refine your dataset selection

```--fformat default:'geotiff'```
>The file type you wish to download.

Documentation detailing the HDX Python API download can be found [here](https://pypi.org/project/hdx-python-api/) and details of the library structure/use can be found [here](http://ocha-dap.github.io/hdx-python-api/).
