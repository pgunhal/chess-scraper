import string
import requests
import re
import json
from bs4 import BeautifulSoup
import random

def generate_random_string(length=3):
    """Generate a random string of letters and digits."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def get_user_data(query):
    """Fetch user profiles based on a random query."""
    url = f"https://www.chess.com/members/search?phrase={query}&sortBy=best-match"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve data for query: {query}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    user_links = soup.find_all('a', class_='members-list-username')
    users = [link.text.strip() for link in user_links]
    return users


def get_user_stats(username):
    """Fetch stats for a given username."""
    url = f"https://www.chess.com/stats/overview/{username}/0"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve stats for {username}")
        return None

    # Extracting JavaScript object containing the stats
    pattern = re.compile(r'window\.chesscom\.stats\s*=\s*(\{.*?\});', re.DOTALL)
    match = pattern.search(response.text)
    if not match:
        print("Failed to find JavaScript data for user stats.")
        return None

    # Clean up JSON string to make it parsable
    json_string = match.group(1)
    # Fix common JSON issues: ensure all keys are in double quotes
    json_string = re.sub(r'([,{\s])(\w+)(:)', r'\1"\2"\3', json_string)
    json_string = json_string.replace("'", '"')  # replace all single quotes with double quotes

    # Manually extract Rapid ELO and games played from the JSON string
    rapid_elo_match = re.search(r'"game_live_rapid":\{"delta":.*?"last_rating":(\d+)', json_string)
    game_count_match = re.search(r'"game_count":(\d+)', json_string)

    rapid_elo = rapid_elo_match.group(1) if rapid_elo_match else "Not Available"
    game_count = game_count_match.group(1) if game_count_match else "Not Available"

    return {'username': username, 'Rapid ELO': rapid_elo, 'Games Played': game_count}


def main():
    with open('test.txt', 'w') as data:  # Open file for writing
        for _ in range(30):  # Generate n different random sequences
            random_query = generate_random_string()
            usernames = get_user_data(random_query)
            if not usernames:
                print(f"No users found for query: {random_query}")
                continue
            selected_username = random.choice(usernames)  # Pick a random user from the list
            stats = get_user_stats(selected_username)
            if stats:
                data.write(f"{stats['username']} - Rapid ELO: {stats['Rapid ELO']}, Games Played: {stats['Games Played']}\n")
                print(stats)


# Run the script
main()
