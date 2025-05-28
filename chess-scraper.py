import string
import requests
import random
from bs4 import BeautifulSoup

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
    """Fetch stats for a given username using Chess.com API."""
    url = f"https://api.chess.com/pub/player/{username}/stats"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve stats for {username}")
        return None

    stats = response.json()
    rapid_elo = stats.get('chess_rapid', {}).get('last', {}).get('rating', 'Not Available')
    rapid_games = stats.get('chess_rapid', {}).get('record', {}).get('win', 0) + \
                  stats.get('chess_rapid', {}).get('record', {}).get('loss', 0) + \
                  stats.get('chess_rapid', {}).get('record', {}).get('draw', 0)
    
    return {'username': username, 'Rapid ELO': rapid_elo, 'Games Played': rapid_games}

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
