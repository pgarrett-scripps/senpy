from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Ip2 File Parser'
LONG_DESCRIPTION = 'Parser for Various Ip2 related file structures: ms2, sqt, dta-select, fasta, idx'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="senpy",
    version=VERSION,
    author="Patrick Garrett",
    author_email="<pgarrett@scripps.edu>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)