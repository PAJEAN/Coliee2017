#!/usr/bin/python

'''
	modification ligne 184 (Right of Demand by Person who is Counterparty to Person with Limited Capacity)
	modification ligne 73, 158, 208, 399
	Manual modification of lines 3124 and 1412: suppression des retours a la ligne
	suppression ligne 1539
	/Library/Java/JavaVirtualMachines/jdk1.8.0_121.jdk/Contents/Home
	export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_121.jdk/Contents/Home
'''



import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
import os
import unicodedata


''' split the given line into a specified number of part. The method returns an array containing the parts. '''
def generate_part(nb_part, line):

    #print " splitting '"+line+"'"
    if nb_part > len(line):
        return [line]
    else:
        data_line = line.split(" ")
        break_step = len(data_line) / nb_part
        i = 0
        splits = []
        while i < len(data_line):
            split = " ".join(data_line[i:i + break_step])
            #print "part ", split
            i += break_step
            splits.append(split)
        return splits




def is_noun(tag):
    return tag in ['NN', 'NNS', 'NNP', 'NNPS']


def is_verb(tag):
    return tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']


def is_adverb(tag):
    return tag in ['RB', 'RBR', 'RBS']


def is_adjective(tag):
    return tag in ['JJ', 'JJR', 'JJS']


def penn_to_wn(tag):
    if is_adjective(tag):
        return wn.ADJ
    elif is_noun(tag):
        return wn.NOUN
    elif is_adverb(tag):
        return wn.ADV
    elif is_verb(tag):
        return wn.VERB
    return None


def lemmatize(s):
    tokens = word_tokenize(s)  # Generate list of tokens
    tokens_pos = pos_tag(tokens)

    # print(tokens_pos)

    sentence_lem = ""

    for tpos in tokens_pos:
        if (penn_to_wn(tpos[1]) == None):
            sentence_lem += " " + tpos[0]
        else:
            sentence_lem += " " + nltk.stem.WordNetLemmatizer().lemmatize(tpos[0], penn_to_wn(tpos[1]))
    sentence_lem = sentence_lem.strip()

    if type(sentence_lem) is unicode:
        sentence_lem = unicodedata.normalize('NFKD', sentence_lem).encode('ascii', 'ignore')
    return sentence_lem


def cleanText(text):
    chars_to_remove = ['.', '!', '?', ',', ':', ';', ')', '(', '\/', '\'']
    text = text.translate(None, ''.join(chars_to_remove))
    # suppress several spaces
    text = ' '.join(text.split())
    return text.lower()


class Part:
    """ Part of the civil code composed of Chapter"""

    def __init__(self, id, title):
        self.chapters = []
        self.id = id
        self.title = title

    def addChapter(self, chapter):
        self.chapters.append(chapter);

    def __str__(self):
        return "{part id: " + str(self.id) + ", title: " + str(self.title) + " chapters :" + str(
            len(self.chapters)) + "}"


class Chapter:
    """ Chapter of the civil code composed of Sections"""

    def __init__(self, id, title):
        self.sections = []
        self.id = id
        self.title = title

    def addSection(self, section):
        self.sections.append(section);

    def __str__(self):
        return "{chapter id: " + str(self.id) + ", title: " + str(self.title) + " sections : " + str(
            len(self.sections)) + "}"


class Section:
    """ Section of the civil code composed of Subsection"""

    def __init__(self, id, title):
        self.subsections = []
        self.id = id
        self.title = title

    def addSubsection(self, subsection):
        self.subsections.append(subsection);

    def __str__(self):
        return "{section id: " + str(self.id) + " title: " + str(self.title) + " subsections : " + str(
            len(self.subsections)) + "}"


class Subsection:
    """ Subsection of the civil code composed of Division"""

    def __init__(self, id, title):
        self.divisions = []
        self.id = id
        self.title = title

    def addDivision(self, division):
        self.divisions.append(division);

    def __str__(self):
        return "{SubSection id: " + str(self.id) + " title: " + str(self.title) + " divisions : " + str(
            len(self.divisions)) + "}"


class Division:
    """ Division of the civil code composed of ArticleGroup"""

    def __init__(self, id, title):
        self.articleGroups = []
        self.id = id
        self.title = title

    def addArticleGroup(self, articleGroup):
        self.articleGroups.append(articleGroup);

    def __str__(self):
        return "{Division id: " + str(self.id) + " title: " + str(self.title) + " article groups : " + str(
            len(self.articleGroups)) + "}"


