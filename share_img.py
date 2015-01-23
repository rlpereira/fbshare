# -*- coding: utf-8 -*-
# vim: ts=4 noet

import os
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

temp_icon_spacer = 20

default_path = os.path.dirname(__file__)
default_font_name = os.path.join(default_path, 'OpenSans-Bold.ttf')
default_font_size = 500
default_spacer = 50
logo_name = os.path.join(default_path, 'logo.png')

def get_font2fit(text, box_size, font_name=default_font_name, font_size=default_font_size):
	font = ImageFont.truetype(font_name, font_size)
	text_size = font.getsize(text)
	ratios = {text_size[0]/box_size[0]: 0, text_size[1]/box_size[1]: 1}
	worst_ratio = max(ratios.keys())
	if worst_ratio < 1:
		return font, text_size
	test_axis = ratios[worst_ratio]
	font_size = int(font_size*box_size[test_axis]/text_size[test_axis])
	while font.getsize(text)[test_axis] > box_size[test_axis]:
		font_size -= 1
		font = ImageFont.truetype(font_name, font_size)
	return font, font.getsize(text)

def pos_n_size_to_points(pos, size):
	return [pos, (pos[0]+size[0], pos[1]+size[1])]

def align(alignment_x, alignment_y, initial_pos, box_size, text_size):
	return one_x_align(alignment_x, initial_pos[0], box_size[0], text_size[0]), \
		one_x_align(alignment_y, initial_pos[1], box_size[1], text_size[1])

def one_x_align(alignment, initial_pos, box_size, text_size):
	if alignment in ['top', 'left']:
		return initial_pos
	elif alignment in ['bottom', 'right']:
		return initial_pos + box_size - text_size
	elif alignment in ['middle', 'center']:
		return initial_pos + box_size/2 - text_size/2

def lighten(color, qtd=20):
	return color[0]+qtd > 255 and 255 or color[0]+qtd, \
		color[1]+qtd > 255 and 255 or color[1]+qtd, \
		color[2]+qtd > 255 and 255 or color[2]+qtd, \
		color[3]

def generate_card(city_name, temp, condition):
	temp_icon_spacer = 20
	icon_name = os.path.join(default_path + 'icons/', condition+'.png')
	temp='%d°'%temp

	card_size = 1200, 600
	card_margin = 50, 50
	card_background = 16, 181, 241, 255
	card_background = 44, 119, 166, 255

	uf_size = card_size[0]-card_margin[0]*2, 0
	uf_pos = card_margin
	uf_font_name = default_font_name

	city_size = card_size[0]-card_margin[0]*2, 150
	city_pos = card_margin[0], uf_pos[1] + uf_size[1]
	city_font_name = default_font_name

	temp_size = 999,236
	icon_size = 256, 256
	temp_size = get_font2fit(temp, temp_size)[1]

	temp_n_icon_box_size = icon_size[0]+temp_size[0]+temp_icon_spacer, 300
	temp_n_icon_box_pos = int(card_size[0]/2 - temp_n_icon_box_size[0]/2), city_pos[1] + city_size[1] + default_spacer
	temp_pos = temp_n_icon_box_pos
	temp_font_name = default_font_name
	icon_pos = temp_n_icon_box_pos[0]+temp_size[0]+temp_icon_spacer, temp_n_icon_box_pos[1]+30

	card_size = card_size[0], city_pos[1] + city_size[1] + default_spacer + temp_n_icon_box_size[1] + default_spacer*2

	card = Image.new("RGBA", card_size, card_background)
	draw = ImageDraw.Draw(card)

	logo_size = 200, 58
	logo_pos = card_size[0]-logo_size[0]-card_margin[0], card_size[1]-logo_size[1]-card_margin[1]

	city_font, city_real_size = get_font2fit(city_name, city_size)
	draw.text(align('center', 'middle', city_pos, city_size, city_real_size), 
		city_name, font=city_font)

	draw.rectangle(pos_n_size_to_points((city_pos[0], city_pos[1]+city_size[1]+20), (city_size[0], 1)), lighten(card_background))

	icon = Image.open(icon_name) 
	card.paste(icon, icon_pos, mask=icon)

	logo = Image.open(logo_name) 
	card.paste(logo, logo_pos, mask=logo)

	temp_font, temp_real_size = get_font2fit(temp, temp_size)
	draw.text(align('right', 'middle', temp_pos, temp_size, temp_real_size), 
		temp, font=temp_font)

	out = BytesIO()
	card.save(out, 'PNG')
	out.seek(0)
	return out

