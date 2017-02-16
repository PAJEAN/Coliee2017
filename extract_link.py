

def cleanText(text):
	chars_to_remove = ['.', '!', '?', ',', ':']
	text = text.translate(None, ''.join(chars_to_remove))
	text = ' '.join(text.split())
	return text

def isInteger(val):
    try: 
        int(val)
        return True
    except ValueError:
        return False



print "Extracting article relationship"


path = "Data/civil_english.txt"

articles = {}

current_article_id = None
current_article_text = None


count = 0

for line in open(path):

	data = line.strip().split()

	if(data[0] == "Article"):

		if(current_article_id != None):
			articles[current_article_id] = current_article_text
			current_article_text = None

		current_article_id = data[1]
		current_article_text = " ".join(data[2:])+" "
	
	elif(current_article_id != None):
		current_article_text += " ".join(data)+" "

articles[current_article_id] = current_article_text


process_id = 1
for article_id in articles:

	cleaned_text = cleanText(articles[article_id])

	if("Article" in cleaned_text or "Articles" in cleaned_text):

		
		index_ref_unique_article = []
		index_ref_multiple_articles = []

		print "-------------------------------"
		print " processing ", process_id,"/",len(articles)
		print "-------------------------------"
		
		print article_id, cleaned_text

		process_id += 1

		data_text = cleaned_text.split(" ")
		for i in range(0,len(data_text)):
			word = data_text[i]
			
			if(word == "Article"):
				index_ref_unique_article.append(i) 

			elif(word == "Articles"):
				index_ref_multiple_articles.append(i) 

		print "unique ",index_ref_unique_article
		
		for article_word_id in index_ref_unique_article:

			next_word = data_text[article_word_id+1].strip()
			previous_word = data_text[article_word_id-1].strip()

			if isInteger(next_word) or ('-' in next_word):
				print "word ",article_word_id, " ref to Article ",next_word

			elif previous_word == "preceding":
				print "word ",article_word_id, " ref to preceding Article ", article_id, " -1"

			elif previous_word == "following":
				print "word ",article_word_id, " ref to following Article ", article_id, " +1"

			else:
				"Execution stopped: unable to detect ref"
				quit()


		print "mulitple ",index_ref_multiple_articles

		for articles_word_id in index_ref_multiple_articles:

			
			next_word = data_text[articles_word_id+1].strip()
			n_next_word = data_text[articles_word_id+2].strip() if len(data_text) > articles_word_id+2 else None 
			n_n_next_word = data_text[articles_word_id+3].strip() if len(data_text) > articles_word_id+3 else None 
			previous_word = data_text[articles_word_id-1].strip()
			p_previous_word = data_text[articles_word_id-2].strip()

			'''
			print "next word", next_word
			print "previous ", previous_word
			print "p previous ", p_previous_word
			'''

			print articles_word_id

			if(p_previous_word == "preceding"):
				print "word ",article_word_id, " refering to ",previous_word," preceding Articles "

			elif(isInteger(next_word) and n_next_word == "to" and isInteger(n_n_next_word)):
				print "word ",article_word_id, " refering to Articles ",next_word," to article ",n_n_next_word

			else:
				print "Cannot detect"

		raw_input('validate')
		print "-------------------------------"
		count+=1

print count