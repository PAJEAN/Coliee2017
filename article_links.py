#!/bin/python
# -*- coding:utf-8 -*-
import re
import boite_a_outils as bao

###### Description ###
###
# Permet de générer un fichier avec les liens des articles.
###

###### Inputs ###
###
path_file = "Data/civcode.xml"
###

###### Ouputs ###
###
#out = open("Data/Index/adjacences_articles.tsv", "w")
###

xml_parser = bao.XML_parser_civil_code(path_file)
xml_parser.extraction_articles()

##########
# Remplacer les articles par leur titre de section.
out = open("Data/Indexation/Articles/codeCivile.ter", "w")
xml_parser.extraction_sections()
articles = {}
for article in xml_parser.articles:
	# Remplacer les articles par leur titre de section.
	#r1 = re.compile("article ([0-9]+-[0-9]+)[\. ]")
	#r2 = re.compile("article ([0-9]+)[\. ]")
	r1 = re.compile(" ([0-9]+-[0-9]+)[\. ]")
	r2 = re.compile(" ([0-9]+)[\. ]")
	
	id_articles = r1.findall(xml_parser.articles[article])
	if len(id_articles) > 0:
		for id_article in id_articles:
			if id_article in xml_parser.sections:
				print id_article
				xml_parser.articles[article] = re.sub(id_article, xml_parser.sections[id_article], xml_parser.articles[article])
				#xml_parser.articles[article] = re.sub("[Aa]rticle "+id_article, xml_parser.sections[id_article], xml_parser.articles[article])
		
	id_articles = r2.findall(xml_parser.articles[article])
	if len(id_articles) > 0:
		for id_article in id_articles:
			if id_article in xml_parser.sections:
				xml_parser.articles[article] = re.sub(id_article, xml_parser.sections[id_article], xml_parser.articles[article])
				#xml_parser.articles[article] = re.sub("[Aa]rticle "+id_article, xml_parser.sections[id_article], xml_parser.articles[article])
	
	
for id_article in xml_parser.articles:
	out.write("<DOC>\n")
	out.write("<DOCNO>"+id_article+"</DOCNO>\n")
	out.write(xml_parser.articles[id_article]+"\n")
	out.write("</DOC>\n")
##########
	
	# Liste d'adjacences.
	"""
	id_articles = []
	r = re.compile("article ([0-9]+)")
	for f in r.findall(xml_parser.articles[article]):
		id_articles.append(f)
		
	r = re.compile("article ([0-9]+-[0-9]+)")
	for f in r.findall(xml_parser.articles[article]):
		id_articles.append(f)
		
	
	if len(id_articles) > 0:
		out.write(article+"\t"+";".join(id_articles)+"\n")
	"""
	
	
	
	
	
	
	
	
	
	
		
