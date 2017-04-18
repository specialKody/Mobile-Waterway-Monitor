#**************************************************************************************#
# Project: River Node
# Authors: Kody Stribrny
# Department: CIDSE
# Semester: Fall 2016/Spring 2017
# Course Number and Name: CSE 492/493 Honors Thesis
# Supervisors: Dr. Sarma Vrudhula & Dr. Carole-Jean Wu
#**************************************************************************************#

# STANDARD LIBRARIES
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd

# MY FILES
from data_calc import *
from list_conversions import *
from map_data import map_points

dataList=[]
#**************************************************************************************#
#								Functions											   #
#**************************************************************************************#

def update_data():
	"""
	Description:
		Updates the data list as well as the feed data.
	"""
	global feed_data
	feed_data = pd.read_json('https://io.adafruit.com/api/v2/specialKody/feeds/river-node-location-ph/data')
	feed_data['created_at'] =  pd.to_datetime(feed_data['created_at'], infer_datetime_format=True)
	#This removes the unused data columns
	feed_data.drop(feed_data.columns[[0,2,4,5,6,9,11]], axis=1, inplace=True)

	lat = feed_data['lat']
	lon = feed_data['lon']
	dist = calculated_distance(lat,lon)
	speedSeries = list_to_series(calculate_speeds(feed_data['created_at'], dist))

	global dataList 
	dataList= [lat, lon, feed_data['ele'], feed_data['value'], feed_data['created_at'], speedSeries]

def map_ph(high_contrast):
	"""
		:param high_contrast: This specifies the color contrast of the map. 0=regular contrast, 1=heightened contrast
		
	Description:
		Maps the pH values on the Basemap map through the map_points function call.
	"""
	map_points((dataList[1]).tolist(), (dataList[0]).tolist(), (pd.Series(dataList[3])).tolist(), high_contrast)

def elev_update(dump, line, ax, high_contrast):
	"""
		:param dump: Believe this is needed as garbage data goes into first parameter
		:param line: The line to be updated
		:param ax: The plot the line is currently on
		:param high_contrast: This specifies the color contrast of the map. 0=regular contrast, 1=heightened contrast
		
	Description:
		Updates the elevation line plot after pulling new data.
	"""
	plt.cla()
	update_data()
	elevation = pd.Series(dataList[2])
	if(high_contrast):
		line = ax.plot(elevation, linewidth=3.0)
	else:
		line = ax.plot(elevation)
	return line

def plot_elev(real_time, high_contrast):
	"""
		:param real_time: This specifies if real time updates are to occur. 0=static data, 1=updating data
		:param high_contrast: This specifies the color contrast of the map. 0=regular contrast, 1=heightened contrast
		
	Description:
		This functions plots the elevation data.
	"""	
	if(real_time):
		elevation = pd.Series(dataList[2])
		fig, ax = plt.subplots()
		fig.canvas.set_window_title("Node Elevation")
		ax.set_ylabel("Elevation (Meters)")
		ax.set_xlabel("Measurment")
		line = ax.plot(elevation)

		ani = animation.FuncAnimation(fig, elev_update, interval=1000, fargs=(line, ax, high_contrast), blit=True)
	else:
		plt.figure("Node Elevation")
		elevation = pd.Series(dataList[2])
		if(high_contrast == 1):
			elevation.plot(linewidth=3.0)
		else:
			elevation.plot()
		plt.ylabel("Elevation (Meters)")
		plt.xlabel("Measurment")
	plt.show()
	
def ph_update(dump, line, ax, high_contrast):
	"""
		:param dump: Believe this is needed as garbage data goes into first parameter
		:param line: The line to be updated
		:param ax: The plot the line is currently on
		:param high_contrast: This specifies the color contrast of the map. 0=regular contrast, 1=heightened contrast
		
	Description:
		Updates the ph line plot after pulling new data.
	"""
	plt.cla()
	update_data()
	values = pd.Series(dataList[3])
	if(high_contrast):
		line = ax.plot(values, linewidth=3.0)
	else:
		line = ax.plot(values)
	return line
	
def plot_ph(real_time, high_contrast):
	"""
		:param real_time: This specifies if real time updates are to occur. 0=static data, 1=updating data
		:param high_contrast: This specifies the color contrast of the map. 0=regular contrast, 1=heightened contrast
	
	Description:
		This function plots the PH data. The PH data is stored as 'value' by the Adafruit IOT website.
	"""
	if(real_time):
		values = pd.Series(dataList[3])
		fig, ax = plt.subplots()
		fig.canvas.set_window_title("Node pH Recordings")
		ax.set_ylabel("PH")
		ax.set_xlabel("Measurment")
		line = ax.plot(values)

		ani = animation.FuncAnimation(fig, ph_update, interval=20000, fargs=(line, ax, high_contrast), blit=True)
	else:
		plt.figure("Node PH Recordings")
		values = pd.Series(dataList[3])
		if(high_contrast == 1):
			values.plot(linewidth=3.0)
		else:
			values.plot()
		plt.ylabel("PH")
		plt.xlabel("Measurment")

	plt.show()
	
def speed_update(dump, line, ax, high_contrast):
	"""
		:param dump: Believe this is needed as garbage data goes into first parameter
		:param line: The line to be updated
		:param ax: The plot the line is currently on
		:param high_contrast: This specifies the color contrast of the map. 0=regular contrast, 1=heightened contrast
		
	Description:
		Updates the speed line plot after pulling new data.
	"""
	plt.cla()
	update_data()
	speed = dataList[5]
	if(high_contrast):
		line = ax.plot(speed, linewidth=3.0)
	else:
		line = ax.plot(speed)
	return line	

