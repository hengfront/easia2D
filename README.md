IMERGE.py :
  從easia_topo.nc及easia_rain.nc中提取東亞地區的重力位高度及降雨分布，而easia_rain.nc中已將2004年的六到九月的17號的降雨訊號抓取下來
  再從檔案內的位置取東經105至140度跟北緯12至37度的位置並繪製出二維的雨量分布圖

IVT.py :
  從各個月份的easia_prs的nc檔中提取重力位高度、比濕、經向及緯向風速，並在與IMERG.py差不多相同的地理位置繪製出各網格點的風向風速、700hPa到1000hPa的垂直水氣傳送(IVT, vertiaclly integrated water vapor transport)、和500hPa的等高線
