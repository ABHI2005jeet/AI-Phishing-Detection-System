import requests # type: ignore

def check_phishtank(url):

    try:

        api_url = "https://checkurl.phishtank.com/checkurl/"

        data = {
            "url": url,
            "format": "json"
        }

        response = requests.post(api_url, data=data)

        result = response.json()

        if result["results"]["in_database"]:
            return True

    except:
        pass

    return False