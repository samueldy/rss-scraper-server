import newspaper
import rfeed
import tqdm
from flask import Flask
from markupsafe import escape

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

    # Download and process articles
    for article in tqdm.tqdm(articles_to_download):
        article.download()
        article.parse()
        article.nlp()
        feed_item = rfeed.Item(
            title=article.title,
            link=article.url,
            description=article.summary,
            creator=", ".join(article.authors),
            guid=rfeed.Guid(guid=article.url.split("?")[0]),
            pubDate=article.publish_date,
        )

        feed_items.append(feed_item)

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

    return feed.rss()


# Run development server
if __name__ == "__main__":
    app.run(debug=True, port=5000)
