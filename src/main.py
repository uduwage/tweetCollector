from tweetCollector import TweetCollector
#https://github.com/suraj-deshmukh/get_tweets/blob/master/tweets-by-daterange.py
def main():
    tc = TweetCollector()
    tc.harvestTweets()

if __name__ == "__main__":
    main()