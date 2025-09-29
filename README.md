# Demonstrate path traversal with Python CVE-2024-23334
## run Python app that uses aiohttp v3.9.1 and allows for directory traversal
* RUN on Linux!
* if you do not already have a virtual environment for Python: `python -m venv venv`
* some convenience scripts `show-vuln.sh` `show-fix.sh` and `clean.sh` have been included
* make sure you have a pip.conf in your venv dir that lists: `https://aaron.miller%40chainguard.dev:****@chainguard.jfrog.io/artifactory/api/pypi/python-all-remediated/simple` as it's [global] index-url

## Fast way
Run from a Linux machine:
`show-vuln.sh`
`show-fix.sh`
`clean.sh`

## To go step-by-step:
* start your local venv, `source venv/bin/activate`
* install `pip install aiohttp==3.9.1`
* start the app `python3 app.py`
* show `curl --path-as-is http://127.0.0.1:8080/static/../private/secrets.txt`
will show 404
* now uninstall `pip uninstall -y -r <(pip freeze)` and `pip cache purge`
* move the pip.conf to pip.conf.bak
* install again and run the app.py
* it'll show the secret
