# Download Dataset

To download the full `Natural Questions` [dataset](https://ai.google.com/research/NaturalQuestions/download) (42Gb) run:
```bash
gsutil -m cp -R gs://natural_questions/v1.0 .
```
Detailed instructions to install `gsutil` can be found [here](https://cloud.google.com/storage/docs/gsutil_install)

Further information about the `Natural Questions` dataset can be found [here](https://ai.google.com/research/NaturalQuestions/dataset)

## Clone this repository (including `dev` data)

The repository includes only the `sample` (~250MB) and `dev` (~1.1GB) data folders:

```bash
git clone https://github.com/stmnk/qa.git
```
Git [large file storage](https://git-lfs.github.com/) extension (`git-lfs`) needs to be installed before the first clone (see below). The first repo clone can take about 20 minutes to dowload all data, depending on connection. The `train` data folder is not included in the repo, because it is too large (44GB).

The (`git-lfs`) has been added to the repo with the followig settings:

```bash
git lfs install
git lfs track "*.gz"
git add .gitattributes
```

Further information about installing `git-lfs` can be found [here](https://git-lfs.github.com/). 