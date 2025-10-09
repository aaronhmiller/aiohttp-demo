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

## The Docker way
First, ensure you have a Chainguard library accessing file named `pip.conf.docker` in your `venv` directory
### Build your containers
`docker build -f Dockerfile-cg -t aiohttp-fix .`
`docker build -f Dockerfile-non-cg -t aiohttp-vuln .`
### Run them
`docker run --name vuln --rm aiohttp-vuln -p 8080:8080`
Run the `docker exec -it vuln curl --path-as-is http://0.0.0.0:8080/static/../private/secrets.txt` command and see the secret text indicating the vulnerability is there.
ctrl-c
`docker run --name fix --rm aiohttp-fix -p 8080:8080`
Now run the same command, but point at the fix container name:
`docker exec -it fix curl --path-as-is http://0.0.0.0:8080/static/../private/secrets.txt`
And see the 404 that indicates the fix is in place.
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
