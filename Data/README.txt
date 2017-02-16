
*****  COLIEE-17 Competition in ICAIL 2017 ******

This zip file consists of:
1. Training data 
      riteval_H18.xml
	  riteval_H19.xml
	  riteval_H20.xml
	  riteval_H21.xml
	  riteval_H22.xml
	  riteval_H23.xml
	  riteval_H24.xml
	  riteval_H25.xml
	  riteval_H26.xml
	  riteval_H27.xml

2. English Translsation of the Japanese Civil Code
	 civil_english.txt

3. Example of answers (You should follow this answer format when you submit your results.)
		3.1. For the Task 1
			H18.task1.YOURID
		3.2 For the Task 2 
			H18.task2.YOURID

4. Output of some publicly available Natural Language Processing (NLP) Tools 
		4.1 Stanford Parser (Output_stanford-parser-2012-11-12/)
		4.2 Stanford Named Entity Recognizer (Output_stanford-ner-2014-06-16/)
		4.3 Stanford Part-Of-Speech(POS) Tagger (Output_stanford-postagger-2012-07-09/)

	The output of the NLP Tools are for the participants who want to use the NLP techniques. You can also download and use the tools from http://nlp.stanford.edu/software/index.shtml
	For details about the Tools and the output formats, please refer to
	   http://nlp.stanford.edu/software/index.shtml	
	
5. Format of the Training Data
The example of the format of the training data is as follows:
-------------------------------
<pair id="H19-1-3" label="N">
<t1>
(Fraud or Duress)Article 96(1)Manifestation of intention which is induced by any fraud or duress may be rescinded.(2)In cases any third party commits any fraud inducing any person to make a manifestation of intention to the other party, such manifestation of intention may be rescinded only if the other party knew such fact.(3)The rescission of the manifestation of intention induced by the fraud pursuant to the provision of the preceding two paragraphs may not be asserted against a third party without knowledge.
</t1>
<t2>
A person who made a manifestation of intention which was induced by duress emanated from a third party may rescind such manifestation of intention on the basis of duress, only if the other party knew or was negligent of such fact.
</t2>
</pair>
-------------------------------
The tag <t2> is a query sentence and the tag <t1> shows corresponding civil codes. 

5.1 Answer for Task 1
The purpose of the Task 1 is to find corresponding articles of a given query sentence. In the example "H19-1-3" above, the corresponding civil code is "96". Therefore the answer for the Task 1 should be 

H19-1-3 96 YOURID

where YOURID should be replaced with your group id.  The first token of each line (whitespace delimited) is the question ID, the second token is the corresponding civil code that you obtained, and the last token is your ID. Each line can include only one civil code. If you obtained multiple civil codes as relevant, you have to add more lines as follows:

H19-1-3 96 YOURID
H19-1-3 97 YOURID

In the test data for the Task 1, the <t1> and label information will not be given. Only <t2> information which is a query sentence will be given. 

5.2 Answer for Task 2
The purpose of the Task 2 is to answer Yes/No combining your information retrieval (IR) system (Task 1) and your entailment system.
First, you retrieve relevant articles using your IR system given a query, and then you induce 'yes' or 'no' using your entailment system between the query sentence and your retrieved articles. 

In the example of "H19-1-3", based on the entailment from the corresponding article 96, the answer of the query sentence <t1> is "No", and you can also validate your Yes/No answer using the "label" information. If the label is "Y", it means the answer of the query sentence is "Yes". Otherwise, if the label is "N", it means the answer of the query sentence is "No". 
In this example, the answer for the Task 2 is as following:

H19-1-3 N YOURID

The test data of Task 2 will include only <t2> information which is a query. The <t1> and label information will not be given.
	
Please see http://webdocs.cs.ualberta.ca/~miyoung2/COLIEE2017/ for details. If you have any queries, please do not hesitate to contact us at miyoung2@ualberta.ca . Thank you for the participation of COLIEE-17 and we look forward to your result submission.

