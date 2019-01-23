import os
import sys
import datetime
import zipfile
import tempfile
import base64
import boto3

from cryptography.hazmat.primitives import hashes 
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def encryptedFileCopy(filename,password):
    nonce = os.urandom(16)
    digest = hashes.Hash(hashes.SHA256(),backend=default_backend())
    digest.update(password.encode("UTF-8"))
    finishedDigest = digest.finalize()
    print (len(finishedDigest))
    #encodedPassword = base64.urlsafe_b64encode(finishedDigest)
    #cipher = Cipher(algorithms.AES(encodedPassword),
    cipher = Cipher(algorithms.AES(finishedDigest),
                    modes.CTR(nonce),
                    backend=default_backend())
    encryptor = cipher.encryptor()
    bytes = " "
    with open(filename,'rb') as source:
        outfilename = filename + ".encrypted"
        with open(outfilename,'wb') as out:
            out.write(nonce)
            while len(bytes) > 0:
                bytes = source.read(1000000)
                out.write(encryptor.update(bytes))
            out.write(encryptor.finalize())
    return outfilename


def makeArchiveName(rootName,today,maxage):
    rootName = rootName.replace("\\","_")
    rootName = rootName.replace(":","_")
    rootName = rootName.replace("__","_")
    return rootName + '_%s_%s' % (today,maxage)

def zipModifiedFilesWithChildren(sourceDir,archive,modifiedSinceTime=0):
    childlist = os.listdir(sourceDir)
    for filename in childlist:
        fullFilename = os.path.join(sourceDir,filename)
        try:
            if os.path.isdir(fullFilename):
                zipModifiedFilesWithChildren(fullFilename,archive,modifiedSinceTime)
            else:
                modifiedTime = os.path.getmtime(fullFilename)
                if modifiedSinceTime.timestamp() < modifiedTime:
                    archive.write(fullFilename)
        except Exception as e:
            print ("traceback.format_exc()",str(e),fullFilename)


# environment variable for backup root ROOT_DIR
rootDir = os.environ['ROOT_DIR']

# environment variable for temp backup location TEMP_BACKUP_DRIVE
#backupDir = os.environ['TEMP_BACKUP_DRIVE']

# environment variable for backup zipfile location TEMP_ARCHIVE_DRIVE
archiveDrive = os.environ['TEMP_ARCHIVE_DRIVE']

# archive password ARCHIVE_PASSWORD
password = os.environ['ARCHIVE_PASSWORD']

# AWS S3 backup destination object name S3_BACKUP_BUCKET
s3dest = os.environ['S3_BACKUP_BUCKET']

# get AWS profile name for bucket access and open session using that profile
awsProfileName = os.environ['AWS_PROFILE_NAME']
session = boto3.Session(profile_name=awsProfileName)

# Log file destination directory BACKUP_LOG_DIR
#logFileDir = os.environ['BACKUP_LOG_DIR']


today = datetime.datetime.today().strftime('%Y%m%d')
#logname = "xxx" # this needs to be constructed from rootDir and date
#logFileName = os.path.join(logFileDir,logname)

zipfileDir = tempfile.TemporaryDirectory(dir=os.path.join(archiveDrive))

maxage = sys.argv[1]

archivename = makeArchiveName(rootDir,today,maxage)
awsObjectName = archivename
archivename = os.path.join(zipfileDir.name,archivename + '.zip')


#os.system(r"robocopy %s %s /E /MAXAGE:%s /R:1 /W:1 /XD %s /LOG:%s" % (rootDir,tempdir.name,maxage,os.path.split(tempdir.name)[1],logFileName))

#if not logFileOkay(logFileName):
#  print ("robocopy error. exiting")


minModifiedTime = datetime.datetime.now() - datetime.timedelta(days=int(maxage))

# create temporary archive file

with zipfile.ZipFile(archivename,'w') as myzip:
  zipModifiedFilesWithChildren(rootDir,myzip,minModifiedTime)
 
# encrypt archive

newFileName = encryptedFileCopy(archivename,password)
 
# copy archive to s3
s3 = session.client('s3')
with open(newFileName,'rb') as data:
    s3.upload_fileobj(data,s3dest,awsObjectName)


