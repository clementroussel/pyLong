# Welcome to pyLong project

**pyLong** is a free and open-source software dedicated to the visualization, analysis, publishing and processing of hydraulic (but not only) longitudinal profile... Visit the online documentation to learn more about **pyLong** : https://pylong.readthedocs.io/en/latest/

## Instructions to build **pyLong** from sources

The easiest way to build **pyLong** from sources is to use *Conda*.

1. Install *Conda* for your operating system: [miniconda](https://docs.conda.io/en/latest/miniconda.html)
2. Download *pyLong main repository* : [pyLong-main](https://github.com/clementroussel/pyLong/archive/refs/heads/main.zip)
3. Unzip the archive and keep only the *src* and *requirements* folders
4. Open a *Conda Powershell Prompt* and move to the **pyLong** directory
5. Create and activate a virtual environment dedicated to **pyLong**:

    ```conda create --name pyLong-venv python=3.6```
    ```conda activate pyLong-venv```

6. Install the required modules:

    ```pip install -r requirements/base.txt```

7. Run **pyLong**:

    ```fbs run```

### About *fbs*

To learn more about *fbs* module, visit https://build-system.fman.io/.
