#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et

from flask import Flask, request, Response, send_file

app = Flask(__name__)

@app.route('/share_img/<cityid>.png', methods=['GET'])
def share_img(cityid):
	import share_img
	response = send_file(share_img.generate_card('Porto Alegre, RS', 20, 'day-thunder-rain'),
		attachment_filename='logo.png',
		mimetype='image/png')

	return response

@app.route("/")
def index():
    fname = os.path.join(os.path.dirname(__file__), './index.html')
    with open(fname) as html:
        data=html.read()
    return Response(data, mimetype="text/html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
