from os import sendfile
import snscrape.modules.twitter as twitterScraper;
import json;

from flask import Flask, redirect, url_for, request
app = Flask(__name__)


@app.route('/success/<name>')
def success(name: str):
	en=name.split("?")
	en1=en[0].split("|")
	email=en1[0]
	num=en1[1]
	
	if(en[1] != "An error occurred in username. Invalid username"):
		l = en[1].split("<br>")
		empty = ""
		for i in l[0:-1]:
			empty += "<tr>"
			empty += "<th>" + i.split(":")[0] + "</th>"
			empty += "<th>:</th>"
			empty += "<td>" + i.split(":")[1] + "</td>"
			empty += "</tr>"
			empty += "\n"
	else:
		empty = "<tr><th>"+en[1]+"</th></tr>"
	# print(empty)
	html = '''
	<!DOCTYPE html>
		<head>
			<meta charset="UTF-8">
			<meta name="viewport" content="width=device-width, initial-scale=1.0">
			<title>Toxicity Detector</title>
		</head>

		<body>
			<center>
				<h1 >Social Media Toxicity Detector</h1> 
				<table>
					<tr><th>Username</th><th>:</th><td>%s</td></tr>
					<tr><th>No. of tweets</th><th>:</th><td>%s</td></tr>
				</table><br><br>
				<table class="t1">
					%s
				</table>
			</center>
			
		</body>
		<style>
			body {
				background-color: #f2e19b;
				font-size: 30px;
			}
			.t1{
				border:5px black solid;
			}
		</style>
	</html>
	''' %(email,num,empty)
	# print(name.split("<br>"))
	return html


@app.route('/login', methods=['POST', 'GET'])
def login():
	email = request.form['email']
	num = int(request.form['number'])

	try:
		scraper=twitterScraper.TwitterUserScraper(email,False)
		tweets=[]
		all_tweet_contents=""

		for i,tweet in enumerate(scraper.get_items()):
			if i>num:
				break
			tweets.append({"id:":tweet.id, "content:" : tweet.content})
			
			# fetched tweet contents directly from scraper
			all_tweet_contents= all_tweet_contents + tweet.content + " "
		json_res=json.dumps({"TWEETS":tweets})

		dataset_file = open('dataset.json')
		result_file = open("result.json","w")

		dataset_data = json.load(dataset_file)

		total_count=0
		total_swear_words_count=0; general_swear_words_count=0; religious_swear_words_count=0; women_swear_words_count=0
		total_swear_words=""; general_swear_words=""; religious_swear_words=""; women_swear_words=""

		all_tweet_contents = all_tweet_contents.replace("\n", " ")
		all_tweet_contents = all_tweet_contents.lower()
		total_count = str(len(all_tweet_contents.split()))

		#make sure all characters in dataset is in lowercase                  
		for k in dataset_data['general_words']:
			if k in all_tweet_contents:
				total_swear_words = total_swear_words + k + ","
				general_swear_words = general_swear_words + k + ","
		for k in dataset_data['religious_words']:
			if k in all_tweet_contents:
				total_swear_words = total_swear_words + k + ","
				religious_swear_words = religious_swear_words + k + ","
		for k in dataset_data['women_words']:
			if k in all_tweet_contents:
				total_swear_words = total_swear_words + k + ","
				women_swear_words = women_swear_words + k + ","

		total_swear_words_count = str(len(total_swear_words.split(",")) - 1)
		general_swear_words_count = str(len(general_swear_words.split(",")) - 1)
		religious_swear_words_count = str(len(religious_swear_words.split(",")) - 1)
		women_swear_words_count = str(len(women_swear_words.split(",")) - 1)

		json_res=json.dumps({"Total words count":total_count,"Total swear words count":total_swear_words_count,"Total General swear words count":general_swear_words_count,"Total Religious swear words count":religious_swear_words_count,"Total Women swear words count":women_swear_words_count,     "Total swear words":total_swear_words,"Total General swear words":general_swear_words,"Total Religious swear words":religious_swear_words,"Total Women swear words":women_swear_words})
		result_file.write(json_res)

		string=email+"|"+str(num)+"?Total words count: "+total_count+"<br>Total swear words count: "+total_swear_words_count+"<br>Total General swear words count: "+general_swear_words_count+"<br>Total Religious swear words count: "+religious_swear_words_count+"<br>Total Women swear words count: "+women_swear_words_count+"<br>Total swear words: "+total_swear_words+"<br>Total General swear words: "+general_swear_words+"<br>Total Religious swear words: "+religious_swear_words+"<br>Total Women swear words: "+women_swear_words+"<br>"

		dataset_file.close()
		result_file.close()
		return redirect(url_for('success', name=string))
	except:
		# print ("An error occurred in username")
		return redirect(url_for('success', name=email+"|"+str(num)+"?An error occurred in username. Invalid username"))

if __name__ == '__main__':
    app.run(port=5000,debug=True) 
if __name__ == '__main__':
	app.run(debug=True)
