import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.animation as animation
from yahoo_fin.stock_info import get_live_price
import numpy as np
import sys
from time import sleep


# CONSTANTS
DATA_LIMIT = 80  # minimum of 80
CHART_REFRESH_TIME = 1500  # in milliseconds


def overwrite_print(message):
	sys.stdout.write("%s\r" % message)
	sys.stdout.flush()


class Ichimoku:
	def __init__(self, ticker):
		style.use("seaborn")
		self.ticker = ticker
		self.figure, self.ax = plt.subplots(1, 1)
		self.time = [i for i in range(-25, DATA_LIMIT + 27)]
		self.price = []
		self.tenkan_data = []
		self.kijun_data = []
		self.chikou_data = []
		self.senkou_A_data = []
		self.senkou_B_data = []

	def get_initial_data(self):
		for i in range(DATA_LIMIT):
			self.price.append(get_live_price(self.ticker))
			# time append
			progress = round(i*100/DATA_LIMIT, 1)
			overwrite_print(f'>>> Initialising data : {progress}%')

	def update(self, j):
		print(f">>> Working on update")
		self.ax.clear()
		# tenkan
		self.tenkan_data = []
		for i in range(DATA_LIMIT - 9):
			tenkan_src = self.price[i:i + 9]
			self.tenkan_data.append((max(tenkan_src) + min(tenkan_src)) / 2)

		# kijun
		self.kijun_data = []
		for i in range(DATA_LIMIT - 26):
			kijun_src = self.price[i:i + 26]
			self.kijun_data.append((max(kijun_src) + min(kijun_src)) / 2)

		# chikou
		self.chikou_data = self.price

		# senkou A
		self.senkou_A_data = [(self.tenkan_data[i + 17] + self.kijun_data[i]) / 2 for i in range(DATA_LIMIT - 26)]

		# senkou B
		self.senkou_B_data = []
		for i in range(DATA_LIMIT - 52):
			senkou_B_src = self.price[i:i + 52]
			self.senkou_B_data.append((max(senkou_B_src) + min(senkou_B_src)) / 2)

		# PLOT
		# Real time data plot
		x1 = self.time[26:26 + DATA_LIMIT]
		y1 = self.price
		self.ax.plot(np.array(x1), np.array(y1), label="LIVE", color='#000000', linewidth=0.7)

		# Tenkan plot
		x2 = self.time[35:35 + DATA_LIMIT - 9]
		y2 = self.tenkan_data
		self.ax.plot(np.array(x2), np.array(y2), label='TENKAN', linestyle='dashed', color='#E00F0F', linewidth=0.5)

		# Kijun plot
		x3 = self.time[52:52 + DATA_LIMIT - 26]
		y3 = self.kijun_data
		self.ax.plot(np.array(x3), np.array(y3), label="KIJUN", linestyle='dashed', color='#151ACE', linewidth=0.5)

		# Chikou plot
		x4 = self.time[:DATA_LIMIT]
		y4 = self.chikou_data
		self.ax.plot(np.array(x4), np.array(y4), label="CHIKOU", linestyle='dashed', color='orange', linewidth=0.3)

		# Senkou A plot
		x5 = self.time[78:78 + DATA_LIMIT - 26]
		y5 = self.senkou_A_data
		self.ax.plot(np.array(x5), np.array(y5), label='Senkou A', color='#39AF20', linewidth=0.5)

		# Senkou B plot
		x6 = self.time[104:104 + DATA_LIMIT - 52]
		y6 = self.senkou_B_data
		self.ax.plot(np.array(x6), np.array(y6), label='Senkou B', color='#AF208E', linewidth=0.5)

		# Fill KUMO CLOUD
		fill_area = np.array(x6)
		z5 = np.array(self.senkou_A_data[26:])
		z6 = np.array(self.senkou_B_data)
		self.ax.fill_between(fill_area, z5, z6, where= z5>=z6, color= 'green', alpha= 0.5)
		self.ax.fill_between(fill_area, z5, z6, where= z5<=z6, color= 'red', alpha= 0.5)

		plt.xlim(self.time[0] - 1, self.time[-1] + 10)
		plt.xlabel('x - axis')
		plt.ylabel('y - axis')
		plt.title(f'ICHIMOKU - {self.ticker}')
		plt.legend()

		# data update
		new_price = get_live_price(self.ticker)
		time = 0  # edit here
		self.time.append(self.time[-1] + 1)
		self.price.append(new_price)
		self.time.__delitem__(0)
		self.price.__delitem__(0)
		print("\tStatus : Success")


if __name__ == "__main__":
	num = 0
	ich = Ichimoku('GAYAHWS.NS')  # set stock ticker here
	ich.get_initial_data()
	print("")
	anim = animation.FuncAnimation(ich.figure, ich.update, interval=CHART_REFRESH_TIME)
	plt.show()
