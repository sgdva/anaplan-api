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
from crytpography.fernet import Fernet
import ssl
import anaplan_api
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

def Return_ObjAPConnection(TxtWorkspaceID:str,TxtModelID:str):

    TxtCertPath=TxtUserDownloadsFolder + './mycert.pem';TxtPrivateKeyPath=TxtUserDownloadsFolder + './myprivatekey.key';TxtFilePathBin='./2.bin';TxtFilePathkey='./1.key'

    NumRetries=0;MaxRetries=3

    while NumRetries < MaxRetries:

        #Likely there's a bug on AP on handshake since the error it's random when logging to the site, we are going to try 3 times before time out (previous ssl handshake has dimminished but it's not completly gone)

        try: # 1. try (do the auth on AP Server)

            APAuth = anaplan_api.generate_authorization(auth_type='Certificate', cert=TxtCertPath, private_key=TxtPrivateKeyPath,TxtFilePathBin=TxtFilePathBin,TxtFilePathkey=TxtFilePathkey)

            ObjAPConnection = anaplan_api.AnaplanConnection(authorization=APAuth, workspace_id=TxtWorkspaceID, model_id=TxtModelID)

            break

        except: # 1. try (do the auth on AP Server)

            time.sleep(5)

            NumRetries+=1

    if NumRetries== MaxRetries: # 1. if NumRetries== MaxRetries

        return None

    else: # 1. if NumRetries== MaxRetries

        return ObjAPConnection

   

ObjAPConnection=Return_ObjAPConnection("TxtWorkspaceID","TxtModelID")

ListFiles = anaplan_api.get_list(conn=ObjAPConnection, resource="files");ListProcesses = anaplan_api.get_list(conn=ObjAPConnection, resource="processes")

ListImports = anaplan_api.get_list(conn=ObjAPConnection, resource="imports");ListActions = anaplan_api.get_list(conn=ObjAPConnection, resource="actions")

ListExports = anaplan_api.get_list(conn=ObjAPConnection, resource="exports");Listlists = anaplan_api.get_list(conn=ObjAPConnection, resource="lists")

print(ListFiles);print(ListProcesses);print(ListImports);print(ListActions)

print(ListExports);print(Listlists)
```

## Known Issues
This library currently uses PyJKS library for handling Java Keystore files. I omitted those since no JKS solution at this time.


## Contributing
Feel free to fork it or use it.

## License
[BSD](https://opensource.org/licenses/BSD-2-Clause)
