from geopy import geocoders
import time

class SingleQuery():
    
    def __init__(self, location_string=''):
        self.location = location_string
    
    def get_coord(self):
        
        gn = geocoders.GoogleV3()
        try:
            test_result = gn.geocode(self.location)
            if test_result is not None:
                place, (lat, lng) = test_result
                result = ('{}, {}'.format(lat, lng)).split(',')
        except ValueError:
            result = None
            
        for i in range(len(result)):
            result[i] = float(result[i])
        
        return (result[0], result[1]) # result[0] is latitude, result[1] is longitude
        
class MultiQuery():
    
    def __init__(self, location_array=[]):
        self.location_array = location_array
    
    def get_coord(self):
        
        coord_list = []
        match = []
        gn = geocoders.GoogleV3()
        
        for i in self.location_array:
            try:
                test_geo = gn.geocode(i)
                if test_geo is not None:
                    place, (lat, lng) = test_geo
                    match = '{}, {}'.format(lat, lng).split(',')
                    for i in match:
                        i = float(i)
                        coord_list.append(i)
                        #print coord_list[-1]
                else:
                    match = None
                    coord_list.append(None), coord_list.append(None)
                    #print coord_list[-1]
                    
            except ValueError:
                match = None
                coord_list.append(None), coord_list.append(None)
                time.sleep(5)
            except gn.timeout:
                match = None
                coord_list.append(None), coord_list.append(None)
                time.sleep(5)
            
            time.sleep(1.5)
                
        return coord_list
