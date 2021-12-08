# Poppy La
# File name: backup.py
# Instructor: Dr.Dimpsey
# Date: 11/14/2021
# Course: CSS436
# Program 3: BACKUP/RESTORE

import boto3
import sys
import os
from datetime import datetime, timezone
s3 = boto3.resource("s3")
session = boto3.session.Session()
myRegion = session.region_name

def main(directoryName, bucketName, bucketDirectory):
   buckets = s3.buckets.all()
   # check every buckets in s3, if matched bucket found, backup the directory
   for bucket in buckets:
      if (bucket.name == bucketName): 
         print("Backing up file at path " + directoryName + " to " + bucketDirectory +  " of " + bucketName + " bucket")
         backupFile(directoryName, bucketName, bucketDirectory)
         return
   
   # create new bucket and backup if bucket not exist
   s3.create_bucket(Bucket=bucketName, CreateBucketConfiguration={"LocationConstraint":myRegion})   
   print("Backing up file at path: " + directoryName + " to " + bucketDirectory +  " of " + bucketName + " bucket")
   backupFile(directoryName, bucketName, bucketDirectory)


def backupFile(directory, bucketName, bucketDirectory):
   bucket = s3.Bucket(bucketName)
   # create directory of the folder in bucket
   bucketDir = dict()
   for obj in bucket.objects.all():
      bucketDir.update({obj.key:obj})
   
   for root, subDirs, files in os.walk(directory):
      # back up the files in directory
      for file in files:
         # the absolute path of the local file
         filePath = os.path.join(root, file)
         # change the cloud directory if use want to add the local file into other folder on cloud
         if(bucketDirectory != directory):
            bucketFilePath = (bucketDirectory + "/" + filePath).replace("\\","/")
         else: 
            bucketFilePath = filePath.replace("\\","/")
         filePath.replace("\\","/")
         filePath.encode('utf-8').strip()
         bucketFilePath.encode('utf-8').strip()

         # if the file exist, update it or skip if it's up to date
         # else back up the file
         if bucketFilePath in bucketDir:
            processExist(bucketDir, bucketName, bucketFilePath, filePath)
         else:
            s3.Object(bucketName, bucketFilePath).put(Body=open(filePath, "rb"))
            print("Backed Up: " + filePath)


# file exist in bucket, update file or skip if the file is up to date
def processExist(bucketDir, bucketName, bucketFilePath, filePath):
   # get last modified time of the local file and cloud file
   localFileTS = os.path.getmtime(filePath)
   bucketFileDT = bucketDir.get(bucketFilePath).last_modified.replace(tzinfo=timezone.utc)
   bucketFileTS = bucketFileDT.timestamp()

   # update file if the local file last modified timestamp is larger than cloud file last modified timestamp
   # else skip
   if(bucketFileTS < localFileTS):
      s3.Object(bucketName, bucketFilePath).put(Body=open(filePath, "rb"))
      print("Updated: " + filePath)
   else: 
      print("File Existed: " + filePath)


# main method to run the program
if __name__ == '__main__':
   # need 3 command line argument: python file, file/folder local location, and bucket name with the 
   # file location to backup on cloud
   if (len(sys.argv) != 3):
      print("Invalid input. Program terminated.")
      sys.exit(0)
   
   directory = sys.argv[1]
   bucket, bucketDirectory = sys.argv[2].split('::',1)
   main(directory, bucket, bucketDirectory)
   print("Backup complete. Program terminated.")
   sys.exit(0)
