#!/usr/bin/env python
#filename: pypca.py

#--------------------------------------------------
# TO DO
#===================================================
# 1. Add astrik over required input field --- done
# 2. check to look for mode-task files within conf setting ----	done
# 3. Resize/adjust NMA tab. -------- done
# 4. Add progress bar
# 5. Add better handling of exceptions in NMA

# pyMODE-TASK  Copyright Notice
# ============================
#
# The pyMODE-TASK -- a plugin for MODE-TASK, source code is copyrighted, but you can freely use and
# copy it as long as you don't change or remove any of the copyright
# notices.
#
# ----------------------------------------------------------------------
# pyMODE-TASK plugin is Copyright (C) 2017 by Bilal Nizami
#
#                        All Rights Reserved
#
# Permission to use, copy, modify, distribute, and distribute modified
# versions of this software and its documentation for any purpose and
# without fee is hereby granted, provided that the above copyright
# notice appear in all copies and that both the copyright notice and
# this permission notice appear in supporting documentation, and that
# the name of Bilal Nizami not be used in advertising or publicity
# pertaining to distribution of the software without specific, written
# prior permission.
#
# BILAL NIZAMI DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS
# SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS.  IN NO EVENT SHALL BILAL NIZAMI BE LIABLE FOR ANY
# SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER
# RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF
# CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
# ----------------------------------------------------------------------

#================================================================
import matplotlib
matplotlib.use('Agg')
import os, sys
import os.path
if sys.version_info[0] < 3:
	import Tkinter
	from Tkinter import *
	from os.path import expanduser
	home = expanduser("~")
else:
	import tkinter as Tkinter
	from tkinter import *
	from pathlib import Path
	home = str(Path.home())
	
import subprocess
from ttk import Separator, Style
import ttk
import Pmw
import tkMessageBox, tkFileDialog
import os
import pymol
from pymol import cmd
import webbrowser



__version__ = "1.0.0"

"""
pyMODE-TASK

"""

def __init__(self):
	self.menuBar.addmenuitem('Plugin', 'command',
		'Launch pyMODE-TASK',
		label='pyMODE-TASK',
		command = lambda s=self: PyMODETASK(s))
		