class ArticleGroup:
    """ ArticleGroup of the civil code composed of Article"""

    def __init__(self, title):
        self.articles = []
        self.title = title

    def addArticle(self, article):
        self.articles.append(article);

    def __str__(self):
        return "{ArticleGroup  title: " + str(self.title) + " articles : " + str(len(self.articles)) + "}"


class Article:
    """ Article of the civil code eventually composed of Paragraphs"""

    def __init__(self, id):
        self.paragraphs = []
        self.id = id

    def addParagraph(self, paragraph):
        self.paragraphs.append(paragraph);

    def __str__(self):
        return "{article id: " + str(self.id) + ", paragraphs : " + str(len(self.paragraphs)) + "}"


class Paragraph:
    """ Paragraph of the civil code associated : an ID and a text"""

    def __init__(self, id, text):
        self.id = id
        self.text = text

    def setText(self, text):
        self.text = text

    def __str__(self):
        return "{paragraph id: " + str(self.id) + ", text: " + str(self.text) + "}"


numberCharacters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "I", "V", "X", "-"]


def isNumeric(numberAsString):
    numberAsString = numberAsString.strip()

    isChapter = True

    for c in numberAsString:
        if c not in numberCharacters:
            isChapter = False

    return isChapter


''' Return None if no chapter header data specified'''


def getChapterHeaderInfo(data):
    if data[0] == "Chapter" and len(data) > 1 and isNumeric(data[1]):
        return [data[1].strip()]
    return None


def getPartHeaderInfo(data):
    if data[0] == "Part" and len(data) > 1 and isNumeric(data[1]):
        return [data[1].strip()]
    return None


def getSectionHeaderInfo(data):
    if data[0] == "Section" and len(data) > 1 and isNumeric(data[1]):
        return [data[1].strip()]
    return None


def getSubsectionHeaderInfo(data):
    if data[0] == "Subsection" and len(data) > 1 and isNumeric(data[1]):
        return [data[1].strip()]
    return None


def getDivisionHeaderInfo(data):
    if data[0] == "Division" and len(data) > 1 and isNumeric(data[1]):
        return [data[1].strip()]
    return None


def getArticleHeaderInfo(data):
    if data[0] == "Article" and len(data) > 1 and isNumeric(data[1]):
        return [data[1].strip()]
    return None


def getArticleGroupHeaderInfo(data):
    # print data

    if data[0][0] == "(" and data[-1][-1] == ")":
        return data
    return None


def getParagraphHeaderInfo(data):
    paragraphNumber = 0
    paragraphText = " ".join(data)

    if data[0][0] == "(" and isNumeric(data[0][1:-1]):
        paragraphNumber = data[0][1:-1]
        paragraphText = " ".join(data[1:])
        return [paragraphNumber, paragraphText]

    return None


def extractParagraph(data):
    paragraphNumber = 0
    paragraphText = " ".join(data)

    if data[0][0] == "(" and isNumeric(data[0][1:-1]):
        paragraphNumber = data[0][1:-1]
        paragraphText = " ".join(data[1:])

    return Paragraph(paragraphNumber, paragraphText)


def basicConvertStringToInt(s):
    s = s.strip().lower()
    if s == "one":
        return 1
    elif s == "two":
        return 2
    elif s == "three":
        return 3
    elif s == "four":
        return 4
    elif s == "five":
        return 5
    elif s == "six":
        return 6
    elif s == "seven":
        return 7
    elif s == "eight":
        return 8
    elif s == "nine":
        return 9
    elif s == "ten":
        return 10
    else:
        return None


def isInteger(val):
    try:
        int(val)
        return True
    except ValueError:
        return False


