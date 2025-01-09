import urllib.request
import json
import argparse

#Requests the data for a specific GitHub user when using: python GithubUserActivity.py (username)
def fetch_user_activity(username):
    #Creation of URL
    url = f'https://api.github.com/users/{username}/events'
    try:
        #Call to GitHub api which gives a 200 if ok or catches corresponding errors
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                return json.load(response)
    #Error handling based on response
    except urllib.error.HTTPError as e:
        print(f"Error: {e.reason}")
    except urllib.error.URLError as e:
        print(f"Network Error: {e.reason}")
    return None

#This uses the data we got from fetch_user_activity and parses with the data we want to display
def parse_activity(events):
    #If there are no events, we return early
    if not events:
        print("No activity found.")
        return
    #Here is where the parsing happens using data we have from the json
    for event in events:
        event_type = event.get("type", "Unknown Event")
        repo_name = event.get("repo", {}).get("name", "Unknown Repository")
        commit_name = event.get("commit", {}).get("name", "Unknown Commit")
        #We print with a readable format, removing the word "Event" and giving data about the repository name and its commits based if it has a push event
        if event_type == "PushEvent":
            commits = event.get("payload", {}).get("commits", [])
            if commits:
                for commit in commits:
                    commit_message = commit.get("message", "No commit message")
                    print(f"- {event_type.replace('Event', '')} in {repo_name}: {commit_message}")
            else:
                print(f"- {event_type.replace('Event', '')} in {repo_name} with no commits.")
        else:
            print(f"- {event_type.replace('Event', '')} in {repo_name}")

#Main function that runs the script
def main():
    #Description of the script
    parser = argparse.ArgumentParser(description="Fetch GitHub user recent activity.")
    #Here we use parser to add an argument for the data.
    parser.add_argument("username", help="GitHub username")
    #This gets the data we input in the terminal and parses it
    args = parser.parse_args()  # Parse the arguments

    print(f"Fetching activity for user: {args.username}")
    #We use the data fetch and the parser to display the GitHub user data
    events = fetch_user_activity(args.username)
    if events:
        parse_activity(events)

if __name__ == "__main__":
    main()
