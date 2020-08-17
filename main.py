from photo_mapper import PhotoMapper

API_KEY_FILE = 'photo_mapper/api_key.txt'
PHOTO_DIRECTORY = 'photo_mapper/RoadTrip2'
OUTPUT_FILE_NAME = 'output'


p = PhotoMapper(API_KEY_FILE)
photos = p.get_photos(PHOTO_DIRECTORY)
p.plot(photos, OUTPUT_FILE_NAME)