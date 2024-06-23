# reddit-username-retriever
 Extract a Reddit user's comment history and save it to a text file using PRAW (Python Reddit API Wrapper)

## Requirements

To run this script, you need:

- Python 3.x
- `praw` library (`pip install praw`)
- Reddit API credentials (`client_id`, `client_secret`, `user_agent`) obtained from Reddit

## Installation

1. Clone the repository:
git clone https://github.com/your/repository.git
cd repository-folder
2. Install dependencies:
pip install praw
3. Obtain Reddit API credentials:
- Create a Reddit account if you don't have one.
- Register an application on Reddit to obtain `client_id`, `client_secret`, and set `user_agent` as required by Reddit's API.
4. Create a `credentials.py` file in the same directory as `main.py`:

- client_id = 'your_client_id'

- client_secret = 'your_client_secret'

- user_agent = 'your_user_agent'

## Usage

1. Run the script:
python main.py
2. Enter the Reddit username when prompted.
3. Enter the number of comments to fetch.
4. The script will fetch comments from Reddit and save them to a file named `username_comments.txt` in the current directory.