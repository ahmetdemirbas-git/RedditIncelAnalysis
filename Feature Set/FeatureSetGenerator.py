import redditwarp.SYNC
import praw
import os
import prawcore
from collections import Counter

# Function to read usernames from a file
def read_usernames_from_file(filepath):
    usernames = []
    try:
        with open(filepath, 'r') as file:
            usernames = [line.strip() for line in file]
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
    except Exception as e:
        print(f"An error occurred while reading the file '{filepath}': {e}")
    return usernames

# Function to fetch the top subreddits a user has commented in
def fetch_top_subreddits(client, praw_client, username, comment_limit=800, top_n=50):
    subreddits = Counter()
    try:
        redditor = praw_client.redditor(username)
        
        if hasattr(redditor, 'fullname'):
            print(username)
            comments = client.p.user.pull.comments(username, comment_limit)
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
    
    top_subreddits = subreddits.most_common(top_n)
    return top_subreddits

# Function to process user lists and save top subreddits to a file
def process_users_and_save_to_file(client, praw_client, input_filepath, output_filepath, comment_limit=800, top_n=50):
    usernames = read_usernames_from_file(input_filepath)
    if not usernames:
        print("No usernames were found in the file.")
        return

    with open(output_filepath, 'w') as output_file:
        for username in usernames:
            top_subreddits = fetch_top_subreddits(client, praw_client, username, comment_limit, top_n)
            subreddit_str = ', '.join([f"{subreddit} ({count})" for subreddit, count in top_subreddits])
            output_file.write(f"{username}: {subreddit_str}\n")

# Main script
if __name__ == "__main__":
    print("start")
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

    # Input file names
    unbanned_incel_filename = '/Users/erdem/Desktop/unbanned_users.txt'
    unbanned_non_incel_filename = '/Users/erdem/Desktop/final_cleaned_top_commenters.txt'

    # Output file names
    incel_output_filename = 'top_subreddits_unbanned_incel_users.txt'
    non_incel_output_filename = 'top_subreddits_unbanned_non_incel_users.txt'

    # Process incel users
    process_users_and_save_to_file(client, praw_client, unbanned_incel_filename, incel_output_filename)

    # Process non-incel users
    process_users_and_save_to_file(client, praw_client, unbanned_non_incel_filename, non_incel_output_filename)

    print("Top subreddits for unbanned users have been written to the output files.")
