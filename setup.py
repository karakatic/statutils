import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stat-utils",
    version="0.1.0",
    author="Sašo Karakatič",
    author_email="karakatic@gmail.com",
    description="Utils for statistics, mainly inspired by R packages.",
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/karakatic/stat-utils",
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
