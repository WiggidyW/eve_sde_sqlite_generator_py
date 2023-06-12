import os
import zipfile
import urllib3

CHECKSUM_URL = 'https://eve-static-data-export.s3-eu-west-1.amazonaws.com/tranquility/checksum'
SDE_URL = 'https://eve-static-data-export.s3-eu-west-1.amazonaws.com/tranquility/sde.zip'

def http():
    return urllib3.PoolManager()

def sde(http, dir):
    # Download the file from SDE_URL and then unzip it
    print('Downloading SDE...')
    with open(dir / 'sde.zip', 'wb') as out_file:
        with http.request('GET', SDE_URL, preload_content=False) as r:
            for chunk in r.stream(1024):
                out_file.write(chunk)
            r.release_conn()
    print('Download complete.')

    # Unzip the file
    print('Unzipping SDE...')
    with zipfile.ZipFile(dir / 'sde.zip', 'r') as zip_ref:
        zip_ref.extractall(dir)
    print('Unzip complete.')
    
    # Delete the zip file
    print('Deleting zip file...')
    os.remove(dir / 'sde.zip')
    print('Zip file deleted.')

def checksum(http):
    return http.request('GET', CHECKSUM_URL).data.decode('utf-8')
