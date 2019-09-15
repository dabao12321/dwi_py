import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

data = pd.read_json('driving.json', lines = True)

idx = data.loc[:, "name"] == "latitude"
t1 = data.loc[:, "timestamp"][idx]
t1 = [60 * i.minute + i.second + 1e-6 * i.microsecond for i in t1]
t1 = [i - t1[0] for i in t1]
lat = data.loc[:, "value"][idx]

idx = data.loc[:, "name"] == "longitude"
t2 = data.loc[:, "timestamp"][idx]
t2 = [60 * i.minute + i.second + 1e-6 * i.microsecond for i in t2]
t2 = [i - t2[0] for i in t2]
lon = data.loc[:, "value"][idx]

lat = np.asarray(lat)
lon = np.asarray(lon)

x = (lon * 51 + 4245) * 5280 + 1200
y = (lat * 69 - 2918) * 5280 - 600

plt.plot(x, y, color = '#0000FF')
plt.margins(0.1, 0.1)
plt.xlabel("$x$ (ft)")
plt.ylabel("$y$ (ft)")
plt.title("location")

#np.savetxt('latlon.csv', np.stack((lat, lon), 1), delimiter = ',', newline = '\n')