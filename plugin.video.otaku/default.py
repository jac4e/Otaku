# -*- coding: utf-8 -*-
"""
    Otaku Add-on

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import pickle

import six
from resources.lib.AniListBrowser import AniListBrowser
from resources.lib.OtakuBrowser import OtakuBrowser
from resources.lib.ui import control, database, player, utils
from resources.lib.ui.router import route, router_process
from resources.lib.WatchlistIntegration import (add_watchlist, set_browser,
                                                watchlist_append,
                                                watchlist_remove,
                                                watchlist_update)

MENU_ITEMS = [
    (control.lang(50000), "anilist_airing", 'airing anime calendar.png'),
    (control.lang(50006), "anilist_airing_anime", 'airing anime.png'),
    (control.lang(50001), "movies", 'movies.png'),
    (control.lang(50002), "tv_shows", 'tv shows.png'),
    (control.lang(50007), "anilist_trending_this_year", 'trending this year.png'),
    (control.lang(50008), "anilist_popular_this_year", 'popular this year.png'),
    (control.lang(50009), "anilist_voted_this_year", 'voted this year.png'),
    (control.lang(50010), "anilist_completed_this_year", 'completed this year.png'),
    (control.lang(50011), "anilist_upcoming_next_year", 'upcoming next year.png'),
    (control.lang(50012), "anilist_trending_this_season", 'trending this season.png'),
    (control.lang(50013), "anilist_popular_this_season", 'popular this season.png'),
    (control.lang(50014), "anilist_voted_this_season", 'voted this season.png'),
    (control.lang(50015), "anilist_completed_this_season", 'completed this season.png'),
    (control.lang(50016), "anilist_upcoming_next_season", 'upcoming next season.png'),
    (control.lang(50017), 'anilist_all_time_trending', 'all time trending.png'),
    (control.lang(50018), 'anilist_all_time_popular', 'all time popular.png'),
    (control.lang(50019), 'anilist_all_time_voted', 'all time voted.png'),
    (control.lang(50020), 'anilist_top_100_anime', 'top 100 anime.png'),
    (control.lang(50003), "anilist_genres", 'genres & tags.png'),
    (control.lang(50004), "search_history", 'search.png'),
    (control.lang(50005), "tools", 'tools.png'),
]
_TITLE_LANG = control.getSetting("titlelanguage")
_BROWSER = OtakuBrowser()
_ANILIST_BROWSER = AniListBrowser(_TITLE_LANG)


@route('movies')
def MOVIES_MENU(payload, params):
    MOVIES_ITEMS = [
        (control.lang(50006), "anilist_airing_anime_movie", 'airing anime.png'),
        (control.lang(50007), "anilist_trending_this_year_movie", 'trending this year.png'),
        (control.lang(50008), "anilist_popular_this_year_movie", 'popular this year.png'),
        (control.lang(50009), "anilist_voted_this_year_movie", 'voted this year.png'),
        (control.lang(50010), "anilist_completed_this_year_movie", 'completed this year.png'),
        (control.lang(50011), "anilist_upcoming_next_year_movie", 'upcoming next year.png'),
        (control.lang(50012), "anilist_trending_this_season_movie", 'trending this season.png'),
        (control.lang(50013), "anilist_popular_this_season_movie", 'popular this season.png'),
        (control.lang(50014), "anilist_voted_this_season_movie", 'voted this season.png'),
        (control.lang(50015), "anilist_completed_this_season_movie", 'completed this season.png'),
        (control.lang(50016), "anilist_upcoming_next_season_movie", 'upcoming next season.png'),
        (control.lang(50017), 'anilist_all_time_trending_movie', 'all time trending.png'),
        (control.lang(50018), 'anilist_all_time_popular_movie', 'all time popular.png'),
        (control.lang(50019), 'anilist_all_time_voted_movie', 'all time voted.png'),
        (control.lang(50020), 'anilist_top_100_anime_movie', 'top 100 anime.png'),
        (control.lang(50003), "anilist_genres", 'genres & tags.png'),
        (control.lang(50004), "search_history", 'search.png'),
    ]

    MOVIES_ITEMS_SETTINGS = MOVIES_ITEMS[:]
    for i in MOVIES_ITEMS:
        if control.getSetting(i[1]) != 'true':
            MOVIES_ITEMS_SETTINGS.remove(i)

    return control.draw_items(
        [utils.allocate_item(name, url, True, image) for name, url, image in MOVIES_ITEMS_SETTINGS],
        contentType="addons",
        draw_cm=False
    )


@route('tv_shows')
def TV_SHOWS_MENU(payload, params):
    TV_SHOWS_ITEMS = [
        (control.lang(50006), "anilist_airing_anime_tv", 'airing anime.png'),
        (control.lang(50007), "anilist_trending_this_year_tv", 'trending this year.png'),
        (control.lang(50008), "anilist_popular_this_year_tv", 'popular this year.png'),
        (control.lang(50009), "anilist_voted_this_year_tv", 'voted this year.png'),
        (control.lang(50010), "anilist_completed_this_year_tv", 'completed this year.png'),
        (control.lang(50011), "anilist_upcoming_next_year_tv", 'upcoming next year.png'),
        (control.lang(50012), "anilist_trending_this_season_tv", 'trending this season.png'),
        (control.lang(50013), "anilist_popular_this_season_tv", 'popular this season.png'),
        (control.lang(50014), "anilist_voted_this_season_tv", 'voted this season.png'),
        (control.lang(50015), "anilist_completed_this_season_tv", 'completed this season.png'),
        (control.lang(50016), "anilist_upcoming_next_season_tv", 'upcoming next season.png'),
        (control.lang(50017), 'anilist_all_time_trending_tv', 'all time trending.png'),
        (control.lang(50018), 'anilist_all_time_popular_tv', 'all time popular.png'),
        (control.lang(50019), 'anilist_all_time_voted_tv', 'all time voted.png'),
        (control.lang(50020), 'anilist_top_100_anime_tv', 'top 100 anime.png'),
        (control.lang(50003), "anilist_genres", 'genres & tags.png'),
        (control.lang(50004), "search_history", 'search.png'),
    ]

    TV_SHOWS_ITEMS_SETTINGS = TV_SHOWS_ITEMS[:]
    for i in TV_SHOWS_ITEMS:
        if control.getSetting(i[1]) != 'true':
            TV_SHOWS_ITEMS_SETTINGS.remove(i)

    return control.draw_items(
        [utils.allocate_item(name, url, True, image) for name, url, image in TV_SHOWS_ITEMS_SETTINGS],
        contentType="addons",
        draw_cm=False
    )


def _add_last_watched():
    anilist_id = control.getSetting("addon.last_watched")
    if not anilist_id:
        return

    try:
        kodi_meta = pickle.loads(database.get_show(anilist_id)['kodi_meta'])
        last_watched = kodi_meta.get('title_userPreferred')
        MENU_ITEMS.insert(0, (
            "%s[I]%s[/I]" % (control.lang(30000), last_watched.encode('utf-8') if six.PY2 else last_watched),
            "animes/%s/null/" % anilist_id,
            kodi_meta['poster']
        ))
    except:
        return


def get_animes_contentType(seasons=None):
    contentType = control.getSetting("contenttype.episodes")
    if seasons and seasons[0]['is_dir']:
        contentType = control.getSetting("contenttype.seasons")

    return contentType


# Will be called at handle_player
def on_percent():
    return int(control.getSetting('watchlist.percent'))


# Will be called when player is stopped in the middle of the episode
def on_stopped():
    return control.yesno_dialog(control.lang(30200), control.lang(30201), control.lang(30202))


# Will be called on genre page
def genre_dialog(genre_display_list):
    return control.multiselect_dialog(control.lang(50003), genre_display_list)


@route('season_correction/*')
def seasonCorrection(payload, params):
    anilist_id, mal_id, filter_lang = payload.split("/")[1:]
    trakt = _BROWSER.search_trakt_shows(anilist_id)
    return control.draw_items(trakt)


@route('season_correction_database/*')
def seasonCorrectionDatabase(payload, params):
    show_id, meta_ids = payload.rsplit("/")
    # clean_show = _BROWSER.clean_show(show_id, meta_ids)
    trakt, content_type = _BROWSER.get_anime_trakt(show_id, True)
    return control.draw_items(trakt, content_type)


@route('trakt_correction/*')
def traktCorrection(payload, params):
    anilist_id, mal_id, filter_lang = payload.split("/")[1:]
    _ANILIST_BROWSER.update_trakt_id(anilist_id)
    return


@route('find_similar/*')
def FIND_SIMILAR(payload, params):
    anilist_id, mal_id, filter_lang = payload.split("/")[1:]
    return control.draw_items(_ANILIST_BROWSER.get_recommendation(anilist_id))


@route('authAllDebrid')
def authAllDebrid(payload, params):
    from resources.lib.debrid.all_debrid import AllDebrid
    AllDebrid().auth()


@route('authDebridLink')
def authDebridLink(payload, params):
    from resources.lib.debrid.debrid_link import DebridLink
    DebridLink().auth()


@route('authRealDebrid')
def authRealDebrid(payload, params):
    from resources.lib.debrid.real_debrid import RealDebrid
    RealDebrid().auth()


@route('authPremiumize')
def authPremiumize(payload, params):
    from resources.lib.debrid.premiumize import Premiumize
    Premiumize().auth()


@route('settings')
def SETTINGS(payload, params):
    return control.settingsMenu()


@route('clear_cache')
def CLEAR_CACHE(payload, params):
    # control.clear_cache()
    return database.cache_clear()


@route('clear_torrent_cache')
def CLEAR_TORRENT_CACHE(payload, params):
    return database.torrent_cache_clear()


@route('rebuild_database')
def REBUILD_DATABASE(payload, params):
    from resources.lib.ui.database_sync import AnilistSyncDatabase
    AnilistSyncDatabase().re_build_database()


@route('wipe_addon_data')
def WIPE_ADDON_DATA(payload, params):
    dialog = control.yesno_dialog(control.lang(30024), control.lang(30025))
    return control.clear_settings(dialog)


@route('change_log')
def CHANGE_LOG(payload, params):
    from resources.lib.ui import control
    return control.getChangeLog()


@route('animes/*')
def ANIMES_PAGE(payload, params):
    anilist_id, mal_id, filter_lang = payload.rsplit("/")
    anime_general, content = _BROWSER.get_anime_init(anilist_id, filter_lang)
    return control.draw_items(anime_general, content)


@route('animes_trakt/*')
def ANIMES_TRAKT(payload, params):
    show_id, season = payload.rsplit("/")
    database._update_season(show_id, season)
    return control.draw_items(_BROWSER.get_trakt_episodes(show_id, season), 'episodes')


@route('run_player_dialogs')
def RUN_PLAYER_DIALOGS(payload, params):
    from resources.lib.ui.player import PlayerDialogs
    try:
        PlayerDialogs().display_dialog()
    except:
        import traceback
        traceback.print_exc()


@route('test')
def TEST(payload, params):
    return


@route('anilist_airing')
def ANILIST_AIRING(payload, params):
    airing = _ANILIST_BROWSER.get_airing()
    from resources.lib.windows.anichart import Anichart

    anime = Anichart(*('anichart.xml', control.ADDON_PATH),
                     get_anime=_BROWSER.get_anime_init, anime_items=airing).doModal()

    if not anime:
        return

    anime, content_type = anime

    return control.draw_items(anime, content_type)


@route('anilist_airing_anime')
def ANILIST_AIRING_ANIME(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_airing_anime())


@route('anilist_airing_anime/*')
def ANILIST_AIRING_ANIME_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_airing_anime(int(payload)))


@route('anilist_trending_this_year')
def ANILIST_TRENDING_THIS_YEAR(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_trending_this_year())


@route('anilist_trending_this_year/*')
def ANILIST_TRENDING_THIS_YEAR_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_trending_this_year(int(payload)))


@route('anilist_popular_this_year')
def ANILIST_POPULAR_THIS_YEAR(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_popular_this_year())


@route('anilist_popular_this_year/*')
def ANILIST_POPULAR_THIS_YEAR_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_popular_this_year(int(payload)))


@route('anilist_voted_this_year')
def ANILIST_VOTED_THIS_YEAR(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_voted_this_year())


@route('anilist_voted_this_year/*')
def ANILIST_VOTED_THIS_YEAR_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_voted_this_year(int(payload)))


@route('anilist_completed_this_year')
def ANILIST_COMPLETED_THIS_YEAR(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_completed_this_year())


@route('anilist_completed_this_year/*')
def ANILIST_COMPLETED_THIS_YEAR_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_completed_this_year(int(payload)))


@route('anilist_upcoming_next_year')
def ANILIST_UPCOMING_NEXT_YEAR(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_upcoming_next_year())


@route('anilist_upcoming_next_year/*')
def ANILIST_UPCOMING_NEXT_YEAR_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_upcoming_next_year(int(payload)))


@route('anilist_trending_this_season')
def ANILIST_TRENDING_THIS_SEASON(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_trending_this_season())


@route('anilist_trending_this_season/*')
def ANILIST_TRENDING_THIS_SEASON_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_trending_this_season(int(payload)))


@route('anilist_popular_this_season')
def ANILIST_POPULAR_THIS_SEASON(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_popular_this_season())


@route('anilist_popular_this_season/*')
def ANILIST_POPULAR_THIS_SEASON_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_popular_this_season(int(payload)))


@route('anilist_voted_this_season')
def ANILIST_VOTED_THIS_SEASON(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_voted_this_season())


@route('anilist_voted_this_season/*')
def ANILIST_VOTED_THIS_SEASON_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_voted_this_season(int(payload)))


@route('anilist_completed_this_season')
def ANILIST_COMPLETED_THIS_SEASON(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_completed_this_season())


@route('anilist_completed_this_season/*')
def ANILIST_COMPLETED_THIS_SEASON_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_completed_this_season(int(payload)))


@route('anilist_upcoming_next_season')
def ANILIST_UPCOMING_NEXT_SEASON(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_upcoming_next_season())


@route('anilist_upcoming_next_season/*')
def ANILIST_UPCOMING_NEXT_SEASON_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_upcoming_next_season(int(payload)))


@route('anilist_all_time_trending')
def ANILIST_ALL_TIME_TRENDING(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_all_time_trending())


@route('anilist_all_time_trending/*')
def ANILIST_ALL_TIME_TRENDING_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_all_time_trending(int(payload)))


@route('anilist_all_time_popular')
def ANILIST_ALL_TIME_POPULAR(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_all_time_popular())


@route('anilist_all_time_popular/*')
def ANILIST_ALL_TIME_POPULAR_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_all_time_popular(int(payload)))


@route('anilist_all_time_voted')
def ANILIST_ALL_TIME_VOTED(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_all_time_voted())


@route('anilist_all_time_voted/*')
def ANILIST_ALL_TIME_VOTED_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_all_time_voted(int(payload)))


@route('anilist_top_100_anime')
def ANILIST_TOP_100_ANIME(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_top_100_anime())


@route('anilist_top_100_anime/*')
def ANILIST_TOP_100_ANIME_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_top_100_anime(int(payload)))


@route('anilist_airing_anime_movie')
def ANILIST_AIRING_ANIME_MOVIE(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_airing_anime_movie())


@route('anilist_airing_anime_movie/*')
def ANILIST_AIRING_ANIME_MOVIE_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_airing_anime_movie(int(payload)))


@route('anilist_trending_this_year_movie')
def ANILIST_TRENDING_THIS_YEAR_MOVIE(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_trending_this_year_movie())


@route('anilist_trending_this_year_movie/*')
def ANILIST_TRENDING_THIS_YEAR_MOVIE_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_trending_this_year_movie(int(payload)))


@route('anilist_popular_this_year_movie')
def ANILIST_POPULAR_THIS_YEAR_MOVIE(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_popular_this_year_movie())


@route('anilist_popular_this_year_movie/*')
def ANILIST_POPULAR_THIS_YEAR_MOVIE_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_popular_this_year_movie(int(payload)))


@route('anilist_voted_this_year_movie')
def ANILIST_VOTED_THIS_YEAR_MOVIE(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_voted_this_year_movie())


@route('anilist_voted_this_year_movie/*')
def ANILIST_VOTED_THIS_YEAR_MOVIE_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_voted_this_year_movie(int(payload)))


@route('anilist_completed_this_year_movie')
def ANILIST_COMPLETED_THIS_YEAR_MOVIE(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_completed_this_year_movie())


@route('anilist_completed_this_year_movie/*')
def ANILIST_COMPLETED_THIS_YEAR_MOVIE_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_completed_this_year_movie(int(payload)))


@route('anilist_upcoming_next_year_movie')
def ANILIST_UPCOMING_NEXT_YEAR_MOVIE(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_upcoming_next_year_movie())


@route('anilist_upcoming_next_year_movie/*')
def ANILIST_UPCOMING_NEXT_YEAR_MOVIE_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_upcoming_next_year_movie(int(payload)))


@route('anilist_trending_this_season_movie')
def ANILIST_TRENDING_THIS_SEASON_MOVIE(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_trending_this_season_movie())


@route('anilist_trending_this_season_movie/*')
def ANILIST_TRENDING_THIS_SEASON_MOVIE_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_trending_this_season_movie(int(payload)))


@route('anilist_popular_this_season_movie')
def ANILIST_POPULAR_THIS_SEASON_MOVIE(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_popular_this_season_movie())


@route('anilist_popular_this_season_movie/*')
def ANILIST_POPULAR_THIS_SEASON_MOVIE_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_popular_this_season_movie(int(payload)))


@route('anilist_voted_this_season_movie')
def ANILIST_VOTED_THIS_SEASON_MOVIE(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_voted_this_season_movie())


@route('anilist_voted_this_season_movie/*')
def ANILIST_VOTED_THIS_SEASON_MOVIE_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_voted_this_season_movie(int(payload)))


@route('anilist_completed_this_season_movie')
def ANILIST_COMPLETED_THIS_SEASON_MOVIE(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_completed_this_season_movie())


@route('anilist_completed_this_season_movie/*')
def ANILIST_COMPLETED_THIS_SEASON_MOVIE_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_completed_this_season_movie(int(payload)))


@route('anilist_upcoming_next_season_movie')
def ANILIST_UPCOMING_NEXT_SEASON_MOVIE(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_upcoming_next_season_movie())


@route('anilist_upcoming_next_season_movie/*')
def ANILIST_UPCOMING_NEXT_SEASON_MOVIE_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_upcoming_next_season_movie(int(payload)))


@route('anilist_all_time_trending_movie')
def ANILIST_ALL_TIME_TRENDING_MOVIE(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_all_time_trending_movie())


@route('anilist_all_time_trending_movie/*')
def ANILIST_ALL_TIME_TRENDING_MOVIE_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_all_time_trending_movie(int(payload)))


@route('anilist_all_time_popular_movie')
def ANILIST_ALL_TIME_POPULAR_MOVIE(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_all_time_popular_movie())


@route('anilist_all_time_popular_movie/*')
def ANILIST_ALL_TIME_POPULAR_MOVIE_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_all_time_popular_movie(int(payload)))


@route('anilist_all_time_voted_movie')
def ANILIST_ALL_TIME_VOTED_MOVIE(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_all_time_voted_movie())


@route('anilist_all_time_voted_movie/*')
def ANILIST_ALL_TIME_VOTED_MOVIE_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_all_time_voted_movie(int(payload)))


@route('anilist_top_100_anime_movie')
def ANILIST_TOP_100_ANIME_MOVIE(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_top_100_anime_movie())


@route('anilist_top_100_anime_movie/*')
def ANILIST_TOP_100_ANIME_MOVIE_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_top_100_anime_movie(int(payload)))


@route('anilist_airing_anime_tv')
def ANILIST_AIRING_ANIME_TV(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_airing_anime_tv())


@route('anilist_airing_anime_tv/*')
def ANILIST_AIRING_ANIME_TV_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_airing_anime_tv(int(payload)))


@route('anilist_trending_this_year_tv')
def ANILIST_TRENDING_THIS_YEAR_TV(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_trending_this_year_tv())


@route('anilist_trending_this_year_tv/*')
def ANILIST_TRENDING_THIS_YEAR_TV_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_trending_this_year_tv(int(payload)))


@route('anilist_popular_this_year_tv')
def ANILIST_POPULAR_THIS_YEAR_TV(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_popular_this_year_tv())


@route('anilist_popular_this_year_tv/*')
def ANILIST_POPULAR_THIS_YEAR_TV_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_popular_this_year_tv(int(payload)))


@route('anilist_voted_this_year_tv')
def ANILIST_VOTED_THIS_YEAR_TV(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_voted_this_year_tv())


@route('anilist_voted_this_year_tv/*')
def ANILIST_VOTED_THIS_YEAR_TV_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_voted_this_year_tv(int(payload)))


@route('anilist_completed_this_year_tv')
def ANILIST_COMPLETED_THIS_YEAR_TV(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_completed_this_year_tv())


@route('anilist_completed_this_year_tv/*')
def ANILIST_COMPLETED_THIS_YEAR_TV_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_completed_this_year_tv(int(payload)))


@route('anilist_upcoming_next_year_tv')
def ANILIST_UPCOMING_NEXT_YEAR_TV(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_upcoming_next_year_tv())


@route('anilist_upcoming_next_year_tv/*')
def ANILIST_UPCOMING_NEXT_YEAR_TV_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_upcoming_next_year_tv(int(payload)))


@route('anilist_trending_this_season_tv')
def ANILIST_TRENDING_THIS_SEASON_TV(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_trending_this_season_tv())


@route('anilist_trending_this_season_tv/*')
def ANILIST_TRENDING_THIS_SEASON_TV_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_trending_this_season_tv(int(payload)))


@route('anilist_popular_this_season_tv')
def ANILIST_POPULAR_THIS_SEASON_TV(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_popular_this_season_tv())


@route('anilist_popular_this_season_tv/*')
def ANILIST_POPULAR_THIS_SEASON_TV_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_popular_this_season_tv(int(payload)))


@route('anilist_voted_this_season_tv')
def ANILIST_VOTED_THIS_SEASON_TV(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_voted_this_season_tv())


@route('anilist_voted_this_season_tv/*')
def ANILIST_VOTED_THIS_SEASON_TV_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_voted_this_season_tv(int(payload)))


@route('anilist_completed_this_season_tv')
def ANILIST_COMPLETED_THIS_SEASON_TV(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_completed_this_season_tv())


@route('anilist_completed_this_season_tv/*')
def ANILIST_COMPLETED_THIS_SEASON_TV_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_completed_this_season_tv(int(payload)))


@route('anilist_upcoming_next_season_tv')
def ANILIST_UPCOMING_NEXT_SEASON_TV(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_upcoming_next_season_tv())


@route('anilist_upcoming_next_season_tv/*')
def ANILIST_UPCOMING_NEXT_SEASON_TV_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_upcoming_next_season_tv(int(payload)))


@route('anilist_all_time_trending_tv')
def ANILIST_ALL_TIME_TRENDING_TV(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_all_time_trending_tv())


@route('anilist_all_time_trending_tv/*')
def ANILIST_ALL_TIME_TRENDING_TV_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_all_time_trending_tv(int(payload)))


@route('anilist_all_time_popular_tv')
def ANILIST_ALL_TIME_POPULAR_TV(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_all_time_popular_tv())


@route('anilist_all_time_popular_tv/*')
def ANILIST_ALL_TIME_POPULAR_TV_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_all_time_popular_tv(int(payload)))


@route('anilist_all_time_voted_tv')
def ANILIST_ALL_TIME_VOTED_TV(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_all_time_voted_tv())


@route('anilist_all_time_voted_tv/*')
def ANILIST_ALL_TIME_VOTED_TV_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_all_time_voted_tv(int(payload)))


@route('anilist_top_100_anime_tv')
def ANILIST_TOP_100_ANIME_TV(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_top_100_anime_tv())


@route('anilist_top_100_anime_tv/*')
def ANILIST_TOP_100_ANIME_TV_PAGES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_top_100_anime_tv(int(payload)))


@route('anilist_genres')
def ANILIST_GENRES(payload, params):
    return control.draw_items(_ANILIST_BROWSER.get_genres(genre_dialog))


@route('anilist_genres/*')
def ANILIST_GENRES_PAGES(payload, params):
    genres, tags, page = payload.split("/")[-3:]
    return control.draw_items(_ANILIST_BROWSER.get_genres_page(genres, tags, int(page)))


@route('add_to_watchlist/*')
def ADD_TO_WATCHLIST(payload, params):
    anilist_id, mal_id = payload.split("/")[1:-1]
    return watchlist_append(anilist_id)


@route('remove_from_watchlist/*')
def REMOVE_FROM_WATCHLIST(payload, params):
    anilist_id = params.get('anilist_id') if params.get('anilist_id') else payload.split("/")[1]
    watchlist_remove(anilist_id)
    control.refresh()
    return


@route('search_history')
def SEARCH_HISTORY(payload, params):
    history = database.getSearchHistory('show')
    if "Yes" in control.getSetting('searchhistory'):
        return control.draw_items(_BROWSER.search_history(history), contentType="addons", draw_cm=False)
    else:
        return SEARCH(payload, params)


@route('clear_history')
def CLEAR_HISTORY(payload, params):
    database.clearSearchHistory()
    return


@route('search')
def SEARCH(payload, params):
    action_args = params.get('action_args')
    if isinstance(action_args, dict):
        query = action_args.get('query')
    else:
        query = control.keyboard(control.lang(50004))
    if not query:
        return False

    # TODO: Better logic here, maybe move functionatly into router?
    if "Yes" in control.getSetting('searchhistory'):
        database.addSearchHistory(query, 'show')
        # history = database.getSearchHistory('show')

    if isinstance(action_args, dict):
        control.draw_items(_ANILIST_BROWSER.get_search(query, (int(action_args.get('page', '1')))))
    else:
        control.draw_items(_ANILIST_BROWSER.get_search(query))

    return


@route('search/*')
def SEARCH_PAGES(payload, params):
    query, page = payload.rsplit("/", 1)
    return control.draw_items(_ANILIST_BROWSER.get_search(query, int(page)))


@route('search_results/*')
def SEARCH_RESULTS(payload, params):
    query = params.get('query')
    items = _ANILIST_BROWSER.get_search(query, 1)
    return control.draw_items(items)


@route('play_latest/*')
def PLAY_LATEST(payload, params):
    debrid_provider, hash_ = payload.rsplit('/')
    link = _BROWSER.get_latest_sources(debrid_provider, hash_)
    player.play_source(link)


@route('play_movie/*')
def PLAY_MOVIE(payload, params):
    anilist_id, episode, filter_lang = payload.rsplit("/")
    sources = _BROWSER.get_sources(anilist_id, episode, filter_lang, 'movie')

    _mock_args = {'anilist_id': anilist_id}

    if control.getSetting('general.playstyle.movie') == '1' or params.get('source_select'):

        from resources.lib.windows.source_select import SourceSelect

        link = SourceSelect(*('source_select.xml', control.ADDON_PATH),
                            actionArgs=_mock_args, sources=sources).doModal()
    else:
        from resources.lib.windows.resolver import Resolver

        resolver = Resolver(*('resolver.xml', control.ADDON_PATH),
                            actionArgs=_mock_args)

        link = resolver.doModal(sources, {}, False)

    player.play_source(link,
                       anilist_id,
                       watchlist_update,
                       None,
                       int(episode))


@route('play_gogo/*')
def PLAY_GOGO(payload, params):
    slug, episode = payload.rsplit('/')
    from resources.lib.pages import gogoanime
    sources = gogoanime.sources()._process_gogo(slug, '', episode)

    _mock_args = {}
    from resources.lib.windows.source_select import SourceSelect

    link = SourceSelect(*('source_select.xml', control.ADDON_PATH),
                        actionArgs=_mock_args, sources=sources).doModal()

    player.play_source(link)


@route('play/*')
def PLAY(payload, params):
    anilist_id, episode, filter_lang = payload.rsplit("/")
    sources = _BROWSER.get_sources(anilist_id, episode, filter_lang, 'show')
    _mock_args = {"anilist_id": anilist_id, "episode": episode}

    if control.getSetting('general.playstyle.episode') == '1' or params.get('source_select'):

        from resources.lib.windows.source_select import SourceSelect

        link = SourceSelect(*('source_select.xml', control.ADDON_PATH),
                            actionArgs=_mock_args, sources=sources).doModal()
    else:
        from resources.lib.windows.resolver import Resolver

        resolver = Resolver(*('resolver.xml', control.ADDON_PATH),
                            actionArgs=_mock_args)

        link = resolver.doModal(sources, {}, False)

    player.play_source(link,
                       anilist_id,
                       watchlist_update,
                       _BROWSER.get_episodeList,
                       int(episode),
                       filter_lang)


@route('rescrape_play/*')
def RESCRAPE_PLAY(payload, params):
    anilist_id, episode, filter_lang = payload.rsplit("/")
    sources = _BROWSER.get_sources(anilist_id, episode, filter_lang, 'show', True)
    _mock_args = {"anilist_id": anilist_id}

    from resources.lib.windows.source_select import SourceSelect

    link = SourceSelect(*('source_select.xml', control.ADDON_PATH),
                        actionArgs=_mock_args, sources=sources, anilist_id=anilist_id, rescrape=True).doModal()

    player.play_source(link,
                       anilist_id,
                       watchlist_update,
                       _BROWSER.get_episodeList,
                       int(episode),
                       filter_lang,
                       rescrape=True)


@route('tools')
def TOOLS_MENU(payload, params):
    TOOLS_ITEMS = [
        (control.lang(30027), "change_log", 'changelog.png'),
        (control.lang(30020), "settings", 'open settings menu.png'),
        (control.lang(30021), "clear_cache", 'clear cache.png'),
        (control.lang(30022), "clear_torrent_cache", 'clear local torrent cache.png'),
        (control.lang(30023), "clear_history", 'clear search history.png'),
        (control.lang(30026), "rebuild_database", 'rebuild database.png'),
        (control.lang(30024), "wipe_addon_data", 'wipe addon data.png'),
    ]

    TOOLS_ITEMS_SETTINGS = TOOLS_ITEMS[:]
    for i in TOOLS_ITEMS:
        if control.getSetting(i[1]) != 'true':
            TOOLS_ITEMS_SETTINGS.remove(i)

    return control.draw_items(
        [utils.allocate_item(name, url, True, image) for name, url, image in TOOLS_ITEMS],
        contentType="addons",
        draw_cm=False
    )


@route('')
def LIST_MENU(payload, params):
    ls = str(control.lang(30000))
    MENU_ITEMS_SETTINGS = MENU_ITEMS[:]
    for i in MENU_ITEMS_SETTINGS:
        if control.getSetting(i[1]) != 'true' and ls not in i[0] and 'watchlist' not in i[1]:
            MENU_ITEMS.remove(i)
    return control.draw_items(
        [utils.allocate_item(name, url, True, image) for name, url, image in MENU_ITEMS],
        contentType="addons",
        draw_cm=False
    )


set_browser(_BROWSER)
_add_last_watched()
add_watchlist(MENU_ITEMS)
router_process(control.get_plugin_url(), control.get_plugin_params())
