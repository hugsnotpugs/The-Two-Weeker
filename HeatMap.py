''' Create a world heatmap using Cartopy '''

import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.feature
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import math
    

# Class for a single cartopy heat map
class HeatMap:
    
    def __init__(self, width=15, height=15, projection=ccrs.Mercator(), cmap=mpl.cm.YlOrRd, stock_image=True, land=True, ocean=False, borders=False):
        self.width = width
        self.height = height
        self.projection = projection
        self.cmap = cmap
        self.stock_image = stock_image
        self.land = land
        self.ocean = ocean
        self.borders = borders
        
    def plot(self, countries, lats, lons, plot_nones=False, show_values=False):
            
        countries = list(countries.values)
        lats = list(lats.values)
        lons = list(lons.values)
        
        # Count the number of times a country is in the list
        unique_countries = set(countries)
        unique_countries = list(unique_countries)
        c_number = []
        for p in unique_countries:
            c_number.append(math.log(countries.count(p)))
            if show_values == True:
                print p, countries.count(p)

        maximo = max(c_number)

    # --- Build Map + Color Scheme ---
        cmap = self.cmap

    # --- Using the shapereader ---
        counter = 0
        shapename = 'admin_0_countries'
        countries_shp = shpreader.natural_earth(resolution='110m',
                                            category='cultural', name=shapename)
                                            
    # --- Plot shapes onto figure --- 
        fig, ax = plt.subplots()
        fig.set_size_inches(self.width, self.height)
        
        map = plt.axes(projection=self.projection)
        map.set_frame_on(False)
        if self.stock_image == True:
            map.stock_img()
        if self.land == True:
            map.add_feature(cartopy.feature.LAND)
        if self.ocean == True:
            map.add_feature(cartopy.feature.OCEAN)
        if self.borders == True:
            map.add_feature(cartopy.feature.BORDERS, edgecolor='lightgray')
        
        for country in shpreader.Reader(countries_shp).records():
            nome = country.attributes['name_long']       

            if nome in unique_countries:
                i = unique_countries.index(nome)
                numero = c_number[i]
                map.add_geometries(country.geometry, ccrs.PlateCarree(),
                              facecolor=cmap(numero / float(maximo), 1),
                              label=nome, alpha=1, linewidth=0)
                counter = counter + 1

            elif plot_nones == True:
                 map.add_geometries(country.geometry, ccrs.PlateCarree(),
                               facecolor='#FAFAFA',
                               label=nome)

        if counter != len(unique_countries):
            print "check country names!"
        
        plt.show()
