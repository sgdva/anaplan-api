*Note: This package is fixed from the original one for typos and coding enhancements.*

# anaplan-api

Anaplan-API is a Python library wrapper for [Anaplan Bulk API](https://anaplanbulkapi20.docs.apiary.io/) and [Anaplan Authentication API](https://anaplanauthentication.docs.apiary.io/).

This has been tested in python 3.9 and 3.12 

## Installation
If you are on a corporate environment you need to install:

pip install pip-system-certs

[S.O. Thread](https://stackoverflow.com/a/57053415/3221380) 

[pip-system-certs project](https://gitlab.com/alelec/pip-system-certs)

You need to install Fernet and cryptography as well

```python
#It is strongly advised to use the line
import pip_system_certs.wrapt_requests
#Before the usage of this API to avoid requests certificates  (causing 443 auth errors) being loaded
import anaplan_api
```

Consider that in corporate environments this may not be enough, in addition, make sure that SSL is being forced to your cert like (do this before your code implementation):
```python
import pip_system_certs.wrapt_requests
from crytpography.fernet import Fernet
import ssl
# Use this context for your SSL connections
TxtCertPath='./mycert.pem';TxtPrivateKeyPath='myprivatekey.key';TxtFilePathBin='./2.bin';TxtFilePathkey='./1.key'
# Load the key
with open(TxtFilePathkey, 'rb') as ObjFile:
    Objkey = ObjFile.read()
# Create a cipher instance
Objciphersuite = Fernet(Objkey)
# Read the encrypted password
with open(TxtFilePathBin, 'rb') as ObjFile:
    ObjEncryptedPass = ObjFile.read()
# Create SSL context with the decrypted passphrase
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=TxtCertPath, keyfile=TxtPrivateKeyPath, password=Objciphersuite.decrypt(ObjEncryptedPass).decode())
# Use this context for your SSL connections
```

You may use the original package manager [pip](https://pypi.org/project/anaplan-api/) to install Anaplan-API from Lewis (see next line), however, to have the updates you need to overwrite the scripts at your environment site packages (usually at yourenvname/Lib/anaplan_api) with the ones provided here. Or you may copy the whole folder structure instead (recommended).

```bash
pip3 install anaplan_api
```



## Usage

```python
import pip_system_certs.wrapt_requests
import ssl
import requests
import re
import anaplan.anaplan
from anaplan.models.AnaplanConnection import AnaplanConnection
from cryptography.fernet import Fernet
import os
import time
import inspect
import sys
#Full example to upload a file and execute an action using a certificate with passphrase (encoded with Fernet in 2 files a bin and a key). You may use the passphrase directly
#We consider that needed files are in downloads
TxtUserDownloadsFolder=os.path.join(os.path.expanduser("~"), "Downloads")
TxtUserDownloadsFolder=TxtUserDownloadsFolder.replace("\\", "/") +"/"
TxtWorkspaceID="myworkspaceID";TxtModelID="mymodelID"
TxtCert="mycert.pem";TxtPrivateKey="myprivatekey.key"
TxtFileBin="2.bin";TxtFilekey="1.key"
TxtServerFileToUpload="myfilenameinAP.csv"
TxtLocalFileToUpload="LocalFilename.csv"
ArrTxtActionsID=["1.0 Test Action"]
# Use this context for your SSL connections
TxtCertPath=TxtUserDownloadsFolder + TxtCert;TxtPrivateKeyPath=TxtUserDownloadsFolder + TxtPrivateKey;TxtFilePathBin=TxtUserDownloadsFolder+ TxtFileBin;TxtFilePathkey=TxtUserDownloadsFolder+TxtFilekey
# Load the key
with open(TxtFilePathkey, 'rb') as key_file:
    key = key_file.read()
# Create a cipher instance
cipher_suite = Fernet(key)
# Read the encrypted password
with open(TxtFilePathBin, 'rb') as file_in:
    encrypted_password = file_in.read()
# Decrypt the password
decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
# Create SSL context with the decrypted passphrase
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=TxtCertPath, keyfile=TxtPrivateKeyPath, password=decrypted_password)
# Use this context for your SSL connections

def Return_IsRegexInStr(TxtToAnalyze,TxtRegexPattern) -> bool:
    return bool(re.search(TxtRegexPattern, TxtToAnalyze))
def Return_VarLookInListsItem(VarValueToLook,ArrLists, IsLookInKey=True):
    """Searches for an element in the given lists and returns its corresponding definition or key.
    :param ArrLists: The dictionary containing the lists with filenames as keys and definitions as values.
    :param element: The element to search for in the lists.
    :param IsLookInKey: A boolean indicating whether to search in the key (True) or the definition (False).
    :return: The filename or definition corresponding to the element if found, or an error message if not found.
    :rtype: str
    --------------
    `EXAMPLE USAGE:
    lists1 = {
    "Item1": "150",
    "Item2": "2",
    }
    lists2 = {
    "Item4": "200",
    "Item7": "300",
    }
    element = "Item7"
    lists=[lists1,lists2]
    result = Return_VarLookInListsItem(element,lists,True)
    print(result)
    """
    TxtCallerFunction = inspect.currentframe().f_code.co_name
    for ItemList in ArrLists:
        for ItemKey, ItemDefinition in ItemList.items():
            if IsLookInKey ==True: # 1. if IsLookInKey ==True
                if ItemKey == VarValueToLook: # 2. if ItemKey == VarValueToLook
                    return ItemDefinition
            else: # 1. if IsLookInKey ==True
                if ItemDefinition == VarValueToLook: # 2. if ItemKey == VarValueToLook
                    return ItemKey
    return "Err01" + TxtCallerFunction + ": Element '" + str(VarValueToLook) + "' was not found in the lists given"
#Anaplan functions
def Return_ObjAPConnection(TxtWorkspaceID:str,TxtModelID:str):
    #Likely there's a bug on AP on handshake since the error it's random when logging to the site, we are going to try 3 times before time out (previous ssl context has dimminished but it's not completly gone)
    TxtCertPath=TxtUserDownloadsFolder + TxtCert;TxtPrivateKeyPath=TxtUserDownloadsFolder + TxtPrivateKey;TxtFilePathBin=TxtUserDownloadsFolder+ TxtFileBin;TxtFilePathkey=TxtUserDownloadsFolder+TxtFilekey
    NumRetries=0;MaxRetries=3
    while NumRetries < MaxRetries:
        try: # 1. try (do the auth on AP Server)    
            APAuth =anaplan.anaplan.authorize("Certificate",private_key=TxtPrivateKeyPath, certificate=TxtCertPath,TxtFilePathBin=TxtFilePathBin,TxtFilePathkey=TxtFilePathkey)
            #You can use TxtPassword="yourpassphrase" instead of bin and key
            #APAuth =anaplan.anaplan.authorize("Certificate",private_key=TxtPrivateKeyPath, certificate=TxtCertPath,TxtPassword="yourpassphrase")
            #Likely there's a bug on AP on handshake since the error it's random when logging to the site, we are going to try 3 times before time out (previous ssl context has dimminished but it's not completly gone)
            ObjAPConnection = AnaplanConnection(authorization=APAuth, workspace_id=TxtWorkspaceID, model_id=TxtModelID)
            break
        except: # 1. try (do the auth on AP Server)
            time.sleep(5)
            NumRetries+=1
    if NumRetries== MaxRetries: # 1. if NumRetries== MaxRetries
        return None
    else:
        return ObjAPConnection
    
NumStartTime = time.time()
ObjAPConnection=Return_ObjAPConnection(TxtWorkspaceID,TxtModelID)
ListFiles = anaplan.anaplan.get_list(conn=ObjAPConnection, resource="files");ListProcesses = anaplan.anaplan.get_list(conn=ObjAPConnection, resource="processes")
ListImports = anaplan.anaplan.get_list(conn=ObjAPConnection, resource="imports");ListActions = anaplan.anaplan.get_list(conn=ObjAPConnection, resource="actions")
ListExports = anaplan.anaplan.get_list(conn=ObjAPConnection, resource="exports");Listlists = anaplan.anaplan.get_list(conn=ObjAPConnection, resource="lists")
#print(ListFiles);print(ListProcesses);print(ListImports);print(ListActions)
#print(ListExports);print(Listlists)
# Convert custom objects to a dictionary
DictListFiles={};DictListProcesses={};DictListImports={};DictListActions={};DictListExports={};DictListlists={}
DictListFiles = {key: value for key, value in ListFiles};DictListProcesses = {key: value for key, value in ListProcesses}
DictListImports = {key: value for key, value in ListImports};DictListActions = {key: value for key, value in ListActions}
DictListExports = {key: value for key, value in ListExports};DictListlists = {key: value for key, value in Listlists}
ArrLists = [DictListFiles, DictListProcesses, DictListImports, DictListActions, DictListExports, DictListlists]
#upload a file, execute its actions and get the log
TxtLogFileUpload = anaplan.anaplan.file_upload(conn=ObjAPConnection,file_id=DictListFiles[TxtServerFileToUpload], chunk_size=25, data=TxtUserDownloadsFolder + TxtLocalFileToUpload, IsReturnLog=True)
if Return_IsRegexInStr(TxtLogFileUpload, r"Err\d{2}") == True: # 1. if Return_IsRegexInStr(TxtLogFileUpload, r"Err\d{2}") == True
    print(TxtLogFileUpload)
    sys.exit()
print(TxtLogFileUpload)

for ItemArrTxtActionsID in ArrTxtActionsID:
    ArrTxtResults = anaplan.anaplan.execute_action(conn=ObjAPConnection, action_id=ListProcesses[ItemArrTxtActionsID], retry_count=3,IsErrorDumpNeeded=False)
    ArrDataFramesErrors=[];ArrTxtOutputs=[]
    for ItemArr in ArrTxtResults.reponses:
        TxtTaskID=ItemArr._raw_response['objectId']
        if ItemArr._error_dump == True: # 2. if ItemArr._error_dump == True
            #If needed 
            #ArrTxtResults.error_dumps[NumErrorsFound]
            #this will get the errors as pandas dataframes, but you must turn on IsErrorDumpNeeded=True (or omit it as by default it gets the errors)
            NumErrorsFound=+1
            ArrTxtOutputs.append("Err01." + Return_VarLookInListsItem(TxtTaskID,ArrLists,False) + ". Warning or errors found! Further Details: " + ItemArr._task_detail.split("\n")[0])
        else: # 2. if ItemArr._error_dump == True
            ArrTxtOutputs.append("Ok01." + Return_VarLookInListsItem(TxtTaskID,ArrLists,False) + ". Process executed successfully!")    
    if len(ArrTxtResults.reponses)==NumErrorsFound: # 3. if len(ArrTxtResults)==NumErrorsFound
        ArrTxtOutputs.append("Err01." + TxtTaskID + ". Process was unable to complete due to errors! Check following logs")
        IsErrorInETL=True
    elif NumErrorsFound==0: # 3. if len(ArrTxtResults)==NumErrorsFound
        ArrTxtOutputs.append("Ok01." + Return_VarLookInListsItem(TxtTaskID,ArrLists,False) + ". Process completed successfully! Following logs are for reference")
        IsAPRanSuccess=True
    elif len(ArrTxtResults.reponses)!=NumErrorsFound: # 3. if len(ArrTxtResults)==NumErrorsFound
        ArrTxtOutputs.append("War01." + Return_VarLookInListsItem(TxtTaskID,ArrLists,False) + ". Process complete but with failures! Check following logs")
        IsAPRanSuccess=True
TxtLogAP = ArrTxtOutputs[len(ArrTxtOutputs)-1] + "\n" +"\n".join(ArrTxtOutputs) 
NumEndTime=time.time()    
print(f"Elapsed time: {round(NumEndTime-NumStartTime,1)} seconds")
print(TxtLogAP)
```

## Known Issues
Sometimes even with SSL patch is not enoguh and a certificate needs to be added to the env variables to be taken by requests


## Contributing
Feel free to fork it or use it.

## License
[BSD](https://opensource.org/licenses/BSD-2-Clause)
