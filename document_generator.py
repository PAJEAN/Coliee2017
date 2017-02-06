#!/bin/python
# -*- coding:utf-8 -*-
import boite_a_outils as bao

###### Description ###
###
# Permet de formater le xml du code civile de Gildas pour l'indexation de Terrier.
# Trois options, soit on formate en fonction des articles (choose == 1) soit en fonction des chapitres (choose == 2) ou soit en fonction des sections (choose > 2)
###

###### Inputs ###
###
path_file = "Data/civcode.xml"
choose = 1
###

###### Ouputs ###
###
if choose == 1:
	out = open("Data/Indexation/Articles/codeCivile.ter", "w")
elif choose == 2:
	out = open("Data/Indexation/Chapitres/codeCivile_chapters.ter", "w")
	out2 = open("Data/Index/num_articles-id_chapitre.tsv", "w")
elif choose == 3:
	out = open("Data/Indexation/Sections/codeCivile_sections.ter", "w")
	#out2 = open("Data/Index/num_articles-id_chapitre.tsv", "w")
elif choose == 4:
	out = open("Data/Indexation/Paragraphs/codeCivile_paragraphs.ter", "w")
###

xml_parser = bao.XML_parser_civil_code(path_file)
xml_parser.extraction_articles()

if choose == 1:		
	for id_article in xml_parser.articles:
		out.write("<DOC>\n")
		out.write("<DOCNO>"+id_article+"</DOCNO>\n")
		out.write(xml_parser.articles[id_article]+"\n")
		out.write("</DOC>\n")

elif choose == 2:
	xml_parser.extraction_chapters()
	for id_chapter in xml_parser.chapters:
		out.write("<DOC>\n")
		out.write("<DOCNO>"+id_chapter+"</DOCNO>\n")
		id_articles = xml_parser.chapters[id_chapter]
		for id_article in id_articles:
			out.write(xml_parser.articles[id_article]+"\n")
			out2.write(id_article+"\t"+id_chapter+"\n")
		out.write("</DOC>\n")

elif choose == 3:
	xml_parser.extraction_sections()
	for id_article in xml_parser.sections:
		out.write("<DOC>\n")
		out.write("<DOCNO>"+id_article+"</DOCNO>\n")
		out.write(xml_parser.sections[id_article]+"\n")
		out.write("</DOC>\n")
		
elif choose == 4:
	xml_parser.extraction_paragraphs()
	for id_paragraph in xml_parser.paragraphs:
		out.write("<DOC>\n")
		out.write("<DOCNO>"+id_paragraph+"</DOCNO>\n")
		out.write(xml_parser.paragraphs[id_paragraph]+"\n")
		out.write("</DOC>\n")

			
			
			
