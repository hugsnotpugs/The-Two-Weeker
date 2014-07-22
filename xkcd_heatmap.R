setwd("~/Dropbox/The Two Weeker/Datasets")
library(rMaps)
xkcd = read.csv('Rmaps Input - XKCD by hour v2.csv')
xkcd$iso3 = as.character(xkcd$iso3)
xkcd$log_count = as.numeric(as.character(xkcd$log_count))
xkcd$log_count = jitter(xkcd$log_count, factor = 0.01)
xkcd$count = as.numeric(as.character(xkcd$count))
xkcd$count = jitter(xkcd$count, factor = 0.01)

map = ichoropleth(count ~ iso3, data = xkcd, ncuts = 9, pal = 'YlOrRd',
                 animate = 'eastern_hour', map ='world')

map$set(
  geographyConfig = list(
    popupTemplate="#!function(geo, data) {
    if ( !data ) return;
    return '<div class=\"hoverinfo\"><strong>' +
    geo.properties.name + '<br>' + 'Total Tweets (all hrs): ' +
    data.hover_count +
    '</strong></div>';}!#"),
    fills = list(
    defaultFill = "gray"),
  scope = 'world',
  projection =  'mercator',
  height = 550,
  labels = FALSE,
  legend = FALSE)

map
