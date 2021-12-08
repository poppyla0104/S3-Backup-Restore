# Poppy La
# File name: restore.py
# Instructor: Dr.Dimpsey
# Date: 11/14/2021
# Course: CSS436
# Program 3: BACKUP/RESTORE

import boto3
import sys
import os
from datetime import datetime, timezone
s3 = boto3.resource("s3")

def main(bucketName, bucketDirectory, directoryName):
   buckets = s3.buckets.all()
   # check every buckets in s3, if matched bucket found, restore the directory/file
   for bucket in buckets:
      if (bucket.name == bucketName): 
         print("Restoring file at path: " + bucketDirectory + " to " + directoryName)
         restoreFiles(bucketName, bucketDirectory, directoryName)
         return
   
   # return if bucket not valid
   print("Invalid bucket name!")


def restoreFiles(bucketName, bucketDirectory, directory):   
   bucket = s3.Bucket(bucketName)
   # check every the object key in bucket as the directory
   for obj in bucket.objects.all():
      dir = obj.key
      
      # restore if the file path on cloud start with the file requested to be restore
      if(dir.startswith(bucketDirectory)):
         localDir = dir

         # if user want to restore the cloud directory in different local directory location
         # add the local location at the beginning of cloud dir
         if (directory not in bucketDirectory):
            localDir = os.path.join(directory, dir)        
         newDir = os.path.dirname(localDir)

         # make new directory if it's not existed (include all the empty file)
         if (os.path.exists(newDir) == False):
            os.makedirs(newDir)

         # restore all the files in directory
         s3.meta.client.download_file(bucketName, dir, localDir)
         print("File restored: " + localDir)


# main method to run the program
if __name__ == '__main__':
   # need 3 command line argument: python file, bucket name with the file location of the 
   # restore directory on cloud, and file/folder local location to restore at
   if (len(sys.argv) != 3):
      print("Invalid input. Program terminated.")
      sys.exit(0)
   
   bucket, bucketDirectory = sys.argv[1].split('::',1)
   directory = sys.argv[2]
   main(bucket, bucketDirectory, directory)
   print("Restore complete. Program terminated.")
   sys.exit(0)
