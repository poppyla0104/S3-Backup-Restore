# S3-Backup-Restore
The program 3 includes 2 python files backup.py and restore.py. The backup.py file will upload the files in a folder or directory in the local machine to the aws cloud. The restore.py file will download/restore a directory/folder with all the files from the aws cloud to the local machine. Both the program will use the user access key stored in the user .aws file in the local machine. Users will need to set up their credentials to access their aws. The backup.py program will also use the region to create a new bucket if the user wants to backup to a new nonexist bucket. Programs will not backup or restore empty folders.

Backup:
The backup.py program will upload/backup the files in a folder or directory in the local machine to the specific bucket or location in the bucket in aws cloud. The bucket name, location to backup in cloud and local location are inputted by the user. The files directory will be kept the same as the local directory, directory can be backuped directly in the bucket or in another folder in the bucket.
If the bucket user requested does not exist in user aws s3, the program will create a new bucket with the proper name and backup the directory in the new bucket/ a folder in the new bucker, depending on user request.

Restore:
The restore.py program will download/restore the files in a folder or directory in the bucket of aws s3 to the specific location in the local machine. The bucket name, location to restore in the local machine and location in s3 bucket are inputted by the user. The files directory will be kept the same as the directory tree in s3, both files in specific directory location and the whole directory can be restored, depending on user request.

Requirements:
● IOS is highly recommended for the most accurate result.
● User credentials have to be set up in a local machine.
● Boto3 needs to be installed in order to compile and run the programs.
● Bucket name should be correct, else it must follow aws bucket name rule to create a new
bucket.
● The directory/folder/file should exist and the name inputted should be correct.
● If the directory in the local machine exists, restore.py will overwrite it.
● All inputs should be correct or precise.
● All folders can not be empty.
