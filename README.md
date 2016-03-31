python-cloudns
==============

python-cloudns is a pythonic module to interact with the ClouDNS HTTP API (http://www.cloudns.net)

Currently it only implements the API functions.

python-cloudns requires the requests module


## Usage

Using python-cloudns is relatively simple

```python
import cloudns

a = cloudns.api('username', 'password');
a.test_login();
```

