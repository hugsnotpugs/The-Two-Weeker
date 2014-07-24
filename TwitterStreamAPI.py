''' Implementation of the Twitter Stream API - Tweepy '''

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time

### Input your own account data here
ckey = '' 
csecret = ''
atoken = ''
asecret = ''

class listener(StreamListener):

    def on_data(self, data):
        try:
            saveFile = open('twitterStream.csv', 'a')
            saveFile.write(data)
            saveFile.write('\n')
            saveFile.close()
            return True
        except BaseException, e:
            print "failed ondata", str(e)
            time.sleep(5)

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["xkcd"]) ### replace with what you want to filter for
