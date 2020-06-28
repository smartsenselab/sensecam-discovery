import setuptools

REQUIREMENTS = [line for line in open('requirements.txt').read().split('\n') if line != '']

VERSION = '2.1.6'
AUTHOR = 'Ricardo Barbosa Filho (Smart Sense Laboratory)'
EMAIL = 'ricardob@dcc.ufmg.br'

setuptools.setup(
    name="sensecam_discovery",
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description="A package to discover all onvif cameras on your network",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/smartsenselab/sensecam-discovery",
    packages=setuptools.find_packages(),
    classifiers=[
        'Natural Language :: English',
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
    ],
    python_requires='>=3.6',
    install_requires=REQUIREMENTS,
)
