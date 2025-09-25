import json
from scraper import scrape_user


def test():
    user_data = scrape_user("MrYBOTEAAAAJ") # Konrad
    print(json.dumps(user_data, indent=2))


if __name__ == "__main__":
    test()
