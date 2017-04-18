#**************************************************************************************#
# Project: River Node
# Authors: Kody Stribrny
# Department: CIDSE
# Semester: Fall 2016/Spring 2017
# Course Number and Name: CSE 492/493 Honors Thesis
# Supervisors: Dr. Sarma Vrudhula & Dr. Carole-Jean Wu
#**************************************************************************************#

# STANDARD LIBRARIES
from tkinter import *
from tkinter import ttk
import threading

# MY FILES
from dashboard_backer import *

#**************************************************************************************#
#								Functions											   #
#**************************************************************************************#

def close_window(*args): 
	"""
		:param *args: allows an undetermined amount of parameters to be passed in. No functional effect.
		
	Description:
		A simmple function which exits the application when the ESC key is pressed.
	"""
	root.destroy()
	
def plot_elev_tk():
	"""		
	Description:
		A Tkinter call which passes in the high_contrast checkbox value to the plot_elev function.
	"""
	plot_elev(CheckVar1.get(), CheckVar2.get())

def plot_ph_tk():
	"""		
	Description:
		A Tkinter call which passes in the high_contrast checkbox value to the plot_ph function.
	"""
	plot_ph(CheckVar1.get(), CheckVar2.get())

def plot_speed_tk():
	"""		
	Description:
		A Tkinter call which passes in the high_contrast checkbox value to the plot_speed function.
	"""
	plot_speed(CheckVar1.get(), CheckVar2.get())

def plot_combined_tk():
	"""		
	Description:
		A Tkinter call which passes in the high_contrast checkbox value to the plot_combined function.
	"""
	
	plot_combined(CheckVar1.get(), CheckVar2.get())
	
def map_ph_tk():
	"""		
	Description:
		A Tkinter call which passes in the high_contrast checkbox value to the map_ph function.
	"""
	map_ph(CheckVar2.get())


def update_data_tk():
	"""		
	Description:
		Initializes the feed data series after the GUI loads.
	"""
	update_data()
	
#**************************************************************************************#
#								TkInter Script										   #
#**************************************************************************************#

root = Tk()
root.title("Mobile Waterway Monitor Dashboard")

mainframe = ttk.Frame(root, padding="12 12 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=0)
mainframe.rowconfigure(0, weight=0)

CheckVar1 = IntVar()
CheckVar2 = IntVar()

ttk.Label(mainframe, text="Welcome to the dashboard. Use the buttons below to complete actions").grid(row=0, column=0,columnspan=3, sticky=(E,W))
C1 = Checkbutton(mainframe, text = "Real Time Update", variable = CheckVar1, onvalue = 1, offvalue = 0).grid(column=0, row=3, sticky=(N, W, S))
C2 = Checkbutton(mainframe, text = "High Color Contrast", variable = CheckVar2, onvalue = 1, offvalue = 0).grid(column=2, row=3, sticky=(N, E, S))

ttk.Button(mainframe, text="View PH Graph", command=plot_ph_tk).grid(column=0, row=1, sticky=(N, W, E, S))
ttk.Button(mainframe, text="View Elevation Graph", command=plot_elev_tk).grid(column=1, row=1, sticky=(N, W, E, S))
ttk.Button(mainframe, text="View Speed Graph", command=plot_speed_tk).grid(column=2, row=1, sticky=(N, W, E, S))

ttk.Button(mainframe, text="Export Data To File", command=export_data).grid(column=0, row=2, sticky=(N, W, E, S))
ttk.Button(mainframe, text="Combined Plot", command=plot_combined_tk).grid(column=1, row=2, sticky=(N, W, E, S))
ttk.Button(mainframe, text="Map pH Values", command=map_ph_tk).grid(column=2, row=2, sticky=(N, W, E, S))

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root.bind('<Escape>', close_window)	#Defines the escape key as a shortcut to close the window

root.after(10,update_data_tk)
root.mainloop()