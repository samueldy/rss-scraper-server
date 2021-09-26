# RSS Scraper Server -- for news websites that don't publish RSS feeds

This short script originally grew out of an effort to read [Associated Press](https://apnews.com/) news articles in a RSS reader installed locally on my laptop. The Associated Press and some other news websites have stopped publishing RSS feeds. Some services (such as [RSS.app](https://rss.app/)) exist to automatically crawl websites and generate RSS feeds from them, but have extremely limited free tiers.

Similar functionality can be easily accomplished within Python, and this small Flask app leverages the `newspaper3k` library to do exactly that. Given a base URL for the news site, it will retrieve a list of articles and locally serve an RSS feed so that your local RSS reader can find it.

## Requirements

- Python 3
- [`newspaper3k`](https://anaconda.org/conda-forge/newspaper3k)
- [`rfeed`](https://pypi.org/project/rfeed/)
- flask
- markupsafe

## Installation and Usage

1. Clone the repo to somewhere on your local disk.
2. Install the necessary Python packages using pip or (recommended) creating a virtual environment using tools such as [conda](https://docs.conda.io/en/latest/).
3. Edit `config.py` to specify news websites you'd like to crawl, as well as other settings.
4. Add the appropriate URL for each feed to your RSS reader.
5. Run the Flask app like this:

```bash
cd "directory_where_you_cloned_the_repo"
FLASK_APP=flask_app flask run
```

6. Refresh your RSS reader. You should see progress bars in the terminal running the Flask app as it downloads articles and generates the feed. You should then see stories appear in your RSS reader.