class PyMODETASK:
	'''Main class of pyMODE-TASK.'''
	def __init__(self, app):
		
		self.master = app.root
		adplugin_font = ("Courier", 12)
		self.frame = Frame(self.master, width=4, height=4, bg="red3", colormap="new")
		self.frame.pack()
		
		# build main window
		adplugin_font = ("Courier", 10)
		self.dialog = Pmw.Dialog(self.master,title = 'pyMODE-TASK',
									buttons = ('Exit pyMODE-TASK',))
		self.dialog.withdraw()
		self.dialog.geometry('1000x730')
		#================================================
		#
		# Menu bar
		#===============================================
		# Create about dialog.
		self.dialog1 = Pmw.MessageDialog(self.dialog.interior(),
			title = 'pyMODE-TASK',
			message_text = 'A pymol plugin for MODE-TASK\n\n'+
				'Version %s\n\n' %__version__ +
				'MODE-TASK and pyMODE-TASK is a open source collection of tools to perform the\n'+
				'Principal component analysis (PCA), MDS and t-SNE on a protein MD trajectory,\n' +
				'and Normal mode analysis (NMA) on protein 3D structure.\n'+
				'pyMODE-TASK- is Copyright (C) 2017 by Bilal Nizami, RUBi, Rhodes University.\n',
			buttonboxpos = 's',
			buttons = ('OK', 'Close'),
			defaultbutton = 'Close')
		self.dialog1.iconname('pyMODE-TASK')
		widget = self.dialog1.component('hull')
		Pmw.Color.changecolor(widget, background = 'brown4', foreground='white')
		self.dialog1.withdraw()
		
		# Create the Balloon.
		self.balloon = Pmw.Balloon(self.master)

		# Create and pack the MenuBar.
		self.menuBar = Pmw.MenuBar(self.dialog.interior(),
				hotkeys=0,
				hull_relief = 'raised',
				hull_borderwidth = 2,
				balloon = self.balloon)
		self.menuBar.pack(fill = 'x')
		
		# Add File menu bar.
		self.menuBar.addmenu('File', 'Close this window or exit')
		self.menuBar.addmenuitem('File', 'command', 'About the pyMODE-TASK',
				label = 'About',
				command=self.dialog1.activate
				)
		self.menuBar.addmenuitem('File', 'separator')
		self.menuBar.addmenuitem('File', 'command', 'Exit the application',
				label = 'Exit',
				command=self.dialog.interior().quit)
	
		# Add Help menu bar.
		page=MyHelpPage("file:///home/bilal/work/pyMODE-TASK/src/docs/build/html/index.html")
		self.menuBar.addmenu('Help', 'Help page')
		self.menuBar.addmenuitem('Help', 'command', label='Help Page',
			command=page.openpage)
		
		page=MyHelpPage("file:///home/bilal/work/MT-PyMOL/docs/build/html/index.html")
		#self.menuBar.addmenu('Help', 'pyMODE-TASK help')
		self.menuBar.addmenuitem('Help', 'command', label='pyMODE-TASK help',
			command=page.openpage)
			
		
		page=MyHelpPage("file:///home/bilal/work/pyMODE-TASK/src/docs/build/html/theory.html")		
		self.menuBar.addmenuitem('Help', 'separator')
		self.menuBar.addmenuitem('Help', 'command', label='PCA Theory',
			command=page.openpage)
		
		page=MyHelpPage("file:///home/bilal/work/pyMODE-TASK/src/docs/build/html/theory.html")		
		self.menuBar.addmenuitem('Help', 'command', label='NMA Theory', 
			command=page.openpage)
		
		self.menuBar.addmenuitem('Help', 'separator')
		page=MyHelpPage("file:///home/bilal/work/pyMODE-TASK/src/docs/build/html/pca_use.html")		
		self.menuBar.addmenuitem('Help', 'command', label='PCA Usage',
			command=page.openpage)
		
		page=MyHelpPage("file:///home/bilal/work/pyMODE-TASK/src/docs/build/html/nma_use.html")		
		self.menuBar.addmenuitem('Help', 'command', label='NMA Usage', 
			command=page.openpage)
		
		page=MyHelpPage("file:///home/bilal/work/pyMODE-TASK/src/docs/build/html/pca_tut.html")			
		self.menuBar.addmenuitem('Help', 'separator')
		self.menuBar.addmenuitem('Help', 'command', label='PCA Tutorial',
			command=page.openpage)
		
		page=MyHelpPage("file:///home/bilal/work/pyMODE-TASK/src/docs/build/html/nma_tut.html")		
		self.menuBar.addmenuitem('Help', 'command', label='NMA Tutorial',
			command=page.openpage)
		
		
		# The title
	
		self.title_label = Label(self.dialog.interior(), text = 'pyMODE-TASK: A pymol plugin of MODE-TASK -- Copyright (C) 2017, Bilal Nizami, RUBi, Rhodes University',
				background = 'brown4',
				foreground = 'white', 
				height=1, 
				width=880,
				font=('Arial', 11))
		self.title_label.pack(expand = 0, fill = 'both', padx = 1, pady = 1)
		
		# the notebook layout

		self.notebook = Pmw.NoteBook(self.dialog.interior())
		Pmw.Color.changecolor(self.dialog.interior(), background='gray70', foreground='black')
		self.notebook.recolorborders()
		self.notebook.pack(fill='both',expand=1,padx=13,pady=13)



        # build pages
		self.configuration_page = self.notebook.add('Configuration')
		self.pca_page = self.notebook.add('PCA')
		self.ipca_page = self.notebook.add('Internal PCA')
		self.mds_page = self.notebook.add('MDS/t-SNE')
		self.nma_page = self.notebook.add('NMA')
		self.about_page = self.notebook.add('About')
		self.citation_page = self.notebook.add('Citation')
		self.help_page = self.notebook.add('Help and Credit')
		
		#---------------------------------------------------------------
        # 							configuration PAGE
		#---------------------------------------------------------------
		
		self.balloon = Pmw.Balloon(self.master)
		about_pca = """Give the location of pyMODE-TASK directory.  For example- If the pyMODE-TASK
directory is in user's home, then pyMODE-TASK directory field should read like /home/user/pyMODE-TASK. 
Normally the core scripts should be within pyMODE-TASK/src directory."""
		
		self.conf_top_group = Pmw.Group(self.configuration_page,tag_text='Configuration instructions')
		self.conf_top_group.pack(fill = 'both', expand = 0, padx = 2, pady = 25)
        
		myfont = Pmw.logicalfont(name='Courier',size=14)
		self.text_field = Pmw.ScrolledText(self.conf_top_group.interior(),
			borderframe=5,
			vscrollmode='dynamic',
			hscrollmode='dynamic',
			labelpos='n',
			text_width=150, text_height=5,
			text_wrap='word',
			text_background='navy',
			text_foreground='white',
			text_font = myfont)
			
		self.text_field.pack(expand = 0, fill = 'both', padx = 4, pady = 4)
		self.text_field.insert('end',about_pca)
		self.text_field.configure(text_state=DISABLED)
		
		# MODE-TASK location tab
		
		self.mode_task_location = Pmw.Group(self.configuration_page, tag_text='Locate MODE-TASK directory:')
		self.mode_task_location.pack(side = TOP,expand=0, fill='x', padx = 4, pady = 25)
		
		# MODE-TASK location files
		self.mode_task_location1 = Pmw.EntryField(self.mode_task_location.interior(),
												labelpos = 'w',
												label_pyclass = DirDialogButtonClassFactory.get(self.set_mode_task_dir),                                                
												label_text = 'pyMODE-TASK directory *:',
												value=home)
		self.balloon.bind(self.mode_task_location1, 'Kindly give the path of pyMODE-TASK directory.\nAll the MODE-TASK core script must be placed\n inside the src directory within the pyMODE-TASK directory.',
                'Locate pyMODE-TASK directory')
				
		self.mode_task_location1.pack(side=TOP, fill = 'x', expand = 0, padx = 2, pady = 25)
		
		#===================================================================
        # 							PCA PAGE
		#===================================================================
		
		# input files
		
		self.pca_trj_file_io = Pmw.Group(self.pca_page, tag_text='MODE-TASK Input/Output')
		self.pca_trj_file_io.pack(side = TOP,expand=1, fill='both', padx = 2, pady = 2)
		
		
		# Read Trajectory 
		self.pca_trj_location = Pmw.EntryField(self.pca_trj_file_io.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.pca_set_trj_filename,mode='r',filter=[("Gromacs",".xtc"), ("DCD",".dcd"), ("Amber",".mdcrd"), ("All","*.*")]),                                                
												label_text = 'Trajectory File *:',
												)
		self.balloon.bind(self.pca_trj_location, 'Read MD Trajectory file',
                'Read MD Trajectory file')
		# Read Topology 						
		self.pca_top_location = Pmw.EntryField(self.pca_trj_file_io.interior(),
                                                labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_top_filename,mode='r',filter=[("PDB",".pdb"), ("GRO",".gro"), ("All","*.*")]),                                                
                                                label_text = 'Topology File *:')
		self.balloon.bind(self.pca_top_location, 'Read Topology file',
                'Read Topology file')
		# RMSD Reference Structure
		
		self.pca_ref_file = Pmw.EntryField(self.pca_trj_file_io.interior(),
                                                labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_ref_filename,mode='r',filter=[("PDB",".pdb"), ("All","*.*")]),                                                
                                                label_text = 'Ref Structure/Frame:')
		
		self.balloon.bind(self.pca_ref_file, 'Reference structure for RMSD',
                'Reference structure for RMSD')
		# output directory
		
		self.pca_out_dir_location = Pmw.EntryField(self.pca_trj_file_io.interior(),
												labelpos = 'w',
												label_pyclass = DirDialogButtonClassFactory.get(self.pca_set_out_location),
												label_text = 'Output Directory:',
												value = os.getcwd())										
		self.balloon.bind(self.pca_out_dir_location, 'Results will be saved here',
                'Results will be saved here')
		entries=(self.pca_trj_location,
					self.pca_top_location,
					self.pca_ref_file,
					self.pca_out_dir_location)
					
		for x in entries:
			x.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
			
		Pmw.alignlabels(entries)
		
		#--------------------------------------------
		# PCA options
		#--------------------------------------------
		
		# PCA Methods
		
		self.pca_page_main_group = Pmw.Group(self.pca_page, tag_text='PCA Options')
		self.pca_page_main_group.pack(fill = 'both', expand = 1, padx=2, pady=2)
		
		self.pca_methods_buttons = Pmw.RadioSelect(self.pca_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'PCA Method:',
				frame_borderwidth = 2,
				frame_relief = 'groove',
				command = self.get_pc_method_selection)
		
		self.balloon.bind(self.pca_methods_buttons, 'PCA Method',
                'PCA Method')
				
		self.pca_methods_buttons.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		self.pca_methods_buttons.add('svd', command = self.ok, text='SVD')
		self.pca_methods_buttons.add('evd', command = self.ok, text='EVD')
		self.pca_methods_buttons.add('kpca', command = self.ok, text='KernelPCA')
		self.pca_methods_buttons.add('ipca', command = self.ok, text='Incremental PCA')
		
		self.pca_methods_buttons.invoke('svd')
		
		# Atom group 
		self.atm_grp_buttons = Pmw.RadioSelect(self.pca_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'Atom group:',
				frame_borderwidth = 2,
				frame_relief = 'groove',
				command = self.get_ag_selection)
				
		self.balloon.bind(self.atm_grp_buttons, 'Select atoms for analysis',
                'Select atoms for analysis')
		self.atm_grp_buttons.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		self.atm_grp_buttons.add('all', command = self.ok, text='All')
		self.atm_grp_buttons.add('CA', command = self.ok, text='C-Alpha')
		self.atm_grp_buttons.add('backbone', command = self.ok, text='Backbone')
		self.atm_grp_buttons.add('protein', command = self.ok, text='Protein')
		self.atm_grp_buttons.invoke('CA')
		

		# Number of PCA component
		self.pca_comp = Pmw.EntryField(self.pca_page_main_group.interior(),
                                                labelpos = 'w',
                                                label_text = 'PCA component:',
												value='All',
												command = self.get_pc_selection)
		self.balloon.bind(self.pca_comp, 'No. of Principal Component to save',
                'No. of Principal Component to save')
		self.pca_comp.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		# Kernel Type
		self.kernel_type = Pmw.RadioSelect(self.pca_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'Kernel Type (kPCA):',
				frame_borderwidth = 2,
				frame_relief = 'groove',
				command = self.get_kt_selection)
		self.balloon.bind(self.kernel_type, 'Type of Kernel.\nUsed with kpca method',
                'Type of Kernel')
		self.kernel_type.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		self.kernel_type.add('linear', command = self.ok, text='Linear')
		self.kernel_type.add('poly', command = self.ok, text='Poly')
		self.kernel_type.add('rbf', command = self.ok, text='RBF')
		self.kernel_type.add('sigmoid', command = self.ok, text='Sigmoid')
		self.kernel_type.add('precomputed', command = self.ok, text='Precomputed')
		self.kernel_type.add('cosine', command = self.ok, text='Cosine')
		self.kernel_type.invoke('linear')
		
		# SVD Solver
		self.svd_solver_type = Pmw.RadioSelect(self.pca_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'SVD solver:',
				frame_borderwidth = 2,
				frame_relief = 'groove',
				command = self.get_st_selection
				)
		self.balloon.bind(self.svd_solver_type, 'Type of SVD solver.\nOnly useful with SVD method',
                'Type of SVD solver')
		self.svd_solver_type.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		self.svd_solver_type.add('auto', command = self.ok, text='Auto')
		self.svd_solver_type.add('full', command = self.ok, text='Full')
		self.svd_solver_type.add('arpack', command = self.ok, text='Arpack')
		self.svd_solver_type.add('randomized', command = self.ok, text='Randomized')
		
		self.svd_solver_type.invoke('auto')
		pca_options_buttons=(self.pca_methods_buttons, self.atm_grp_buttons, self.pca_comp, self.kernel_type, self.svd_solver_type)
		Pmw.alignlabels(pca_options_buttons)
		
		# progress bar
		#self.pb = ttk.Progressbar(self.pca_page_main_group.interior(), 
		#	orient="horizontal",
		#	length=500, 
		#	mode="indeterminate")
		#self.pb.pack()
		
		# Run button
		
		self.run_pca_button = Pmw.ButtonBox(self.pca_page_main_group.interior(),orient='horizontal', padx=2,pady=2)
		self.run_pca_button.add('Run PCA',fg='blue', command = self.run_pca)
		self.run_pca_button.pack(side=LEFT, expand = 1, padx = 2, pady = 2)
		
		
		
		##============================================================
		#
		#	internal PCA page
		#===========================================================
		
		# input files
		
		self.icpca_trj_file_io = Pmw.Group(self.ipca_page, tag_text='MODE-TASK Input/Output')
		self.icpca_trj_file_io.pack(side = TOP,expand=1, fill='both')
		
		
		# Read Trajectory 
		self.ipca_trj_location = Pmw.EntryField(self.icpca_trj_file_io.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.ipca_set_trj_filename,mode='r',filter=[("Gromacs",".xtc"), ("DCD",".dcd"), ("Amber",".mdcrd"), ("All","*.*")]),                                                
												label_text = 'Trajectory File *:',
												)
		self.balloon.bind(self.ipca_trj_location, 'Read MD Trajectory file',
			'Read MD Trajectory file')
		
		# Read Topology 						
		self.ipca_top_location = Pmw.EntryField(self.icpca_trj_file_io.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.ipca_set_top_filename,mode='r',filter=[("PDB",".pdb"), ("GRO",".gro"), ("All","*.*")]),                                                
												label_text = 'Topology File *:')
		self.balloon.bind(self.ipca_top_location, 'Read topology file',
			'Read topology file')
		
		# output directory
		
		self.ipca_out_dir_location = Pmw.EntryField(self.icpca_trj_file_io.interior(),
												labelpos = 'w',
												label_pyclass = DirDialogButtonClassFactory.get(self.ipca_set_out_location),
												label_text = 'Output Directory:',
												value = os.getcwd())
		self.balloon.bind(self.ipca_out_dir_location, 'Results will be saved here',
			'Results will be saved here')
		entries=(self.ipca_trj_location,
					self.ipca_top_location,
					self.ipca_out_dir_location)
					
		for x in entries:
			x.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
			
		Pmw.alignlabels(entries)	
		
		#==========================================
		# internal PCA options
		#------------------------------------------
		
	
		self.ipca_page_main_group = Pmw.Group(self.ipca_page, tag_text='Internal PCA Options')
		self.ipca_page_main_group.pack(fill = 'both', expand = 1, padx=2, pady=2)
		
		## cordinate type
		self.ct_buttons = Pmw.RadioSelect(self.ipca_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'Cordinate type:',
				frame_borderwidth = 2,
				frame_relief = 'groove')
		self.ct_buttons.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		self.ct_buttons.add('distance', command = self.ok)
		self.ct_buttons.add('angle', command = self.ok)
		self.ct_buttons.add('phi', command = self.ok)
		self.ct_buttons.add('psi', command = self.ok)
		
		self.ct_buttons.invoke('distance')
		self.balloon.bind(self.ct_buttons, 'Type of internal cordinate',
			'Type of internal cordinate')

		# Atom group 
		self.ipca_atm_grp_buttons = Pmw.RadioSelect(self.ipca_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'Atom group:',
				frame_borderwidth = 2,
				frame_relief = 'groove')

		self.ipca_atm_grp_buttons.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		self.ipca_atm_grp_buttons.add('all', command = self.ok, text='All')
		self.ipca_atm_grp_buttons.add('CA', command = self.ok, text='CA')
		self.ipca_atm_grp_buttons.add('backbone', command = self.ok, text='Backbone')
		self.ipca_atm_grp_buttons.add('protein', command = self.ok, text='Protein')
		self.ipca_atm_grp_buttons.invoke('CA')
		
		self.balloon.bind(self.ipca_atm_grp_buttons, 'Select atoms for analysis',
			'Select atoms for analysis')

		

		# Number of PCA component
		self.pca_comp = Pmw.EntryField(self.ipca_page_main_group.interior(),
                                                labelpos = 'w',
                                                label_text = 'PCA component:',
												value='All',
												command = self.get_pc_selection)
		self.pca_comp.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		self.balloon.bind(self.pca_comp, 'No. of principal component to save',
			'No. of principal component to save')

		
		pca_options_buttons=(self.ct_buttons, 
			self.ipca_atm_grp_buttons,
			self.pca_comp)
		Pmw.alignlabels(pca_options_buttons)
		
		# Run button
		
		self.run_pca_button = Pmw.ButtonBox(self.ipca_page_main_group.interior(),
			orient='horizontal',
			padx=2,	pady=2)
		self.run_pca_button.add('Run Internal PCA',fg='blue', command = self.run_ipca)
		self.run_pca_button.pack(side=LEFT, expand = 1, padx = 2, pady = 2)
				
		
		##============================================================
		# MDS/ t-SNE page
		#
		#==============================================================
		
		
		# input files
		
		self.mds_trj_file_io = Pmw.Group(self.mds_page, tag_text='MDS, t-SNE Input/Output')
		self.mds_trj_file_io.pack(side = TOP,expand=1, fill='both', padx = 2, pady = 2)
		
		
		# Read Trajectory 
		self.mds_trj_location = Pmw.EntryField(self.mds_trj_file_io.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.mds_set_trj_filename,mode='r',filter=[("Gromacs",".xtc"), ("DCD",".dcd"), ("Amber",".mdcrd"), ("All","*.*")]),                                                
												label_text = 'Trajectory File *:',
												)
		self.balloon.bind(self.mds_trj_location, 'Read MD trajectory file',
			'Read MD trajectory file')

		# Read Topology 						
		self.mds_top_location = Pmw.EntryField(self.mds_trj_file_io.interior(),
                                                labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.mds_set_top_filename,mode='r',filter=[("PDB",".pdb"), ("GRO",".gro"), ("All","*.*")]),                                                
                                                label_text = 'Topology File *:')
		self.balloon.bind(self.mds_top_location, 'Read topology file',
			'Read topology file')

		# output directory
		
		self.mds_out_dir_location = Pmw.EntryField(self.mds_trj_file_io.interior(),
												labelpos = 'w',
												label_pyclass = DirDialogButtonClassFactory.get(self.mds_set_out_location),
												label_text = 'Output Directory:',
												value = os.getcwd())
		self.balloon.bind(self.mds_out_dir_location, 'Results will be saved here',
			'Results will be saved here')

		entries=(self.mds_trj_location,
					self.mds_top_location,
					self.mds_out_dir_location)
					
		for x in entries:
			x.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
			
		Pmw.alignlabels(entries)	
		
		# MDS options
		#-------------------------------------------------
		
		# MDS Type
		self.radioframe = Frame(self.mds_page)
		radiogroups = []
		
		self.mds_page_main_group = Pmw.Group(self.radioframe, tag_text='MDS Options')
		self.mds_page_main_group.pack(side=LEFT, fill = 'both', expand = 1, padx=2, pady=2)
		
		radiogroups.append(self.mds_page_main_group)
		self.mds_type_buttons = Pmw.RadioSelect(self.mds_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'MDS Method:',
				frame_borderwidth = 2,
				frame_relief = 'groove',
				command = self.get_mds_type_selection)
				
		self.balloon.bind(self.mds_type_buttons, 'Type of MDS',
			'Type of MDS')

		self.mds_type_buttons.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		self.mds_type_buttons.add('metric', command = self.ok, text='metric')
		self.mds_type_buttons.add('nm', command = self.ok, text ='nonmetric')
	
		
		self.mds_type_buttons.invoke('metric')
		
		# Atom group 
		self.atm_grp_buttons = Pmw.RadioSelect(self.mds_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'Atom group:',
				frame_borderwidth = 2,
				frame_relief = 'groove',
				command = self.get_ag_selection)
		
		self.balloon.bind(self.atm_grp_buttons, 'Select atoms for analysis',
			'Select atoms for analysis')

		self.atm_grp_buttons.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		self.atm_grp_buttons.add('all', command = self.ok, text='All')
		self.atm_grp_buttons.add('CA', command = self.ok, text='CA')
		self.atm_grp_buttons.add('backbone', command = self.ok, text='Backbone')
		self.atm_grp_buttons.add('protein', command = self.ok, text='Protein')
		self.atm_grp_buttons.invoke('CA')
		
		# Dissimilarity Type
		self.mds_dissimilarity_type = Pmw.RadioSelect(self.mds_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'Dissimilarity type:',
				frame_borderwidth = 2,
				frame_relief = 'groove',
				command = self.get_mds_dissimilarity_type)
		
		self.balloon.bind(self.mds_dissimilarity_type, 'Type of dissimilarity matrix',
			'Type of dissimilarity matrix')

		self.mds_dissimilarity_type.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		self.mds_dissimilarity_type.add('euc', command = self.ok, text='Euclidean distance')
		self.mds_dissimilarity_type.add('rmsd', command = self.ok, text='RMSD')
		self.mds_dissimilarity_type.invoke('rmsd')
		
		# Cordinate Type
		self.mds_cord_type = Pmw.RadioSelect(self.mds_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'Cordinate Type:',
				frame_borderwidth = 2,
				frame_relief = 'groove',
				command = self.get_mds_cord_type
				)
		self.balloon.bind(self.mds_cord_type, 'Internal coordinates type.Only used with euclidean distance',
			'Internal coordinates type.Only used with euclidean distance')

		self.mds_cord_type.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		self.mds_cord_type.add('distance', command = self.ok)
		self.mds_cord_type.add('phi', command = self.ok)
		self.mds_cord_type.add('psi', command = self.ok)
		self.mds_cord_type.add('angle', command = self.ok)
		
		self.mds_cord_type.invoke('distance')
		
		# Atom Indices 
		self.mds_atm_ind_buttons = Pmw.RadioSelect(self.mds_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'Atom indices:',
				frame_borderwidth = 2,
				frame_relief = 'groove',
				command = self.get_ag_selection)
				
		self.balloon.bind(self.mds_atm_ind_buttons, 'Group of atom for pairwise distance',
			'Group of atom for pairwise distance')

		self.mds_atm_ind_buttons.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		self.mds_atm_ind_buttons.add('all', command = self.ok, text='All')
		self.mds_atm_ind_buttons.add('alpha', command = self.ok, text='CA')
		self.mds_atm_ind_buttons.add('backbone', command = self.ok, text='Backbone')
		self.mds_atm_ind_buttons.add('minimal', command = self.ok, text='Minimal')
		self.mds_atm_ind_buttons.invoke('alpha')
		
		mds_options_buttons=(self.mds_type_buttons, 
			self.atm_grp_buttons,  
			self.mds_dissimilarity_type, 
			self.mds_cord_type,
			self.mds_atm_ind_buttons)
		Pmw.alignlabels(mds_options_buttons)
		
		# Run MDS button
		
		self.run_mds_button = Pmw.ButtonBox(self.mds_page_main_group.interior(),
			orient='horizontal',
			padx=2, pady=2)
			
		self.run_mds_button.add('Run MDS',
			fg='blue', 
			command = self.run_mds)
		self.run_mds_button.pack(side=LEFT, expand = 1, padx = 2, pady = 2)
		
		
		##=========================================
		# t-SNE options
		#-----------------------------------------
		
		# t-SNE options
		
		self.tsne_page_main_group = Pmw.Group(self.radioframe, tag_text='t-SNE Options')
		self.tsne_page_main_group.pack(side=LEFT, fill = 'both', expand = 1, padx=2, pady=2)
		
		radiogroups.append(self.tsne_page_main_group)

		Pmw.aligngrouptags(radiogroups,)
		self.radioframe.pack(padx = 2, pady = 2, expand='yes', fill='both')
		
		# Atom group 
		self.atm_grp_buttons = Pmw.RadioSelect(self.tsne_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'Atom group:',
				frame_borderwidth = 2,
				frame_relief = 'groove',
				command = self.get_ag_selection)
		self.atm_grp_buttons.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		self.atm_grp_buttons.add('all', command = self.ok, text='All')
		self.atm_grp_buttons.add('CA', command = self.ok, text='CA')
		self.atm_grp_buttons.add('backbone', command = self.ok, text='Backbone')
		self.atm_grp_buttons.add('protein', command = self.ok, text='Protein')
		self.atm_grp_buttons.invoke('CA')
		
		# Dissimilarity Type
		self.tsne_dissimilarity_type = Pmw.RadioSelect(self.tsne_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'Dissimilarity type:',
				frame_borderwidth = 2,
				frame_relief = 'groove',
				command = self.get_mds_dissimilarity_type)
		self.tsne_dissimilarity_type.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		self.tsne_dissimilarity_type.add('euc', command = self.ok, text='Euclidean distance')
		self.tsne_dissimilarity_type.add('rmsd', command = self.ok, text='RMSD')
		self.tsne_dissimilarity_type.invoke('rmsd')
		
		# Cordinate Type
		self.tsne_cord_type = Pmw.RadioSelect(self.tsne_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'Cordinate Type:',
				frame_borderwidth = 2,
				frame_relief = 'groove',
				command = self.get_mds_cord_type
				)
		self.tsne_cord_type.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		self.tsne_cord_type.add('distance', command = self.ok)
		self.tsne_cord_type.add('phi', command = self.ok)
		self.tsne_cord_type.add('psi', command = self.ok)
		self.tsne_cord_type.add('angle', command = self.ok)
		
		self.tsne_cord_type.invoke('distance')
		
		# Atom Indices 
		self.atm_ind_buttons = Pmw.RadioSelect(self.tsne_page_main_group.interior(),
				buttontype = 'radiobutton',
				selectmode = 'single',
				labelpos = 'w',
				label_text = 'Atom indices:',
				frame_borderwidth = 2,
				frame_relief = 'groove',
				command = self.get_ag_selection)
		self.atm_ind_buttons.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		self.atm_ind_buttons.add('all', command = self.ok, text='All')
		self.atm_ind_buttons.add('CA', command = self.ok, text='CA')
		self.atm_ind_buttons.add('backbone', command = self.ok, text='Backbone')
		self.atm_ind_buttons.add('protein', command = self.ok, text='Protein')
		self.atm_ind_buttons.invoke('CA')
		mds_options_buttons=(self.mds_type_buttons, 
			self.atm_grp_buttons,  
			self.tsne_dissimilarity_type, 
			self.tsne_cord_type,
			self.atm_ind_buttons)
		Pmw.alignlabels(mds_options_buttons)
		
		# Run t-SNE button
		
		self.run_mds_button = Pmw.ButtonBox(self.tsne_page_main_group.interior(),orient='horizontal', padx=2,pady=2)
		self.run_mds_button.add('Run t-SNE',fg='blue', command = self.run_tsne)
		self.run_mds_button.pack(side=LEFT, expand = 1, padx = 2, pady = 2)
				
		
		
		#==============================================================
        # NMA PAGE
		#==============================================================
		
		
		# input files
		self.nma_top_group1 = Pmw.Group(self.nma_page, tag_pyclass = None)
		self.nma_top_group1.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		self.nma_trj_file_io = Pmw.Group(self.nma_top_group1.interior(), tag_text='Coarse Graining (1)')
		self.nma_trj_file_io.pack(expand=1, fill='both', side=LEFT)
		
		
		# Read PDB file 
		self.cg_pdb_location = Pmw.EntryField(self.nma_trj_file_io.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_cg_pdb_filename,mode='r',filter=[("PDB",".pdb")]),                                                
												label_text = 'PDB File *:',
												)
		self.balloon.bind(self.cg_pdb_location, 'PDB for coarse graining',
			'Read PDB for coarse graining')
		
		# coarse graining
		self.cg_level = Pmw.EntryField(self.nma_trj_file_io.interior(),
                                                labelpos = 'w',
                                                label_text = 'CG Level:')
		
		self.balloon.bind(self.cg_level, 'level of coarse graining',
			'coarse graining')
		
		# Atom Type
		self.cg_at_var = StringVar()
		self.cg_at_var.set('CB')
		self.cg_atm_type = Pmw.OptionMenu(self.nma_trj_file_io.interior(),
				labelpos = 'w',
				label_text = 'Atom Type:',
				menubutton_textvariable = self.cg_at_var,
				items = ['CB', 'CA'],
				menubutton_width = 5,
		)
		self.balloon.bind(self.cg_atm_type, 'Atom type',
			'Atom type')
		
		# Starting atom
		self.cg_start_atm = Pmw.EntryField(self.nma_trj_file_io.interior(),
			labelpos = 'w',
			label_text = 'Starting atom:',
			value='1')
		
		self.balloon.bind(self.cg_start_atm, 'Residue number of the starting atom',
			'Residue number of the starting atom')
		
		# output directory
		
		self.cg_out_dir_location = Pmw.EntryField(self.nma_trj_file_io.interior(),
												labelpos = 'w',
												label_pyclass = DirDialogButtonClassFactory.get(self.set_cg_out_location),                                                
												label_text = 'Output Directory:',
												value  = os.getcwd())
		
		# out pdb file name
		self.cg_out_pdb = Pmw.EntryField(self.nma_trj_file_io.interior(),
			labelpos = 'w',
			label_text = 'Output PDB:',
			value='ComplexCG.pdb')
			
		self.balloon.bind(self.cg_out_pdb, 'Output PDB name',
			'Output PDB name')
			
		entries=(self.cg_pdb_location,
					self.cg_level,
					self.cg_start_atm,
					self.cg_atm_type,
					self.cg_out_dir_location,
					self.cg_out_pdb)
					
		for x in entries:
			x.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
			
		# Run coarse garining
		self.run_cg_button = Pmw.ButtonBox(self.nma_trj_file_io.interior(),
			orient='horizontal',
			padx=2,
			pady=2)
		self.run_cg_button.add('Run Coarse Graining',fg='blue', command = self.run_cg)
		self.run_cg_button.pack(side=RIGHT, expand = 1, padx = 2, pady = 2)
			
		Pmw.alignlabels(entries)
		
		# NMA options
		
		self.nma_group = Pmw.Group(self.nma_top_group1.interior(), tag_text='NMA (2)')
		self.nma_group.pack(expand=1, fill='both', side=LEFT)
		
		# Read PDB file 
		self.nma_pdb_location = Pmw.EntryField(self.nma_group.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_nma_pdb_filename,mode='r',filter=[("PDB",".pdb")]),                                                
												label_text = 'PDB File *:',
												)
		self.nma_pdb_location.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		

		# Cutoff in Ang
		self.nma_cut = Pmw.EntryField(self.nma_group.interior(),
                                                labelpos = 'w',
                                                label_text = 'Cutoff (Angstrom):',
												value='15',
												command = self.get_pc_selection)
		self.nma_cut.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		# Atom Type
		self.nma_at_var = StringVar()
		self.nma_at_var.set('CB')
		self.nma_atm_type = Pmw.OptionMenu(self.nma_group.interior(),
				labelpos = 'w',
				label_text = 'Atom Type:',
				menubutton_textvariable = self.nma_at_var,
				items = ['CB', 'CA'],
				menubutton_width = 5,
		)
		self.nma_atm_type.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		# output directory
		
		self.nma_out_dir_location = Pmw.EntryField(self.nma_group.interior(),
												labelpos = 'w',
												label_pyclass = DirDialogButtonClassFactory.get(self.nma_set_out_location),
												label_text = 'Output Directory:',
												value = os.getcwd())
		self.nma_out_dir_location.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
												
		pca_options_buttons=(self.nma_pdb_location, 
			self.nma_cut,
			self.nma_atm_type,
			self.nma_out_dir_location)
		Pmw.alignlabels(pca_options_buttons)
		
		# Run button
		
		self.run_pca_button = Pmw.ButtonBox(self.nma_group.interior(),
			orient='horizontal',
			padx=2,
			pady=2)
		self.run_pca_button.add('Run NMA',fg='blue', command = self.run_nma)
		self.run_pca_button.pack(side=LEFT, expand = 1, padx = 2, pady = 2)
		
		##====================================
		# conformation/ combination mode
		#======================================
		
		self.nma_conf_mode = Pmw.Group(self.nma_top_group1.interior(),
			tag_text='Conformation/Combination mode (3)')
		self.nma_conf_mode.pack(expand=1, fill='both', side=LEFT)
		
		## PDB file
		self.conf_mode_Unalgn_pdb1 = Pmw.EntryField(self.nma_conf_mode.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_conf_mode_Unalgn_pdb,mode='r',filter=[("PDB",".pdb")]),                                                
												label_text = 'PDB File *:',
												)
		self.conf_mode_Unalgn_pdb1.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		## PDB file (Conformational change)
		self.conf_mode_pdb = Pmw.EntryField(self.nma_conf_mode.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_conf_mode_pdb,mode='r',filter=[("PDB",".pdb")]),                                                
												label_text = 'PDB(Conf. change)*:',
												)
		self.balloon.bind(self.conf_mode_pdb, 'PDB file of conformation change',
                'PDB file of conformation change')
		self.conf_mode_pdb.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		# Modes
		self.comb_modes = Pmw.EntryField(self.nma_conf_mode.interior(),
												labelpos = 'w',
												label_text = 'Modes *:',
												value='1,5,7'
												)
		self.balloon.bind(self.comb_modes, 'Calculate the overlap for a combination of specific modes.\nNumbers are separated by commas: 1,5,7.\nOnly used for combination mode.',
                'Modes')	
		self.comb_modes.pack(fill='both',expand = 1, padx = 2, pady = 2)
		
		# Atom Type
		self.conf_at_var = StringVar()
		self.conf_at_var.set('CB')
		self.conf_atm_type = Pmw.OptionMenu(self.nma_conf_mode.interior(),
				labelpos = 'w',
				label_text = 'Atom Type:',
				menubutton_textvariable = self.conf_at_var,
				items = ['CB', 'CA'],
				menubutton_width = 5,
		)
		self.conf_atm_type.pack(fill='both',expand = 1, padx = 2, pady = 2)
		
		## VT Matrix file
		self.conf_mode_vtfile = Pmw.EntryField(self.nma_conf_mode.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_conf_mode_vtfile_location,mode='r',filter=[("TXT",".txt")]),                                                
												label_text = 'VT Matrix file *:',
												)
		self.conf_mode_vtfile.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		## Output file
		self.conf_mode_out = Pmw.EntryField(self.nma_conf_mode.interior(),
												labelpos = 'w',
												label_pyclass = DirDialogButtonClassFactory.get(self.set_conf_mode_out),                                                
												label_text = 'Output directory:',
												value = os.getcwd())
		self.conf_mode_out.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		# Get conformation mode
		self.run_msf_button = Pmw.ButtonBox(self.nma_conf_mode.interior(),
			orient='horizontal',
			padx=2,
			pady=2)
		self.run_msf_button.add('Get conf. modes',fg='blue', command = self.run_conf_mode)
		self.run_msf_button.pack(side=LEFT, expand = 1, padx = 2, pady = 2)
		
		# Get combination mode
		self.run_msf_button = Pmw.ButtonBox(self.nma_conf_mode.interior(),
			orient='horizontal',
			padx=2,
			pady=2)
		self.run_msf_button.add('Get comb. modes',fg='blue', command = self.run_comb_mode)
		self.run_msf_button.pack(side=LEFT, expand = 1, padx = 2, pady = 2)
		
		
		#============================================
		## second group
		#===============================================
		self.nma_second_group = Pmw.Group(self.nma_page,  tag_pyclass = None)
		self.nma_second_group.pack(expand=1, fill='both')
		
		
		#==========================================
		## Mean square fluctuation
		#============================================
		
		self.nma_msf = Pmw.Group(self.nma_second_group.interior(), tag_text='Mean square fluctuation (4)')
		self.nma_msf.pack(expand=1, fill='both', side=LEFT)
		
		# read first PDB
		self.msf_pdb = Pmw.EntryField(self.nma_msf.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_msf_pdb,mode='r',filter=[("PDB",".pdb")]),                                                
												label_text = 'PDB file *:',
												)
		self.balloon.bind(self.msf_pdb, 'First PDB file to compare',
                'First PDB file to compare')
		self.msf_pdb.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		#W matrix file
		self.msf_WMatrixFile = Pmw.EntryField(self.nma_msf.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_msf_WMatrixFile,mode='r',filter=[("TXT",".txt")]),                                                
												label_text = 'W Matrix File *:',
												)
		self.balloon.bind(self.msf_WMatrixFile, 'W matrix file for first PDB',
                'W matrix file for first PDB')
		self.msf_WMatrixFile.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		#VT matrix file
		self.msf_VTMatrixFile = Pmw.EntryField(self.nma_msf.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_msf_VTMatrixFile,mode='r',filter=[("TXT",".txt")]),                                                
												label_text = 'VT Matrix File *:',
												)
		self.balloon.bind(self.msf_VTMatrixFile, 'VT matrix file for first PDB',
                'VT matrix file for first PDB')
		self.msf_VTMatrixFile.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		# read comparison PDB
		self.msf_conf_pdb = Pmw.EntryField(self.nma_msf.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_msf_conf_pdb,mode='r',filter=[("PDB",".pdb")]),                                                
												label_text = 'Comparison PDB:',
												)
		self.balloon.bind(self.msf_conf_pdb, 'VT matrix file for comparison PDB',
                'VT matrix file for comparison PDB')
				
		self.msf_conf_pdb.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		#W matrix file
		self.msf_WMatrixFile1 = Pmw.EntryField(self.nma_msf.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_msf_WMatrixFile1,mode='r',filter=[("TXT",".txt")]),                                                
												label_text = 'W Matrix File:',
												)
		self.balloon.bind(self.msf_WMatrixFile1, 'W matrix file for comparison PDB',
                'W matrix file for comparison PDB')
		self.msf_WMatrixFile1.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		#VT matrix file
		self.msf_VTMatrixFile1 = Pmw.EntryField(self.nma_msf.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_msf_VTMatrixFile1,mode='r',filter=[("TXT",".txt")]),                                                
												label_text = 'VT Matrix File:',
												)
		self.balloon.bind(self.msf_VTMatrixFile1, 'VT matrix file for comparison PDB',
                'VT matrix file for comparison PDB')
		self.msf_VTMatrixFile1.pack(fill = 'both', expand = 1, padx = 2, pady = 2)

		# Atom Type
		self.msf_at_var = StringVar()
		self.msf_at_var.set('CB')
		self.msf_atm_type = Pmw.OptionMenu(self.nma_msf.interior(),
				labelpos = 'w',
				label_text = 'Atom Type:',
				menubutton_textvariable = self.msf_at_var,
				items = ['CB', 'CA'],
				menubutton_width = 5,
		)
		self.msf_atm_type.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		# modes
		
		self.msf_mode = Pmw.EntryField(self.nma_msf.interior(),
                                                labelpos = 'w',
                                                label_text = 'Modes:',
												value = '7:27')
												
		self.balloon.bind(self.msf_mode, 'List of modes: string OR comma separated String OR colon separated string ',
                'List of modes')
		self.msf_mode.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		# Run MSF
		self.run_msf_button = Pmw.ButtonBox(self.nma_msf.interior(),
			orient='horizontal',
			padx=2,
			pady=2)
		self.run_msf_button.add('Run MSF',fg='blue', command = self.run_msf)
		self.run_msf_button.pack(side=LEFT, expand = 1, padx = 2, pady = 2)
		
		
		#==========================================
		##  Assembly Covariance
		#============================================
		
		self.assem_cov = Pmw.Group(self.nma_second_group.interior(), tag_text='Assembly Covariance (5)')
		self.assem_cov.pack(expand=1, fill='both', side=LEFT)
		
		# read PDB
		self.ac_pdb = Pmw.EntryField(self.assem_cov.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_ac_pdb,mode='r',filter=[("PDB",".pdb")]),                                                
												label_text = 'PDB file *:',
												)
		self.balloon.bind(self.ac_pdb, 'Give a PDB file',
                'Give a PDB file')
		self.ac_pdb.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		#W matrix file
		self.ac_WMatrixFile = Pmw.EntryField(self.assem_cov.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_ac_WMatrixFile,mode='r',filter=[("TXT",".txt")]),                                                
												label_text = 'W Matrix File *:',
												)
		self.balloon.bind(self.ac_WMatrixFile, 'W matrix file',
                'W matrix file')
		self.ac_WMatrixFile.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		#VT matrix file
		self.ac_VTMatrixFile = Pmw.EntryField(self.assem_cov.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_ac_VTMatrixFile,mode='r',filter=[("TXT",".txt")]),                                                
												label_text = 'VT Matrix File *:',
												)
		self.balloon.bind(self.ac_VTMatrixFile, 'VT matrix file',
                'VT matrix file')
		self.ac_VTMatrixFile.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		# Modes
		self.ac_modes = Pmw.EntryField(self.assem_cov.interior(),
												labelpos = 'w',
												label_text = 'Modes:',
												value='all'
												)
		self.balloon.bind(self.ac_modes, 'Modes: String OR Colon Separated String OR Comma Separated String',
                'Modes')
				
		self.ac_modes.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		# Asymmetric Unit
		self.ac_asymm_unit = Pmw.EntryField(self.assem_cov.interior(),
												labelpos = 'w',
												label_text = 'Asymmetric Unit:'
												)
		self.balloon.bind(self.ac_asymm_unit, 'Asymmetric Unit: String OR Colon Separated String OR Comma Separated String',
				'Asymmetric Unit')
				
		self.ac_asymm_unit.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		# Zoom
		self.ac_zoom = Pmw.EntryField(self.assem_cov.interior(),
												labelpos = 'w',
												label_text = 'Zoom:',
												value='1,2'
												)
		self.balloon.bind(self.ac_zoom, 'Zoom: Comma Separated String The format is: [Unit,Chain]',
				'Zoom')
				
		self.ac_zoom.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		# Vmin
		self.ac_Vmin = Pmw.EntryField(self.assem_cov.interior(),
												labelpos = 'w',
												label_text = 'Vmin:',
												value='-0.5'
												)
		self.balloon.bind(self.ac_Vmin, 'Minimum axes value for plot',
				'Minimum axes value for plot')
				
		self.ac_Vmin.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		# Vmax
		self.ac_Vmax = Pmw.EntryField(self.assem_cov.interior(),
												labelpos = 'w',
												label_text = 'Vmax:',
												value='0.5'
												)
		self.balloon.bind(self.ac_Vmax, 'Maximum axes value for plot',
				'Maximum axes value for plot')
				
		self.ac_Vmax.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		# Atom Type
		self.ac_at_var = StringVar()
		self.ac_at_var.set('CB')
		self.ac_atm_type = Pmw.OptionMenu(self.assem_cov.interior(),
				labelpos = 'w',
				label_text = 'Atom Type:',
				menubutton_textvariable = self.ac_at_var,
				items = ['CB', 'CA'],
				menubutton_width = 5,
		)
		self.ac_atm_type.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		# Run Assembly Covariance
		self.run_ac_button = Pmw.ButtonBox(self.assem_cov.interior(),
			orient='horizontal',
			padx=2,
			pady=2)
		self.run_ac_button.add('Run',fg='blue', command = self.run_ac)
		self.run_ac_button.pack(side=LEFT, expand = 1, padx = 2, pady = 2)
		
		#=============================================
		# Get eigenvectors and mode visualization
		#=============================================
		
		#self.gi_mv_group = Pmw.Group(self.nma_second_group.interior(), tag_pyclass = None)
		#self.gi_mv_group.pack(expand=1, fill='both', side=LEFT)
		
		##Sub window
		self.get_eig_group = Pmw.Group(self.nma_second_group.interior(), tag_text='Mode Visualisation (6)')
		self.get_eig_group.pack(expand=1, fill='both', side=LEFT)
		
		# read VT file
		self.ge_vtfile_location = Pmw.EntryField(self.get_eig_group.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_ge_vtfile_location,mode='r',filter=[("TXT",".txt")]),                                                
												label_text = 'VT Matrix file *:',
												)
		self.ge_vtfile_location.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		#self.ge_vtfile_location.grid(row=0, column=0, columnspan=2, sticky=W)
		
		# mode index 
		
		self.ge_mode_idx = Pmw.EntryField(self.get_eig_group.interior(),
												labelpos = 'w',
												label_text = 'Mode index *:',
												value=1
												)
		self.balloon.bind(self.ge_mode_idx, 'Mode index for visualisation',
			'Index of mode for visualisation')
		# Direction
		
		self.ge_direction = Pmw.OptionMenu(self.get_eig_group.interior(),
				labelpos = 'w',
				label_text = 'Direction:',
				items = ['1', '-1'],
				menubutton_width = 5,
		)
		
		#self.ge_mode_idx.grid(row=1, column=0, columnspan=2, sticky=W)
		self.ge_mode_idx.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		self.ge_direction.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		#self.ge_direction.grid(row=2, column=0, columnspan=2, sticky=W)
		
		# Get eigenvectors
		self.nma_get_eigev = Pmw.ButtonBox(self.get_eig_group.interior(),
			orient='horizontal',
			padx=2,
			pady=2)
		self.nma_get_eigev.add('Get eigenvectors',fg='blue', command = self.run_get_eigen)		
		#self.nma_get_eigev.pack(side=BOTTOM, expand = 1, padx = 2, pady = 2, fill='x')
		#self.nma_get_eigev.grid(row=3, column=0, sticky=W)

		##====================================
		# mode visualization
		#=========================================
		
		#self.nma_mode_vis = Pmw.Group(self.gi_mv_group.interior(), tag_text='Mode visualization (7)')
		#self.nma_mode_vis.pack(expand=1, fill='both', side=BOTTOM)
		
		## CG PDB file
		self.mv_mode_pdb = Pmw.EntryField(self.get_eig_group.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_mv_mode_pdb,mode='r',filter=[("PDB",".pdb")]),                                                
												label_text = 'CG PDB file *:',
												)
		self.mv_mode_pdb.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		# Atom Type
		self.mv_at_var = StringVar()
		self.mv_at_var.set('CB')
		self.mv_atm_type = Pmw.OptionMenu(self.get_eig_group.interior(),
				labelpos = 'w',
				label_text = 'Atom Type:',
				menubutton_textvariable = self.mv_at_var,
				items = ['CB', 'CA'],
				menubutton_width = 5,
		)
		self.mv_atm_type.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		## mode index value
		self.mv_indx_value = Pmw.EntryField(self.get_eig_group.interior(),
												labelpos = 'w',                                                
												label_text = 'Mode index value *:',
												)
		#self.mv_indx_value.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		## Vector file
		self.mv_vector_file = Pmw.EntryField(self.get_eig_group.interior(),
												labelpos = 'w',
												label_pyclass = FileDialogButtonClassFactory.get(self.set_mv_vector_file,mode='r',filter=[("TXT",".txt")]),                                                
												label_text = 'Vector file *:',
												)
		self.balloon.bind(self.mv_vector_file, 'File containing eigen vectors',
			'File containing eigen vectors')

		#self.mv_vector_file.pack(fill = 'both', expand = 1, padx = 2, pady = 2)
		
		# Get eigenvectors button
		#self.nma_get_eigev = Pmw.ButtonBox(self.nma_mode_vis.interior(),
		#	orient='horizontal',
		#	padx=2,
		#	pady=2)
		#self.nma_get_eigev.add('Get eigenvectors',fg='blue', command = self.run_get_eigen)		
		#self.nma_get_eigev.pack(side=LEFT, expand = 1, padx = 2, pady = 2)
		
		# Get mode visualization
		self.run_msf_button = Pmw.ButtonBox(self.get_eig_group.interior(),
			orient='horizontal',
			padx=2,
			pady=2)
		self.run_msf_button.add('Get modes Vis',fg='blue', command = self.run_mode_vis)
		self.run_msf_button.pack(expand = 1, padx = 2, pady = 2)
		
		
		
		#=====================================================
        # ABOUT PAGE
		#=======================================================
		
		# about section
		
		about_pca = """

pyMODE-TASK- is Copyright (C) 2017 by Bilal Nizami, RUBi, Rhodes University.		
MODE-TASK is a collection of tools for analysing normal modes and performing principal component analysis.		
pyMODE-TASK is the pymol plugin of MODE-TASK. Original command line version of MODE-TASK can be found at https://github.com/RUBi-ZA/MODE-TASK. 

Authors. (1)- MODE-TASK, B Nizami, CJ Ross, M Glenister, O. Sheik Amamuddy, AR Atilgan, C Atilgan and O Tastan Bishop.

(2)- pyMODE-TASK is written by:

Bilal Nizami

Research Unit in Bioinformatics (RUBi)
Rhodes University
Grahamstown, South Africa   
https://rubi.ru.ac.za 
2017. 

email: nizamibilal1064@gmail.com"""
		self.about_top_group = Pmw.Group(self.about_page,tag_text='About')
		self.about_top_group.pack(fill = 'both', expand = 0, padx = 2, pady = 2)

		myfont = Pmw.logicalfont(name='Courier',size=14, spacing='2')
		self.text_field = Pmw.ScrolledText(self.about_top_group.interior(),
                             borderframe=5,
                             vscrollmode='dynamic',
                             hscrollmode='dynamic',
                             labelpos='n',
                             text_width=150, text_height=23,
                             text_wrap='word',
                             text_background='black',
                             text_foreground='white',
                             text_font = myfont
                             )
		self.text_field.pack(expand = 0, fill = 'both', padx = 4, pady = 4)
		self.text_field.insert('end',about_pca)
		self.text_field.configure(text_state=DISABLED)
		
		#---------------------------------------------------------------
        # CITATION PAGE
		#=======================================================
		
		# citation section
		
		citation = """
pyMODE-TASK- is Copyright (C) 2017 by Bilal Nizami, RUBi, Rhodes University.
		
pyMODE-TASK is a pymol plugin for MODE-TASK. If you use MODE-TASK and/or pyMODE-TASK, kindly cite the 
following papers.

(1)- MODE-TASK, B Nizami, CJ Ross, M Glenister, O. Sheik Amamuddy, AR Atilgan, C Atilgan and O Tastan Bishop.

(2)- pyMODE-TASK is written by:

Bilal Nizami

Research Unit in Bioinformatics (RUBi)
Rhodes University
Grahamstown, South Africa   
https://rubi.ru.ac.za 
2017. 

Report bug at:

email: nizamibilal1064@gmail.com"""
		self.citation_top_group = Pmw.Group(self.citation_page,tag_text='Citation')
		self.citation_top_group.pack(fill = 'both', expand = 0, padx = 2, pady = 2)

		myfont = Pmw.logicalfont(name='Courier',size=14, spacing='2')
		self.text_field = Pmw.ScrolledText(self.citation_top_group.interior(),
                             borderframe=5,
                             vscrollmode='dynamic',
                             hscrollmode='dynamic',
                             labelpos='n',
                             text_width=150, text_height=23,
                             text_wrap='word',
                             text_background='black',
                             text_foreground='white',
                             text_font = myfont
                             )
		self.text_field.pack(expand = 0, fill = 'both', padx = 4, pady = 4)
		self.text_field.insert('end',citation)
		self.text_field.configure(text_state=DISABLED)
		
		#---------------------------------------------------------------
        # HELP PAGE
		#=======================================================
		
		help = """
See the help page of MODE-TASK at   http://mode-task.readthedocs.io/en/latest/index.html


Credit:

1. Bilal Nizami - plugin design and implementaion, PCA implementaion

2. Caroline Ross - NMA implementaion

3. Ozlem Tastan Bishop - Design, idea and principle investigator

Research Unit in Bioinformatics (RUBi), Rhodes University, Grahamstown, South Africa


"""
		link = '''Read the doc'''
		
		self.help_top_group = Pmw.Group(self.help_page,tag_text='Help and Credit')
		self.help_top_group.pack(fill = 'both', expand = 0, padx = 2, pady = 2)
		
		myfont = Pmw.logicalfont(name='Courier',size=14, spacing='2')
		self.text_field = Pmw.ScrolledText(self.help_top_group.interior(),
                             borderframe=5,
                             vscrollmode='dynamic',
                             hscrollmode='dynamic',
                             labelpos='n',
                             text_width=150, text_height=15,
                             text_wrap='word',
                             text_background='black',
                             text_foreground='white',
                             text_font = myfont
                             )
		self.text_field.pack(expand = 0, fill = 'both', padx = 4, pady = 4)
		self.text_field.insert('end',help)
		self.text_field.configure(text_state=DISABLED)
		
		# Create dialog.
		Pmw.aboutversion('%s' % __version__)
		Pmw.aboutcopyright('Copyright Bilal Nizami 2017\nAll rights reserved\n The project is licensed under GNU GPL 3.0')
		Pmw.aboutcontact(
            'To report bug, for help and suggestion contact:\n' +
            '  email: nizamibilal1064@gmail.com'
		)
		self.about = Pmw.AboutDialog(self.help_top_group.interior(), applicationname = 'pyMODE-TASK')
		self.about.withdraw()

        # Create button to launch the dialog.
		w = Button(self.help_top_group.interior(), text = 'About pyMODE-TASK',
				command = self.execute)
		w.pack(padx = 8, pady = 8)
		
		
		self.notebook.setnaturalsize()
		self.dialog.show()
		
	def execute(self):
		self.about.show()

	def ok(self):
		print 'You clicked on OK'
	
	def check_conf_status(self):
		'''Check if the configuration tab is set and core files exist'''
		path = self.mode_task_location1.getvalue()
		if path != '':
			result = 1
			pca_file_chk = path+'/src/pca.py'
			intPca_file_chk = path+'/src/internal_pca.py'
			mds_file_chk = path+'/src/mds.py'
			tsne_file_chk = path+'/src/tsne.py'
			pca_file_chk = path+'/src/pca.py'
			ac_file_chk = path+'/src/assemblyCovariance.py'
			cg_file_chk = path+'/src/coarseGrain.py'
			com_mod_file_chk = path+'/src/combinationMode.py'
			conf_mod_file_chk = path+'/src/conformationMode.py'
			msf_file_chk = path+'/src/meanSquareFluctuations.py'
			visualiseVector_file_chk = path+'/src/visualiseVector.py'
			getEigenVectors_file_chk = path+'/src/getEigenVectors'
			ANM_file_chk = path+'/src/ANM'
			file_name_list = [pca_file_chk, intPca_file_chk, mds_file_chk, tsne_file_chk, pca_file_chk,\
								ac_file_chk, cg_file_chk, com_mod_file_chk, conf_mod_file_chk, msf_file_chk,\
								visualiseVector_file_chk, getEigenVectors_file_chk, ANM_file_chk]
			for i in file_name_list:
				chk=1
				if os.path.isfile(i):
					chk=1
				else:
					chk = 0
			if chk == 0:
				tkMessageBox.showinfo("pyMODE-TASK Warning!", "Can not locate some core MODE-TASK scripts. Please insure that the path given in configuration tab is correct and contains MODE-TASK core scripts , otherwise it might give an error in the next steps")				
		else:
			result = 0
			tkMessageBox.showinfo("pyMODE-TASK Error!", "Location of pyMODE-TASK directory not given. Please specify the location of pyMODE-TASK directory in configuration page of the plugin!")
		return result
		
	def run_pca(self):
		'''run pca'''
		# core scripts are located at src directory under pyMODE-TASK directory
		#cmd_dir = './src'
		status = self.check_conf_status()
		#self.pb.start(100)
		if status:
			cmd_dir = self.mode_task_location1.getvalue() + '/src/'
			trj_loc = self.pca_trj_location.getvalue()
			top_loc = self.pca_top_location.getvalue()
			pc_sele = self.pca_methods_buttons.getvalue()
			st_sele = self.svd_solver_type.getvalue()
			kt_sele = self.kernel_type.getvalue()
			ag_sele = self.atm_grp_buttons.getvalue()
			pc_comp = self.pca_comp.getvalue()
			out_loc = self.pca_out_dir_location.getvalue()
			ref_loc = self.pca_ref_file.getvalue()
	
			# run SVD
			
			if pc_sele == 'svd':
			
				if trj_loc == '':
					tkMessageBox.showinfo("pyMODE-TASK Error!", "No trajectory location given!")
				if top_loc == '':
					tkMessageBox.showinfo("pyMODE-TASK Error!", "No topology location given!")
				
				else:
					if ref_loc != '':
						
						cmd = cmd_dir+'pca.py -t '+ trj_loc + ' -p ' + top_loc + ' -ag '+ ag_sele + ' -pt '+ pc_sele + ' -out ' + out_loc + ' -r ' + ref_loc + ' -st ' + st_sele
						
					else:				
						tkMessageBox.showinfo("pyMODE-TASK warning!", "No Ref structure given, using deafult first frame!")
						cmd = cmd_dir+'pca.py -t '+ trj_loc + ' -p ' + top_loc + ' -ag '+ ag_sele + ' -pt '+ pc_sele + ' -out ' + out_loc + ' -st ' + st_sele
					out=subprocess.Popen(os.system(cmd), shell=False)
					#self.pb.start(100)
					out = `os.system(cmd)`
					#while out.poll() is None:
					#	self.update()
					#self.pb.stop()
					if out == '0':
						tkMessageBox.showinfo("pyMODE-TASK!", "PCA (SVD) run successful!\nResults are written in\n" + out_loc)
					else:
						tkMessageBox.showinfo("pyMODE-TASK!", "PCA (SVD) run failed. See terminal for details!")			
			
			# run EVD
			elif pc_sele == 'evd':
				if trj_loc == '':
					tkMessageBox.showinfo("pyMODE-TASK Error!", "No trajectory location given!")
				if top_loc == '':
					tkMessageBox.showinfo("pyMODE-TASK Error!", "No topology location given!")
				
				else:
					if ref_loc != '':
						cmd = cmd_dir+'pca.py -t '+ trj_loc + ' -p ' + top_loc + ' -ag '+ ag_sele + ' -pt '+ pc_sele + ' -out ' + out_loc + ' -r ' + ref_loc
					else:				
						tkMessageBox.showinfo("pyMODE-TASK warning!", "No Ref structure given, using deafult first frame!")
						cmd = cmd_dir+'pca.py -t '+ trj_loc + ' -p ' + top_loc + ' -ag '+ ag_sele + ' -pt '+ pc_sele + ' -out ' + out_loc
					
					out = `os.system(cmd)`
					if out == '0':
						tkMessageBox.showinfo("pyMODE-TASK!", "PCA (EVD) run successful!\nResults are written in \n" + out_loc)
					else:
						tkMessageBox.showinfo("pyMODE-TASK!", "PCA (EVD) run failed. See terminal for details!")
			
			# run kernel PCA
			elif pc_sele == 'kpca':
				if trj_loc == '':
					tkMessageBox.showinfo("pyMODE-TASK Error!", "No trajectory location given!")
				if top_loc == '':
					tkMessageBox.showinfo("pyMODE-TASK Error!", "No topology location given!")
				
				else:
					if ref_loc != '':
						cmd = cmd_dir+'pca.py -t '+ trj_loc + ' -p ' + top_loc + ' -ag '+ ag_sele + ' -pt '+ pc_sele + ' -out ' + out_loc + ' -r ' + ref_loc + ' -kt ' + kt_sele
					else:				
						tkMessageBox.showinfo("pyMODE-TASK warning!", "No Ref structure given, using deafult first frame!")
						cmd = cmd_dir+'pca.py -t '+ trj_loc + ' -p ' + top_loc + ' -ag '+ ag_sele + ' -pt '+ pc_sele + ' -out ' + out_loc + ' -kt ' + kt_sele
					
					out = `os.system(cmd)`
					if out == '0':
						tkMessageBox.showinfo("pyMODE-TASK!", "Kernel PCA run successful!\nResults are written in \n" + out_loc)
					else:
						tkMessageBox.showinfo("pyMODE-TASK!", "Kernel PCA run failed. See terminal for details!")
			
			# run ipca
			elif pc_sele == 'ipca':
				if trj_loc == '':
					tkMessageBox.showinfo("pyMODE-TASK Error!", "No trajectory location given!")
				if top_loc == '':
					tkMessageBox.showinfo("pyMODE-TASK Error!", "No topology location given!")
				
				else:
					if ref_loc != '':
						cmd = cmd_dir+'pca.py -t '+ trj_loc + ' -p ' + top_loc + ' -ag '+ ag_sele + ' -pt '+ pc_sele + ' -out ' + out_loc + ' -r ' + ref_loc 
					else:				
						tkMessageBox.showinfo("pyMODE-TASK warning!", "No Ref structure given, using deafult first frame!")
						cmd = cmd_dir+'pca.py -t '+ trj_loc + ' -p ' + top_loc + ' -ag '+ ag_sele + ' -pt '+ pc_sele + ' -out ' + out_loc
					
					out = `os.system(cmd)`
					if out == '0':
						tkMessageBox.showinfo("pyMODE-TASK!", "Incremental PCA run successful!\nResults are written in \n" + out_loc)
					else:
						tkMessageBox.showinfo("pyMODE-TASK!", "Incremental PCA run failed. See terminal for details!")	
		#self.pb.stop()
	def run_ipca(self):
	
		# core scripts are located at src directory under pyMODE-TASK directory
		#cmd_dir = './src'
		status = self.check_conf_status()
		if status:
			cmd_dir = self.mode_task_location1.getvalue() + '/src/'
			trj_loc = self.ipca_trj_location.getvalue()
			top_loc = self.ipca_top_location.getvalue()
			ct_sele = self.ct_buttons.getvalue()
			ag_sele = self.ipca_atm_grp_buttons.getvalue()
			pc_comp = self.pca_comp.getvalue()
			out_loc = self.ipca_out_dir_location.getvalue()
		
			if trj_loc == '':
				tkMessageBox.showinfo("pyMODE-TASK Error!", "No trajectory location given!")
			if top_loc == '':
				tkMessageBox.showinfo("pyMODE-TASK Error!", "No topology location given!")
			else:	
				cmd = cmd_dir+'internal_pca.py -t '+ trj_loc + ' -p ' + top_loc + ' -ag ' + ag_sele + ' -out ' + out_loc + ' -ct ' + ct_sele
				out = `os.system(cmd)`
				#print type(out)
				if out == '0':
					tkMessageBox.showinfo("pyMODE-TASK!", "Internal PCA run successful!\nResults are written in Output Directory!")
				else:
					tkMessageBox.showinfo("pyMODE-TASK!", "Internal PCA run failed. See terminal for details!")
	
	def run_mds(self):
	
		# core scripts are located at src directory under pyMODE-TASK directory
		#cmd_dir = './src'
		status = self.check_conf_status()
		if status:
			cmd_dir = self.mode_task_location1.getvalue() + '/src/'
			trj_loc = self.mds_trj_location.getvalue()
			top_loc = self.mds_top_location.getvalue()
			mds_type = self.mds_type_buttons.getvalue()
			ct_sele = self.mds_cord_type.getvalue()
			ag_sele = self.atm_grp_buttons.getvalue()
			dist_type = self.mds_dissimilarity_type.getvalue()
			out_loc = self.mds_out_dir_location.getvalue()
			atm_ind = self.mds_atm_ind_buttons.getvalue()
			if trj_loc == '':
				tkMessageBox.showinfo("pyMODE-TASK Error!", "No trajectory location given!")
			if top_loc == '':
				tkMessageBox.showinfo("pyMODE-TASK Error!", "No topology location given!")
			else:	
				cmd = cmd_dir+'mds.py -t '+ trj_loc + ' -p ' + top_loc + ' -mt ' + mds_type +' -ag ' + ag_sele + ' -out ' + out_loc + ' -ct ' + ct_sele + ' -ai ' + atm_ind + ' -dt ' + dist_type
				out = `os.system(cmd)`
				#print type(out)
				if out == '0':
					tkMessageBox.showinfo("pyMODE-TASK!", "MDS run successful!\nResults are written in \n" + out_loc)
				else:
					tkMessageBox.showinfo("pyMODE-TASK!", "MDS run failed. See terminal for details!")
	
	def run_tsne(self):
	
		# core scripts are located at src directory under pyMODE-TASK directory
		#cmd_dir = './src'
		status = self.check_conf_status()
		if status:
			cmd_dir = self.mode_task_location1.getvalue() + '/src/'
			trj_loc = self.mds_trj_location.getvalue()
			top_loc = self.mds_top_location.getvalue()
			ct_sele = self.mds_cord_type.getvalue()
			ag_sele = self.atm_grp_buttons.getvalue()
			dist_type = self.mds_dissimilarity_type.getvalue()
			out_loc = self.mds_out_dir_location.getvalue()
			atm_ind = self.mds_atm_ind_buttons.getvalue()
			if trj_loc == '':
				tkMessageBox.showinfo("pyMODE-TASK Error!", "No trajectory location given!")
			if top_loc == '':
				tkMessageBox.showinfo("pyMODE-TASK Error!", "No topology location given!")
			else:	
				cmd = cmd_dir+'tsne.py -t '+ trj_loc + ' -p ' + top_loc + ' -ag ' + ag_sele + ' -out ' + out_loc + ' -ct ' + ct_sele + ' -ai ' + atm_ind + ' -dt ' + dist_type
				out = `os.system(cmd)`
				#print type(out)
				if out == '0':
					tkMessageBox.showinfo("pyMODE-TASK!", "t-SNE run successful!\nResults are written in \n" + out_loc)
				else:
					tkMessageBox.showinfo("pyMODE-TASK!", "t-SNE run failed. See terminal for details!")
	
	def run_cg(self):
		# core scripts are located at src directory under pyMODE-TASK directory
		#cmd_dir = './src'
		status = self.check_conf_status()
		if status:
			cmd_dir = self.mode_task_location1.getvalue() + '/src/'
			pdb_loc = self.cg_pdb_location.getvalue()
			cg_level = self.cg_level.getvalue()
			out_loc = self.cg_out_dir_location.getvalue()
			out_pdb = self.cg_out_pdb.getvalue()
			#print out_loc
			start_atm = self.cg_start_atm.getvalue()
			#print type(start_atm)
			atm_type = 'CB'
			if pdb_loc == '':
				tkMessageBox.showinfo("pyMODE-TASK Error!", "No PDB location given!")
			else:	
				cmd = cmd_dir+'coarseGrain.py --pdb ' + pdb_loc + ' --cg ' + cg_level + ' --atomType ' + atm_type + ' --startingAtom ' + start_atm + ' --outdir ' + out_loc + ' --output ' + out_pdb
				out = `os.system(cmd)`
				if out == '0':
					tkMessageBox.showinfo("pyMODE-TASK!", "Coarse graining run successful!\nResults are written in \n" + out_loc)
				else:
					tkMessageBox.showinfo("pyMODE-TASK!", "Coarse graining run failed. See terminal for details!")
	
	def run_nma(self):
		# core scripts are located at src directory under pyMODE-TASK directory
		#cmd_dir = './src'
		status = self.check_conf_status()
		if status:
			cmd_dir = self.mode_task_location1.getvalue() + '/src/'
			pdb_loc = self.nma_pdb_location.getvalue()
			cutoff = self.nma_cut.getvalue()
			out_loc = self.nma_out_dir_location.getvalue()
			atm_type = self.nma_atm_type.getvalue()
			if pdb_loc == '':
				tkMessageBox.showinfo("pyMODE-TASK Error!", "No PDB location given!")
			else:	
				cmd = cmd_dir+'ANM --pdb ' + pdb_loc + ' --cutoff ' + cutoff + ' --outdir ' + out_loc + ' --atomType ' + atm_type
				out = `os.system(cmd)`
				#print type(out)
				if out == '0':
					tkMessageBox.showinfo("pyMODE-TASK!", "NMA run successful!\nResults are written in \n" + out_loc)
				else:
					tkMessageBox.showinfo("pyMODE-TASK!", "NMA run failed. See terminal for details!")
	
	def run_conf_mode(self):
		status = self.check_conf_status()
		unal_pdb = self.conf_mode_Unalgn_pdb1.getvalue()
		pdb = self.conf_mode_pdb.getvalue()
		vtfile = self.conf_mode_vtfile.getvalue()
		out_loc = self.conf_mode_out.getvalue()
		atm_type = self.conf_atm_type.getvalue()
		if status:
			# core scripts are located at src directory under pyMODE-TASK directory
			cmd_dir = self.mode_task_location1.getvalue() + '/src/'
			
			if unal_pdb == '':
				tkMessageBox.showinfo("pyMODE-TASK Error!", "No unaligned PDB location given!")
			if pdb == '':
				tkMessageBox.showinfo("pyMODE-TASK Error!", "No PDB location given!")
			if vtfile == '':
				tkMessageBox.showinfo("pyMODE-TASK Error!", "No VT File location given!")
			else:
				cmd = cmd_dir+'conformationMode.py --pdbConf ' + unal_pdb + ' --pdbANM ' + pdb + ' --vtMatrix ' +  vtfile + ' --outdir ' + out_loc + ' --atomType ' + atm_type
				out = `os.system(cmd)`
				#print out
				if out == '0':
						tkMessageBox.showinfo("pyMODE-TASK!", "conformationMode run successful!\nResults are written in \n" + out_loc)
				else:
					tkMessageBox.showinfo("pyMODE-TASK!", "conformationMode run failed. See terminal for details!")
	
	def run_comb_mode(self):
		status = self.check_conf_status()
		unal_pdb = self.conf_mode_Unalgn_pdb1.getvalue()
		pdb = self.conf_mode_pdb.getvalue()
		vtfile = self.conf_mode_vtfile.getvalue()
		out_loc = self.conf_mode_out.getvalue()
		atm_type = self.conf_atm_type.getvalue()
		modes = self.comb_modes.getvalue()
		if status:
			# core scripts are located at src directory under pyMODE-TASK directory
			cmd_dir = self.mode_task_location1.getvalue() + '/src/'
			
			if unal_pdb == '':
				tkMessageBox.showinfo("pyMODE-TASK Error!", "No unaligned PDB location given!")
			if pdb == '':
				tkMessageBox.showinfo("pyMODE-TASK Error!", "No PDB location given!")
			if vtfile == '':
				tkMessageBox.showinfo("pyMODE-TASK Error!", "No VT File location given!")
			else:
				cmd = cmd_dir+'combinationMode.py --pdbConf ' + unal_pdb + ' --pdbANM ' + pdb + ' --vtMatrix ' +  vtfile + ' --outdir ' + out_loc + ' --atomType ' + atm_type + ' --modes ' + modes
				out = `os.system(cmd)`
				if out == '0':
						tkMessageBox.showinfo("pyMODE-TASK!", "combinationMode run successful!\nResults are written in \n" + out_loc)
				else:
					tkMessageBox.showinfo("pyMODE-TASK!", "combinationMode run failed. See terminal for details!")
	
	def run_msf(self):
		status = self.check_conf_status()
		pdb = self.msf_pdb.getvalue()
		pdb_conf = self.msf_conf_pdb.getvalue()
		wMatrix1 = self.msf_WMatrixFile.getvalue()
		vtMatrix1 = self.msf_VTMatrixFile.getvalue()
		wMatrix2 = self.msf_WMatrixFile1.getvalue()
		vtMatrix2 = self.msf_VTMatrixFile1.getvalue()
		at_type = self.msf_atm_type.getvalue()
		modes = self.msf_mode.getvalue()
		if status:
			# core scripts are located at src directory under pyMODE-TASK directory
			cmd_dir = self.mode_task_location1.getvalue() + '/src/'
			if pdb == '':
				tkMessageBox.showinfo("pyMODE-TASK Error!", "No PDB given!")
			if wMatrix1 == '':
				tkMessageBox.showinfo("pyMODE-TASK Error!", "No WMatrix file given!")
			if vtMatrix1 == '':
				tkMessageBox.showinfo("pyMODE-TASK Error!", "No VT Matrix file given!")
			elif pdb_conf == '':
				cmd = cmd_dir+'meanSquareFluctuations.py --pdb ' + pdb + ' --vtMatrix ' +  vtMatrix1  + ' --atomType ' + at_type + ' --wMatrix ' + wMatrix1 + ' --modes ' + modes
				out = `os.system(cmd)`
			else:
				cmd = cmd_dir+'meanSquareFluctuations.py --pdb ' + pdb + ' --pdbC ' + pdb_conf + ' --vtMatrix ' +  vtMatrix1  + ' --vtMatrixC ' +  vtMatrix2  + ' --atomType ' + at_type + ' --wMatrix ' + wMatrix1 + ' --wMatrixC ' + wMatrix2 + ' --modes ' + modes
				out = `os.system(cmd)`
				if out == '0':
					tkMessageBox.showinfo("pyMODE-TASK!", "MSF run successful!\nResults are written in output directory")
				else:
					tkMessageBox.showinfo("pyMODE-TASK!", "MSF run failed. See terminal for details!")
		
	def run_ac(self):
		status = self.check_conf_status()
		ac_pdb = self.ac_pdb.getvalue()
		ac_wmf = self.ac_WMatrixFile.getvalue()
		ac_vtf = self.ac_VTMatrixFile.getvalue()
		mode = self.ac_modes.getvalue()
		asymm_unit = self.ac_asymm_unit.getvalue()
		zoom = self.ac_zoom.getvalue()
		vmin = self.ac_Vmin.getvalue()
		vmax = self.ac_Vmax.getvalue()
		atm_type = self.ac_atm_type.getvalue()
		#print type(vmin)
		#print type(vmax)
		if status:
			# core scripts are located at src directory under pyMODE-TASK directory
			cmd_dir = self.mode_task_location1.getvalue() + '/src/'
			if ac_pdb == '':
				tkMessageBox.showinfo("pyMODE-TASK Error!", "No PDB given!")
			if ac_wmf == '':
				tkMessageBox.showinfo("pyMODE-TASK Error!", "No WMatrix file given!")
			if ac_vtf == '':
				tkMessageBox.showinfo("pyMODE-TASK Error!", "No VT Matrix file given!")
			elif asymm_unit == '': 
				cmd = cmd_dir+'assemblyCovariance.py --pdb ' + ac_pdb + ' --vtMatrix ' +  ac_vtf  + ' --atomType ' + atm_type + ' --wMatrix ' + ac_wmf + ' --modes ' + mode + ' --zoom ' + zoom + ' --vmin ' + vmin + ' --vmax ' + vmax
				out = `os.system(cmd)`
				#print out
				if out == '0':
					tkMessageBox.showinfo("pyMODE-TASK!", "assembly Covariance run successful!\nResults are written in \n output directory")
				else:
					tkMessageBox.showinfo("pyMODE-TASK!", "assembly Covariance run failed. See terminal for details!")
			else:
				cmd = cmd_dir+'assemblyCovariance.py --pdb ' + ac_pdb + ' --vtMatrix ' +  ac_vtf  + ' --atomType ' + atm_type + ' --wMatrix ' + ac_wmf + ' --modes ' + mode + ' --zoom ' + zoom + ' --vmin ' + vmin + ' --vmax ' + vmax + ' --aUnits ' + asymm_unit
				out = `os.system(cmd)`
				if out == '0':
					tkMessageBox.showinfo("pyMODE-TASK!", "assembly Covariance run successful!\nResults are written in \n output directory")
				else:
					tkMessageBox.showinfo("pyMODE-TASK!", "assembly Covariance run failed. See terminal for details!")
				
	def run_get_eigen(self):
		status = self.check_conf_status()
		if status:
			# core scripts are located at src directory under pyMODE-TASK directory
			#cmd_dir = './src'
			cmd_dir = self.mode_task_location1.getvalue() + '/src/'
			ge_vt_file=self.ge_vtfile_location.getvalue()
			mode_idx = self.ge_mode_idx.getvalue()
			direction = self.ge_direction.getvalue()
			print ge_vt_file
			if ge_vt_file == '':
				tkMessageBox.showinfo("pyMODE-TASK Error!", "No VT Matrix file given!")
			if mode_idx == '':
				tkMessageBox.showinfo("pyMODE-TASK Error!", "No mode index given!")
			else:	
				cmd = cmd_dir+'getEigenVectors --vtMatrix ' + ge_vt_file + ' --mode ' + mode_idx + ' --direction ' + direction
				out = `os.system(cmd)`
				if out == '0':
					tkMessageBox.showinfo("pyMODE-TASK!", "getEigenVectors run successful!\nResults are written in output directory\n")
				else:
					tkMessageBox.showinfo("pyMODE-TASK!", "getEigenVectors run failed. See terminal for details!")
	
	def run_mode_vis(self):
		status = self.check_conf_status()
		if status:
			# core scripts are located at src directory under pyMODE-TASK directory
			cmd_dir = self.mode_task_location1.getvalue() + '/src/'
			mv_pdb=self.mv_mode_pdb.getvalue()
			mv_at=self.mv_atm_type.getvalue()
			#mv_mode_idx = self.mv_indx_value.getvalue()
			#mv_vector_file = self.mv_vector_file.getvalue()
			ge_vt_file=self.ge_vtfile_location.getvalue()
			mode_idx = self.ge_mode_idx.getvalue()
			direction = self.ge_direction.getvalue()
			if mv_pdb == '':
				tkMessageBox.showinfo("pyMODE-TASK Error!", "No PDB file given!")
			if mode_idx == '':
				tkMessageBox.showinfo("pyMODE-TASK Error!", "No mode index given!")
			if ge_vt_file == '':
				tkMessageBox.showinfo("pyMODE-TASK Error!", "No vtMatrix file given!")

			else:	
				cmd = cmd_dir+'visualiseVector.py --pdb ' + mv_pdb + ' --vtMatrix ' + ge_vt_file + ' --mode ' + mode_idx + ' --atomType  ' + mv_at + ' --direction ' + direction
				out = `os.system(cmd)`
				if out == '0':
					tkMessageBox.showinfo("pyMODE-TASK!", "Mode visualization run successful!\nResults are written in output directory\n")
				else:
					tkMessageBox.showinfo("pyMODE-TASK!", "Mode visualization run failed. See terminal for details!")
	
	#=====================================
	# Configuration tab methods
	#=====================================
	
	def set_mode_task_dir(self, dirname):
		n = self.mode_task_location1.setvalue(dirname)
		return n
	
	#=========================================
	
	def pca_set_trj_filename(self, filename):
		n = self.pca_trj_location.setvalue(filename)
		return n
				
	def ipca_set_trj_filename(self, filename):
		n = self.ipca_trj_location.setvalue(filename)
		return n
		
	def set_pdb_filename(self, filename):
		n = self.pdb_location.setvalue(filename)
		return n
	
	def set_conf_mode_Unalgn_pdb(self, filename):
		n = self.conf_mode_Unalgn_pdb1.setvalue(filename)
		return n
		
	def set_conf_mode_pdb(self, filename):
		n = self.conf_mode_pdb.setvalue(filename)
		return n	
		
	def set_conf_mode_vtfile_location(self, filename):
		n = self.conf_mode_vtfile.setvalue(filename)
		return n
		
	def set_conf_mode_out(self, filename):
		n = self.conf_mode_out.setvalue(filename)
		return n
	
	#======================================
	# MSF methods
	#=====================================
	def set_msf_pdb(self, filename):
		n = self.msf_pdb.setvalue(filename)
		return n
	
	def set_msf_WMatrixFile(self, filename):
		n = self.msf_WMatrixFile.setvalue(filename)
		return n
		
	def set_msf_VTMatrixFile(self, filename):
		n = self.msf_VTMatrixFile.setvalue(filename)
		return n
	
	def set_msf_conf_pdb(self, filename):
		n = self.msf_conf_pdb.setvalue(filename)
		return n
		
	def set_msf_WMatrixFile1(self, filename):
		n = self.msf_WMatrixFile1.setvalue(filename)
		return n
		
	def set_msf_VTMatrixFile1(self, filename):
		n = self.msf_VTMatrixFile1.setvalue(filename)
		return n
		
	#===========================================
	# assembly Covariance methods
	#============================================
	
	def set_ac_pdb(self, filename):
		n = self.ac_pdb.setvalue(filename)
		return n
		
	def set_ac_WMatrixFile(self, filename):
		n = self.ac_WMatrixFile.setvalue(filename)
		return n
	
	def set_ac_VTMatrixFile(self, filename):
		n = self.ac_VTMatrixFile.setvalue(filename)
		return n
		
	#===========================================
	def get_pc_method_selection(self, sele_option):
		n=self.pca_methods_buttons.getvalue()
		return n
		
	def get_mds_type_selection(self, sele_option):
		n=self.mds_type_buttons.getvalue()
		return n
	
	def mds_set_trj_filename(self, filename):
		n = self.mds_trj_location.setvalue(filename)
		return n

	def mds_set_top_filename(self, filename):
		self.mds_top_location.setvalue(filename)
	
	def mds_set_out_location(self, dirname):
		self.mds_out_dir_location.setvalue(dirname)

	def get_st_selection(self, sele_option):
		n=self.svd_solver_type.getvalue()
		return n
		
	def get_kt_selection(self, sele_option):
		n=self.kernel_type.getvalue()
		return n
		
	def get_ag_selection(self, sele_option):
		n=self.atm_grp_buttons.getvalue()
		return n
		
	def get_ipca_ag_selection(self, sele_option):
		n=self.ipca_atm_grp_buttons.getvalue()
		return n
		
	def get_pc_selection(self, sele_option):
		n= self.pca_comp.getvalue()
		return n
		
	def get_cg_selection(self, sele_option):
		n= self.cg_level.getvalue()
		return n

	def set_top_filename(self, filename):
		self.pca_top_location.setvalue(filename)
	
	def ipca_set_top_filename(self, filename):
		self.ipca_top_location.setvalue(filename)
	
		
	def set_ref_filename(self, filename):
		self.pca_ref_file.setvalue(filename)
		
	def pca_set_out_location(self, dirname):
		self.pca_out_dir_location.setvalue(dirname)
	
	def ipca_set_out_location(self, dirname):
		self.ipca_out_dir_location.setvalue(dirname)
		
	def nma_set_out_location(self, dirname):
		self.nma_out_dir_location.setvalue(dirname)
	
	def get_mds_dissimilarity_type(self, sele_option):
		n= self.mds_dissimilarity_type.getvalue()
		return n
		
	def get_mds_cord_type(self, sele_option):
		n=self.mds_cord_type.getvalue()
		return n
	
	def set_cg_pdb_filename(self, filename):
		n = self.cg_pdb_location.setvalue(filename)
		return n
		
	def set_cg_out_location(self, dirname):
		self.cg_out_dir_location.setvalue(dirname)
		
	def set_nma_pdb_filename(self, filename):
		n = self.nma_pdb_location.setvalue(filename)
		return n
		
	def set_nma_vtfile_location(self, filename):
		n =self.nma_vtfile_location.setvalue(filename)
		return n
		
	def set_gi_out_location(self, filename):
		n=self.gi_out_dir_location.setvalue(filename)
		return n
		
	#==================================================
	# Get Eigenvectors methods
	#=====================================================
	
	def set_ge_vtfile_location(self, filename):
		n=self.ge_vtfile_location.setvalue(filename)
		return n 
		
	#===================================================
	# Mode visualisation methods
	#============================================
	def set_mv_mode_pdb(self, filename):
		n=self.mv_mode_pdb.setvalue(filename)
		return n 
	
	def set_mv_vector_file(self, filename):
		n=self.mv_vector_file.setvalue(filename)
		return n
		
	def about(self):
		print "pyMODE-TASK!\n pymol plugin of MODE-TASK\n MODE-TASK: a software tool to perform PCA and NMA of protein structure and MD trajectories"

