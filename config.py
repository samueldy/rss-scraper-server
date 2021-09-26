## Configuration file

# Global variables
NUM_ARTICLES_PER_FEED = None
CACHE_ARTICLES = True

# Need to specify the websites we'd like to scrape Note that in the example
# below, the first-level keys represent the URL stub where your feed will be
# available. E.g, if Flask is serving your app at http://localhost:5000, then
# point your RSS reader to http://localhost:5000/feeds/ap_main.
websites = {
    "ap_main": {
        "shortname": "AP News Main Page",
        "fullname": "Associated Press News - Main Page",
        "url": "https://apnews.com/",
    },
}