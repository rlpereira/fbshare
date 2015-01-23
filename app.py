#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et
import os, random, requests, json
from flask import Flask, request, Response, send_file, render_template

app = Flask(__name__)

@app.route('/share_img/<cityid>.png', methods=['GET'])
def share_img(cityid):
	import share_img
	response = send_file(share_img.generate_card('Porto Alegre, RS', int(request.args['temp']), 'day-thunder-rain'),
		attachment_filename='logo.png',
		mimetype='image/png')

	return response

@app.route("/<city_id>")
def index(city_id):
	city_id = int(city_id)
	api_url = 'http://tempo.clic.com.br/api/weather_now?id=%d' % city_id
	data = requests.get(api_url).content
	data = data.decode()
	api_data = json.loads(data)
	temp = int(api_data['temperature'])

	og_url = 'http://104.131.147.80:5050/%d?temp=%d' % (city_id, temp)
	og_img_url = 'http://104.131.147.80:5050/share_img/%d.png?temp=%d' % (city_id, temp)
	fb_url = 'https://www.facebook.com/sharer/sharer.php?u=http://104.131.147.80:5050/%d?temp=%d' % (city_id, temp)

	return render_template('index.html', og_url=og_url, fb_url=fb_url, og_img_url=og_img_url)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