class FileDialogButtonClassFactory:
	def get(fn,mode = 'r',filter=[("Executable",'*')]):
		"""This returns a FileDialogButton class that will
		call the specified function with the resulting file.
		"""
		class FileDialogButton(Button):
            # This is just an ordinary button with special colors.

			def __init__(self, master=None, cnf={}, **kw):
				'''when we get a file, we call fn(filename)'''
				self.fn = fn
				self.__toggle = 0
				apply(Button.__init__, (self, master, cnf), kw)
				self.configure(command=self.set)
			def set(self):
				if mode == 'r':
					n = MyFileDialog(types = filter).getopenfile()
				elif mode == 'w':
					n = MyFileDialog(types = filter).getsavefile()
				if n is not None:
					self.fn(n)
		return FileDialogButton
	get = staticmethod(get)
	
class DirDialogButtonClassFactory:
	def get(fn):
		"""This returns a FileDialogButton class that will
		call the specified function with the resulting file.
		"""
		class DirDialogButton(Button):
			# This is just an ordinary button with special colors.

			def __init__(self, master=None, cnf={}, **kw):
				'''when we get a file, we call fn(filename)'''
				self.fn = fn
				self.__toggle = 0
				apply(Button.__init__, (self, master, cnf), kw)
				self.configure(command=self.set)
			def set(self):
				fd = PmwDirDialog(self.master)
				fd.title('Please choose a directory')
				n=fd.askfilename()
				if n is not None:
					self.fn(n)
		return DirDialogButton
	get = staticmethod(get)
