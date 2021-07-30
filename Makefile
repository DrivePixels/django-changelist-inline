PHONY: clean lint test build publish

clean:
	rm -rf build/ dist/ django_changelist_inline.egg-info/

lint:
	flake8 django_changelist_inline/ testing/ tests/ settings.py setup.py

test:
	pytest

build:
	python setup.py build sdist bdist_wheel

publish:
	twine upload --repository pypi --skip-existing dist/*
