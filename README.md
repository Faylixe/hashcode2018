# hashcode2018

Qualification round code for Google Hash Code 2018

## Installation

First retrieve repository content using ``git`` and initialize the contest
environment using ``init.sh`` script :

```bash
git clone https://github.com/Faylixe/hashcode2018
bash init.sh workspace_name
```

It will prompt for your google account credential which will be used for automatic submission.

The **workspace_name** parameter should be your initial.

## Usage

The initialization script will configure required environment variable and a ``virtualenv`` which
have required python dependencies and the ``run`` command.

```bash
run greedy.py small
```

It will run the script ``greedy.py`` located in your workspace (under ``workspace/your_initial``directory),
using small dataset.

The run command ensure the repository is up to date by performing a ``git pull`` command, then run your script
managing automatically solution storage and managment, computing score and uploading code and solution file
to the judge platform automatically.
