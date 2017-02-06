#!/bin/python
# -*- coding:utf-8 -*-
import boite_a_outils as bao

path_file = "Data/civcode.xml"
articles = bao.XML_parser_civil_code(path_file)
articles.extraction_sections()
"""
articles.extraction_articles()
articles.extraction_chapters()
print articles.articles["1"]
print
print articles.chapters["1.1"]
"""
