*Note: This package is fixed from the original one for typos and coding enhancements.*

# anaplan-api

Anaplan-API is a Python library wrapper for [Anaplan Bulk API](https://anaplanbulkapi20.docs.apiary.io/) and [Anaplan Authentication API](https://anaplanauthentication.docs.apiary.io/).

## Installation
If you are on a corporate environment you need to install:

pip install pip-system-certs

[S.O. Thread](https://stackoverflow.com/a/57053415/3221380) 

[pip-system-certs project](https://gitlab.com/alelec/pip-system-certs)


```python
#It is strongly advised to use the line
import pip_system_certs.wrapt_requests
#Before the usage of this API to avoid requests being loaded
import anaplan_api
```

Use the package manager [pip](https://pypi.org/project/anaplan-api/) to install Anaplan-API.


```bash
pip3 install anaplan_api
```
You may overwrite the original install of that one with the scripts of this one, or directly use this package.

## Usage

```python
import logging
from anaplan_api import anaplan
from anaplan_api.AnaplanConnection import AnaplanConnection
from anaplan_api.KeystoreManager import KeystoreManager

logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
					datefmt='%H:%M:%S',
					level=logging.INFO)

logger = logging.getLogger(__name__)

if __name__ == '__main__':
	keys = KeystoreManager(path='/keystore.jks', passphrase='', alias='', key_pass='')

	auth = anaplan.generate_authorization(auth_type='Certificate', cert=keys.get_cert(), private_key=keys.get_key())
	conn = AnaplanConnection(authorization=auth, workspace_id='', model_id='')

	anaplan.file_upload(conn=conn, file_id="", chunk_size=5, data='/Users.csv')

	results = anaplan.execute_action(conn=conn, action_id="", retry_count=3)

	for result in results:
		if result: # Boolean check of ParserResponse object, true if failure dump is available
			print(result.get_error_dump())
```

## Known Issues
This library currently uses PyJKS library for handling Java Keystore files. I omitted those since they create issues.


## Contributing
Feel free to fork it or use it.

## License
[BSD](https://opensource.org/licenses/BSD-2-Clause)
