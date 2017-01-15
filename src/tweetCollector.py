import tweepy
import json
import pdb
import time
from datetime import datetime
import io

from fileLocator import FileLocator
from tweepyApiWrapper import TweepyApiWrapper
from datetime import datetime


class TweetCollector():

    def __init__(self):
        print "collecting tweets"
        self.fl = FileLocator()
        tokens = self.fl.getTwitterTokens()
        self.CONSUMER_KEY = tokens['CONSUMER_KEY']
        self.CONSUMER_SECRET = tokens['CONSUMER_SECRET']
        self.ACCESS_KEY = tokens['ACCESS_KEY']
        self.ACCESS_SECRET = tokens['ACCESS_SECRET']
        self.fileName = '_' + datetime.now().strftime("%Y%m%d")

    def harvestTweets(self):
        fileLocation = self.fl.getFileLocations()
        _input_root = fileLocation['ROOT_LOCATION'] + fileLocation['INPUT_FOLDER']
        _output_root = fileLocation['ROOT_LOCATION'] + fileLocation['OUTPUT_FOLDER']
        twitter_names = [line.strip() for line in open(_input_root + '/twitter_names.txt', 'r')]
        api_call = TweepyApiWrapper(self.CONSUMER_KEY, self.CONSUMER_SECRET,
                                  self.ACCESS_KEY, self.ACCESS_SECRET, True, True)
        api = api_call.api
        x = api.rate_limit_status()
        print x
        print type(api)

        for name in twitter_names:
            print "collecting " + name
            with io.open(_output_root + name + self.fileName + '.txt', 'w+', encoding='utf-8') as tweets_of_user:
                tweets = tweepy.Cursor(api.user_timeline, screen_name=name).items()
                count = 0
                while True and count < 10:
                    # as long as I still have a tweet to grab
                    try:
                        data = tweets.next()
                    except tweepy.TweepError:
                        time.sleep(60 * 15)
                    except StopIteration:
                        break
                    # convert from Python dict-like structure to JSON format
                    jsoned_data = json.dumps(data._json, ensure_ascii=True, indent=2)
                    # print jsoned_data
                    # tweet = json.loads(jsoned_data)
                    # print tweet
                    tweets_of_user.write(unicode(jsoned_data))
                    tweets_of_user.write(unicode('\n'))
                    tweets_of_user.write(unicode(','))
                    tweets_of_user.write(unicode('\n'))
                    #count += 1
            tweets_of_user.close()
            # insert the information in the database
            #collection.insert(tweet)

    def test_rate_limit(api, wait=True, buffer=.1):
        """
        Tests whether the rate limit of the last request has been reached.
        :param api: The `tweepy` api instance.
        :param wait: A flag indicating whether to wait for the rate limit reset
                     if the rate limit has been reached.
        :param buffer: A buffer time in seconds that is added on to the waiting
                       time as an extra safety margin.
        :return: True if it is ok to proceed with the next request. False otherwise.
        """
        print type(api)
        x = tweepy.API.rate_limit_status
        pdb.set_trace()
        #Get the number of remaining requests
        remaining = int(api.last_response.getheader('X-Rate-Limit-Remaining'))
        #Check if we have reached the limit
        if remaining == 0:
            limit = int(api.last_response.getheader('X-Rate-Limit-Limit'))
            reset = int(api.last_response.getheader('X-Rate-Limit-Reset'))
            #Parse the UTC time
            reset = datetime.fromtimestamp(reset)
            #Let the user know we have reached the rate limit
            print "0 of {} requests remaining until {}.".format(limit, reset)

            if wait:
                #Determine the delay and sleep
                delay = (reset - datetime.now()).total_seconds() + buffer
                print "Sleeping for {}s...".format(delay)
                time.sleep(delay)
                #We have waited for the rate limit reset. OK to proceed.
                return True
            else:
                #We have reached the rate limit. The user needs to handle the rate limit manually.
                return False

        #We have not reached the rate limit
        return True