class PmwFileDialog(Pmw.Dialog):
    """File Dialog using Pmw"""
    def __init__(self, parent = None, **kw):
        # Define the megawidget options.
        optiondefs = (
            ('filter',    '*',              self.newfilter),
            ('directory', os.getcwd(),      self.newdir),
            ('filename',  '',               self.newfilename),
            ('historylen',10,               None),
            ('command',   None,             None),
            ('info',      None,             None),
            )
        self.defineoptions(kw, optiondefs)
        # Initialise base class (after defining options).
        Pmw.Dialog.__init__(self, parent)

        self.withdraw()

        # Create the components.
        interior = self.interior()

        if self['info'] is not None:
            rowoffset=1
            dn = self.infotxt()
            dn.grid(row=0,column=0,columnspan=2,padx=3,pady=3)
        else:
            rowoffset=0

        dn = self.mkdn()
        dn.grid(row=0+rowoffset,column=0,columnspan=2,padx=3,pady=3)
        del dn

        # Create the directory list component.
        dnb = self.mkdnb()
        dnb.grid(row=1+rowoffset,column=0,sticky='news',padx=3,pady=3)
        del dnb

        # Create the filename list component.
        fnb = self.mkfnb()
        fnb.grid(row=1+rowoffset,column=1,sticky='news',padx=3,pady=3)
        del fnb

        # Create the filter entry
        ft = self.mkft()
        ft.grid(row=2+rowoffset,column=0,columnspan=2,padx=3,pady=3)
        del ft

        # Create the filename entry
        fn = self.mkfn()
        fn.grid(row=3+rowoffset,column=0,columnspan=2,padx=3,pady=3)
        fn.bind('<Return>',self.okbutton)
        del fn

        # Buttonbox already exists
        bb=self.component('buttonbox')
        bb.add('OK',command=self.okbutton)
        bb.add('Cancel',command=self.cancelbutton)
        del bb

        Pmw.alignlabels([self.component('filename'),
                         self.component('filter'),
                         self.component('dirname')])

    def infotxt(self):
        """ Make information block component at the top """
        return self.createcomponent(
                'infobox',
                (), None,
                Tkinter.Label, (self.interior(),),
                width=51,
                relief='groove',
                foreground='darkblue',
                justify='left',
                text=self['info']
            )

    def mkdn(self):
        """Make directory name component"""
        return self.createcomponent(
            'dirname',
            (), None,
            Pmw.ComboBox, (self.interior(),),
            entryfield_value=self['directory'],
            entryfield_entry_width=40,
            entryfield_validate=self.dirvalidate,
            selectioncommand=self.setdir,
            labelpos='w',
            label_text='Directory:')

    def mkdnb(self):
        """Make directory name box"""
        return self.createcomponent(
            'dirnamebox',
            (), None,
            Pmw.ScrolledListBox, (self.interior(),),
            label_text='directories',
            labelpos='n',
            hscrollmode='none',
            dblclickcommand=self.selectdir)

    def mkft(self):
        """Make filter"""
        return self.createcomponent(
            'filter',
            (), None,
            Pmw.ComboBox, (self.interior(),),
            entryfield_value=self['filter'],
            entryfield_entry_width=40,
            selectioncommand=self.setfilter,
            labelpos='w',
            label_text='Filter:')

    def mkfnb(self):
        """Make filename list box"""
        return self.createcomponent(
            'filenamebox',
            (), None,
            Pmw.ScrolledListBox, (self.interior(),),
            label_text='files',
            labelpos='n',
            hscrollmode='none',
            selectioncommand=self.singleselectfile,
            dblclickcommand=self.selectfile)

    def mkfn(self):
        """Make file name entry"""
        return self.createcomponent(
            'filename',
            (), None,
            Pmw.ComboBox, (self.interior(),),
            entryfield_value=self['filename'],
            entryfield_entry_width=40,
            entryfield_validate=self.filevalidate,
            selectioncommand=self.setfilename,
            labelpos='w',
            label_text='Filename:')
    
    def dirvalidate(self,string):
        if os.path.isdir(string):
            return Pmw.OK
        else:
            return Pmw.PARTIAL
        
    def filevalidate(self,string):
        if string=='':
            return Pmw.PARTIAL
        elif os.path.isfile(string):
            return Pmw.OK
        elif os.path.exists(string):
            return Pmw.PARTIAL
        else:
            return Pmw.OK
        
    def okbutton(self):
        """OK action: user thinks he has input valid data and wants to
           proceed. This is also called by <Return> in the filename entry"""
        fn=self.component('filename').get()
        self.setfilename(fn)
        if self.validate(fn):
            self.canceled=0
            self.deactivate()

    def cancelbutton(self):
        """Cancel the operation"""
        self.canceled=1
        self.deactivate()

    def tidy(self,w,v):
        """Insert text v into the entry and at the top of the list of 
           the combobox w, remove duplicates"""
        if not v:
            return
        entry=w.component('entry')
        entry.delete(0,'end')
        entry.insert(0,v)
        list=w.component('scrolledlist')
        list.insert(0,v)
        index=1
        while index<list.index('end'):
            k=list.get(index)
            if k==v or index>self['historylen']:
                list.delete(index)
            else:
                index=index+1
        w.checkentry()

    def setfilename(self,value):
        if not value:
            return
        value=os.path.join(self['directory'],value)
        dir,fil=os.path.split(value)
        self.configure(directory=dir,filename=value)
        
        c=self['command']
        if callable(c):
            c()

    def newfilename(self):
        """Make sure a newly set filename makes it into the combobox list"""
        self.tidy(self.component('filename'),self['filename'])
        
    def setfilter(self,value):
        self.configure(filter=value)

    def newfilter(self):
        """Make sure a newly set filter makes it into the combobox list"""
        self.tidy(self.component('filter'),self['filter'])
        self.fillit()

    def setdir(self,value):
        self.configure(directory=value)

    def newdir(self):
        """Make sure a newly set dirname makes it into the combobox list"""
        self.tidy(self.component('dirname'),self['directory'])
        self.fillit()

    def singleselectfile(self):
        """Single click in file listbox. Move file to "filename" combobox"""
        cs=self.component('filenamebox').curselection()
        if cs!=():
            value=self.component('filenamebox').get(cs)
            self.setfilename(value)

    def selectfile(self):
        """Take the selected file from the filename, normalize it, and OK"""
        self.singleselectfile()
        value=self.component('filename').get()
        self.setfilename(value)
        if value:
            self.okbutton()

    def selectdir(self):
        """Take selected directory from the dirnamebox into the dirname"""
        cs=self.component('dirnamebox').curselection()
        if cs!=():
            value=self.component('dirnamebox').get(cs)
            dir=self['directory']
            if not dir:
                dir=os.getcwd()
            if value:
                if value=='..':
                    dir=os.path.split(dir)[0]
                else:
                    dir=os.path.join(dir,value)
            self.configure(directory=dir)
            self.fillit()

    def askfilename(self,directory=None,filter=None):
        """The actual client function. Activates the dialog, and
           returns only after a valid filename has been entered 
           (return value is that filename) or when canceled (return 
           value is None)"""
        if directory!=None:
            self.configure(directory=directory)
        if filter!=None:
            self.configure(filter=filter)
        self.fillit()
        self.canceled=1 # Needed for when user kills dialog window
        self.activate()
        if self.canceled:
            return None
        else:
            return self.component('filename').get()

    lastdir=""
    lastfilter=None
    lasttime=0
    def fillit(self):
        """Get the directory list and show it in the two listboxes"""
        # Do not run unnecesarily
        if self.lastdir==self['directory'] and self.lastfilter==self['filter'] and self.lasttime>os.stat(self.lastdir)[8]:
            return
        self.lastdir=self['directory']
        self.lastfilter=self['filter']
        self.lasttime=time()
        dir=self['directory']
        if not dir:
            dir=os.getcwd()
        dirs=['..']
        files=[]
        try:
            fl=os.listdir(dir)
            fl.sort()
        except os.error,arg:
            if arg[0] in (2,20):
                return
            raise
        for f in fl:
            if os.path.isdir(os.path.join(dir,f)):
                dirs.append(f)
            else:
                filter=self['filter']
                if not filter:
                    filter='*'
                if fnmatch.fnmatch(f,filter):
                    files.append(f)
        self.component('filenamebox').setlist(files)
        self.component('dirnamebox').setlist(dirs)
    
    def validate(self,filename):
        """Validation function. Should return 1 if the filename is valid, 
           0 if invalid. May pop up dialogs to tell user why. Especially 
           suited to subclasses: i.e. only return 1 if the file does/doesn't 
           exist"""
        return 1
		
