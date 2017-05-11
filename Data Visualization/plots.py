import yaml
from os.path import expanduser
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from rf_job import _get_data


def main():
	creds = yaml.load(open(expanduser('../qpx_express_cred.yml')))
	df = _get_data(creds)
	df['price'] = df['price'].apply(lambda x: float(x[1:].replace(",", "")))
	df['duration'] = df['duration'].astype(int)
	make_duration_vs_price(df)
	make_avg_plots(df)


def make_avg_plots(df):

	fig = plt.figure(num=1, figsize=(10, 10))
	ax = fig.add_subplot(111)

	airline = df['origin_carrier'].unique()
	price = df.groupby(by='origin_carrier')['price'].mean().reset_index()

	sns.stripplot(x='origin_carrier', y='price', data=df, jitter=True)

	fig.savefig("../plots/price_avg_airline.jpg")
	print("Finished price avg plot")
	plt.close()


def make_duration_vs_price(df):

	fig = plt.figure(num=1, figsize=(10, 10))
	ax = fig.add_subplot(111)

	duration = df['duration'].as_matrix()
	price = df['price'].as_matrix()

	ax.set_xlim([min(duration)*0.95, max(duration)*1.05])
	ax.set_ylim([min(price)*0.95, max(price)*1.05])
	ax.set_xlabel("Total Trip Duration")
	ax.set_ylabel("Roundtrip Price")

	x1 = duration
	y1 = price
	idx = np.argsort(x1)
	x1 = x1[idx]
	y1 = y1[idx]

	def c_maps(carrier):
		if carrier == "UA":
			return 'b'
		elif carrier == "CM":
			return 'g'
		elif carrier == "AM":
			return 'r'
		return 'y'

	c1 = df['origin_carrier'].apply(c_maps).as_matrix()[idx]
	print(df['origin_carrier'].unique())

	ax.scatter(x1, y1, c=c1)
	print("Finished Scatter plot")

	fig.savefig("../plots/dur_vs_price.jpg")
