#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et
import os, random
from flask import Flask, request, Response, send_file, render_template

app = Flask(__name__)

@app.route('/share_img/<cityid>.png', methods=['GET'])
def share_img(cityid):
	import share_img
	response = send_file(share_img.generate_card('Porto Alegre, RS', int(request.args['temp']), 'day-thunder-rain'),
		attachment_filename='logo.png',
		mimetype='image/png')

	return response

@app.route("/")
def index():
	temp = random.randint(0,42)
	og_url = 'http://104.131.147.80:5050'
	og_img = 'http://104.131.147.80:5050/share_img/363.png?temp=%d' % temp
    fb_url = 'https://www.facebook.com/sharer/sharer.php?u=http://104.131.147.80:5050/?temp=%d' % temp

    return render_template('index.html', og_url=og_url, fb_url=fb_url, og_img_url=og_img_url)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
