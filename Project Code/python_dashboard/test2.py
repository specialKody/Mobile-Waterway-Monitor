#**************************************************************************************#
# Project: River Node
# Authors: Kody Stribrny
# Department: CIDSE
# Semester: Fall 2016/Spring 2017
# Course Number and Name: CSE 492/493 Honors Thesis
# Supervisors: Dr. Carole-Jean Wu & Dr. Sarma Vrudhula
#**************************************************************************************#

#**************************************************************************************#
#**************************************************************************************#
#								BROKEN - Cannot animate basemap
#**************************************************************************************#
#**************************************************************************************#

# STANDARD LIBRARIES
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import matplotlib.animation as animation
import numpy as np

# MY FILES
from data_calc import *
from list_conversions import *
#from map_data import map_points
import variables

variables.init()
#**************************************************************************************#
#								Functions											   #
#**************************************************************************************#

def update_data():
	feed_data = pd.read_json('https://io.adafruit.com/api/v2/specialKody/feeds/river-node-location-ph/data')
	feed_data['created_at'] =  pd.to_datetime(feed_data['created_at'], infer_datetime_format=True)
	#This removes the unused data columns
	feed_data.drop(feed_data.columns[[0,2,4,5,6,9,11]], axis=1, inplace=True)

	lat = feed_data['lat']
	lon = feed_data['lon']
	dist = calculated_distance(lat,lon)
	speedSeries = list_to_series(calculate_speeds(feed_data['created_at'], dist))

	variables.dataList 
	variables.dataList= [lat, lon, feed_data['ele'], feed_data['value'], feed_data['created_at'], speedSeries]
	print("pulling new data")
	# return variables.dataList

def map_update(dump):
	#Work in progress
	update_data()
	longitudes =(variables.dataList[1]).tolist()
	latitudes =(variables.dataList[0]).tolist()
	values = (pd.Series(variables.dataList[3])).tolist()
	for lon, lat, val in zip(longitudes, latitudes, values):
		print(lon)
		print(lat)
		x,y = map(-112, 33)
		clr=ph_color_code(val)
		test = map.plot(x, y, marker='o', color=mcolors.cnames[clr], markersize=5)
	return test

def map_points(longitudes, latitudes, values, real_time, high_contrast):
	#Comment block needs more parameter detail
	"""
		:param high_contrast: This specifies the color contrast of the map. 0=regular contrast, 1=heightened contrast
		
	Description:
		This maps all points (which can be imagined as a 3-tuple) from the longitudes, latitudes, and values list.
		The function builds the tuple by selecting a long, lat, and value from the same list row.
		It is VERY IMPORTANT that longitudes, latitudes, and value have the same length.
		High_Contrast determines it the map is drawn with realistic color or a uniform tan.
	"""
	fig=plt.figure("pH Map")
	map = Basemap(projection='merc', lat_0 = 34.049, lon_0 = -111.094, resolution = 'h', area_thresh = 0.1, llcrnrlon=-114.85, llcrnrlat=31.4, urcrnrlon=-108.93, urcrnrlat=37.15)

	map.drawcoastlines()
	map.drawcountries()
	map.drawstates()
	map.drawrivers()
	#Defining the legend
	navy_patch = mpatches.Patch(color=mcolors.cnames['navy'], label='12.6<pH<14')
	blue_patch = mpatches.Patch(color=mcolors.cnames['blue'], label='11.2<pH<12.6')
	db_patch = mpatches.Patch(color=mcolors.cnames['dodgerblue'], label='9.8<pH<11.2')
	aqua_patch = mpatches.Patch(color=mcolors.cnames['aqua'], label='8.4<pH<9.8')
	dg_patch= mpatches.Patch(color=mcolors.cnames['darkgreen'], label='7.0<pH<8.4')
	lg_patch = mpatches.Patch(color=mcolors.cnames['lawngreen'], label='5.6<pH<7.0')
	yellow_patch = mpatches.Patch(color=mcolors.cnames['yellow'], label='4.2<pH<4.2')
	orange_patch = mpatches.Patch(color=mcolors.cnames['orange'], label='2.8<pH<4.2')
	ir_patch = mpatches.Patch(color=mcolors.cnames['indianred'], label='1.4<pH<2.8')
	red_patch = mpatches.Patch(color=mcolors.cnames['red'], label='0.0<pH<1.4')
	plt.legend(handles=[navy_patch, blue_patch, db_patch, aqua_patch, dg_patch, lg_patch, yellow_patch, orange_patch, ir_patch, red_patch],loc=2,bbox_to_anchor=(1,1), title='pH Color Codes')
	
	# Use fill continents with tan for high contrast
	if(high_contrast):
		map.fillcontinents(color = 'tan')
	else:
		map.bluemarble()
	map.drawmapboundary()
	
	if(real_time):
		for lon, lat, val in zip(longitudes, latitudes, values):
			x,y = map(lon, lat)
			clr=ph_color_code(val)
			test=map.plot(x, y, marker='o', color=mcolors.cnames[clr], markersize=5)
		ani = animation.FuncAnimation(fig, map_update, interval=10000, blit=False)
	else:
		for lon, lat, val in zip(longitudes, latitudes, values):
			x,y = map(lon, lat)
			clr=ph_color_code(val)
			test=map.plot(x, y, marker='o', color=mcolors.cnames[clr], markersize=5)

	#shows map
	plt.show()
	
