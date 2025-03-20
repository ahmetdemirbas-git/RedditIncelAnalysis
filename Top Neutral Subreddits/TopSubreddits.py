import redditwarp.SYNC
import praw
from collections import Counter
import os
import prawcore

# Function to read usernames from a file
def read_usernames_from_file(filepath):
    usernames = []
    try:
        with open(filepath, 'r') as file:
            usernames = [line.split(':')[0].strip() for line in file]
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
    except Exception as e:
        print(f"An error occurred while reading the file '{filepath}': {e}")
    return usernames

# Function to fetch subreddits a user has commented in
def fetch_user_subreddits(client, praw_client, username, limit=500):
    subreddits = Counter()
    try:
        redditor = praw_client.redditor(username)
        
        if hasattr(redditor, 'fullname'):
            comments = client.p.user.pull.comments(username, limit)
            for comm in comments:
                subreddit_name = comm.subreddit.name
                subreddits[subreddit_name] += 1
        elif hasattr(redditor, 'is_suspended'):
            print(f"User {username} is suspended.")
        else:
            print(f"User {username} is shadowbanned or not found.")
    except prawcore.exceptions.NotFound:
        print(f"User {username} not found (404 error).")
    except Exception as e:
        print(f"An error occurred while fetching subreddits for user {username}: {e}")
    return subreddits

# Main script
if __name__ == "__main__":
    # Initialize Reddit client
    try:
        client = redditwarp.SYNC.Client()
        praw_client = praw.Reddit(
            client_id="-mEbO67KsABp_Y6NoR9CUA",
            client_secret="sL1Qk_uMIrOrbuv7cg_-5dN-0Er5fw",
            user_agent="reddit scraper by u/disguisedmoron",
        )
    except Exception as e:
        print(f"An error occurred while initializing the Reddit client: {e}")
        exit(1)

    # Input file name
    input_filename = '/Users/erdem/Desktop/top_2000_incel_users.txt'

    # Get the absolute path of the input file
    filepath = os.path.abspath(input_filename)

    # Ensure the input file exists
    if not os.path.isfile(filepath):
        print(f"Error: The file '{filepath}' does not exist.")
        exit(1)

    # Read usernames from the file
    usernames = read_usernames_from_file(filepath)
    if not usernames:
        print("No usernames were found in the file.")
        exit(1)

    # Counter for all subreddits
    total_subreddits_counter = Counter()

    # Fetch subreddits for each user and update the counter
    for username in usernames:
        user_subreddits = fetch_user_subreddits(client, praw_client, username)
        total_subreddits_counter.update(user_subreddits)

    # Get the top 50 subreddits by comment count
    top_50_subreddits = total_subreddits_counter.most_common(50)

    # Print the top 50 subreddits and their counts
    print("Top 50 subreddits:")
    for subreddit, count in top_50_subreddits:
        print(f"{subreddit}: {count}")

