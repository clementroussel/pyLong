# Welcome to pyLong project

**pyLong** is a free and open-source software dedicated to the visualization, analysis, publishing and processing of hydraulic (but not only) longitudinal profile... Visit the online documentation to learn more about **pyLong** : https://pylong.readthedocs.io/en/latest/

## Instructions to build **pyLong** from sources

The easiest way to build **pyLong** from sources is to use *Conda*.

1. Install *Conda* for your operating system: [miniconda](https://docs.conda.io/en/latest/miniconda.html)
2. Download *pyLong main repository* : https://github.com/clementroussel/pyLong/archive/refs/heads/main.zip
3. Unzip the archive and keep only the *src* and *requirements* folders
4. Open a *Conda Powershell Prompt* and move to the **pyLong** directory
5. Create and activate a virtual environment dedicated to **pyLong**:

    ```conda create --name pyLong-venv python=3.6```
    ```conda activate pyLong-venv```

6. Install the required modules:

    ```pip install -r requirements/base.txt```

7. Run **pyLong**:

    ```fbs run```

[On Windows 10](#on-windows-10)  
[On Ubuntu 20.04](#on-ubuntu)  
[On macOS Big Sur](#on-macOS)  

### On Windows 10

#### Python installation

Because *pyLong* depends on *fbs==0.9.0*, it needs *python 3.6* to be properly configured.  

* Download *python 3.6.8* : https://www.python.org/downloads/release/python-368/
* Launch the installer and watch to activate *Add Python 3.6 to PATH* checkbox

#### Download *pyLong* repository

* Download *pyLong repository* : https://github.com/clementroussel/pyLong/archive/refs/heads/main.zip
* Unzip the archive and keep only the *src* and *requirements* folders

#### Create a virtual environment

* Launch a terminal and use *cd* command:

   ```cd path/to/pyLong-main/folder```

* Use *PyPI* to install *virtualenv* module

   ```py -3.6 -m pip install virtualenv```

* Create a virtual environment with *python* *virtualenv* module:

    ```py -3.6 -m virtualenv venv```

* Activate the virtual environment with:

   ```venv\Scripts\activate```

#### Install *pyLong* dependancies

* Use *PyPI* to install the required dependencies:

   ```pip install -r requirements/base.txt```

#### Launch *pyLong*

* Use *fbs run* command to run *pyLong*

   ```fbs run```

### On Ubuntu

balbla

### On macOS



#### About *fbs*

To learn more about *fbs* module, visit https://build-system.fman.io/.








