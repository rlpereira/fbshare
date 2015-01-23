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

@app.route("/lala")
def yr_hour_by_hour(uf, city):
    fname = os.path.join(os.path.dirname(__file__), 'xmls/forecast_hour_by_hour.xml')
    with open(fname) as xml:
        data=xml.read()
    return Response(data, mimetype="text/xml")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
