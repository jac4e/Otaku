import json
from resources.lib.ui import control, client


def div_flavor(f):
    def wrapper(*args, **kwargs):
        if control.getSetting("general.divflavors") == "true":
            mal_dub = _get_mal_dub()

            return f(dub=mal_dub, *args, **kwargs)

        return f(*args, **kwargs)

    return wrapper


def _get_mal_dub():
    try:
        mal_dub = open(control.maldubFile, 'r+')
        mal_dub = json.load(mal_dub)
    except:
        file_to_dump = open(control.maldubFile, 'a+')
        mal_dub = client.request('https://armkai.vercel.app/api/maldub')
        mal_dub = json.loads(mal_dub)
        json.dump(mal_dub, file_to_dump, indent=4)

    return mal_dub
