import redditwarp.SYNC
import praw
import os
import prawcore

# Function to read usernames from a file
def read_usernames_from_file(filepath):
    usernames = []
    try:
        with open(filepath, 'r') as file:
            for line in file:
                if ':' in line:
                    username = line.split(':')[0].strip()
                    usernames.append(username)
                else:
                    usernames.append(line.strip())
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
    except Exception as e:
        print(f"An error occurred while reading the file '{filepath}': {e}")
    return usernames

# Function to check if a user is banned, suspended, or shadowbanned
def check_user_status(praw_client, username):
    try:
        redditor = praw_client.redditor(username)
        if hasattr(redditor, 'fullname'):
            return True
        elif hasattr(redditor, 'is_suspended'):
            print(f"User {username} is suspended.")
            return False
        else:
            print(f"User {username} is shadowbanned or not found.")
            return False
    except prawcore.exceptions.NotFound:
        print(f"User {username} not found (404 error).")
        return False
    except Exception as e:
        print(f"An error occurred while checking status for user {username}: {e}")
        return False

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

    # List to hold unbanned users
    unbanned_users = []

    # Check the status of each user
    for username in usernames:
        if check_user_status(praw_client, username):
            unbanned_users.append(username)

    # Save the unbanned users to a file
    output_filename = 'unbanned_users.txt'
    with open(output_filename, 'w') as file:
        for user in unbanned_users:
            file.write(f"{user}\n")

    print(f"Unbanned users have been written to {output_filename}")
