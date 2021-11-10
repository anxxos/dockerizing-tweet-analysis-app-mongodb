python twitterstream.py ${TIME} ${ATK} ${ATS} ${CK} ${CS} > tweets.json 
python sentiment_analysis.py tweets.json -r local --file AFINN_111.txt > output.txt
python mongodb.py
