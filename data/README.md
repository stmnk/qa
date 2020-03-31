# Download Dataset

To download the full `Natural Questions` 
[dataset](https://ai.google.com/research/NaturalQuestions/download) (42Gb) run:

```bash
gsutil -m cp -R gs://natural_questions/v1.0 .
```

Detailed instructions to install `gsutil` can be found 
[here](https://cloud.google.com/storage/docs/gsutil_install)

Further information about the `Natural Questions` dataset can be found 
[here](https://ai.google.com/research/NaturalQuestions/dataset)

## Clone this repository (including `dev` data)

The repository includes only the `sample` (~250MB) and `dev` (~1.1GB) data folders:

```bash
git clone https://github.com/stmnk/qa.git
```

Git [large file storage](https://git-lfs.github.com/) extension (`git-lfs`) needs to be 
installed before the first clone (see below). The first repo clone can take about 20 minutes 
to dowload all data (depending on connection). The `train` data folder is not included in the 
repo (because it is too large ~44GB).

The (`git-lfs`) has been added to the repo with the followig settings:

```bash
git lfs install
git lfs track "*.gz"
git add .gitattributes
```

Further information about installing `git-lfs` can be found [here](https://git-lfs.github.com/).

## Work with the NQ dataset in a cloud environment

It is possible to work with the dataset in a cloud environment.

### Colab

Upload the full dataset in simplified format (~4.7GB) to Google Drive. Use the following steps to 
load the `.jsonl` files into a dataframe.

Mount the Google Drive content into the Jupyter Notebook.

```python
from google.colab import drive
DRIVE_ROOT = '/content/drive'
drive.mount(DRIVE_ROOT)
```

Authenticate to your drive account.

A pre-processing step (used in [2]) that reduces the size a bit eliminates data for questions that do 
not have an answer. Further data wrangling steps are described in the 
[NQ_dataset_sample.ipynb](sample/NQ_dataset_sample.ipynb) notebook.

The unsimplified format of NQ has ~47GB and therefore exceeds the 15GB upper limit of a free plan for 
Google Drive.

### AWS

#### S3

##### Price estimation

Fully expanded data is about 220GB for full format and ~30 for simplified format plus other subsets. 
On AWS S3 with a *standard* tier this will cost ~5$ per month. 2 or 3 months of storage during 
development will have a total estimated cost of 10 or 15$. Using an *infrequent access* tier might 
reduce the cost a bit.

##### Setting-up AWS S3

TODO: add info
