import shapefile
from shapely.geometry import Point # Point class
from shapely.geometry import shape # shape() is a function to convert geo objects through the interface

from pyproj import Proj, transform

def load_roads(filename):
    myshp = open(filename+".shp", "rb")
    mydbf = open(filename+".dbf", "rb")
    r = shapefile.Reader(shp=myshp, dbf=mydbf)
    return r


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
           name = all_records[i]["name"] # get the second field of the corresponding record
           # print("The point is in", name)
           val = True
    return val

def outofwidth(points, shp):
    #point = [lat, long, time]
    mintime = points[0][2]
    maxtime = 0
    out = 0
    for point in points:
        if point[2] > maxtime:
            maxtime = point[2]
        if point[2] < mintime:
            mintime = point[2]
        if in_polygon(point[0], point[1], shp):
            out += 1
    period = maxtime - mintime
    return out/len(points), out/period




if __name__ == "__main__":
    myfile = load_roads("../data/testroads")
    print(myfile)
    for road in myfile:
        print(road.shape.points)

    poly = load_roads("../data/polytest")
    print(in_polygon(-71.0935, 42.3593, poly))


    in_polygon
