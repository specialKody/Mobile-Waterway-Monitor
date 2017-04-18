#**************************************************************************************#
# Project: River Node
# Authors: Kody Stribrny
# Department: CIDSE
# Semester: Fall 2016/Spring 2017
# Course Number and Name: CSE 492/493 Honors Thesis
# Supervisors: Dr. Sarma Vrudhula & Dr. Carole-Jean Wu
#**************************************************************************************#

# STANDARD LIBRARIES
import math

#**************************************************************************************#
#								Functions											   #
#**************************************************************************************#

def haversine_distance(lat1, lat2, long1, long2):
	"""
		:param lat1: Point 1's latitude
		:param lat2: Point 2's latitude
		:param long1: Point 1's longitude
		:param long2: Point 2's longitude
		
	Description:
		The function returns the haversine (big circle) distances from the two points on earth. Does not take into account elevation change.
	"""
	radius = 6371000				#Radius of the earth (meters)
	lat1r = math.radians(lat1)
	lat2r = math.radians(lat2)
	long1r = math.radians(long1)
	long2r = math.radians(long2)
	deltaLat = lat2r-lat1r
	deltaLong = long2r - long1r
	
	a = (math.sin(deltaLat/2)*math.sin(deltaLat/2)) + math.cos(lat1r)*math.cos(lat2r)*(math.sin(deltaLong)*math.sin(deltaLong))
	c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
	return radius*c

def calculated_distance(latitudes, longitudes):
	"""
		:param latitudes: A list of latitudes (floating point format)
		:param longitudes: A list of longitudes (floating point format)
		
	Description:
		This function calls the haversine_distance function for each pair of points. Each pair is i, i+1 in the list.
		Returns distances which is a listing of haversine distances. This has length of len(latitudes)-1
		Input parameters longitudes and latitudes must have the same number of elements.
	"""
	i = 0
	distances =[]
	for i in range(0, len(latitudes)-1):
		distances.append(haversine_distance(latitudes[i], latitudes[i+1], longitudes[i], longitudes[i+1]))
	return distances

def elevation_change(elevation):
	"""
		:param elevation: A list of elevation points (floating point format)
		
	Description:
		Calculates and returns the differences in elevation between two points. This is completed for all sequential pairs in a list.
		Returns deltaElev which is a listing of elevation changes. This has a length of len(elevation) -1
	"""
	deltaElev =[]
	for i in range (0, len(elevation)-1):
		deltaElev.append((elevation[i+1]-elevation[i]))
	return deltaElev
	
def calculate_speeds(times, distances):
	"""
		:param times: A list of datetime objects which corresponds to the timestamps on transmissions
		:param distances: A list of calculated distances. Each I distance corresponds to location difference between I and I+1
		
	Description:
		Takes a list of times and distances and returns the speed in KPH for the river node.	
	"""
	speeds=[]
	for i in range (0, len(distances)-1):
		deltaTime = times[i] - times[i+1]						#calculate time difference here
		calc_speed = distances[i]/(deltaTime.total_seconds())	#Right now returns the speed in meters per second
		if(calc_speed >10.0):									#Added if check to remove speeds >10m/s.
			speeds.append(0)
		else:
			speeds.append(calc_speed)
	return speeds
		