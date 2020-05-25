#GPS GPSLatitude
#GPS GPSLongitude
import gmplot
import os
import sys
from photoData import PhotoData

f = open("api_key.txt","r")
API_KEY = f.readline()
f.close()


#returns sorted list of all photos objects in directory
#order is first to last
def get_photos(directory):
	photos = []
	directory = "RoadTrip2"

	i = 1
	#Looping through all files in Dir
	for filename in os.listdir(directory):
		if filename.endswith(".JPG") or filename.endswith(".jpeg"):
			path = os.path.join(directory, filename)

			#Creating Photos object
			temp = PhotoData(path)
			if temp.has_GPS:
				photos.append(temp)

			print(i)
			i += 1


	photos.sort()
	return photos


def plot(photos):

	latitude_list = []
	longitude_list = []

	for p in photos:
		latitude_list.append(p.GPS[0])
		longitude_list.append(p.GPS[1])

	gmap = gmplot.GoogleMapPlotter(latitude_list[0], longitude_list[0], 13,
									apikey = API_KEY)

	gmap.apikey = API_KEY

	# scatter method of map object
	# scatter points on the google map
	gmap.scatter( latitude_list, longitude_list, '# FF0000',
								  size = 40, marker = False )

	# Plot method Draw a line in
	# between given coordinates
	gmap.plot(latitude_list, longitude_list,
			   'cornflowerblue', edge_width = 2.5)

	gmap.draw( "testmap.html" )


if __name__ == "__main__":
	photos = get_photos("RoadTrip2")
	plot(photos)
