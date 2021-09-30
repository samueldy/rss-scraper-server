import newspaper
import rfeed
import tqdm
import time
from flask import Flask
from markupsafe import escape
from newspaper.article import ArticleException

# Import website config
from config import websites, NUM_ARTICLES_PER_FEED, CACHE_ARTICLES


# Instantiate Flask app
app = Flask(__name__)


def get_site_articles(url):
    """
    Reach out and download article objects from a news site.
    """

    feed_items = []

    site = newspaper.build(url, memoize_articles=CACHE_ARTICLES)

    articles = [newspaper.Article(art_url) for art_url in site.article_urls()]

    data = []

    # Download all articles if no limit specified, else limit the articles
    articles_to_download = (
        articles if not NUM_ARTICLES_PER_FEED else articles[:NUM_ARTICLES_PER_FEED]
    )

    print(articles_to_download)

    # Download and process articles
    for article in tqdm.tqdm(articles_to_download):
        # try:
        # time.sleep(1)
        article.download()
        article.parse()
        article.nlp()
        feed_item = rfeed.Item(
            title=article.title,
            link=article.url,
            description=article.summary,
            creator=", ".join(article.authors),
            # guid=rfeed.Guid(guid=url),
            pubDate=article.publish_date,
        )

        feed_items.append(feed_item)
        # except ArticleException as e:
        #     # If the download fails, just skip so don't lose all the data we've
        #     # already downloaded.
        #     print(f"Failed on article {article.title}")
        #     pass

    return feed_items


@app.route("/feeds/<feed_id>")
def get_site_feed(feed_id):
    """
    Download articles and form a RSS feed.
    """

    site_info = websites[escape(feed_id)]

    feed_items = get_site_articles(site_info["url"])

    feed = rfeed.Feed(
        title=site_info["shortname"],
        link=site_info["url"],
        description=site_info["fullname"],
        items=feed_items,
    )

    # print(feed.rss())

    return feed.rss()
