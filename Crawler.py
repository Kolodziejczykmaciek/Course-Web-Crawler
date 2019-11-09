import requests

def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass

target_url = "google.com"

with open("subdomains-wodlist.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()                     #delete the "/n" at the end of each line
        test_url = word + "." + target_url
        response = request(test_url)
        if response:
            print("[+] Discoverd subdomain --> " + test_url )

            #######gicik
