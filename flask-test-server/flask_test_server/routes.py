#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import io
import random
import time

from collections import OrderedDict
from flask_test_server import app
from flask import Flask, render_template, render_template_string, request, jsonify, session, send_file, flash, url_for, redirect

from bs4 import BeautifulSoup

import re

@app.route("/")
def home():
	return "hello from flask!"
	
def getAuthorText(messageSoup):
	div = messageSoup.find('div', attrs={'class': re.compile('^contents.*')})
	if div:
		return div.text
	else:
		return ""
		
def getEmbedDescText(messageSoup):
	div = messageSoup.find('div', attrs={'class': re.compile('^embedDescription.*')})
	if div:
		return div.text
	else:
		return ""
		
def getEmbedFooterText(messageSoup):
	div = messageSoup.find('div', attrs={'class': re.compile('^embedFooter.*')})
	if div:
		return div.text
	else:
		return ""
		
def getEmbedFields(htmlSoup):
	divs = htmlSoup.find_all('div', attrs={'class': re.compile('^embedFields.*')})
	return divs
	
answers = open(os.path.join(app.config["DATAFRAMES_DIR"], "answers.txt"), "rb").read().decode("u8").split("\n")
	
def matchWord(s, letters_tried = []):
	print("matchWord(\"%s\", \"%s\"" % (s, letters_tried))
	print(s)
	if s[0].isspace():
		s = s[1:]
	s=s.replace(" ", "").replace("\u2000", " ").replace("◯", ".")
	print(s)
	s = s.capitalize()
	letters_tried = list(letters_tried)
	for i in list(letters_tried):
		letters_tried.append(i.upper())
	pattern = re.compile("^%s$"%s)
	def reject(word):
		for c in word:
			if c in letters_tried:
				return True
		return False
	print([x for x in answers if pattern.match(x) if not reject(x)])
	
def filterTextByCircleSymbol(s):
	res = []
	for line in s.split("\n"):
		if "◯" in line:
			res.append(line)
			
	return res

@app.route("/my_node", methods=['GET', 'POST'])
def my_node():
	global last_filtered_messages
	if request.method == "POST":
		soup = BeautifulSoup(request.data, 'html.parser')

		messages = soup.find_all('code')
		if messages:
			message = messages[-1]
			embedFooterText = getEmbedFooterText(message.parent.parent)
			letters_tried = [i for i in embedFooterText.replace(" ", "") if not i in message.text]
			matchWord(message.text, letters_tried = letters_tried)
	return "hello from flask!"
