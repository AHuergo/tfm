import credentials
import tweepy
from pandas import DataFrame

# twitterUsers = ['elperiodico', 'elmundoes', '20m', 'publico_es', 'elespanolcom', 'noticias_cuatro', 'A3Noticias', 'lanuevaespana']

# for idUser in twitterUsers:
idUser = ''
client = tweepy.Client(bearer_token=credentials.BEARER_TOKEN,
                       consumer_key=credentials.API_KEY,
                       consumer_secret=credentials.API_SECRET_KEY,
                       access_token=credentials.ACCESS_TOKEN,
                       access_token_secret=credentials.ACCESS_TOKEN_SECRET,
                       return_type=dict,
                       wait_on_rate_limit=True)

auth = tweepy.OAuthHandler(credentials.API_KEY, credentials.API_SECRET_KEY)
auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

tweets = api.user_timeline(screen_name=idUser,
                           count=200,  # maximum allowed = 200
                           include_rts=False,
                           tweet_mode='extended')

all_tweets = []
all_tweets.extend(tweets)
oldest_id = tweets[-1].id

while True:
    tweets = api.user_timeline(screen_name=idUser,
                               count=200, #200 peticiones por cada 15 minutos (limitación de la API)
                               include_rts=False,
                               max_id=oldest_id - 1,
                               tweet_mode='extended'
                               )
    if len(tweets) == 0:
        break
    oldest_id = tweets[-1].id
    all_tweets.extend(tweets)
    print('Tweets descargados: {}'.format(len(all_tweets)))

outtweets = [[tweet.id_str,
              tweet.created_at,
              tweet.favorite_count,
              tweet.retweet_count,
              client.get_tweet(tweet.id_str, user_auth=False, tweet_fields=["public_metrics"])['data']['public_metrics']
              ['reply_count'], tweet.full_text.encode("utf-8").decode("utf-8")]
             for idx, tweet in enumerate(all_tweets)]

df = DataFrame(outtweets, columns=["ID", "Fecha de creación", "Likes", "Retweets", "Nº comentarios", "Texto"])
df.to_csv('%s_tweets.csv' % idUser, index=False)
df.head(3)
