import pandas as pd
import json
import time


class TwitterGrabber:
    
    def __init__(self, query, numRuns, smallest_ID, API):
        
        ## Initializing class variables
        self.q = query
        self.n = numRuns
        self.smallest_ID = smallest_ID
        self.API = API
    
    def getTweets(self, statuses):
        followers = []
        status_counts = []
        descriptions = []
        friends= []
        locations = []
        names = []
        favorites = []
        time_zones = []
        tweets = []
        created_at = []
        user_id = []
    
        smallest_id = statuses[0]['id']

        for k in range(len(statuses)):    
            followers.append(int(statuses[k]['user']['followers_count']))
            status_counts.append(int(statuses[k]['user']['statuses_count']))
            descriptions.append(statuses[k]['user']['description'].encode('utf-8'))                     
            friends.append(int(statuses[k]['user']['friends_count']))
            locations.append(statuses[k]['user']['location'].encode('utf-8'))
            names.append(statuses[k]['user']['name'].encode('utf-8'))
            favorites.append(int(statuses[k]['user']['favourites_count']))
            time_zones.append(str(statuses[k]['user']['time_zone']))
            tweets.append(str((statuses[k]['text'].encode('utf-8'))))
            created_at.append(str((statuses[k]['created_at'].encode('utf-8'))))
            user_id.append(int(statuses[k]['user']['id']))
            
            ## getting smallest_id
            if(statuses[k]['id'] < smallest_id):
                smallest_id = statuses[k]['id'] 
    
    
        tweetDict = {'followers': followers,
                'statuses': status_counts,
                'descriptions': descriptions,
                'friends': friends,
                'locations': locations,
                'names': names,
                'favorites': favorites,
                'time_zones': time_zones,
                'tweets': tweets,
                'created_at': created_at,
                'user_id': user_id}
        return (pd.DataFrame(tweetDict), smallest_id)

    
    def grab(self):        
        count = 100

        ## Initial Run
        if self.smallest_ID == 0:
            search_results = self.API.search.tweets(q=self.q, count=count)
        else:
            search_results = self.API.search.tweets(q=self.q, count=count, max_id = self.smallest_ID - 1, result_type = 'mixed')
            
        #print json.dumps(search_results, indent=1)

        statuses = search_results['statuses']
        (data, smallest_id) = self.getTweets(statuses)
 

        # Iterating runs to grab next results
        for i in range(self.n):
            
            print smallest_id
            search_results = self.API.search.tweets(q = self.q, count = count, max_id = smallest_id - 1, result_type = 'mixed')
            #print json.dumps(search_results, indent=1)
            
            statuses = search_results['statuses']
            
            if len(statuses) > 0: # if API call works
                x = self.getTweets(statuses)
                df = x[0] #x[0] returns the 1st result of getTweets; the data dataframe
                smallest_id = x[1] #x[1] returns the 2nd result of getTweets; the smallest_id
                data = pd.concat([data,df]) 
                print "data retrieved"
            else:
                print "NOTHING HERE"
                break

        return(data, smallest_id)

