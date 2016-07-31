"""Packaging, dependency management, and distribution via setuptools.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject

Extracted 2016-06-05
"""

# Always prefer setuptools over distutils
from setuptools import setup
# To use a consistent encoding
import os.path

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as ff:
    long_description = ff.read()

setup(
    # TBD: entry_points, classifiers, keywords
    name='jobflask',
    description='JobFlask: an implementation of JobJar using Flask.',
    long_description=long_description, # Extracted from README.rst, above
    use_scm_version=True,
    setup_requires=[ 'setuptools_scm' ],
    license='GNU General Public License, Version 2',
    author='Hal Peterson',
    packages=[ 'jobflask' ],
    scripts=[ 'jobflask.py' ],
    install_requires=['sqlalchemy', 'flask'], # ... and more TBD
    package_data={
        'jobflask' : ['static/*', 'templates/*'],
    }
)
