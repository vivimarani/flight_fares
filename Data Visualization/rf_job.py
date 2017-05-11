import psycopg2
import yaml
from os.path import expanduser
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor


def main():
	creds = yaml.load(open(expanduser('../qpx_express_cred.yml')))
	df = _get_data(creds)
	create_error_plot(df, 100, 5)
	print("Plot Creation Completed.")


def create_error_plot(df, max_trees, incr):
	''' for RF Regressor, oob_scores is R^2 '''

	models, oob_scores, test_errors = build_amazon(df, max_trees, incr)

	fig = plt.figure(num=1, figsize=(10, 10))
	ax = fig.add_subplot(111)

	ax.set_xlim([0, max(models.keys())*1.1])
	ax.set_ylim([min(test_errors.values())*0.9, max(test_errors.values())*1.1])
	ax.set_xlabel("Number of Trees")
	ax.set_ylabel("Test MSE")

	x1 = np.array(list(models.keys()))
	y1 = np.array([test_errors[k] for k in x1])
	idx = np.argsort(x1)
	x1 = x1[idx]
	y1 = y1[idx]

	ax.plot(x1, y1)

	fig.savefig("../rf_plots.jpg")


def build_amazon(df, max_trees, incr):

	iterator = [incr*i for i in range(1, int(max_trees/incr))]

	X, y = _transform(df)

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)
	oob_scores, models, test_errors = {}, {}, {}

	for n_trees in iterator:
		models[n_trees] = _spawn_one_forest(X_train, y_train, n_trees)
		oob_scores[n_trees] = models[n_trees].oob_score_
		mse = mean_squared_error(y_test, models[n_trees].predict(X_test))
		test_errors[n_trees] = mse

	return models, oob_scores, test_errors


def _spawn_one_forest(X, y, n_trees):

	model = RandomForestRegressor(n_estimators=n_trees,
		oob_score=True, random_state=1)

	model.fit(X, y)

	return model


def _transform(df):
	y = df.pop('price').apply(lambda x: float(x[1:].replace(",","")))
	X = df['duration']

	for col in ['origin_aircraft', 'dest_aircraft', 'origin_carrier', 'dest_carrier']:
		dums = pd.get_dummies(df[col])
		X = pd.concat([X, dums], axis=1)

	return X, y


def _get_data(creds):

	query = '''SELECT * FROM trips'''
	_, cur = _connect_DB(creds)

	cur.execute(query)

	columns = [x[0] for x in cur.description]
	data = np.array([row for row in cur])
	df = pd.DataFrame(data=data, columns=columns)

	return df


def _connect_DB(credentials):

	try:
		conn = psycopg2.connect(**credentials['rds'])
		cur = conn.cursor()
		print("Connection Established")
	except:
		print("Error Establishing Connection")
		return None, None

	return conn, cur
