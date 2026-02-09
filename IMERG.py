import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap

# Load rain data
rootgrp = nc.Dataset('easia_rain.nc')

rain_tot = rootgrp.variables['rain'][:]  #(time 4,lat 250,lon 350)

rootgrp.close()

# Load TOPO data
rootgrp = nc.Dataset('easia_topo.nc')

topo = rootgrp.variables['topo'][:]  #(lat 250,lon 350)
file_lon = rootgrp.variables['lon'][:]
file_lat = rootgrp.variables['lat'][:]

rootgrp.close()



X, Y= np.meshgrid(file_lon,file_lat)


topo /= 9.8
topo = np.where(topo < 0, 0, topo)

fig, ax = plt.subplots(figsize=(8,6))

# 建立 Basemap：範圍改成 105–135E, 12–37N
m = Basemap(projection='cyl',
            llcrnrlon=105, urcrnrlon=135,
            llcrnrlat=12, urcrnrlat=37,
            resolution='l', ax=ax)

# 畫海岸線、國界、經緯線
m.drawcoastlines(linewidth=0.8)
m.drawcountries(linewidth=0.8)
m.drawparallels(np.arange(12, 38, 5), labels=[1,0,0,0])
m.drawmeridians(np.arange(105, 136, 5), labels=[0,0,0,1])

# 將經緯度轉為地圖座標
x, y = m(X, Y)



CS = m.contourf(x,y,topo, levels=np.arange(0, 2600, 200),cmap='Greys', extend = 'max', alpha=0.6)
cbar = plt.colorbar(CS, orientation = 'vertical')
cbar.set_label('TOPO [m]')

for i in range(4):
  rain_tot[i,:,:] = np.flipud(rain_tot[i,:,:])

C = m.contourf(x,y,rain_tot[0,:,:], levels=[1,2,5,10,15,20,30,50,100], cmap='RdYlBu_r', extend='max', alpha=0.8)
cbar = plt.colorbar(C, orientation = 'vertical')
cbar.set_label('rain [mm/d]')

plt.title('2004-06-17\nIMERG')
#plt.savefig('2004_JUN_rain.png', dpi=300)

plt.show()


