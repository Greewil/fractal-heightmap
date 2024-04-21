from setuptools import setup, find_packages
import codecs
import os

from src.world_map_generator.default_values import GENERATOR_VERSION

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "src/README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = GENERATOR_VERSION
print(f'App version: {VERSION}')
DESCRIPTION = 'Heightmap landscape generator which allows to generate and modify infinite size 2d worlds.'

# Setting up
setup(
    name="world_map_generator",
    version=VERSION,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    author="Greewil (Shishkin Sergey)",
    author_email="shishkin.sergey.d@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/Greewil/fractal-heightmap",
    install_requires=['Pillow', 'numpy', 'scipy', 'typing_extensions'],
    keywords=['python', 'map generation', 'world generation', 'heightmap'],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.10"
)

# https://pypi.org/classifiers/

# # Usage:
# pip install wheel
# python setup.py bdist_wheel sdist
# twine check dist/*
# twine upload -r testpypi dist/*
# twine upload dist/*
