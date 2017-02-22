#/bin/bash


/home/tagny/bin/anaconda2/bin/python kb_generator.py > tmp/kb_generator.tmp
/home/tagny/bin/anaconda2/bin/python queries_generator.py $1 $2 > tmp/queries_generator.tmp

bash terrier.sh


/home/tagny/bin/anaconda2/bin/python score.py 1 > tmp/score.log


cat tmp/score.log