def detectArticleLinks(article_id, cleaned_text):
    links = []

    if "article" in cleaned_text or "articles" in cleaned_text:

        index_ref_unique_article = []
        index_ref_multiple_articles = []

        print article_id, cleaned_text

        data_text = cleaned_text.split(" ")
        for i in range(0, len(data_text)):
            word = data_text[i]

            if word == "article":
                index_ref_unique_article.append(i)

            elif word == "articles":
                index_ref_multiple_articles.append(i)

        print "unique ", index_ref_unique_article

        for article_word_id in index_ref_unique_article:

            print article_word_id, len(data_text)

            next_word = data_text[article_word_id + 1].strip() if article_word_id + 1 < len(data_text) else None
            previous_word = data_text[article_word_id - 1].strip()

            if next_word is not None and (isInteger(next_word) or ('-' in next_word)):
                print "word ", article_word_id, " ref to Article ", next_word
                links.append(next_word)

            elif previous_word == "preceding":
                print "word ", article_word_id, " ref to preceding Article ", article_id, " -1"
                links.append("-1")

            elif previous_word == "following":
                print "word ", article_word_id, " ref to following Article ", article_id, " +1"
                links.append("+1")
            else:
                "Execution stopped: unable to detect ref"

        print "mulitple ", index_ref_multiple_articles

        for articles_word_id in index_ref_multiple_articles:

            next_word = data_text[articles_word_id + 1].strip()
            n_next_word = data_text[articles_word_id + 2].strip() if len(data_text) > articles_word_id + 2 else None
            n_n_next_word = data_text[articles_word_id + 3].strip() if len(data_text) > articles_word_id + 3 else None
            previous_word = data_text[articles_word_id - 1].strip()
            p_previous_word = data_text[articles_word_id - 2].strip()

            '''
            print "next word", next_word
            print "previous ", previous_word
            print "p previous ", p_previous_word
            '''

            if p_previous_word == "preceding":
                print "word ", articles_word_id, " refering to ", previous_word, " preceding Articles "
                nb = basicConvertStringToInt(previous_word)
                if nb is not None:
                    for i in range(0, nb):
                        links.append("-" + str(i + 1))


            elif isInteger(next_word) and n_next_word == "to" and isInteger(n_n_next_word):
                print "word ", articles_word_id, " refering to Articles ", next_word, " to article ", n_n_next_word
                start = int(next_word)
                end = int(n_n_next_word)

                for i in range(start - 1, end):
                    links.append(str(i + 1))

            elif isInteger(next_word) and n_next_word == "through" and isInteger(n_n_next_word):
                print "word ", articles_word_id, " refering to Articles ", next_word, " to article ", n_n_next_word
                start = int(next_word)
                end = int(n_n_next_word)

                for i in range(start - 1, end):
                    links.append(str(i + 1))
            else:
                print "Cannot detect links"

            print links
            # raw_input()
    return links


