pip install googletrans==4.0.0-rc1
import numpy as np 
import pandas as pd 
import re
import tweepy


# ضع هنا Bearer Token الخاص بك
bearer_token = "AAAAAAAAAAAAAAAAAAAAAIH90gEAAAAANesuwnn2XDGjXVZSwU98jr1AWUA%3DIvWDtKPRzuhtpUI1XVIMoWFyaMVTeBroaRPPgyXy75FIPFbw9X"

# الاتصال بـ Twitter API باستخدام Tweepy v2
client = tweepy.Client(bearer_token=bearer_token)

# استعلام لجلب آخر 100 تغريدة تحتوي على كلمة "الذكاء الاصطناعي"
query = "الذكاء الاصطناعي lang:ar"
tweets = client.search_recent_tweets(query=query, max_results=100)


def clean_text(tweet):
    tweet = re.sub(r"http\S+", "", tweet)  # حذف الروابط
    tweet = re.sub(r"@\w+", "", tweet)     # حذف المنشن
    tweet = re.sub(r"#", "", tweet)        # حذف رمز الهاشتاغ
    tweet = re.sub(r"[^\w\s]", "", tweet)  # حذف الرموز والعلامات
    tweet = re.sub(r"artificial intelligence", "", tweet)
    tweet = re.sub(r"RT", "", tweet)
    tweet = re.sub(r"AI", "", tweet)
    return tweet

df['Cleaned_Tweet'] = df['Tweet'].apply(clean_text)

from googletrans import Translator

# تهيئة المترجم
translator = Translator()

# دالة لترجمة النصوص من العربية إلى الإنجليزية
df['Translated_Tweet'] = df['Cleaned_Tweet'].apply(lambda x: translator.translate(x, src='ar', dest='en').text)

# عرض النتائج
print(df[['Cleaned_Tweet', 'Translated_Tweet']].head())


from textblob import TextBlob

def get_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "إيجابي"
    elif polarity < 0:
        return "سلبي"
    else:
        return "محايد"

df['Sentiment'] = df['Translated_Tweet'].apply(get_sentiment)


import seaborn as sns
import matplotlib.pyplot as plt

sns.countplot(x='Sentiment', data=df)
plt.title('تحليل المشاعر للتغريدات')
plt.show()


from wordcloud import WordCloud
import matplotlib.pyplot as plt

# دمج كل التغريدات في نص واحد
all_words = ' '.join([text for text in df['Translated_Tweet']])

# إنشاء الـ WordCloud بدون تحديد font_path
wordcloud = WordCloud(background_color='white', width=800, height=500).generate(all_words)

# عرض الـ WordCloud
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

