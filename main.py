import praw
import datetime
import credentials

# Reddit API credentials
client_id = credentials.client_id
client_secret = credentials.client_secret
user_agent = credentials.user_agent


def fetch_comments(username, limit=1000):
    # Initialize the Reddit instance
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent)

    # Get the Redditor object for the given username
    redditor = reddit.redditor(username)

    # Fetch the comments
    comments = []
    try:
        for comment in redditor.comments.new(limit=limit):
            comment_details = {
                'body': comment.body,
                'subreddit': comment.subreddit.display_name,
                'created_utc': comment.created_utc,
                'thread_title': comment.submission.title
            }
            comments.append(comment_details)
    except Exception as e:
        print(f"An error occurred: {e}")

    return comments


def save_comments_to_file(comments, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for comment in comments:
            created_time = datetime.datetime.utcfromtimestamp(comment['created_utc'])
            file.write(f"Thread Title: {comment['thread_title']}\n")
            file.write(f"Subreddit: {comment['subreddit']}\n")
            file.write(f"Date (UTC): {created_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"Comment:\n{comment['body']}\n")
            file.write("\n---\n\n")


if __name__ == "__main__":
    username = input("Enter the Reddit username: ")
    limit = int(input("Enter the number of comments to fetch: "))
    filename = f"{username}_comments.txt"

    comments = fetch_comments(username, limit)
    if comments:
        save_comments_to_file(comments, filename)
        print(f"Comments have been saved to {filename}")
    else:
        print("No comments found or an error occurred.")
