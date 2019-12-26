from flask import Flask, render_template, redirect, request, url_for, jsonify
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.neighbors import KNeighborsClassifier
from collections import Counter
from sklearn.metrics import accuracy_score
import pickle
import json
import glob
import csv
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def home() :
	return render_template('ks_signin.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		data = dict(request.get_json())

		print(data)

		new_X = data['data']
		id = data['id']
		pwd = data['pwd']

		f = open('idpwd/idpwd','rb')
		content = pickle.load(f)
		if id in content.keys():
			if pwd == content[id]:
				name = glob.glob('user/*.csv')
				print(name)
				X = []
				y = []
				count = 0
				feature_length = 30
				for i in name:
					count = 0
					with open(i, newline='') as csvfile:
						reader = csv.reader(csvfile)
						for j in reader :
							if count < feature_length :
								while '' in j :
									j.pop()
								for k in range(len(j)) :
									j[k] = float(j[k])
								j = np.array(j)
								X.append(j)
								for k in range(len(name)) :
									if i == name[k] :
										y.append(k+1)
							count += 1
				new_X = new_X[0]
				for i in range(len(new_X)):
					new_X[i] = float(new_X[i])

				new_X = np.array(new_X)

				X.append(new_X)
				y.append(-1)

				X = MultiLabelBinarizer().fit_transform(X)
				X = np.array(X)

				vote = []
				predict_label = []
				true_label = []
				predict_name = 'user/' + id + '_' + pwd + '.csv'
				for k in range(1,50):
					clf = KNeighborsClassifier(n_neighbors=k)
					clf.fit(X,y)
					predict = clf.predict([X[-1]])
					predict_label.append(int(predict))
					true_label.append(name.index(predict_name) + 1)
					vote.append(predict[0])
				print(vote)
				vote = Counter(vote)
				vote = vote.most_common()
				value, count = vote[0]
				print('[{}] - {}'.format(value, count))

				accuracy = accuracy_score(true_label, predict_label)
				print('[+] Accuracy - {}'.format(accuracy))

				#predict_name = 'user/' + id + '_' + pwd + '.csv'
				if value == name.index(predict_name)+1:
					print(value)
					msg = "Succeeded!!</br> Accuracy : <span class='text-danger'>{:.2f}</span>%".format(accuracy*100)
					return jsonify({'bool' : 'true', 'accuracy' : accuracy , 'msg' : msg})
				else:
					print(value)
					attacker = name[value-1]
					attacker = attacker.replace('user/', '')
					attacker = attacker.split('_')[0]
					msg = "Failed</br> You're <span class='text-danger'>'{}'</span> ! </br>Aren't you?</br> Accuray : <span class='text-danger'>{:.2f}</span>%".format(attacker, 100.0 - accuracy)
					return jsonify({'bool' : 'false', 'msg' : msg})
			else: # 비밀번호 틀림
				return jsonify({'bool':'wrong','msg':'ID/Password is wrong!'})
		else: # id pwd 틀림
			return jsonify({'bool':'wrong','msg':'ID password does not exist!'})
		return '',204

@app.route('/signup')
def signup():
	return render_template('ks_signup.html')

@app.route('/check', methods = ['POST'])
def check():
	if request.method == 'POST':
		data = dict(request.get_json())

		f = open('idpwd/idpwd','rb')
		content=pickle.load(f)
		for key in content.keys():
			if data['data'] == key:
				is_idpwd = 'false'
			else:
				is_idpwd = 'true'
		f.close()

		return jsonify({'bool':is_idpwd})

@app.route('/get_data', methods = ['GET', 'POST'])
def get_data():
	if request.method == 'POST':
		r_data = dict(request.get_json())
		print(r_data['data'])
		data = r_data['data']
		id  = r_data['id']
		pwd = r_data['pwd']

		csv_path = 'user/' + id + '_' + pwd + '.csv'
		dataframe = pd.DataFrame(data)
		dataframe.to_csv(csv_path, header=False, index=False)

		# writing id pwd to file
		if os.path.isfile('idpwd/idpwd'):
			f=open('idpwd/idpwd', 'rb')
			content=pickle.load(f)
			content[id] = pwd
			f.close()
			print(content)
			edit_f=open('idpwd/idpwd', 'wb')
			pickle.dump(content,edit_f)
			edit_f.close()
		else:
			D = {}
			f = open('idpwd/idpwd', 'wb')
			pickle.dump(D, f)
			f.close()
		# feature hashing

		print('[+] feature hashing completed..')


		return '',204
	return '',204

if __name__ == '__main__':
	app.run(host='www.nichijou.kr', debug=True, port=5073)

