import shapefile
from shapely.geometry import Point # Point class
from shapely.geometry import shape # shape() is a function to convert geo objects through the interface

from pyproj import Proj, transform

def load_roads(filename):
    myshp = open(filename+".shp", "rb")
    mydbf = open(filename+".dbf", "rb")
    r = shapefile.Reader(shp=myshp, dbf=mydbf)
    return r

    #will need to load in gml

def in_polygon(lat, lon, shp, transform=False):
    all_shapes = shp.shapes() # get all the polygons
    all_records = shp.records()

    if transform:
        inProj = Proj(init='epsg:3857')
        outProj = Proj(init='epsg:4326')
        x1,y1 = lat,lon
        pt = (transform(inProj,outProj,x1,y1))
    else:
        pt = (lat,lon)

    val = False
    for i in range(len(all_shapes)):
        boundary = all_shapes[i] # get a boundary polygon
        if Point(pt).within(shape(boundary)): # make a point and see if it's in the polygon
           name = all_records[i][2] # get the second field of the corresponding record
           # print("The point is in", name)
           val = True
    return val

if __name__ == "__main__":
    myfile = load_roads("testroads")
    print(myfile)

    poly = load_roads("polytest")
    print(in_polygon(-71.0935, 42.3593, poly))


    in_polygon
