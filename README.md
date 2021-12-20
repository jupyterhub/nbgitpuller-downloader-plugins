# nbgitpuller-downloader-plugins
jupyterhub/nbgitpuller allows for content provider plugins, this python package provides downloader plugins

There are three downloader-plugins included in this repository:
- nbgitpuller-downloader-generic-web
- nbgitpuller-downloader-googledrive
- nbgitpuller-downloader-dropbox

When this package is installed next to nbgitpuller in a jupyterhub instance, you can use nbgitpuller links
to compressed archives(zip an tar) in Google Drive, Dropbox or any publicly exposed URL to download your notebooks(or any files)
into a jupyterhub. 

This plugin expects URLs included in the nbgitpuller link to be in the following format:
- Generic Web: https://www.example.com/materials-sp20-external.zip
- Dropbox: https://www.dropbox.com%/<dropbox-idd>/materials-sp20-external.zip?dl=0
- Google Drive: https://drive.google.com/file/d/<google-file-id/view?usp=sharing

In all of these cases, the archive must be publicly available or "shared" with everyone in the case of Google Drive.

## Installation

```shell
python3 -m pip install nbgitpuller-downloader-plugins
