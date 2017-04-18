#**************************************************************************************#
# Project: River Node
# Authors: Kody Stribrny
# Department: CIDSE
# Semester: Fall 2016/Spring 2017
# Course Number and Name: CSE 492/493 Honors Thesis
# Supervisors: Dr. Sarma Vrudhula & Dr. Carole-Jean Wu
#**************************************************************************************#

#STANDARD LIBRARIES
import pandas

#**************************************************************************************#
#								Functions											   #
#**************************************************************************************#

def list_to_series(list):
	"""
		:param list: A list of values
		
	Description:
		This function takes a generic list of values and converts to
		a Pandas series with the iterator as the index.
	"""
	dict={}
	for i in range(0, len(list)):
		dict[i] = list[i]
	return pandas.Series(dict)
	