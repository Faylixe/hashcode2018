# hashcode2018

Qualification round code for Google Hash Code 2018

## Installation

First retrieve repository content using ``git`` and initialize the contest
environment using ``init.sh`` script :

```bash
git clone https://github.com/Faylixe/hashcode2018
bash init.sh
```

It will prompt for your google account credential which will be used for automatic submission,
and for target round identifier, which can be found in the round URL as following :

![round](https://github.com/Faylixe/hashcode2018/blob/master/docs/round.png)

Dataset files will be downloaded automatically for the given round, and written into the ``dataset`` folder.

## Usage

The initialization script will configure required environment variable and a ``virtualenv`` which
have required python dependencies and the ``run`` command.

```bash
run greedy.py small
```