def ph_color_code(value):
	"""
		:param value: This is a pH value which is having its color multiplexed.
		
	Description:
		This takes a pH value as input and returns a color to be used in the form of a string.
	"""
	if value > 12.6:
		return 'navy'
	elif value >11.2:
		return 'blue'
	elif value >9.8:
		return 'dodgerblue'
	elif value >8.4:
		return 'aqua'
	elif value >7.0:
		return 'darkgreen'
	elif value >5.6:
		return 'lawngreen'
	elif value >4.2:
		return 'yellow'
	elif value >2.8:
		return 'orange'
	elif value >1.4:
		return 'indianred'
	else:
		return 'red'

def map_ph(real_time, high_contrast):
	"""
		:param high_contrast: This specifies the color contrast of the map. 0=regular contrast, 1=heightened contrast
		
	Description:
		Maps the pH values on the Basemap map through the map_points function call.
	"""
	map_points((variables.dataList[1]).tolist(), (variables.dataList[0]).tolist(), (pd.Series(variables.dataList[3])).tolist(), real_time, high_contrast)

def elev_update(dump, line, ax, high_contrast):
#********************************needs commenting******************************************************#
	plt.cla()
	update_data()
	elevation = pd.Series(variables.dataList[2])
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
		elevation = pd.Series(variabls.variables.dataList[2])
		fig, ax = plt.subplots()
		fig.canvas.set_window_title("Node Elevation")
		ax.set_ylabel("Elevation (Meters)")
		ax.set_xlabel("Measurment")
		line = ax.plot(elevation)

		ani = animation.FuncAnimation(fig, elev_update, interval=1000, fargs=(line, ax, high_contrast), blit=True)
	else:
		plt.figure("Node Elevation")
		elevation = pd.Series(variables.dataList[2])
		if(high_contrast == 1):
			elevation.plot(linewidth=3.0)
		else:
			elevation.plot()
		plt.ylabel("Elevation (Meters)")
		plt.xlabel("Measurment")
	plt.show()
	
def ph_update(dump, line, ax, high_contrast):
#********************************needs commenting******************************************************#
	plt.cla()
	update_data()
	values = pd.Series(variables.dataList[3])
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
		values = pd.Series(variables.dataList[3])
		fig, ax = plt.subplots()
		fig.canvas.set_window_title("Node pH Recordings")
		ax.set_ylabel("PH")
		ax.set_xlabel("Measurment")
		line = ax.plot(values)

		ani = animation.FuncAnimation(fig, ph_update, interval=20000, fargs=(line, ax, high_contrast), blit=True)
	else:
		plt.figure("Node PH Recordings")
		values = pd.Series(variables.dataList[3])
		if(high_contrast == 1):
			values.plot(linewidth=3.0)
		else:
			values.plot()
		plt.ylabel("PH")
		plt.xlabel("Measurment")

	plt.show()
	
def speed_update(dump, line, ax, high_contrast):
#********************************needs commenting******************************************************#
	plt.cla()
	update_data()
	speed = variables.dataList[5]
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
		speed = variables.dataList[5]
		fig, ax = plt.subplots()
		fig.canvas.set_window_title("Node Speed")
		ax.set_ylabel("Speed (Meters/Second)")
		ax.set_xlabel("Measurment")
		line = ax.plot(speed)

		ani = animation.FuncAnimation(fig, speed_update, interval=20000, fargs=(line, ax, high_contrast), blit=True)
	else:
		plt.figure("Node Speed")
		speedSeries = variables.dataList[5]
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
	a = feed_data.to_string(buf=None, columns=None, col_space=None, header=True, index=True, na_rep='NaN', formatters=None, float_format=None, sparsify=None, index_names=True, justify=None, line_width=None, max_rows=None, max_cols=None, show_dimensions=False)
	f = open('json_data.txt', 'w')
	f.write(a)

#nr = no refresh (don't pull data)
def elev_update_nr(dump, line, ax, high_contrast):
#********************************needs commenting******************************************************#
	plt.cla()
	elevation = pd.Series(variables.dataList[2])
	if(high_contrast):
		line = ax.plot(elevation, linewidth=3.0)
	else:
		line = ax.plot(elevation)
	return line
	
#nr = no refresh (don't pull data)
def speed_update(dump, line, ax, high_contrast):
#********************************needs commenting******************************************************#
	plt.cla()
	update_data()
	speed = variables.dataList[5]
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
		elevation = pd.Series(variables.dataList[2])
		values = pd.Series(variables.dataList[3])
		speed = variables.dataList[5]
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
		values = pd.Series(variables.dataList[3])
		elevation = pd.Series(variables.dataList[2])
		speedSeries = variables.dataList[5]
		
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
		
#**************************************************************************************#
#								Script												   #
#**************************************************************************************#

# feed_data = pd.read_json('https://io.adafruit.com/api/v2/specialKody/feeds/river-node-location-ph/data')
# feed_data['created_at'] =  pd.to_datetime(feed_data['created_at'], infer_datetime_format=True)
#This removes the unused data columns
# feed_data.drop(feed_data.columns[[0,2,4,5,6,9,11]], axis=1, inplace=True)

#This should be called every 15 seconds (to pull data from Adafruit)
# update_data()