if __name__ == "__main__":

    ''' True: documents are also generated by splitting the articles '''
    GENERATE_ARTICLE_SPLITS = False
    GENERATE_MUTATIS_MUTANDIS_MIXED = True

    print "Knowledge base generation"

    print "GENERATE_ARTICLE_SPLITS: ",GENERATE_ARTICLE_SPLITS


    civil_code = "./Data/civil_english_modified.txt"

    print "Loading kb from ", civil_code

    previous_data_line = None
    previous_line = None
    buffer = []

    parts = []

    current_part = None
    current_chapter = None
    current_section = None
    current_subsection = None
    current_division = None
    current_article_group = None
    current_article = None
    current_paragraph = None

    for current_line in open(civil_code):

        '''
        raw_input('Type a key to process KB extraction')
        print "---------------------------------------------------------"
        for part in parts:
            print "Part ", part.id, part.title

            for chapter in part.chapters:
                print "\tChapter ", chapter.id, chapter.title

                for section in chapter.sections:
                    print "\t\tSection ", section.id, section.title

                    for subsection in section.subsections:
                        print "\t\t\tSubection ", subsection.id, subsection.title

                        for division in subsection.divisions:
                            print "\t\t\t\tDivision ", division.id, division.title

                            for aG in division.articleGroups:
                                print "\t\t\t\t\tArticleGroup ", aG.title

                                for article in aG.articles:
                                    print "\t\t\t\t\t\tArticle ", article.id

                                    for paragraph in article.paragraphs:
                                        print "\t\t\t\t\t\t\tParagraph ", paragraph.id, paragraph.text

        print "---------------------------------------------------------"
        '''
        print "processing: ", current_line.strip()

        # replace multiple spaces to a single space
        # important for the process
        current_line = ' '.join(current_line.split())
        current_line = current_line.strip()
        current_data_line = current_line.split()

        partHeaderInfo = getPartHeaderInfo(current_data_line)
        chapterHeaderInfo = getChapterHeaderInfo(current_data_line)
        sectionHeaderInfo = getSectionHeaderInfo(current_data_line)
        subSectionHeaderInfo = getSubsectionHeaderInfo(current_data_line)
        divisionHeaderInfo = getDivisionHeaderInfo(current_data_line)
        articleHeaderInfo = getArticleHeaderInfo(current_data_line)
        paragraphHeaderInfo = getParagraphHeaderInfo(current_data_line)
        # print chapterHeaderInfo

        if partHeaderInfo is not None:

            current_part = None
            current_chapter = None
            current_section = None
            current_subsection = None
            current_division = None
            current_article_group = None
            current_article = None
            current_paragraph = None

            id_part = partHeaderInfo[0]
            title_part = " ".join(current_data_line[2:])
            print "*** Detect part", id_part, title_part

            current_part = Part(id_part, title_part)
            parts.append(current_part)

        elif chapterHeaderInfo is not None:

            current_section = None
            current_subsection = None
            current_division = None
            current_article_group = None
            current_article = None
            current_paragraph = None

            id_chapter = chapterHeaderInfo[0]
            title_chapter = " ".join(current_data_line[2:])
            print "*** Detect chapter", id_chapter, title_chapter

            current_chapter = Chapter(id_chapter, title_chapter)

            if current_part is None:
                current_part = Part(0, "FICTIVE")

            current_part.addChapter(current_chapter)

        elif sectionHeaderInfo is not None:

            current_section = None
            current_subsection = None
            current_division = None
            current_article_group = None
            current_article = None
            current_paragraph = None

            id_section = sectionHeaderInfo[0]
            title_section = " ".join(current_data_line[2:])
            print "*** Detect section", id_section, title_section

            current_section = Section(id_section, title_section)

            if current_chapter is None:
                current_chapter = Chapter(0, "FICTIVE")
                if current_part is None:
                    current_part = Part(0, "FICTIVE")
                current_part.addChapter(current_chapter)

            # print "Add to chapter: ", current_chapter.id
            current_chapter.addSection(current_section)

        elif subSectionHeaderInfo is not None:

            current_subsection = None
            current_division = None
            current_article_group = None
            current_article = None
            current_paragraph = None

            id_subsection = subSectionHeaderInfo[0]
            title_subsection = " ".join(current_data_line[2:])
            print "*** Detect subsection", id_subsection, title_subsection

            current_subsection = Subsection(id_subsection, title_subsection)

            if current_section is None:
                current_section = Section(0, "FICTIVE")

                if current_chapter is None:
                    current_chapter = Chapter(0, "FICTIVE")
                    if current_part is None:
                        current_part = Part(0, "FICTIVE")
                    current_part.addChapter(current_chapter)

                current_chapter.addSection(current_section)

            current_section.addSubsection(current_subsection)

        elif divisionHeaderInfo is not None:

            current_division = None
            current_article_group = None
            current_article = None
            current_paragraph = None

            id_division = divisionHeaderInfo[0]
            title_division = " ".join(current_data_line[2:])
            print "*** Detect division", id_division, title_division

            current_division = Division(id_subsection, title_subsection)

            if current_subsection is None:
                current_subsection = Subsection(0, "FICTIVE")

                if current_section is None:
                    current_section = Section(0, "FICTIVE")

                    if current_chapter is None:
                        current_chapter = Chapter(0, "FICTIVE")
                        if current_part is None:
                            current_part = Part(0, "FICTIVE")
                        current_part.addChapter(current_chapter)

                    current_chapter.addSection(current_section)
                current_section.addSubsection(current_subsection)

            current_subsection.addDivision(current_division)

        elif articleHeaderInfo is not None:

            # check if the Article is not Deleted
            if len(current_data_line) > 2 and current_data_line[2].lower() == "deleted":
                print "skipping DELETED ARTICLE", current_line
            else:
                articleGroupHeaderInfo = getArticleGroupHeaderInfo(previous_data_line)

                newArticleGroup = False

                if articleGroupHeaderInfo is not None:

                    current_article_group = None
                    current_article = None
                    current_paragraph = None

                    article_group_title = " ".join(articleGroupHeaderInfo).replace("(", "").replace(")", "")
                    current_article_group = ArticleGroup(article_group_title)
                    print "*** Detect article group ", article_group_title
                    newArticleGroup = True

                elif current_article_group is None:
                    current_article_group = ArticleGroup("FICTIVE")
                    newArticleGroup = True

                if newArticleGroup:
                    if current_division is None:
                        current_division = Division(0, "FICTIVE")

                        if current_subsection is None:
                            current_subsection = Subsection(0, "FICTIVE")

                            if current_section is None:
                                current_section = Section(0, "FICTIVE")

                                if current_chapter is None:
                                    current_chapter = Chapter(0, "FICTIVE")
                                    if current_part is None:
                                        current_part = Part(0, "FICTIVE")
                                    current_part.addChapter(current_chapter)

                                current_chapter.addSection(current_section)
                            current_section.addSubsection(current_subsection)
                        current_subsection.addDivision(current_division)

                    current_division.addArticleGroup(current_article_group)

                id_article = articleHeaderInfo[0]
                print "*** Detect Article: ", id_article

                current_article = Article(id_article)
                current_article_group.addArticle(current_article)
                print "adding article to current article group ", current_article_group.title

                pararagraphText = " ".join(current_data_line[2:])
                pararagraphText = pararagraphText.strip()

                p = extractParagraph(pararagraphText.split())
                print "*** Detect paragraph (from article header) ", p
                current_article.addParagraph(p)
                current_paragraph = p

        elif paragraphHeaderInfo is not None:
            print "*** Detect paragraph (from paragraph header)", paragraphHeaderInfo
            p = Paragraph(paragraphHeaderInfo[0], paragraphHeaderInfo[1])
            current_article.addParagraph(p)
            current_paragraph = p

        elif current_part is not None:

            if current_line[0][0] != "(" and current_line[0][-1] != ")":

                if current_paragraph is None:

                    current_paragraph = Paragraph("0", current_line)
                    print "*** Detect paragraph (no existing paragraph)", current_paragraph
                    current_article.addParagraph(current_paragraph)
                else:
                    print "*** Extending paragraph", current_paragraph.id
                    current_paragraph.setText(current_paragraph.text + " " + current_line)

        previous_data_line = current_data_line

    indexed_doc = {}
    indexed_doc_articles = {}
    orderingArticleIds = []

    links_mutatis_mutantis = {}

    for part in parts:
        print "Part", part.id, part.title

        for chapter in part.chapters:
            print "\tChapter", chapter.id, chapter.title

            for section in chapter.sections:
                print "\t\tSection", section.id, section.title

                for subsection in section.subsections:
                    print "\t\t\tSubection", subsection.id, subsection.title

                    for division in subsection.divisions:
                        print "\t\t\t\tDivision", division.id, division.title

                        for aG in division.articleGroups:
                            print "\t\t\t\t\tArticleGroup", aG.title

                            for article in aG.articles:
                                print "\t\t\t\t\t\tArticle", article.id
                                orderingArticleIds.append(article.id)

                                article_text = "";

                                for paragraph in article.paragraphs:
                                    print "\t\t\t\t\t\t\tParagraph", paragraph.id, paragraph.text

                                    paragraph_index_text = ""
                                    '''
                                    if part.title != "FICTIVE":
                                        paragraph_index_text += part.title + " "

                                    if chapter.title != "FICTIVE":
                                        paragraph_index_text += chapter.title + " "

                                    if section.title != "FICTIVE":
                                        paragraph_index_text += "Section " +  section.id + " " + section.title + " "

                                    if subsection.title != "FICTIVE":
                                        paragraph_index_text += "Subsection " + subsection.id + " " + subsection.title + " "

                                    if division.title != "FICTIVE":
                                        paragraph_index_text += "Division " + division.id + " " + division.title + " "
                                    if aG.title != "FICTIVE":
                                        paragraph_index_text += aG.title + " "
                                     '''
                                    # paragraph_index_text += "Article " + str(article.id) + " "

                                    # if paragraph.id != 0:
                                    # paragraph_index_text += "Paragraph " + str(paragraph.id) + " "


                                    '''paragraph_index_id = str(part.id) + "_" + str(chapter.id) + "_" + str(
                                        section.id) + "_" + str(subsection.id) + "_" + str(article.id) + "_" + str(
                                        paragraph.id)
                                    '''
                                    paragraph_index_id = "PARAGRAPH_" + str(article.id) + "_" + str(paragraph.id)
                                    paragraph_index_text += cleanText(paragraph.text)

                                    # print paragraph_index_id, "\t", paragraph_index_text
                                    indexed_doc[paragraph_index_id] = lemmatize(paragraph_index_text).lower()
                                    indexed_doc_articles[paragraph_index_id] = [article.id]

                                    article_text += paragraph_index_text + "\n"

                                # indexed_paragraph["ARTICLE_"+str(article.id)] = cleanText(article_text).lower()

                                lemmatized_string = lemmatize(article_text)

                                indexed_doc["ARTICLE_" + str(article.id)] = lemmatized_string
                                indexed_doc_articles["ARTICLE_" + str(article.id)] = [article.id]

                                # Generate part of articles
                                if GENERATE_ARTICLE_SPLITS:
                                    split_factor = 2
                                    while split_factor <= 6:
                                        splits = generate_part(split_factor, lemmatized_string)
                                        if len(splits) > 1:
                                            count_k  = 0
                                            for k in splits:
                                                split_name = "ARTICLE_" + str(article.id)+"_SPLIT_F"+str(split_factor)+"_"+str(count_k)
                                                indexed_doc[split_name] = k
                                                indexed_doc_articles[split_name] = [article.id]
                                                count_k += 1
                                        split_factor+=1

                                # detect Mutatis mutantis links
                                if GENERATE_MUTATIS_MUTANDIS_MIXED:
                                    if "mutatis" in article_text.lower():
                                        print "-----"
                                        print "Mutatis Mutantis"
                                        print "-----"
                                        print article_text
                                        print "-----"
                                        links = detectArticleLinks(article.id, cleanText(article_text).lower())
                                        links_mutatis_mutantis[article.id] = links
                                        print links

                                    # raw_input("validate")

    if GENERATE_MUTATIS_MUTANDIS_MIXED:
        print "Generating Mutatis Mutandis index"

        for article_id in links_mutatis_mutantis:

            print "ARTICLE: ", article_id

            text = indexed_doc["ARTICLE_" + str(article_id)]
            order_id = orderingArticleIds.index(article_id)

            for linked_article_code in links_mutatis_mutantis[article_id]:

                if linked_article_code[0] == "-":
                    id_linked_article = orderingArticleIds[int(order_id) - int(linked_article_code[1])]
                elif linked_article_code[0] == "+":
                    id_linked_article = orderingArticleIds[int(order_id) + int(linked_article_code[1])]
                else:
                    id_linked_article = linked_article_code

                if "ARTICLE_" + str(id_linked_article) not in indexed_doc:
                    print "Warning: Article ", str(id_linked_article), " not found"
                else:
                    text_linked = indexed_doc["ARTICLE_" + str(id_linked_article)]

                    print str(id_linked_article)
                    print text_linked

                    mix_index_id = "MIX_" + str(article_id) + "_" + str(id_linked_article)
                    mix_text = text_linked + " " + text

                    print "MIX_TEXT\n", mix_text

                    todel_terms = ["provision", "shall", "apply", "mutatis", "mutandis",
                                   "case", "article", "articles", "act", "paragraph",
                                   "paragraphs", "no", "preceding", "precede", "provision"]

                    # remove all numbers
                    mix_text_clean = ''.join([i for i in mix_text if not i.isdigit()])

                    for term in todel_terms:
                        mix_text_clean = mix_text_clean.replace(" " + term.strip() + " ", " ")

                    mix_text_clean = cleanText(mix_text_clean)
                    print "MIX_TEXT\n", mix_text_clean
                    indexed_doc[mix_index_id] = mix_text
                    indexed_doc_articles[mix_index_id] = [article_id, id_linked_article]
                    indexed_doc[mix_index_id + "_CLEANED"] = mix_text_clean
                    indexed_doc_articles[mix_index_id + "_CLEANED"] = [article_id, id_linked_article]

                    # raw_input("press enter")

    print "Generating index"

    index_file_path = "tmp/index/index.xml"
    index_file_path_tsv = "tmp/index.tsv"
    docArticle_path = "tmp/docToArticles.tsv"

    # create index dir if not existing
    d = os.path.dirname("tmp/index/")
    if not os.path.exists(d):
        os.makedirs(d)

    index_file = open(index_file_path, 'w')
    index_file_tsv = open(index_file_path_tsv, 'w')
    docArticle_file = open(docArticle_path, 'w')

    for k in indexed_doc:
        index_file.write("<DOC>\n")
        print k, "\t", indexed_doc[k]
        index_file.write("<DOCNO>" + k + "</DOCNO>\n")
        index_file.write(indexed_doc[k] + "\n")
        index_file_tsv.write(k + "\t" + indexed_doc[k] + "\n")
        index_file.write("</DOC>\n")

        docArticle_file.write(k + "\t" + ",".join(indexed_doc_articles[k]) + "\n")
    index_file.close()
    index_file_tsv.close()
    docArticle_file.close()
