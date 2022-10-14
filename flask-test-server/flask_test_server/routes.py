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
	
def getAuthor(messageSoup):
	div = messageSoup.find('div', attrs={'class': re.compile('^contents.*')})
	if div:
		return div.text
	else:
		return ""
		
def getEmbedDesc(messageSoup):
	div = messageSoup.find('div', attrs={'class': re.compile('^embedDescription.*')})
	if div:
		return div.text
	else:
		return ""
		
def getEmbedFooter(messageSoup):
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
	
last_filtered_messages = []

@app.route("/my_node", methods=['GET', 'POST'])
def my_node():
	global last_filtered_messages
	if request.method == "POST":
		htmlDoc = request.data
		soup = BeautifulSoup(htmlDoc, 'html.parser')

		#messages = soup.find_all('div', attrs={'class': re.compile('^message.*')})
		messages = soup.find_all('code')
		embedFooters = soup.find_all('span', attrs={'class': re.compile('^embedFooterText.*')})
		last_message = [i.text for i in messages][-1]
		letters_tried = [i for i in embedFooters[-1].text.replace(" ", "") if not i in last_message]
		matchWord(last_message)
		matchWord(last_message, letters_tried = letters_tried)

		#filtered_messages = [message for message in messages if "Bouncer+BOT" in getAuthor(message)]

		# if filtered_messages == last_filtered_messages:
			# print("already have this list of messages, skipping")
			# return "repeat"
			
		# last_filtered_messages = filtered_messages

		#print([i.text for i in filtered_messages if "◯" in i.text])
		#filtered_messages1 = [[line for line in i.text.split("\n") if "◯" in line] for i in filtered_messages]
		#last_message = [msg[-1] for msg in filtered_messages1 if len(msg) >= 1][-1]
		#print(last_message)
		#matchWord(last_message)
		#filtered_messages = [[getEmbedDesc(i), getEmbedFooter(i)] for i in messages]
		#last_message = [[line for line in getEmbedDesc(i).split("\n") if "◯" in line] for i in messages if "◯" in getEmbedDesc(i)][-1][0]
		#print(matchWord(last_message))
		#if len(filtered_messages1) > 1:
		#	print([i for i in filtered_messages1[-1][0].split("\n") if "◯" in i])
		#if len(filtered_messages1) > 1:
		#	filtered_messages2 = [i for i in filtered_messages1[-1][0].split("\n") if "◯" in i]
		#	last_message = filtered_messages2[-1]
		#	print(last_message)
		#	matchWord(last_message)
		
		#print([i for i in filtered_messages1[-1][0].split("\n") if "◯" in i])
		#print([i.text for i in getEmbedFields(soup)])
	return "hello from flask!"
