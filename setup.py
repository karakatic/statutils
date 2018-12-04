import setuptools
import os
import logging

PACKAGE_NAME = 'stat-utils'


def read_package_variable(key, filename='__init__.py'):
    """Read the value of a variable from the package without importing."""
    module_path = os.path.join(PACKAGE_NAME, filename)
    with open(module_path) as module:
        for line in module:
            parts = line.strip().split(' ', 2)
            if parts[:-1] == [key, '=']:
                return parts[-1].strip("'")
    logging.warning("'%s' not found in '%s'", key, module_path)
    return None


with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name=read_package_variable('__project__'),
    version=read_package_variable('__version__'),
    author='Sašo Karakatič',
    author_email='karakatic@gmail.com',
    description='Utils for statistics, mainly inspired by R packages.',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/karakatic/stat-utils',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering',
    ],
    install_requires=[
        'numpy'
    ]
)
