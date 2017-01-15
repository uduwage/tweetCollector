import tweepy

class TweepyApiWrapper(object):

    """
    Create a new TwitterCollector instance
    """
    def __init__(self, consumer_key, consumer_secret, access_token,
                 access_token_secret, wait_on_rate_limit, wait_on_rate_limit_notify):
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.secure = True
        self.auth.set_access_token(access_token, access_token_secret)
        self.__api = tweepy.API(self.auth,
                                wait_on_rate_limit=False,
                                wait_on_rate_limit_notify=False)

    @property
    def api(self):
        """
        property method for api object
        :return: api object
        """
        return self.__api