import requests
import re


#                     spotify:album:1AoWfy7iH5J5Y7Exn07s2q
# https://open.spotify.com/playlist/37i9dQZF1E39AlqC6bMfws?si=3po-KekaRIWeWcIB2BY6IA
#                  spotify:playlist:37i9dQZF1E39AlqC6bMfws

def parseURI(uri):

    if uri.startswith("spotify:") and uri.count(':') == 2 and len(uri.split(":")[2]) == 22:
        # assume spotify URI is passed
        return uri
    elif "spotify.com/" in uri:
        # assume web uri is passed
        # create spotify uri
        pattern = r"\/\w+\/\w{22}"
        res = re.search(pattern, uri)
        if res:
            return "spotify" + res.group().replace("/", ":")

    return None


def get_code(uri):

    r = requests.get('https://scannables.scdn.co/uri/plain/svg/000000/white/1000/' + uri)
    
    if not r.status_code == 200:
        return None

    pattern = re.compile(r'(?<=height=")[0-9]{2}(?=\.00)')
    code = pattern.findall(r.text)
    return [int(v) for v in code]