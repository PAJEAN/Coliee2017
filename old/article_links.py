#!/usr/bin/python
# -*- coding:utf-8 -*-
import re
import boite_a_outils as bao


class Part:
	""" Part of the civil code composed of Chapter"""

	def __init__(self, id, title):
		self.chapters = []
		self.id = id
		self.title = title

	def addChapter(self, chapter):
		self.chapters.append(chapter);

	def __str__(self):
		chapter_str = "{"
		for p in self.chapters:
			chapter_str += str(p)
			chapter_str += "}"
		return "{part id: "+str(self.id)+", title: "+str(self.title)+" chapters : "+str(chapter_str)+"}"

class Chapter:
	""" Chapter of the civil code composed of Sections"""

	def __init__(self, id, title):
		self.sections = []
		self.id = id
		self.title = title

	def addSection(self, section):
		self.sections.append(section);

	def __str__(self):
		section_str = "{"
		for p in self.sections:
			section_str += str(p)
			section_str += "}"
		return "{chapter id: "+str(self.id)+", title: "+str(self.title)+" sections : "+str(section_str)+"}"

class Section:
	""" Section of the civil code composed of Articles"""

	def __init__(self, title):
		self.articles = []
		self.title = title

	def addArticle(self, article):
		self.articles.append(article);

	def __str__(self):
		article_str = "{"
		for a in self.articles:
			article_str += str(a)
		article_str += "}"
		return "{section title: "+str(self.title)+" articles : "+str(article_str)+"}"

class Article:
	""" Article of the civil code eventually composed of Paragraphs"""

	def __init__(self, id, text):
		self.paragraphs = []
		self.id = id
		self.text = text

	def addParagraph(self, paragraph):
		self.paragraphs.append(paragraph);

	def __str__(self):
		paragraph_str = "{"
		for p in self.paragraphs:
			paragraph_str += str(p)
		paragraph_str += "}"
		return "{article id: "+str(self.id)+", text: "+str(self.text)+" paragraphs : "+str(paragraph_str)+"}"

class Paragraph:
	""" Paragraph of the civil code associated : an ID and a text"""

	def __init__(self, id, text):
		self.id = id
		self.text = text

	def __str__(self):
		return "{paragraph id: "+str(self.id)+", text: "+str(self.text)+"}"


class FileParserUtils:
	@staticmethod
	def queries(text):
		minuscules = "a b c d e f g h i j k l m n o p q r s t u v w x y z".split(" ")
		num = "0 1 2 3 4 5 6 7 8 9".split(" ")
		phrase = ""
		for s in text.lower():
			if s in minuscules or s in num or s in [" ", "-", "."]:
				phrase += s
			elif s in ["\n"]:
				phrase += " "
		return phrase

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
out = open("Data/Index/adjacences_articles.tsv", "w")
###

from lxml import etree

tree = etree.parse(path_file)
root = tree.getroot()

# part > chapter > section > article > paragraph

parts = []

for part_node in root.iter("part"):

	part_id = part_node.get("id")
	part_title = part_node.get("title")

	part = Part(part_id, part_title)

	for chapter_node in part_node.iter("chapter"):

		print "\t", chapter_node, "\t"
		chapter_id = chapter_node.get("id")
		chapter_title = chapter_node.get("title")

		chapter = Chapter(chapter_id, FileParserUtils.queries(chapter_title))
		part.addChapter(chapter)

		for section_node in chapter_node.iter("section"):

			print "\t\t", section_node
			#section_id = section_node.get("id")
			section_title = section_node.get("title")

			section = Section(FileParserUtils.queries(section_title))
			chapter.addSection(section)

			for article_node in section_node.iter("article"):

				print "\t\t\t", article_node
				article_id = article_node.get("id")
				article = Article(article_id, FileParserUtils.queries(article_node.text))
				section.addArticle(article)

				for paragraph_node in article_node.iter("paragraph"):

					print "\t\t\t\t", paragraph_node
					paragraph_id = paragraph_node.get("id")
					paragraph = Paragraph(paragraph_id, FileParserUtils.queries(paragraph_node.text))
					article.addParagraph(paragraph)



	print part
	parts.append(part)


""" Generating index Document """
# part > chapter > section > article > paragraph
for part in parts:
	for chapter in part.chapters:
		for section in chapter.sections:
			for article in section.articles:
				for paragraph in article.paragraphs:
					p_id = part.id+"-"+chapter.id+"-"+""+section.title.replace(" ", "_")+"-"+article.id+"-"+paragraph.id
					print p_id+"\t"+paragraph.text

quit()

for article in xml_parser.articles:
    id_articles = []
    r = re.compile("article ([0-9]+)")
    for f in r.findall(xml_parser.articles[article]):
        id_articles.append(f)

    r = re.compile("article ([0-9]+-[0-9]+)")
    for f in r.findall(xml_parser.articles[article]):
        id_articles.append(f)

    if len(id_articles) > 0:
        out.write(article + "\t" + ";".join(id_articles) + "\n")
