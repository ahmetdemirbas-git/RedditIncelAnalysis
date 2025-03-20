import praw
from collections import Counter
import os

# Function to read subreddits and number of top users from a file
def read_subreddits_from_file(filepath):
    subreddits = []
    try:
        with open(filepath, 'r') as file:
            for line in file:
                parts = line.split(': ')
                if len(parts) == 2:
                    subreddit_name = parts[0].strip()
                    try:
                        top_n = int(parts[1].strip())
                        subreddits.append((subreddit_name, top_n))
                    except ValueError:
                        print(f"Warning: Invalid number format for subreddit {subreddit_name}. Skipping.")
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
    except Exception as e:
        print(f"An error occurred while reading the file '{filepath}': {e}")
    return subreddits

# Function to fetch commenters in a subreddit
def fetch_commenters(praw_client, subreddit_name, limit):
    commenters = Counter()
    try:
        subreddit = praw_client.subreddit(subreddit_name)
        for comment in subreddit.comments(limit=limit):
            if comment.author:  # Check if the author is not None
                commenters[comment.author.name] += 1
    except Exception as e:
        print(f"An error occurred while fetching commenters for subreddit {subreddit_name}: {e}")
    return commenters

# Main script
if __name__ == "__main__":
    # Initialize Reddit client
    try:
        praw_client = praw.Reddit(
            client_id="-mEbO67KsABp_Y6NoR9CUA",
            client_secret="sL1Qk_uMIrOrbuv7cg_-5dN-0Er5fw",
            user_agent="reddit scraper by u/disguisedmoron",
        )
    except Exception as e:
        print(f"An error occurred while initializing the Reddit client: {e}")
        exit(1)

    # Input file name for top subreddits
    input_filename = '/Users/erdem/Desktop/Top50RelatedSubredditsCounts.txt'

    # Get the absolute path of the input file
    filepath = os.path.abspath(input_filename)

    # Ensure the input file exists
    if not os.path.isfile(filepath):
        print(f"Error: The file '{filepath}' does not exist.")
        exit(1)

    # Read subreddits and number of top users from the file
    subreddits = read_subreddits_from_file(filepath)
    if not subreddits:
        print("No subreddits were found in the file.")
        exit(1)

    # Dictionary to hold top commenters for each subreddit
    top_commenters_per_subreddit = {}

    # Fetch commenters for each subreddit
    for subreddit, top_n in subreddits:
        # Use a higher limit for fetching comments to ensure we get a good sample size
        limit = top_n * 100  # Example: 100 comments per top user to find
        subreddit_commenters = fetch_commenters(praw_client, subreddit, limit=limit)
        
        # Get the top N commenters for this subreddit
        top_commenters = subreddit_commenters.most_common(top_n)
        top_commenters_per_subreddit[subreddit] = [user for user, count in top_commenters]

    # Save the top commenters to a file
    top_commenters_filepath = 'top_commenters_per_subreddit.txt'
    with open(top_commenters_filepath, 'w') as f:
        for subreddit, top_commenters in top_commenters_per_subreddit.items():
            f.write(f"{subreddit}: {', '.join(top_commenters)}\n")

    print("Top commenters per subreddit saved to 'top_commenters_per_subreddit.txt'")
