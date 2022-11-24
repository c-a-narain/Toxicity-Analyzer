import snscrape.modules.twitter as twitterScraper;
import json;


name=input("Enter user name:")
n=int(input("Enter the number of tweets to retrive:"))
scraper=twitterScraper.TwitterUserScraper(name,False)

tweets=[]
all_tweet_contents=""

for i,tweet in enumerate(scraper.get_items()):
    if i>n:
        break
    tweets.append({"id:":tweet.id, "content:" : tweet.content})
    
    # fetched tweet contents directly from scraper
    all_tweet_contents= all_tweet_contents + tweet.content + " "

tweets_file = open("tweets.json","w")
json_res=json.dumps({"TWEETS":tweets})
tweets_file.write(json_res)
tweets_file.close()



# tweets_file = open('tweets.json')
dataset_file = open('dataset.json')
result_file = open("result.json","w")

# tweets_data = json.load(tweets_file)
dataset_data = json.load(dataset_file)

total_count=0
total_swear_words_count=0; general_swear_words_count=0; religious_swear_words_count=0; women_swear_words_count=0
total_swear_words=""; general_swear_words=""; religious_swear_words=""; women_swear_words=""


# for i in tweets_data['TWEETS']:
#     for j in i:
#         if j=="content:":
#             content=i[j]
#             content = content.replace("\n", " ")
#             all_tweet_contents= all_tweet_contents + content

all_tweet_contents = all_tweet_contents.replace("\n", " ")
all_tweet_contents = all_tweet_contents.lower()
total_count = total_count + len(all_tweet_contents.split())

# for i in tweets_data['TWEETS']:
#     for j in i:
#         if j=="content:":
#             content=i[j]
#             for k in dataset_data['general_words']:
#                 if k in content:
#                     print("General swear word(s) found is/are : "+k)
#                     total_swear_words_count = total_swear_words_count + 1
#                     general_swear_words_count = general_swear_words_count + 1
#             for k in dataset_data['religious_words']:
#                 if k in content:
#                     print("Religious swear word(s) found is/are : "+k)
#                     total_swear_words_count = total_swear_words_count + 1
#                     religious_swear_words_count = religious_swear_words_count + 1
#             for k in dataset_data['women_words']:
#                 if k in content:
#                     print("Women swear word(s) found is/are : "+k)
#                     total_swear_words_count = total_swear_words_count + 1
#                     women_swear_words_count = women_swear_words_count + 1

#make sure all characters in dataset is in lowercase                  
for k in dataset_data['general_words']:
    if k in all_tweet_contents:
        # print("General swear word(s) found is/are : "+k)
        total_swear_words = total_swear_words + k + ","
        general_swear_words = general_swear_words + k + ","
for k in dataset_data['religious_words']:
    if k in all_tweet_contents:
        # print("Religious swear word(hello tirugnanams) found is/are : "+k)
        total_swear_words = total_swear_words + k + ","
        religious_swear_words = religious_swear_words + k + ","
for k in dataset_data['women_words']:
    if k in all_tweet_contents:
        # print("Women swear word(s) found is/are : "+k)
        total_swear_words = total_swear_words + k + ","
        women_swear_words = women_swear_words + k + ","

total_swear_words_count = len(total_swear_words.split(",")) - 1
general_swear_words_count = len(general_swear_words.split(",")) - 1
religious_swear_words_count = len(religious_swear_words.split(",")) - 1
women_swear_words_count = len(women_swear_words.split(",")) - 1

json_res=json.dumps({"Total words count":total_count,"Total swear words count":total_swear_words_count,"Total General swear words count":general_swear_words_count,"Total Religious swear words count":religious_swear_words_count,"Total Women swear words count":women_swear_words_count,     "Total swear words":total_swear_words,"Total General swear words":general_swear_words,"Total Religious swear words":religious_swear_words,"Total Women swear words":women_swear_words})
result_file.write(json_res)

tweets_file.close()
dataset_file.close()
result_file.close()
# print ("content-type: text/html")
# webbrowser.open('index.html') 

#hello tiru