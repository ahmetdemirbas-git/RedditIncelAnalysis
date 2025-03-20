import json
from collections import Counter
import os

# Function to remove subreddit names and filter out "AutoModerator"
def cleanse_data(input_filepath, output_filepath):
    users = set()
    with open(input_filepath, 'r') as file:
        for line in file:
            # Split line to get subreddit and users
            parts = line.split(': ')
            if len(parts) == 2:
                subreddit_users = parts[1].strip().split(', ')
                for user in subreddit_users:
                    if user != "AutoModerator":
                        users.add(user)
    
    with open(output_filepath, 'w') as file:
        for user in users:
            file.write(f"{user}\n")

# Function to check if users are in incel subreddit dumps and remove them
def remove_incel_users(cleaned_filepath, incel_filepaths, final_output_filepath):
    incel_users = set()
    
    # Collect all incel users from incel subreddit dumps
    for filepath in incel_filepaths:
        with open(filepath, 'r') as file:
            for line in file:
                comment = json.loads(line.strip())
                author = comment.get('author', '')
                if author:
                    incel_users.add(author)
    
    # Read the cleaned users and filter out incel users
    with open(cleaned_filepath, 'r') as file:
        users = file.readlines()
    
    final_users = [user.strip() for user in users if user.strip() not in incel_users]
    
    # Write the final users to a file
    with open(final_output_filepath, 'w') as file:
        for user in final_users:
            file.write(f"{user}\n")

# Main script
if __name__ == "__main__":
    # Step 1: Cleanse the data
    input_filepath = '/Users/erdem/Desktop/top_commenters_per_subreddit.txt'
    cleaned_filepath = 'cleaned_top_commenters.txt'
    cleanse_data(input_filepath, cleaned_filepath)
    
    # Step 2: Remove users in incel subreddit dumps
    incel_filepaths = [
        '/Users/erdem/Desktop/BrainCells/reddit/subreddits23/Braincels_comments',
        '/Users/erdem/Desktop/BrainCells/reddit/subreddits23/antifeminists_comments',
        '/Users/erdem/Desktop/BrainCells/reddit/subreddits23/ForeverAlone_comments',
        '/Users/erdem/Desktop/BrainCells/reddit/subreddits23/hapas_comments',
        '/Users/erdem/Desktop/BrainCells/reddit/subreddits23/Incels_comments',
        '/Users/erdem/Desktop/BrainCells/reddit/subreddits23/MensRights_comments',
        '/Users/erdem/Desktop/BrainCells/reddit/subreddits23/MGTOW_comments',
        '/Users/erdem/Desktop/BrainCells/reddit/subreddits23/ProMaleCollective_comments',
        '/Users/erdem/Desktop/BrainCells/reddit/subreddits23/TheRedPill_comments'
    ]
    final_output_filepath = 'final_cleaned_top_commenters.txt'
    remove_incel_users(cleaned_filepath, incel_filepaths, final_output_filepath)
    
    print(f"Cleaned data has been saved to {final_output_filepath}")
