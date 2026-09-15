import time
import requests
from bs4 import BeautifulSoup

REQUEST_DELAY_SECONDS = 2

def check_instagram_username(username):
    base_url = f"https://www.instagram.com/{username}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    try:
        response = requests.get(base_url, headers=headers, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            og_title = soup.find('meta', property='og:title')

            if og_title is None:
                return False, None
            else:
                return True, base_url
        elif response.status_code == 404:
            return False, None
        else:
            return None, None
    except requests.RequestException:
        return None, None

def main():
    usernames_file = "usernames.txt"  # Replace with the actual name of your .txt file containing usernames
    results_file = "results.txt"  # Tested usernames are appended here as "username - free"/"username - taken"

    with open(usernames_file, "r") as file:
        usernames = [line.strip() for line in file if line.strip()]

    unresolved = []
    with open(results_file, "a") as results:
        for i, username in enumerate(usernames):
            exists, profile_url = check_instagram_username(username)

            if exists is True:
                print(f"Username '{username}' is taken. Profile: {profile_url}")
                results.write(f"{username} - taken\n")
            elif exists is False:
                print(f"Username '{username}' is available.")
                results.write(f"{username} - free\n")
            else:
                print(f"Username '{username}': could not verify (request failed or was blocked), left in {usernames_file} for a retry.")
                unresolved.append(username)

            if i < len(usernames) - 1:
                time.sleep(REQUEST_DELAY_SECONDS)

    with open(usernames_file, "w") as file:
        file.writelines(f"{username}\n" for username in unresolved)

if __name__ == "__main__":
    main()
