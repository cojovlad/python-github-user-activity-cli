import urllib.request
import json
import argparse
from collections import defaultdict

# Requests the data for a specific GitHub user when using: python GithubUserActivity.py (username)
def fetch_user_activity(username):
    # Creation of URL
    url = f'https://api.github.com/users/{username}/events'
    try:
        # Call to GitHub API which gives a 200 if ok or catches corresponding errors
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                return json.load(response)
            # Rate limit exceeded, as github gives access to 60 calls for non connected users
            elif response.status == 403:
                print("Error: API rate limit exceeded.")
                reset_time = response.headers.get('X-RateLimit-Reset')
                print(f"Rate limit will reset at: {reset_time}")
    # Error handling based on response
    except urllib.error.HTTPError as e:
        print(f"Error: {e.reason}")
    except urllib.error.URLError as e:
        print(f"Network Error: {e.reason}")
    return None

# This uses the data we got from fetch_user_activity and parses with the data we want to display
def parse_activity(events):
    # If there are no events, we return early
    if not events:
        print("No activity found.")
        return

    # Create a dictionary to store events by repo
    events_by_repo = defaultdict(lambda: defaultdict(list))

    # Group events first by repo and then by event type
    for event in events:
        repo_name = event.get("repo", {}).get("name", "Unknown Repository")
        event_type = event.get("type", "Unknown Event")
        events_by_repo[repo_name][event_type].append(event)

    # Now iterate over each repo and event type, sorting events by 'created_at'
    for repo_name, event_types in events_by_repo.items():
        print(f"\n--- Repository: {repo_name} ---")

        # Iterate over each event type (e.g., PushEvent, IssuesEvent)
        for event_type, event_list in event_types.items():
            print(f"\n  --- Event Type: {event_type.replace('Event', '')} ---")

            # Sort events by 'created_at' (event time)
            event_list.sort(key=lambda x: x['created_at'], reverse=False)

            # Print each event's details
            for event in event_list:
                created_at = event.get("created_at", "Unknown Time")
                if event_type == "PushEvent":
                    commits = event.get("payload", {}).get("commits", [])
                    for commit in commits:
                        commit_message = commit.get("message", "No commit message")
                        print(f"    - Commit at {created_at}: {commit_message}")
                else:
                    print(f"    - {event_type.replace('Event', '')} at {created_at}")

# Main function that runs the script
def main():
    # Description of the script
    parser = argparse.ArgumentParser(description="Fetch GitHub user recent activity.")
    # Here we use parser to add an argument for the data.
    parser.add_argument("username", help="GitHub username")
    # This gets the data we input in the terminal and parses it
    args = parser.parse_args()  # Parse the arguments

    print(f"Fetching activity for user: {args.username}")
    # We use the data fetch and the parser to display the GitHub user data
    events = fetch_user_activity(args.username)
    if events:
        parse_activity(events)

if __name__ == "__main__":
    main()
