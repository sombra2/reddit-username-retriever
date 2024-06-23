import praw
import datetime
import credentials
from collections import Counter

# Reddit API credentials
client_id = credentials.client_id
client_secret = credentials.client_secret
user_agent = credentials.user_agent


def fetch_comments(username):
    # Initialize the Reddit instance
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent)

    # Get the Redditor object for the given username
    redditor = reddit.redditor(username)

    # Fetch all comments to determine total comments and date range
    comments = list(redditor.comments.new(limit=None))

    if not comments:
        return [], 0, None, None

    total_comments = len(comments)
    oldest_comment_date = min(comment.created_utc for comment in comments)
    newest_comment_date = max(comment.created_utc for comment in comments)

    return comments, total_comments, oldest_comment_date, newest_comment_date


def fetch_comments_limit(username, limit):
    # Initialize the Reddit instance
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent)

    # Get the Redditor object for the given username
    redditor = reddit.redditor(username)

    # Fetch specified number of comments
    comments = list(redditor.comments.new(limit=limit))

    return comments


def calculate_stats(comments):
    if not comments:
        return 0, None, None, 0, 0, None

    num_comments = len(comments)
    oldest_comment = min(comment.created_utc for comment in comments)
    newest_comment = max(comment.created_utc for comment in comments)
    total_upvotes = sum(comment.ups for comment in comments)
    total_downvotes = sum(comment.downs for comment in comments)

    # Find the most active subreddit
    subreddit_counts = Counter(comment.subreddit.display_name for comment in comments)
    most_active_subreddit = subreddit_counts.most_common(1)[0][0]

    return num_comments, oldest_comment, newest_comment, total_upvotes, total_downvotes, most_active_subreddit


def save_comments_to_file(comments, filename, username, comment_option, limit=None):
    # Calculate statistics including most active subreddit
    num_comments, oldest_comment, newest_comment, total_upvotes, total_downvotes, most_active_subreddit = calculate_stats(comments)

    # Convert timestamps to datetime objects
    oldest_date = datetime.datetime.utcfromtimestamp(oldest_comment).strftime('%Y-%m-%d %H:%M:%S') if oldest_comment else None
    newest_date = datetime.datetime.utcfromtimestamp(newest_comment).strftime('%Y-%m-%d %H:%M:%S') if newest_comment else None

    # Write to file
    with open(filename, 'w', encoding='utf-8') as file:
        # Write header with statistics
        file.write(f"The parsed user {username} has written {num_comments} comments\n")
        file.write(f"For the dates parsed {oldest_date} to {newest_date}\n")
        file.write(f"And has accrued a total of {total_upvotes} upvotes and {total_downvotes} downvotes\n")
        file.write(f"The user's most active subreddit for the period is {most_active_subreddit}\n\n")

        # Write comments
        for comment in comments:
            created_time = datetime.datetime.utcfromtimestamp(comment.created_utc)
            file.write(f"Thread Title: {comment.submission.title}\n")
            file.write(f"Permalink: https://reddit.com{comment.permalink}\n")
            file.write(f"Subreddit: {comment.subreddit.display_name}\n")
            file.write(f"Date (UTC): {created_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"Upvotes: {comment.ups} | Downvotes: {comment.downs}\n")
            file.write(f"Comment:\n{comment.body}\n")
            file.write("\n---\n\n")


if __name__ == "__main__":
    username = input("Enter the Reddit username: ")

    # Fetch all comments to get total comments and date range
    comments_all, total_comments, oldest_comment_date, newest_comment_date = fetch_comments(username)

    if not comments_all:
        print("No comments found for the user or an error occurred.")
        exit()

    oldest_date = datetime.datetime.utcfromtimestamp(oldest_comment_date).strftime('%Y-%m-%d %H:%M:%S') if oldest_comment_date else None
    newest_date = datetime.datetime.utcfromtimestamp(newest_comment_date).strftime('%Y-%m-%d %H:%M:%S') if newest_comment_date else None

    print(f"The user '{username}' has written {total_comments} comments.")
    print(f"The oldest comment is from {oldest_date} and the newest comment is from {newest_date}.")

    comment_option = input("Fetch [a]ll comments or specify [n]umber of comments to fetch (a/n): ").lower()

    if comment_option == 'a':
        comments = comments_all
        limit = None  # No limit specified when fetching all comments
        filename = f"{username}_all_comments.txt"
    elif comment_option == 'n':
        limit = int(input("Enter the number of comments to fetch: "))
        comments = fetch_comments_limit(username, limit)
        filename = f"{username}_comments_{limit}.txt"
    else:
        print("Invalid option. Please enter 'a' or 'n'.")
        exit()

    if comments:
        save_comments_to_file(comments, filename, username, comment_option, limit)
        print(f"Comments have been saved to {filename}")
    else:
        print("No comments found or an error occurred.")
