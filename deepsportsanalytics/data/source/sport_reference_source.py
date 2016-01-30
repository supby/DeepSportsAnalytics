# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import sys
import datetime
from dateutil.parser import parse
import logging
from urlparse import urlparse

from pyquery import PyQuery as pq

from source_base import DataSourceBase

logger = logging.getLogger(__name__)

class NHLReferenceRowParseStrategy(object):

    def get_row_data(self, tr_obj):
        return parse(tr_obj('td:eq(0)').text().strip()),\
            tr_obj('td:eq(1) a')[0],\
            tr_obj('td:eq(3) a')[0],\
            tr_obj('td:eq(2)').text().strip(),\
            tr_obj('td:eq(4)').text().strip()

class NBAReferenceRowParseStrategy(object):

    def get_row_data(self, tr_obj):
        return parse(tr_obj('td:eq(0)')[0].attrib['csk'].strip()[:8]),\
            tr_obj('td:eq(3) a')[0],\
            tr_obj('td:eq(5) a')[0],\
            tr_obj('td:eq(4)').text().strip(),\
            tr_obj('td:eq(6)').text().strip()


class SportReferenceDataSource(DataSourceBase):
    """
    inplement data source for sport-reference site
    """

    __GAMES_URL_FORMAT = '/leagues/{0}_{1}_games.html'
    __TEAM_STAT_URL_FORMAT = '/teams/{0}/{1}.html'

    def __init__(self, base_url, team_stat_season, games_season, game_type,
                row_parse_strategy,
                cache=None, fvector_len=None, cache_team_stats=False):

        self.__cache = cache
        self.__fvector_len = fvector_len
        self.__cache_team_stats = cache_team_stats

        self.__base_url = base_url
        self.__team_stat_season = team_stat_season
        self.__games_season = games_season

        self.__games_url = self.__GAMES_URL_FORMAT.format(game_type, games_season)

        self.__row_parse_strategy = row_parse_strategy

        if self.__cache_team_stats:
            self.__team_stat_cache = {}

    def load(self, filter):
        """load nhl data"""

        cache_key = '{0}_{1}'.format(self.__games_url, str(filter))

        data = None
        if self.__cache:
            data = self.__cache.get(cache_key)

        if data == None:
            data = [],[],[]
            for table_selector in ['table#games tbody:eq(0) tr',
                                   'table#games_playoffs tbody:eq(0) tr']:
                logger.info("Process table: %s" % table_selector)

                d = self.__extract_data(
                    table_rows=pq(url=self.__base_url+self.__games_url)(table_selector),
                                base_url=self.__base_url,
                                date_from=filter['date_from'],
                                date_to=filter['date_to'])

                data = data[0]+d[0], data[1]+d[1], data[2] + d[2]

            if self.__cache:
                self.__cache.set(cache_key, data)

        return data

    def __extract_stats(self, stats_url):

        logger.info('stat url: %s' % (stats_url))

        stats = []
        if self.__cache_team_stats:
            stats = self.__team_stat_cache.get(stats_url, [])

        if not stats:
            d = pq(url=stats_url)
            tds = d('table#team_stats tbody:eq(0) tr:eq(0) td')
            for i in range(1, min(len(tds), self.__fvector_len)
                                if self.__fvector_len > 0 else len(tds)):
                val = float(0)
                if tds[i].text:
                    val = float(tds[i].text)
                stats.append(val)
            if self.__cache_team_stats:
                self.__team_stat_cache[stats_url] = stats
        else:
            logger.info('found in cache, url: %s' % (stats_url))

        return stats

    def __get_diff(self, stats1, stats2):
        return [float(stats1[i] - stats2[i]) for i in range(len(stats1))]

    def __get_team_code(self, path):
        return path.strip('/').split('/')[1]

    def __proccess_team_stats(self, train_samples, team1Link, team2Link):
        team1url = self.__TEAM_STAT_URL_FORMAT\
                        .format(self.__get_team_code(urlparse(team1Link).path),
                                self.__team_stat_season)
        team2url = self.__TEAM_STAT_URL_FORMAT\
                        .format(self.__get_team_code(urlparse(team2Link).path),
                        self.__team_stat_season)

        team1Stats = self.__extract_stats(self.__base_url + team1url)
        team2Stats = self.__extract_stats(self.__base_url + team2url)

        if team1Stats and team2Stats:
            train_samples.append(self.__get_diff(team1Stats, team2Stats))

    def __extract_data(self, table_rows, base_url, date_from=None, date_to=None):
        X = []
        Y = []
        metadata = []

        for tr in table_rows:
            game_date, team1A, team2A, score1Str, score2Str\
                                    = self.__row_parse_strategy.get_row_data(pq(tr))

            if date_from != None and game_date < date_from:
                continue
            if date_to != None and game_date >= date_to:
                break

            logger.info('%s: %s - %s' % (game_date, team1A.text, team2A.text))

            metadata.append(dict(game_date=game_date,
                                team1_name=team1A.text,
                                team2_name=team2A.text))
            self.__proccess_team_stats(X,
                                       base_url + team1A.attrib['href'],
                                       base_url + team2A.attrib['href'])

            if score1Str and score2Str:
                Y.append(1) if int(score1Str) - int(score2Str) >= 0 else Y.append(0)
            else:
                Y.append(None)

        return X, Y, metadata
