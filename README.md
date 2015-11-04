# Clinical Trials Research Downloader


### Summary

This program downloads research of specified criteria from clinicaltrials.gov and stores said research in Pandas DataFrames on disk.


### Installation

Once cloned from the repository, you will need to be able to run Python 3 with a few additional libraries installed. If you do not have Python 3 installed, now is a great time to install it. Thankfully, Pip makes installation of these really easy once the program has been downloaded with the reuirements file in the root-level directory of the repository folder (If you haven't set up a virtual environment yet, please read below first):
```
pip install -r requirements.txt
```

It is recommended, however that you set up a virtual environment for this.

To do this, you will need to install virtualenv via pip. It's pretty easy to do:
(On Windows exclude the *sudo*)
```
sudo pip install virtualenv
```

Once this is done, you will want to create a 'virtualenv'. This is done, unsurprisingly, by using the *virtualenv* command. You will want to place this environment outside of the repository, but generally close-by. You will need to specify the path to your Python 3 installation as well. Something like:
```
virtualenv ../venv --python=path/to/Python3
```

This will mask all calls to Pip and Python with that respective version of python, and will encapsulate all the libraries you want installed within the virtual environment so you can have a "virtualenv" prepared for every program or project.

You can activate the environment with:
```
source ../venv/bin/activate
```
and deactivate it with:
```
deactivate
```

Now that your virtual environment is configured, activate it and run:
```
pip install -r requirements.txt
```
...and your program should be ready to run!


If you want to automate the program, possibly via cron job, through the env, instead of calling python normally you can do:
```
../full/path/to/venv/bin/*python3* /full/path/to/main.py
```
...with the Python command dependent on which python you initialized the virtual environment with.


### Specifying Search Parameters

This program can download research for any number of criteria as specified in a text file in the root directory of the program titled *params.txt*.

Each line of this file specifies separate search criteria which will be used
to gather results for that criteria in a folder within *root_directory*/downloads/*criteria*.

For example, say you want to look up trials and research relevant to lung transplants, seizures, and brain tumors. You will format the file as such:

*params.txt*
```
lung transplant
seizure
brain tumor
```

Once this file is in place, just run the program as normal and it will retrieve all the relevant research!