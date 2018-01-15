Installation
====================================
MODE-TASK can be installed by following the instruction given at http://mode-task.readthedocs.io/en/latest/installation.html

**For installing the pyMODE-TASK - a pymol plugin.**

*Requirements:*

::

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
::
	
	git clone https://github.com/RUBi-ZA/pyMODE-TASK.git


**OR**

Download zip from github page and extract to a directory.

**2. Install dependencies:**

Run the following command from within pyMODE-TASK directory
::

	sudo pip install -r requirements.txt


pyMODE-TASK requires Tkinter and Pmw.1.3. Tkinter comes prepackaged with most standard python. Pmw could be installed by following the instruction from:
http://pmw.sourceforge.net/doc/starting.html

**3. Install pyMODE-TASK plugin in pymol:**

3.1. Start pymol

3.2. Go to Plugin -> Plugin Manager, and clcik on install new plugin tab. Under install from local file click on 'choose file...' button.
Browse the pyMODE-TASK.py and follow the on screen installation instructions.
 
3.3. If everything goes well, you can start the plugin from pymol plugin menu. 

**Usage**

For more detailed documentation on installation and usage of the tool suite please see our [ReadTheDocs](http://pymode-task.readthedocs.io/en/latest/index.html) site


