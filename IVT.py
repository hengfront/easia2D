import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import cartopy.crs as ccrs
import cartopy.feature as cfeature




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

# 700mb 以下的x,y方向ivt
ivtx = qv_tot[:, 15:26, :, :] * u_tot[:, 15:26, :, :] / g *dz
ivty = qv_tot[:, 15:26, :, :] * v_tot[:, 15:26, :, :] / g *dz

# axis = 1  => 在高度層方向加總
ivtx_sum = np.sum(ivtx, axis=1)
ivty_sum = np.sum(ivty, axis=1)
IVT = np.sqrt(ivtx_sum**2 + ivty_sum**2)



X, Y= np.meshgrid(lon,lat)



# Plot

def plot_ivt(month):
  fig = plt.figure(figsize=(10, 8))
  ax = plt.axes(projection=ccrs.PlateCarree())  # 使用 PlateCarree 投影
  ax.set_extent([105, 135, 12, 37], crs=ccrs.PlateCarree())  # 設定地圖範圍

# --- 3. 加入地圖特徵 ---
  ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
  ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.8)
  ax.add_feature(cfeature.OCEAN, facecolor='lightcyan')
  ax.add_feature(cfeature.LAND, facecolor='whitesmoke')

# 加入經緯度網格線
  gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.5)
  gl.top_labels = False
  gl.right_labels = False

# --- 4. 數據填色與向量場 ---
# 在 Cartopy 中繪圖必須指定 transform=ccrs.PlateCarree()
  clevs = np.linspace(0, 1000, 11)
  cf = ax.contourf(lon, lat, IVT[month-6,:,:], levels=clevs, cmap='Blues', 
                 extend='max', transform=ccrs.PlateCarree())

# 畫風場箭頭 (抽稀處理)
  step = 5
  ax.quiver(lon[::step], lat[::step], u_tot[month-6,20,::step,::step], v_tot[month-6,20,::step,::step],
          transform=ccrs.PlateCarree(), scale=300, width=0.002)



# --- 5. 圖表修飾 ---
  plt.colorbar(cf, orientation='vertical', pad=0.05, label='IVT (kg/m/s)')


  plt.title('2004-%02d-17\nERA5 / low-level IVT [kg/m/s] / Z500 [5880m]' % (month))
  #plt.savefig('2004_%02d_17.png' % (month), dpi=300)
  plt.show()

plot_ivt(6)  # 6月



