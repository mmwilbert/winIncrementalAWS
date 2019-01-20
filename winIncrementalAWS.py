
import os
import sys
import datetime
import zipfile
import tempfile


def zipWithChildren(sourceDir,archive):
    global writeCount
    childlist = os.listdir(sourceDir)
    for filename in childlist:
        fullFilename = os.path.join(sourceDir,filename)
        try:
            if os.path.isdir(fullFilename):
                zipWithChildren(fullFilename,archive)
            else:
                writeCount = writeCount + 1
                if writeCount % 1000 == 0:
                    print (writeCount, fullFilename)
            archive.write(fullFilename)
        except Exception as e:
            print ("traceback.format_exc()",str(e),fullFilename)

# environment variable for backup root ROOT_DIR
rootDir = os.environ['ROOT_DIR']

# environment variable for temp backup location TEMP_BACKUP_DRIVE
backupDir = os.environ['TEMP_BACKUP_DRIVE']

# environment variable for backup zipfile location TEMP_ZIPFILE_DRIVE
zipfileDir = op.environ['TEMP_ZIPFILE_DRIVE']

# AWS S3 backup destination object name S3_BACKUP_OBJECT
s3dest = os.environ['S3_BACKUP_OBJECT']

# Log file destination directory BACKUP_LOG_DIR
logFileDir = os.environ['BACKUP_LOG_DIR']

today = datetime.datetime.today().strftime('%Y%m%d')
logname = "xxx" # this needs to be constructed from rootDir and date
logFileName = os.path.join(logFileDir,logname)

tempdir = tempfile.TemporaryDirectory(dir=zipfileDriveLetter + ":\")
tempdirname = tempdir.name

archivename = "yyy" # this needs to be constructed from backupDir and rootDir and date
maxage = sys.argv[1]

os.system(r"robocopy %s %s /E /MAXAGE:%s /LOG:%s" % (rootDir,tempdir,logFileName)

if not logFileOkay(logFileName):
  print ("robocopy error. exiting")

with zipfile.ZipFile(archivename,'w') as myzip:
  zipWithChildren(tempdir,archivename)
  
