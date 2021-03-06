

## Simple Reddit Scraper

This code shows an example of a fairly general way to scrape reddit with the help of the [praw module](https://praw.readthedocs.org/en/stable/). Set your desired subreddit, number of threads, and number comments per thread to record in `redditconfig.py` along with your MongoDB database and collection name. 

The script includes a praw wrapper class and a PyMongo wrapper class. With these wrappers, `with` statements can be used to control the database connection and to limit the number of separate Reddit connections even in the case of ThreadPools, as used here. 

This script should be ready-to-go for any way you wish to monitor a subreddit over time. I keep a few of these running with cron jobs, each with a separate redditconfig file. To get started, take a look at `scrape.py` to adjust threading to your optimum level and then set your desired thread retrieval parameters (how many threads and where to store them) in `redditconfig.py`.

I mostly used this script to keep track of Reddit's front page offerings for a few months. With this data, I was able to see what subreddits were the most popular and what their general trajectories were on the front page. You can see more of that work [here](https://github.com/sunnysideprodcorp/PlottingNonRectangularData)

