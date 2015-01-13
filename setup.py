import os
from setuptools import setup

# suri-pdns
# Parse suricata logs and output DNS data.

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "suri-pdns",
    version = "0.0.1",
    description = "Parse suricata logs and output DNS data.",
    author = "Johan Nestaas",
    author_email = "johan.nestaas@riskiq.com",
    license = "BSDv2",
    keywords = "suricata,pdns",
    url = "https://github.com/RiskIQ/suri-pdns",
    packages=['suri_pdns'],
    package_dir={'suri_pdns': 'suri_pdns'},
    long_description=read('README.md'),
    classifiers=[
        #'Development Status :: 1 - Planning',
        #'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        #'Development Status :: 6 - Mature',
        #'Development Status :: 7 - Inactive',
        'License :: OSI Approved :: BSD License',
        'Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
    ],
    install_requires=[
        'ujson',
    ],
    entry_points = {
        'console_scripts': [
            'suri-pdns = suri_pdns.pdns:main',
        ],
    },
    #package_data = {
        #'suri-pdns': ['catalog/*.edb'],
    #},
    #include_package_data = True,
)
