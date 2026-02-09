import numpy              as np
import netCDF4            as nc
from   concurrent.futures import ProcessPoolExecutor
# ==================================================

rootgrp = nc.Dataset("/home/teachers/fortran_ta/data/LSM2025/ECMWF_ERA5_EAsia/era5_EAsia_surface_geopotential_0p1deg.nc")

lat  = rootgrp.variables['latitude' ][...]
lon  = rootgrp.variables['longitude' ][...]

lon_min, lon_max = 105, 140
lat_min, lat_max = 12, 37

#loc  = [120.81324, 23.50821] # [lon, lat]
x1 = np.abs(lon - lon_min).argmin()
x2 = np.abs(lon - lon_max).argmin()
y1 = np.abs(lat - lat_min).argmin()
y2 = np.abs(lat - lat_max).argmin()

if y1 > y2: y1, y2 = y2, y1
if x1 > x2: x1, x2 = x2, x1

TOPO = rootgrp.variables['z'][0,y1:y2,x1:x2]

rootgrp.close()






fw = nc.Dataset('easia_topo.nc', 'w', format = 'NETCDF4')

fw . createDimension('lon' , 350)
fw . createDimension('lat' , 250)
fw . createDimension('topo', 2  )

fw . createVariable('topo', np.float32  , ('lat', 'lon'))
fw . createVariable('lat' , np.float32  , ('lat'))
fw . createVariable('lon' , np.float32  , ('lon'))

rootgrp = nc.Dataset("/home/teachers/fortran_ta/data/LSM2025/ECMWF_ERA5_EAsia/era5_EAsia_surface_geopotential_0p1deg.nc")


fw . variables['topo'][:] = TOPO
fw . variables['lat'][:]  = lat
fw . variables['lon'][:]  = lon

rootgrp.close()
fw.close()
