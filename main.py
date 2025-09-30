from PIL import Image
import exifread
from pathlib import Path

#convert GPS coordinates to decimal
def convert_to_degrees(value):
    # Extract degrees, minutes, and seconds from the EXIF GPS tags
    d = float(value.values[0])  # Degrees
    m = float(value.values[1])  # Minutes
    s = float(value.values[2])  # Seconds

    # Calculate the decimal degrees
    return d + (m / 60.0) + (s / 3600.0)

# function to extract EXIF metadata from an image
def get_exif_metadata(image_path):
    #open image in binary mode
    with open(image_path, 'rb') as img_file: #rb = open it in binarry mode 
        tags = exifread.process_file(img_file)
        
        # extract GPS information if available
        # print("\n[GPS Information]")
        gps_latitude = tags.get("GPS GPSLatitude")
        gps_latitude_ref = tags.get("GPS GPSLatitudeRef")
        gps_longitude = tags.get("GPS GPSLongitude")
        gps_longitude_ref = tags.get("GPS GPSLongitudeRef")

        #check if the GPS information is available and convert to decimal
        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = convert_to_degrees(gps_latitude)
            lon = convert_to_degrees(gps_longitude)

            #adjust the latitude and longitude based on the reference values
            if gps_latitude_ref.values[0] != 'N':
                lat = -lat
            if gps_longitude_ref.values[0] != 'E':
                lon = -lon
            
            #print the GPS coordinates in decimal format
            print(f"Latitude: {lat:.6f}°")
            print(f"Longitude: {lon:.6f}°")
        else:
            print("No GPS data available.")

if __name__ == "__main__":

    pictures = ["monster.JPEG", "park.JPEG"]
    pictures_folder = Path("pictures")

    for i in pictures: 
        print(f"Picture ({i}): \n")
        get_exif_metadata(pictures_folder/i)
        print("")
        print("")
        