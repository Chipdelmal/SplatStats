
import os
import setuptools
from version import version as this_version

this_directory =  os.path.abspath(os.path.dirname(__file__))
version_path = os.path.join(this_directory, 'SplatStats', '_version.py')
with open(version_path, 'wt') as fversion:
    fversion.write('__version__ = "'+this_version+'"')

REQUIRED_PACKAGES=[
    'dill', 'termcolor', 'colorutils', 'tqdm',
    'numpy', 'scipy', 'pandas', 
    'matplotlib', 'pywaffle', 'squarify'
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SplatStats",
    install_requires=REQUIRED_PACKAGES,
    version=this_version,
    author="chipdelmal",
    scripts=[],                           
    author_email="chipdelmal@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Chipdelmal/SplatStats",
    packages=setuptools.find_packages(),
    extras_require={
        'dev': ['twine', 'wheel', 'sphinx', 'sphinx-bootstrap-theme']
    },
    python_requires='>=3.10',
    license='GPLv3',
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ]
)