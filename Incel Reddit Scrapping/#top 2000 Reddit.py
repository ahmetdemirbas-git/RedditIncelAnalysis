#top 1000 Reddit
import json
from collections import Counter

# Function to process multiple data files and extract the top 1000 users
def extract_top_users(filepaths, top_n=2000):
    user_counter = Counter()

    # Loop through each file
    for filepath in filepaths:
        # Open and read the data file
        with open(filepath, 'r') as file:
            for line in file:
                # Parse each line as a JSON object
                comment = json.loads(line.strip())
                # Extract the author (username)
                author = comment.get('author', '')
                if author:
                    user_counter[author] += 1
    
    # Get the top N users by comment count
    top_users = user_counter.most_common(top_n)

    return top_users

def write_top_users_to_file(top_users, filename):
    with open(filename, 'w') as file:
        for user, count in top_users:
            file.write(f"{user}: {count}\n")

# Example usage
if __name__ == "__main__":
    # List of file paths for the 9 subreddits
    filepaths = [
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
    
    top_users = extract_top_users(filepaths)
    
    # Write top users to a file
    output_filename = 'top_2000_incel_users.txt'
    write_top_users_to_file(top_users, output_filename)
    
    print(f"Top 2000 users have been written to {output_filename}")
