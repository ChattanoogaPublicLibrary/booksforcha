.PHONY: clean-pyc clean-build docs clean

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "sniffer - autotest"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "dist - package"
	@echo "install - install the package to the active Python's site-packages"

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint:
	flake8 booksforcha tests

test:
	RSS_FEED_LIST='' REDIS_KEYSPACE='BFC_TEST' REDIS_URL='redis://localhost:6379' CONSUMER_KEY='' CONSUMER_SECRET='' ACCESS_TOKEN='' ACCESS_TOKEN_SECRET='' nosetests

test-all:
	tox

coverage:
	RSS_FEED_LIST='' REDIS_KEYSPACE='BFC_TEST' REDIS_URL='redis://localhost:6379' CONSUMER_KEY='' CONSUMER_SECRET='' ACCESS_TOKEN='' ACCESS_TOKEN_SECRET='' coverage run --source booksforcha setup.py test
	coverage report -m
	coverage html

sniffer:
	RSS_FEED_LIST='' REDIS_KEYSPACE='BFC_TEST' REDIS_URL='redis://localhost:6379' CONSUMER_KEY='' CONSUMER_SECRET='' ACCESS_TOKEN='' ACCESS_TOKEN_SECRET='' sniffer

docs:
	rm -f docs/booksforcha.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ booksforcha
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

release: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean
	python setup.py install
