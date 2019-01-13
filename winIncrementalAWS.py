import os
import sys
import datetime
import zipfile

# environment variable for backup root ROOT_DIR
rootDir = os.environ['ROOT_DIR']
# environment variable for temp backup location TEMP_BACKUP_DIR
backupDir = os.environ['TEMP_BACKUP_DIR']
# AWS S3 backup destination object name S3_BACKUP_OBJECT
s3dest = os.environ['S3_BACKUP_OBJECT']
# Log file destination directory BACKUP_LOG_DIR
logFileDir = os.environ['BACKUP_LOG_DIR']
today = datetime.datetime.today().strftime('%Y%m%d')

logname = "xxx" # this needs to be constructed from rootDir and date
logFileName = os.path.join(logFileDir,logname)
maxage = sys.argv[1]

os.system(r"robocopy %s %s /E /MAXAGE:%s /LOG:%)
archivename = r:'e:\backup-%s.zip' % today
with zipfile.ZipFile(archivename,'w') as myzip:
    