def plot_speed(real_time, high_contrast):
	"""	
		:param real_time: This specifies if real time updates are to occur. 0=static data, 1=updating data
		:param high_contrast: This specifies the color contrast of the map. 0=regular contrast, 1=heightened contrast
	
	Description:
		This function plots the calculated speed values. This requires a call to the list_to_series fucntion and the 
		calculate_speeds function.
	"""
	if(real_time):
		speed = dataList[5]
		fig, ax = plt.subplots()
		fig.canvas.set_window_title("Node Speed")
		ax.set_ylabel("Speed (Meters/Second)")
		ax.set_xlabel("Measurment")
		line = ax.plot(speed)

		ani = animation.FuncAnimation(fig, speed_update, interval=20000, fargs=(line, ax, high_contrast), blit=True)
	else:
		plt.figure("Node Speed")
		speedSeries = dataList[5]
		if(high_contrast == 1):
			speedSeries.plot(linewidth=3.0)
		else:
			speedSeries.plot()
		plt.ylabel("Speed (Meters/Second)")
		plt.xlabel("Measurment")
	plt.show()	

def export_data():
	"""		
	Description:
		Exports the feed data to a text file. This feed data has unused columns trimmed.
	"""
	global feed_data
	a = feed_data.to_string(buf=None, columns=None, col_space=None, header=True, index=True, na_rep='NaN', formatters=None, float_format=None, sparsify=None, index_names=True, justify=None, line_width=None, max_rows=None, max_cols=None, show_dimensions=False)
	f = open('dashboard_export.txt', 'w')
	f.write(a)

def elev_update_nr(dump, line, ax, high_contrast):
	"""
		:param dump: Believe this is needed as garbage data goes into first parameter
		:param line: The line to be updated
		:param ax: The plot the line is currently on
		:param high_contrast: This specifies the color contrast of the map. 0=regular contrast, 1=heightened contrast
		
	Description:
		Updates the elevation plot without updating data.
	"""
	plt.cla()
	elevation = pd.Series(dataList[2])
	if(high_contrast):
		line = ax.plot(elevation, linewidth=3.0)
	else:
		line = ax.plot(elevation)
	return line
	
def speed_update_nr(dump, line, ax, high_contrast):
	"""
		:param dump: Believe this is needed as garbage data goes into first parameter
		:param line: The line to be updated
		:param ax: The plot the line is currently on
		:param high_contrast: This specifies the color contrast of the map. 0=regular contrast, 1=heightened contrast
		
	Description:
		Updates the speed plot without updating data.
	"""
	plt.cla()
	speed = dataList[5]
	if(high_contrast):
		line = ax.plot(speed, linewidth=3.0)
	else:
		line = ax.plot(speed)
	return line	

def plot_combined(real_time, high_contrast):
	"""
		:param real_time: This specifies if real time updates are to occur. 0=static data, 1=updating data
		:param high_contrast: This specifies the color contrast of the map. 0=regular contrast, 1=heightened contrast
		
	Description:
		This function places all three line plots (pH, elevation, speed) on a single window one above another.
		This is a seperate button as the stacking creates smaller graphing windows.
	"""
	if(real_time):
		elevation = pd.Series(dataList[2])
		values = pd.Series(dataList[3])
		speed = dataList[5]
		fig,(ax1, ax2, ax3) = plt.subplots(3, sharex=False, sharey=False)
		fig.canvas.set_window_title("Combined Plots")
		ax1.set_title("Node pH Recordings")
		ax2.set_title("Node Elevation")
		ax3.set_title("Node Speed")
		ax1.set_ylabel("pH")
		ax1.set_xlabel("Measurment")
		ax2.set_ylabel("Meters")
		ax2.set_xlabel("Measurment")
		ax3.set_ylabel("Meters/Second")
		ax3.set_xlabel("Measurment")
		line1 = ax1.plot(values)
		line2 = ax2.plot(elevation)
		line3 = ax3.plot(speed)

		ani1 = animation.FuncAnimation(fig, ph_update, interval=20000, fargs=(line1, ax1, high_contrast), blit=True)
		ani2 = animation.FuncAnimation(fig, elev_update_nr, interval=20000, fargs=(line2, ax2, high_contrast), blit=True)
		ani3 = animation.FuncAnimation(fig, speed_update_nr, interval=20000, fargs=(line3, ax3, high_contrast), blit=True)
	else:
		fig,(ax1, ax2, ax3) = plt.subplots(3, sharex=False, sharey=False)
		values = pd.Series(dataList[3])
		elevation = pd.Series(dataList[2])
		speedSeries = dataList[5]
		
		if(high_contrast):
			ax1.plot(values, linewidth=3.0)
			ax2.plot(elevation, linewidth=3.0)
			ax3.plot(speedSeries, linewidth=3.0)
		else:
			ax1.plot(values)
			ax2.plot(elevation)
			ax3.plot(speedSeries)
		ax1.set_title("pH Values")
		ax2.set_title("Elevation (Meters)")
		ax3.set_title("Speed (Meters/Second)")
		ax1.set_ylabel("pH")
		ax1.set_xlabel("Measurment")
		ax2.set_ylabel("Meters")
		ax2.set_xlabel("Measurment")
		ax3.set_ylabel("Meters/Second")
		ax3.set_xlabel("Measurment")
		fig.canvas.set_window_title("Combined Plot")
	plt.tight_layout(h_pad=2.0)
	plt.show()
	