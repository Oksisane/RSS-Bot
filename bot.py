import feedparser,time,sys
from trolly.card import Card
from trolly.client import Client
from HTMLParser import HTMLParser
ftc_rss_url = "http://ftcforum.usfirst.org/external.php?lastpost=true&type=rss2"
threads_to_check = ["http://ftcforum.usfirst.org/showthread.php?3034-Robot-Electronics-and-Power-Answer-Thread" ,
                    "http://ftcforum.usfirst.org/showthread.php?3033-Robot-Parts-and-Materials-Answer-Thread" ,
                    "http://ftcforum.usfirst.org/showthread.php?3035-Game-Rules-and-Game-Play-Answer-Thread" ,
                    "http://ftcforum.usfirst.org/showthread.php?3036-The-Field-The-Tournament-Judging-and-Advancement-Answer-Thread"]
detected = []
client = Client("APIKEY", "APITOKEN")
card = Card(client, "card")
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
def convTrello (htmlcomment):
    array = htmlcomment.split('A:')
    question = array[0].split('<div class="message">')[1]
    reply = array[1]
    question =  ">"  + strip_tags(question)
    reply = "**Answer:" + strip_tags(reply) + "**"
    return question + reply
def main():
	while 1:
            feed = feedparser.parse( ftc_rss_url)
            for item in feed [ "items" ]:
                if (item["guid"] in threads_to_check) & (item["content"] not in detected):
                    detected.append(item["content"])
                    card.add_comments(convTrello(item["content"][0]["value"].encode(sys.stdout.encoding, errors='replace')))
            print ( "Resting for 30 sec....")
	    time.sleep(30)
if __name__ == "__main__":

	main()
