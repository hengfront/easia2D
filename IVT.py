import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap

# 建立 Basemap 對象 (東亞區域)
m = Basemap(projection='cyl', llcrnrlon=100, urcrnrlon=140,
            llcrnrlat=10, urcrnrlat=40, resolution='l')


def load_monthly_data(filename):
    with nc.Dataset(filename) as ds:
        return {
            'zp': ds.variables['zp'][:],   # (lev, lat, lon)   
            'qv': ds.variables['qv'][:],   # (27,  100, 140)
            'u': ds.variables['u'][:],     # (11 = 500hPa,  15 = 700hPa, 20 = 850hPa)
            'v': ds.variables['v'][:],     # (11 = 500h Pa,  15 = 700hPa, 20 = 850hPa)
            'lon': ds.variables['lon'][:],
            'lat': ds.variables['lat'][:]
        }

months = ['jun', 'jul', 'aug', 'sep']
data_list = [load_monthly_data(f'easia_prs_{month}.nc') for month in months]

zp_tot = np.stack([d['zp'] for d in data_list])
qv_tot = np.stack([d['qv'] for d in data_list])
u_tot = np.stack([d['u'] for d in data_list])
v_tot = np.stack([d['v'] for d in data_list])
lon, lat  = data_list[0]['lon'], data_list[0]['lat']


g = 9.8

dz = np.abs(zp_tot[:, 15:26, :, :] - zp_tot[:, 14:25, :, :])  # (4, 11, 100, 140)

IVT = np.zeros((4,100,140))
IVTx = np.zeros((4,100,140))
IVTy = np.zeros((4,100,140))


def integrand(u,v,qv,z1,z2):
    ivtx = qv * u * np.abs(z2 - z1)
    ivty = qv * v * np.abs(z2 - z1)
    return ivtx, ivty

for i in range(4):
    # integrate from 700hPa
    for j in range(15,26):
        IVTx[i,:,:] += 1/g * integrand(u_tot[i,j,:,:], v_tot[i,j,:,:], qv_tot[i,j,:,:], zp_tot[i,j-1,:,:], zp_tot[i,j,:,:])[0]
        IVTy[i,:,:] += 1/g * integrand(u_tot[i,j,:,:], v_tot[i,j,:,:], qv_tot[i,j,:,:], zp_tot[i,j-1,:,:], zp_tot[i,j,:,:])[1]

IVT = np.sqrt(IVTx**2 + IVTy**2)


X, Y= np.meshgrid(file_lon,file_lat)



# Plot

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

# 畫 IVT 填色圖
CS = m.contourf(x, y, IVT[3,:,:],
                levels=np.linspace(0, 1000, 11),
                cmap='Blues', extend='max')

# 抽稀風場箭頭
step = 5
m.quiver(x[::step, ::step], y[::step, ::step],
         u_tot[3,20,::step,::step], v_tot[3,20,::step,::step],
         width=0.002, scale=300)

# 畫出Z500的等高線 (例: 5880m)
m.contour(x, y, zp_tot[3,11,:,:] / g,
          levels=[5880], colors='r', linewidths=2)

# 顏色條
cbar = plt.colorbar(CS, orientation='vertical', pad=0.02)
cbar.set_label('IVT (kg/m/s)')

plt.title('2004-09-17\nERA5 / low-level IVT [kg/m/s] / Z500 [5880m]')
#plt.savefig('2004_SEP.png', dpi=300)
plt.show()




