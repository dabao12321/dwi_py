import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

data = pd.read_json('driving.json', lines = True)

idx = data.loc[:, "name"] == "steering_wheel_angle"
t = data.loc[:, "timestamp"][idx]
t = [60 * i.minute + i.second + 1e-6 * i.microsecond for i in t]
t = [i - t[0] for i in t]
x = data.loc[:, "value"][idx]

t = t[1300:1480]
x = x[1300:1480]

plt.plot(t, x, color = '#0000FF')
plt.margins(0, 0.1)
plt.xlabel("$t$")
plt.ylabel("$x$")
plt.title("steering wheel angle")

#np.savetxt('latlon.csv', np.stack((lat, lon), 1), delimiter = ',', newline = '\n')
