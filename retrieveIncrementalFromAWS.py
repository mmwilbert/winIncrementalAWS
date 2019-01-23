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


def decryptedFileCopy(filename,password):
    digest = hashes.Hash(hashes.SHA256(),backend=default_backend())
    digest.update(password.encode("UTF-8"))
    finishedDigest = digest.finalize()
    with open(filename,'rb') as source:
        nonce = source.read(16)
        cipher = Cipher(algorithms.AES(finishedDigest),
                        modes.CTR(nonce),
                        backend=default_backend())
        decryptor = cipher.decryptor()
        outfilename = filename[:-10]
        bytes = " "
        with open(outfilename,'wb') as out:
            while len(bytes) > 0:
                bytes = source.read(1000000)
                out.write(decryptor.update(bytes))
            out.write(decryptor.finalize())
    return outfilename


# archive password ARCHIVE_PASSWORD
password = os.environ['ARCHIVE_PASSWORD']

# AWS S3 backup destination object name S3_BACKUP_BUCKET
s3source = os.environ['S3_BACKUP_BUCKET']

# get AWS profile name for bucket access and open session using that profile
awsProfileName = os.environ['AWS_PROFILE_NAME']
session = boto3.Session(profile_name=awsProfileName)

# archive password ARCHIVE_PASSWORD
password = os.environ['ARCHIVE_PASSWORD']

# where to put downloaded file and decrypted zip file
restorePath = os.environ['RESTORE_PATH']

backupObjectKey = sys.argv[1]

# get AWS profile name for bucket access and open session using that profile
awsProfileName = os.environ['AWS_PROFILE_NAME']
session = boto3.Session(profile_name=awsProfileName)

# copy archive from s3
s3 = session.resource('s3')
print (backupObjectKey)
newFileName = backupObjectKey.replace('\\',"_")
print (newFileName)
newFileName = newFileName.replace(":","_")
print (newFileName)
newFileName = os.path.join(restorePath,newFileName)
print ("newFileName",newFileName)

s3.Bucket(s3source).download_file(backupObjectKey,newFileName)

# decrypt archive

decryptedFileName = decryptedFileCopy(newFileName,password)
print (decryptedFileName)

sys.exit(0)


