class PmwDirDialog(PmwFileDialog):
    """Directory Dialog using Pmw"""
    def __init__(self, parent = None, **kw):
        # Define the megawidget options.
        optiondefs = (
            ('directory', os.getcwd(),      self.newdir),
            ('historylen',10,               None),
            ('command',   None,             None),
            ('info',      None,             None),
            )
        self.defineoptions(kw, optiondefs)
        # Initialise base class (after defining options).
        Pmw.Dialog.__init__(self, parent)

        self.withdraw()

        # Create the components.
        interior = self.interior()

        if self['info'] is not None:
            rowoffset=1
            dn = self.infotxt()
            dn.grid(row=0,column=0,columnspan=2,padx=3,pady=3)
        else:
            rowoffset=0

        dn = self.mkdn()
        dn.grid(row=1+rowoffset,column=0,columnspan=2,padx=3,pady=3)
        dn.bind('<Return>',self.okbutton)
        del dn

        # Create the directory list component.
        dnb = self.mkdnb()
        dnb.grid(row=0+rowoffset,column=0,columnspan=2,sticky='news',padx=3,pady=3)
        del dnb

        # Buttonbox already exists
        bb=self.component('buttonbox')
        bb.add('OK',command=self.okbutton)
        bb.add('Cancel',command=self.cancelbutton)
        del bb



    lastdir=""
    def fillit(self):
        """Get the directory list and show it in the two listboxes"""
        # Do not run unnecesarily
        if self.lastdir==self['directory']:
            return
        self.lastdir=self['directory']
        dir=self['directory']
        if not dir:
            dir=os.getcwd()
        dirs=['..']
        try:
            fl=os.listdir(dir)
            fl.sort()
        except os.error,arg:
            if arg[0] in (2,20):
                return
            raise
        for f in fl:
            if os.path.isdir(os.path.join(dir,f)):
                dirs.append(f)
        self.component('dirnamebox').setlist(dirs)

    def okbutton(self):
        """OK action: user thinks he has input valid data and wants to
           proceed. This is also called by <Return> in the dirname entry"""
        fn=self.component('dirname').get()
        self.configure(directory=fn)
        if self.validate(fn):
            self.canceled=0
            self.deactivate()
    
    def askfilename(self,directory=None):
        """The actual client function. Activates the dialog, and
           returns only after a valid filename has been entered 
           (return value is that filename) or when canceled (return 
           value is None)"""
        if directory!=None:
            self.configure(directory=directory)
        self.fillit()
        self.activate()
        if self.canceled:
            return None
        else:
            return self.component('dirname').get()

    def dirvalidate(self,string):
        if os.path.isdir(string):
            return Pmw.OK
        elif os.path.exists(string):
            return Pmw.PARTIAL
        else:
            return Pmw.OK

    def validate(self,filename):
        """Validation function. Should return 1 if the filename is valid, 
           0 if invalid. May pop up dialogs to tell user why. Especially 
           suited to subclasses: i.e. only return 1 if the file does/doesn't 
           exist"""
        if filename=='':
            _errorpop(self.interior(),"Empty filename")
            return 0
        if os.path.isdir(filename) or not os.path.exists(filename):
            return 1
        else:
            _errorpop(self.interior(),"This is not a directory")
            return 0   
			
class MyFileDialog:

    def __init__(self,types = [("Executable","*")]):
        self.types = types

    def getopenfile(self):
        result = tkFileDialog.askopenfilename(filetypes=self.types)
        if result == "":
            return None
        else:
            return result
    def getsavefile(self):
        result = tkFileDialog.asksaveasfilename(filetypes=self.types)
        if result == "":
            return None
        else:
            return result

class IORedirector(object):
	'''A general class for redirecting I/O to this Text widget.'''
	def __init__(self,text_area):
		self.text_area = text_area


class MyHelpPage:
	'A class for opening web help pages'
	def __init__(self, url):
		self.url=url
		
	def openpage(self):
		webbrowser.open_new(self.url)
		
#root = Tk()
#app = App(root)
#root.title("pyMODE-TASK")
#root.geometry("1000x700")
##root.iconbitmap('icons.ico')
#root.mainloop()
