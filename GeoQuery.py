''' Uses geocoders.GoogleV3 to query lat/lon coordinates based on string inputs
    SingleQuery class queries a single location, while MultiQuery queries an array of locations
    Note: GoogleV3 only allows 1 query per 1.5 seconds. Occasionally queries will time out or fail '''

from geopy import geocoders
import time

class SingleQuery():
    
    def __init__(self, location_string=''):
        self.location = location_string
    
    def coords(self):
        
        gn = geocoders.GoogleV3()
        try:
            test_geo = gn.geocode(self.location)
            if test_geo is not None:
                place, (lat, lng) = test_geo
                match = ('{}, {}'.format(lat, lng)).split(',')
        except ValueError:
            match = None
            
        for i in range(len(match)):
            match[i] = float(match[i])
        
        return (match[0], match[1]) # match[0] is latitude, match[1] is longitude
        
class MultiQuery():
    
    def __init__(self, location_array=[]):
        self.location_array = location_array
    
    def coords(self):
        
        lats = []
        lons = []
        gn = geocoders.GoogleV3()
        
        for i in self.location_array:
            try:
                test_geo = gn.geocode(i)
                if test_geo is not None:
                    place, (lat, lng) = test_geo
                    match = '{}, {}'.format(lat, lng).split(',')
                    for j in range(len(match)):
                        match[j] = float(match[j])
                    lats.append(match[0])
                    lons.append(match[1])
                else:
                    match = None
                    lats.append(None), lons.append(None)
                                        
            except ValueError:
                match = None, lats.append(None), lons.append(None)
                time.sleep(5)
            except gn.timeout:
                match = None, lats.append(None), lons.append(None)
                time.sleep(5)
            time.sleep(1.5)
                
        return {'lats': lats, 'lons': lons}
        
        
