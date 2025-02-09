import itertools
import json
import time

from resources.lib.ui import control
from resources.lib.WatchlistFlavor.WatchlistFlavorBase import \
    WatchlistFlavorBase
from six.moves import urllib_parse


class KitsuWLF(WatchlistFlavorBase):
    _URL = "https://kitsu.io/api"
    _TITLE = "Kitsu"
    _NAME = "kitsu"
    _IMAGE = "kitsu.png"
    _mapping = None

    def login(self):
        params = {
            "grant_type": "password",
            "username": self._auth_var,
            "password": self._password
        }
        resp = self._post_request(self._to_url("oauth/token"), params=params, json='')

        if not resp:
            return

        data = json.loads(resp)
        self._token = data['access_token']
        resp2 = self._get_request(self._to_url("edge/users"), headers=self.__headers(), params={'filter[self]': True})
        data2 = json.loads(resp2)["data"][0]

        login_data = {
            'username': data2["attributes"]["name"],
            'userid': data2['id'],
            'token': data['access_token'],
            'refresh': data['refresh_token'],
            'expiry': str(time.time() + int(data['expires_in']))
        }

        return login_data

    def refresh_token(self, control):
        params = {
            "grant_type": "refresh_token",
            "refresh_token": control.getSetting('kitsu.refresh'),
        }
        resp = self._post_request(self._to_url("oauth/token"), params=params, json='')

        if not resp:
            return

        data = json.loads(resp)
        control.setSetting('kitsu.token', data['access_token'])
        control.setSetting('kitsu.refresh', data['refresh_token'])
        control.setSetting('kitsu.expiry', str(time.time() + int(data['expires_in'])))

    def __headers(self):
        headers = {
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json',
            'Authorization': "Bearer {}".format(self._token),
        }

        return headers

    def _handle_paging(self, hasNextPage, base_url, page):
        if not hasNextPage:
            return []
        next_page = page + 1
        name = "Next Page (%d)" % (next_page)
        parsed = urllib_parse.urlparse(hasNextPage)
        offset = urllib_parse.parse_qs(parsed.query)['page[offset]'][0]
        return self._parse_view({'name': name, 'url': base_url % (offset, next_page), 'image': 'next.png', 'plot': None, 'fanart': 'next.png'})

    def watchlist(self):
        params = {"filter[user_id]": self._user_id}
        url = self._to_url("edge/library-entries")
        return self._process_watchlist_status_view(url, params, "watchlist/%d", page=1)

    def _base_watchlist_status_view(self, res):
        base = {
            "name": res[0],
            "url": 'watchlist_status_type/%s/%s' % (self._NAME, res[1]),
            "image": res[0].lower() + '.png',
            "plot": '',
        }

        return self._parse_view(base)

    def _process_watchlist_status_view(self, url, params, base_plugin_url, page):
        all_results = list(map(self._base_watchlist_status_view, self.__kitsu_statuses()))
        all_results = list(itertools.chain(*all_results))
        return all_results

    def __kitsu_statuses(self):
        statuses = [
            ("Next Up", "current?next_up=true"),
            ("Current", "current"),
            ("Want to Watch", "planned"),
            ("Completed", "completed"),
            ("On Hold", "on_hold"),
            ("Dropped", "dropped"),
        ]
        return statuses

    def get_watchlist_status(self, status, next_up, offset=0, page=1):
        url = self._to_url("edge/library-entries")

        params = {
            "fields[anime]": "titles,canonicalTitle,posterImage,episodeCount,synopsis,episodeLength,subtype,averageRating,ageRating,youtubeVideoId",
            "filter[user_id]": self._user_id,
            "filter[kind]": "anime",
            "filter[status]": status,
            "include": "anime,anime.mappings,anime.mappings.item",
            "page[limit]": "50",
            "page[offset]": offset,
            "sort": self.__get_sort(),
        }

        return self._process_watchlist_view(url, params, next_up, "watchlist_status_type_pages/kitsu/%s/%%s/%%d" % status, page)

    def _process_watchlist_view(self, url, params, next_up, base_plugin_url, page):
        result = self._get_request(url, headers=self.__headers(), params=params)
        result = json.loads(result)
        _list = result["data"]

        if not result.get('included'):
            result['included'] = []

        el = result["included"][:len(_list)]
        # self._mapping = filter(lambda x: x['type'] == 'mappings', result['included'])
        self._mapping = [x for x in result['included'] if x['type'] == 'mappings']

        if next_up:
            all_results = list(map(self._base_next_up_view, _list, el))
        else:
            all_results = list(map(self._base_watchlist_view, _list, el))

        all_results = list(itertools.chain(*all_results))

        all_results += self._handle_paging(result['links'].get('next'), base_plugin_url, page)
        return all_results

    def _base_watchlist_view(self, res, eres):
        _id = eres['id']
        mal_id = self._mapping_mal(_id)
        info = {}

        try:
            info['plot'] = eres['attributes'].get('synopsis')
        except:
            pass

        try:
            info['title'] = eres["attributes"]["titles"].get(self.__get_title_lang(), eres["attributes"]['canonicalTitle'])
        except:
            pass

        try:
            info['duration'] = eres['attributes']['episodeLength'] * 60
        except:
            pass

        try:
            info['rating'] = float(eres['attributes']['averageRating']) / 10
        except:
            pass

        try:
            info['mpaa'] = eres['attributes']['ageRating']
        except:
            pass

        try:
            info['trailer'] = 'plugin://plugin.video.youtube/play/?video_id={0}'.format(eres['attributes']['youtubeVideoId'])
        except:
            pass

        info['mediatype'] = 'tvshow'

        base = {
            "name": '%s - %d/%d' % (eres["attributes"]["titles"].get(self.__get_title_lang(), eres["attributes"]['canonicalTitle']),
                                    res["attributes"]['progress'],
                                    eres["attributes"]['episodeCount'] if eres["attributes"]['episodeCount'] is not None else 0),
            "url": "watchlist_to_ep/%s/%s/%s" % (mal_id, _id, res["attributes"]['progress']),
            "image": eres["attributes"]['posterImage']['large'],
            "plot": info,
        }

        if eres['attributes']['subtype'] == 'movie' and eres['attributes']['episodeCount'] == 1:
            base['url'] = "watchlist_to_movie/%s" % (mal_id)
            base['plot']['mediatype'] = 'movie'
            return self._parse_view(base, False)

        return self._parse_view(base)

    def _base_next_up_view(self, res, eres):
        _id = eres['id']
        mal_id = self._mapping_mal(_id)

        progress = res["attributes"]['progress']
        next_up = progress + 1
        anime_title = eres["attributes"]["titles"].get(self.__get_title_lang(), eres["attributes"]['canonicalTitle'])
        episode_count = eres["attributes"]['episodeCount'] if eres["attributes"]['episodeCount'] is not None else 0
        title = '%s - %d/%d' % (anime_title, next_up, episode_count)
        poster = image = eres["attributes"]['posterImage']['large']
        plot = None

        anilist_id, next_up_meta = self._get_next_up_meta(mal_id, int(progress))
        if next_up_meta:
            url = 'play/%d/%d/' % (anilist_id, next_up)
            if next_up_meta.get('title'):
                title = '%s - %s' % (title, next_up_meta.get('title'))
            if next_up_meta.get('image'):
                image = next_up_meta.get('image')
            plot = next_up_meta.get('plot')

        info = {}

        info['episode'] = next_up

        info['title'] = title

        info['tvshowtitle'] = anime_title

        info['plot'] = plot

        info['mediatype'] = 'episode'

        base = {
            "name": title,
            "url": "watchlist_to_ep/%s/%s/%s" % (mal_id, _id, res["attributes"]['progress']),
            "image": image,
            "plot": info,
            "fanart": image,
            "poster": poster,
        }

        if next_up_meta:
            base['url'] = url
            return self._parse_view(base, False)

        if eres['attributes']['subtype'] == 'movie' and eres['attributes']['episodeCount'] == 1:
            base['url'] = "watchlist_to_movie/%s" % (mal_id)
            base['plot']['mediatype'] = 'movie'
            return self._parse_view(base, False)

        return self._parse_view(base)

    def _mapping_mal(self, kitsu_id):
        mal_id = ''
        for i in self._mapping:
            if i['attributes']['externalSite'] == 'myanimelist/anime':
                if i['relationships']['item']['data']['id'] == kitsu_id:
                    mal_id = i['attributes']['externalId']
                    break

        return mal_id

    def get_watchlist_anime_entry(self, anilist_id):
        kitsu_id = self._get_mapping_id(anilist_id, 'kitsu_id')

        if not kitsu_id:
            return

        url = self._to_url("edge/library-entries")
        params = {
            "filter[user_id]": self._user_id,
            "filter[anime_id]": kitsu_id
        }
        result = self._get_request(url, headers=self.__headers(), params=params)
        result = json.loads(result)
        item_dict = result['data'][0]['attributes']

        anime_entry = {}
        anime_entry['eps_watched'] = item_dict['progress']
        anime_entry['status'] = item_dict['status']
        anime_entry['score'] = item_dict['ratingTwenty']

        return anime_entry

    def watchlist_update(self, anilist_id, episode):
        kitsu_id = self._get_mapping_id(anilist_id, 'kitsu_id')

        if not kitsu_id:
            return

        url = self._to_url("edge/library-entries")
        params = {
            "filter[user_id]": self._user_id,
            "filter[anime_id]": kitsu_id
        }
        scrobble = self._get_request(url, headers=self.__headers(), params=params)
        item_dict = json.loads(scrobble)
        if len(item_dict['data']) == 0:
            return lambda: self.__post_params(url, episode, kitsu_id)

        animeid = item_dict['data'][0]['id']
        return lambda: self.__patch_params(url, animeid, episode)

    def __post_params(self, url, episode, kitsu_id):
        params = {
            "data": {
                "type": "libraryEntries",
                "attributes": {
                    'status': 'current',
                    'progress': int(episode)
                },
                "relationships": {
                    "user": {
                        "data": {
                            "id": self._user_id,
                            "type": "users"
                        }
                    },
                    "anime": {
                        "data": {
                            "id": int(kitsu_id),
                            "type": "anime"
                        }
                    }
                }
            }
        }

        self._post_request(url, headers=self.__headers(), json=params)

    def __patch_params(self, url, animeid, episode):
        params = {
            'data': {
                'id': int(animeid),
                'type': 'libraryEntries',
                'attributes': {
                    'progress': int(episode)}
            }
        }

        self._patch_request("%s/%s" % (url, animeid), headers=self.__headers(), json=params)

    def __get_sort(self):
        sort_types = {
            "Date Updated": "-progressed_at",
            "Progress": "-progress",
            "Title": "anime.titles." + self.__get_title_lang(),
        }

        return sort_types[self._sort]

    def __get_title_lang(self):
        title_langs = {
            "Canonical": "canonical",
            "English": "en",
            "Romanized": "en_jp",
        }

        return title_langs[self._title_lang]

    def watchlist_append(self, anilist_id):
        kitsu_id = self._get_mapping_id(anilist_id, 'kitsu_id')
        if not kitsu_id:
            return
        url = self._to_url("edge/library-entries")
        params = {
            "data": {
                "type": "libraryEntries",
                "attributes": {
                    'status': 'planned',
                },
                "relationships": {
                    "user": {
                        "data": {
                            "id": self._user_id,
                            "type": "users"
                        }
                    },
                    "anime": {
                        "data": {
                            "id": int(kitsu_id),
                            "type": "anime"
                        }
                    }
                }
            }
        }
        result = json.loads(self._post_request(url, headers=self.__headers(), json=params))
        if result.get('data'):
            control.notify('Added to Watchlist')
        return

    def watchlist_remove(self, mal_id):
        kitsu_id = self._get_mapping_id_mal(mal_id, 'kitsu_id')
        if not kitsu_id:
            return
        url = self._to_url("edge/library-entries")
        params = {
            "filter[user_id]": self._user_id,
            "filter[anime_id]": kitsu_id
        }
        result = self._get_request(url, headers=self.__headers(), params=params)
        item_id = json.loads(result).get('data')[0].get('id')
        url = self._to_url("edge/library-entries/%s" % (item_id))
        _ = self._delete_request(url, headers=self.__headers())
        control.notify('Removed from Watchlist')
        return
