<img src='https://readthedocs.org/projects/pymode-task/badge/?version=latest'  align="right"/> <img src ='https://img.shields.io/badge/python-3-blue.svg' align="right"> 


# pyMODE-TASK

update: 13Apr2023. Earlier version was only python2 compatible. Now it works with python3 only.

MODE-TASK plugin for PyMOL

Command line version is [available here](https://github.com/RUBi-ZA/MODE-TASK).

**For installing the pyMODE-TASK - a pymol plugin.**

*Requirements:*

	python
	Tkinter
	Pmw
	numpy==1.13.1
	cython==0.26
	scikit-learn==0.19.0
	scipy==0.19.1
	sklearn==0.0
	matplotlib==2.0.2
	mdtraj==1.8.0


**1. Download the project:**
	
	git clone https://github.com/RUBi-ZA/pyMODE-TASK.git


**OR**

Download zip from github page and extract to a directory.

**2. Install dependencies:**

Run the following command from within pyMODE-TASK directory

	sudo pip install -r requirements.txt


pyMODE-TASK requires Tkinter and Pmw.1.3. Tkinter comes prepackaged with most standard python. Pmw could be installed by following the instruction from:
http://pmw.sourceforge.net/doc/starting.html

**3. Install pyMODE-TASK plugin in pymol:**

3.1. Start pymol

3.2. Go to Plugin -> Plugin Manager, and clcik on install new plugin tab. Under install from local file click on 'choose file...' button.
Browse the pyMODE-TASK.py and follow the on screen installation instructions.
 
3.3. If everything goes well, you can start the plugin from pymol plugin menu. 

## Usage

For more detailed documentation on installation and usage of the tool suite please see our [ReadTheDocs](http://pymode-task.readthedocs.io/en/latest/index.html) site

## Contributing to the project

Questions and issues can be posted to the [issue tracker](https://github.com/RUBi-ZA/pyMODE-TASK/issues).

Pull requests are welcome and will be reviewed however a guarentee can not me made as to your request being accepted.

The documentation is hosted by [ReadTheDocs](https://readthedocs.org/) and makes use of reStructuredText for markdown with Latex for mathematical equasions. See [here](https://docs.readthedocs.io/en/latest/getting_started.html) for a more detailed guideline on creating documentation for ReadTheDocs.


## Citation

**MODE-TASK: Large-scale protein motion tools**

*Caroline Ross, Bilal Nizami, Michael Glenister, Olivier Sheik Amamuddy, Ali Rana Atilgan, Canan Atilgan, Özlem Tastan Bishop;*
[Bioinformatics, Volume 34, Issue 21, 1 November 2018](https://academic.oup.com/bioinformatics/article/34/21/3759/5021681) <br/>
[![doi](http://img.shields.io/badge/doi-10.1093%2Fbioinformatics%2Fbty427-blue.svg?style=flat)](https://academic.oup.com/bioinformatics/article/34/21/3759/5021681) 
[![pubmed](http://img.shields.io/badge/pubmed-29850770-blue.svg?style=flat)](https://www.ncbi.nlm.nih.gov/pubmed/29850770)


### TODO list:
- [X] Fully functional and ready to install plugin.
- [X] Resize/adjust NMA tab.
- [ ] Add progress bar.
- [X] Update link in MODE-TASK documentation.
- [ ] Add better handling of exceptions in NMA tab.
- [ ] Add feature to identify the MD frame in the PCA projection plot. 

