# Welcome to pyLong project

Visit the online documentation to learn more about **pyLong** : https://pylong.readthedocs.io/en/latest/

## Instructions to build **pyLong** from sources

### On Windows

#### Python installation

Beaucune *pyLong* depends on *fbs==0.9.0*, it needs *python 3.6* to be properly configured.  

* Download *python 3.6.8* : https://www.python.org/downloads/release/python-368/
* Launch the installer and watch to activate *Add Python 3.6 to PATH* checkbox

#### Download *pyLong* repository

* Download *pyLong repository* : https://github.com/clementroussel/pyLong/archive/refs/heads/main.zip
* Unzip the archive and keep only the *src* and *requirements* folders

#### Create a virtual environment

* Launch a terminal and use *cd* command:

   ```cd path/to/pyLong-main/folder```

* Use *pypi* to install *virtualenv module*

   py -3.6 -m pip install virtualenv

* Create a virtual environment with *python virtualenv module*:

    py -3.6 -m virtualenv venv

* Activate the virtual environment with:

   venv\Scripts\activated

#### Install *pyLong* dependancies

* Use *pypi* to install the required dependancies:

   pip install -r requirements/base.txt

#### Launch *pyLong*

* Use *fbs run* command to run *pyLong*

   fbs run







