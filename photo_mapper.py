# Author : Angus Emmett
import gmplot
import os
import sys
from photoData import PhotoData

class PhotoMapper:

	def __init__(self, API_dir):
		self.API_KEY = self.open_API_key(API_dir)


	def open_API_key(self, API_dir):
		f = open(API_dir,"r")
		key = f.readline()
		f.close()
		return key


	#returns sorted list of all photos objects in directory
	#order is first to last
	def get_photos(self, directory):
		photos = []

		#Looping through all files in Dir
		for filename in os.listdir(directory):
			if filename.endswith(".JPG") or filename.endswith(".jpeg"):
				path = os.path.join(directory, filename)

				#Creating Photos object
				temp = PhotoData(path)
				if temp.has_GPS:
					photos.append(temp)

		photos.sort()
		return photos


	def plot(self, photos, output_file_name = "output"):


		latitude_list = [x.GPS[0] for x in photos]
		longitude_list = [x.GPS[1] for x in photos]

		gmap = gmplot.GoogleMapPlotter(latitude_list[0], longitude_list[0], 13,
										apikey = self.API_KEY)

		gmap.apikey = self.API_KEY

		# scatter method of map object
		# scatter points on the google map
		gmap.scatter( latitude_list, longitude_list, '# FF0000',
									size = 40, marker = False )

		# Plot method Draw a line in
		# between given coordinates
		gmap.plot(latitude_list, longitude_list,
				'cornflowerblue', edge_width = 2.5)

		gmap.draw( f"{output_file_name}.html" )