import boto3
from botocore.vendored import requests
import logging
import base64
import os
import time
import shutil
from zipfile import ZipFile

verify = False

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logging.info("hello")

### Define variables
s3_client = boto3.client('s3')
s3 = boto3.resource('s3')
user = os.environ.get('USER')
token = os.environ.get('GITHUB_TOKEN')
repo_name = [os.environ.get('GITHUB_REPO1'), os.environ.get('GITHUB_REPO2')]
link = os.environ.get('GITHUB_LINK')
bucket_name = os.environ.get('S3_BUCKET_UPLOAD')
bundle_dir = os.environ.get('BUNDLE_DIR')
timestr = time.strftime("%Y_%m_%d-%H_%M")


def lambda_handler(event, context):
   for repo in repo_name:
      ### variables
      path   =  "/tmp" 
      clone  =  f"git clone https://{user}:{token}@{link}{repo}.git" 
      ### Variable to use git bundle instead of zip archiving
      #bundle =  f"git bundle create {repo}-{timestr}.bundle --all"
      
      ### Change directory to clone repository
      os.chdir(path) 
      os.system(clone)
      
      ######## git bundle usage
      ### Create git bundle inside repository directory
      #os.chdir(path + "/" + repo)
      ### Create variable with bundle file
      #s3_bundle_file = f"{repo}-{timestr}.bundle"
      #os.system(bundle)
      ### Create variable with bundle file
      #s3_bundle_file = f"{repo}-{timestr}.bundle"
      #os.system(bundle)
      
      ### Create zip archive, using sh
      s3_bundle_file = f"{repo}-{timestr}.zip"
      shutil.make_archive(f'{repo}-{timestr}', 'zip', os.getcwd())
      
      ### Upload created bundle file to AWS S3
      logger.info("Uploading zip to S3://%s/%s" % (bucket_name, s3_bundle_file))
      s3.meta.client.upload_file(os.getcwd() + "/" + s3_bundle_file, bucket_name, s3_bundle_file)
      logger.info('Upload Complete')
      ### Remove files after execution
      logger.info('Removing files after execution')
      shutil.rmtree(path + '/' + repo)
      os.remove(s3_bundle_file)
      logger.info(os.getcwd())
