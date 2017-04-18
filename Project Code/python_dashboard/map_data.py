#**************************************************************************************#
# Project: River Node
# Authors: Kody Stribrny
# Department: CIDSE
# Semester: Fall 2016/Spring 2017
# Course Number and Name: CSE 492/493 Honors Thesis
# Supervisors: Dr. Sarma Vrudhula & Dr. Carole-Jean Wu
#**************************************************************************************#

# STANDARD LIBRARIES
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import numpy as np

#**************************************************************************************#
#								Functions											   #
#**************************************************************************************#

def map_points(longitudes, latitudes, values, high_contrast):
	"""
		:param high_contrast: This specifies the color contrast of the map. 0=regular contrast, 1=heightened contrast
		
	Description:
		This maps all points (which can be imagined as a 3-tuple) from the longitudes, latitudes, and values list.
		The function builds the tuple by selecting a long, lat, and value from the same list row.
		It is VERY IMPORTANT that longitudes, latitudes, and value have the same length.
		High_Contrast determines it the map is drawn with realistic color or a uniform tan.
	"""
	map = Basemap(projection='merc', resolution = 'h', area_thresh = 0.01, llcrnrlon=-114.85, llcrnrlat=31.4, urcrnrlon=-108.93, urcrnrlat=37.15)
	cmap1 = mcolors.LinearSegmentedColormap.from_list("my_colormap", ((0, 0, 0), (1, 1, 1)), N=14)

	plt.figure("pH Map")
	map.drawcoastlines()
	map.drawcountries()
	map.drawstates()
	map.drawrivers()
	# Use fill continents with tan for high contrast
	if(high_contrast):
		map.fillcontinents(color = 'tan')
	else:
		map.bluemarble()
	map.drawmapboundary()

	for lon, lat, val in zip(longitudes, latitudes, values):
		x,y = map(lon, lat)
		clr=ph_color_code(val)
		test=map.plot(x, y, marker='o', color=mcolors.cnames[clr], markersize=5)
		
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
