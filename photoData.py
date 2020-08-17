#Author : Angus Emmett
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


class PhotoData():
    '''Class that takes the path of the image and strips
    the GPS and time data for the photos'''

    def __init__(self, path):
        self.path = path
        self.data = self.get_exif(path)
        self.has_GPS = False

        if 'GPSInfo' in self.data.keys() and "DateTimeDigitized" in self.data.keys():
            self.GPS = self.get_decimal_coordinates(self.data["GPSInfo"]) #[0] = Latitude [1]=Longitude
            self.datetime = self.convert_to_datetime(self.data["DateTimeDigitized"])
            self.has_GPS = True

            if self.GPS == None:
                self.has_GPS = False


    def convert_to_datetime(self, time_str):
        return datetime.strptime(str(time_str), "%Y:%m:%d %H:%M:%S")

    def get_exif(self,filename):
        exif = Image.open(filename)._getexif()
        out_dict = {}
        if exif is not None:
            readable_exif = {}
            for key, value in exif.items():
                name = TAGS.get(key, key)
                readable_exif[name] = exif[key]
            
            if 'GPSInfo' in readable_exif and 'DateTimeDigitized' in readable_exif:
                out_dict = {"DateTimeDigitized":readable_exif['DateTimeDigitized'], "GPSInfo":{}}
                for key in readable_exif['GPSInfo'].keys():
                    name = GPSTAGS.get(key,key)
                    out_dict['GPSInfo'][name] = readable_exif['GPSInfo'][key]

        return out_dict

    def get_decimal_coordinates(self,info):

        for key in ['Latitude', 'Longitude']:
            if 'GPS'+key in info and 'GPS'+key+'Ref' in info:
                e = info['GPS'+key]
                ref = info['GPS'+key+'Ref']
                info[key] = ( e[0][0]/e[0][1] +
                              e[1][0]/e[1][1] / 60 +
                              e[2][0]/e[2][1] / 3600
                            ) * (-1 if ref in ['S','W'] else 1)

        if 'Latitude' in info and 'Longitude' in info:
            return [info['Latitude'], info['Longitude']]



    def __eq__(self, other):
        return self.datetime == other.datetime

    def __lt__(self, other):
        return self.datetime < other.datetime

    def __str__(self):
        return str(self.datetime)
