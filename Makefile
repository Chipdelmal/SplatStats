SHELL=bash
python=python
pip=pip
tests=.
version:=$(shell $(python) version.py)
sdist_name:=SplatStats-$(version).tar.gz


###############################################################################
# Dev
###############################################################################
develop:
	$(pip) install -e .

clean_develop:
	- $(pip) uninstall -y SplatStats
	- rm -rf *.egg-info

clean_sdist:
	- rm -rf dist

clean: 
	- make clean_develop 
	- make clean_pypi

pypi: clean clean_sdist
	set -x \
	&& $(python) setup.py sdist bdist_wheel \
	&& twine check dist/* \
	&& twine upload dist/* \
	&& pip install .

clean_pypi:
	- rm -rf build/

doc:
	- pip install .
	- sphinx-apidoc -f -o docs/source SplatStats
	- sphinx-build -b html docs/source/ docs/build/html

###############################################################################
# Conda
###############################################################################
conda_update:
	- conda update --all -y
	- pip freeze > ./requirements.txt
	- conda env export | cut -f 1 -d '=' | grep -v "prefix" > ./requirements.yml

conda_export:
	- pip freeze > ./requirements.txt
	- conda env export | cut -f 1 -d '=' | grep -v "prefix" > ./requirements.yml

###############################################################################
# Docker SplatStats
###############################################################################
docker_build:
	- docker rmi splatstats:dev -f
	- docker build -f Dockerfile.splatstats -t splatstats:dev .

docker_build_force:
	- docker rmi splatstats:dev -f
	- docker build -f Dockerfile.splatstats --no-cache -t splatstats:dev .

docker_run:
	- docker run -v "$(pwd)":/data/ splatstats:dev  --download "True" --upload "True" --player 'čħîþ ウナギ'

docker_run_python:
	- docker run -it splatstats:dev python

docker_run_bash:
	- docker run -it --entrypoint /bin/bash splatstats:dev

docker_exec:
	- docker run -v "$(pwd)":/data/ -it splatstats:dev bash

docker_release:
	- docker build -f Dockerfile.splatstats -t chipdelmal/splatstats:$(version) .
	- docker push chipdelmal/splatstats:$(version)
	- docker build -f Dockerfile.splatstats -t chipdelmal/splatstats:latest .
	- docker push chipdelmal/splatstats:latest

###############################################################################
# Docker InkStats
###############################################################################
docker_build_ink:
	- docker rmi inkstats:dev -f
	- docker build -f Dockerfile.inkstats -t inkstats:dev .

docker_build_force_ink:
	- docker rmi inkstats:dev -f
	- docker build -f Dockerfile.inkstats --no-cache -t inkstats:dev .

docker_run_ink:
	- docker run -v "$(pwd)":/data/ inkstats:dev  --download "True" --upload "True" --player 'čħîþ ウナギ'

docker_run_python_ink:
	- docker run -it inkstats:dev python

docker_run_bash_ink:
	- docker run -it --entrypoint /bin/bash inkstats:dev

docker_exec_ink:
	- docker run -v "$(pwd)":/data/ -it inkstats:dev bash

docker_release_ink:
	- docker build -f Dockerfile.splat -t chipdelmal/inkstats:$(version) .
	- docker push chipdelmal/inkstats:$(version)
	- docker build -f Dockerfile.splat -t chipdelmal/inkstats:latest .
	- docker push chipdelmal/inkstats:latest

###############################################################################
# Full version release
###############################################################################
full_release:
	- make pypi
	- make docker_release