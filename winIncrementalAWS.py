
import os
import sys
import datetime
import zipfile
import tempfile


def logFileOkay(logfilename):
  return True

def zipWithChildren(sourceDir,archive):
    childlist = os.listdir(sourceDir)
    for filename in childlist:
        fullFilename = os.path.join(sourceDir,filename)
        try:
            if os.path.isdir(fullFilename):
                zipWithChildren(fullFilename,archive)
            else:
              archive.write(fullFilename)
        except Exception as e:
            print ("traceback.format_exc()",str(e),fullFilename)

# environment variable for backup root ROOT_DIR
rootDir = os.environ['ROOT_DIR']

# environment variable for temp backup location TEMP_BACKUP_DRIVE
backupDir = os.environ['TEMP_BACKUP_DRIVE']

# environment variable for backup zipfile location TEMP_ZIPFILE_DRIVE
zipfileDriveLetter = os.environ['TEMP_ZIPFILE_DRIVE']

# AWS S3 backup destination object name S3_BACKUP_BUCKET
s3dest = os.environ['S3_BACKUP_BUCKET']

# Log file destination directory BACKUP_LOG_DIR
logFileDir = os.environ['BACKUP_LOG_DIR']

today = datetime.datetime.today().strftime('%Y%m%d')
logname = "xxx" # this needs to be constructed from rootDir and date
logFileName = os.path.join(logFileDir,logname)

tempdir = tempfile.TemporaryDirectory(dir=os.path.join(zipfileDriveLetter))
tempdirname = tempdir.name

archivename = "yyy" # this needs to be constructed from backupDir and rootDir and date
maxage = sys.argv[1]

os.system(r"robocopy %s %s /E /MAXAGE:%s /R:1 /W:1 /XD %s /LOG:%s" % (rootDir,tempdir.name,maxage,os.path.split(tempdir.name)[1],logFileName))

if not logFileOkay(logFileName):
  print ("robocopy error. exiting")

with zipfile.ZipFile(archivename,'w') as myzip:
  zipWithChildren(tempdir.name,myzip)
  
