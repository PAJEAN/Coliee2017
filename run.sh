#/bin/bash


python kb_generator.py > tmp/kb_generator.tmp
python queries_generator.py > tmp/queries_generator.tmp

bash terrier.sh


python score.py 1 > tmp/score.log


cat tmp/score.log
