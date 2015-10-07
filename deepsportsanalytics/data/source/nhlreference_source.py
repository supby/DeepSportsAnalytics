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
from shared.cache import CacheBase

logger = logging.getLogger(__name__)

class NHLRefDataSource(DataSourceBase):
    """
    inplement data source for nhl-reference site
    """

    __GAMES_URL_FORMAT = '/leagues/NHL_{0}_games.html'
    __TEAM_STAT_URL_FORMAT = '/teams/{0}/{1}.html'
    __BASE_URL = 'http://www.hockey-reference.com'

    def __init__(self, team_stat_season, games_season, cache=None,
                 fvector_len=None, cache_team_stats=False):
        if cache:
            assert isinstance(cache, CacheBase), \
                "cache must have CacheBase class as base one"

        self.__cache = cache
        self.__fvector_len = fvector_len
        self.__cache_team_stats = cache_team_stats

        self.__team_stat_season = team_stat_season
        self.__games_season = games_season

        self.__games_url = self.__GAMES_URL_FORMAT.format(games_season)

        if self.__cache_team_stats:
            self.__team_stat_cache = {}

    def load(self, filter, skip_no_score):
        """load nhl data"""
        super(NHLRefDataSource, self).load(filter)

        data = (([],[]), [])
        if self.__cache and self.__cache.contains(str(filter)):
            data = self.__cache.get(str(filter))
        else:
            for table_selector in ['table#games tbody tr',
                                   'table#games_playoffs tbody tr']:
                logger.info("Process table: %s" % table_selector)

                d = self.__extract_data(table_rows=pq(url=self.__BASE_URL
                                            + self.__games_url)(table_selector),
                                            base_url=self.__BASE_URL,
                                            date_from=filter.dateFrom,
                                            date_to=filter.dateTo,
                                            limit=filter.limit,
                                            proccess_if_no_scores=not skip_no_score)

                data = ((data[0][0]+d[0][0], data[0][1]+d[0][1]), data[1] + d[1])

            if self.__cache:
                self.__cache.set(str(filter), data)

        return data

    def __extract_stats(self, stats_url):

        logger.info('stat url: %s' % (stats_url))

        stats = []
        if self.__cache_team_stats:
            stats = self.__team_stat_cache.get(stats_url, [])

        if not stats:
            d = pq(url=stats_url)
            tds = d('table#team_stats tbody tr:eq(0) td')
            for i in range(1, min(len(tds), self.__fvector_len)
                                if self.__fvector_len > 0 else len(tds)):
                val = float(0)
                if tds[i].text:
                    val = float(tds[i].text)
                stats.append(val)
            if self.__cache_team_stats:
                self.__team_stat_cache[stats_url] = stats
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

        team1Stats = self.__extract_stats(self.__BASE_URL + team1url)
        team2Stats = self.__extract_stats(self.__BASE_URL + team2url)

        if team1Stats and team2Stats:
            train_samples.append(self.__get_diff(team1Stats, team2Stats))

    def __extract_data(self, table_rows, base_url, date_from=None,
                       date_to=None, limit=-1, proccess_if_no_scores=True):
        train_samples = []
        train_Y = []
        metadata = []

        i = 0

        for tr in table_rows:
            tr_obj = pq(tr)
            game_date = datetime.datetime.date(parse(tr_obj('td:eq(0)')
                                .text().strip()))
            if date_from != None and game_date < date_from:
                continue
            if date_to != None and game_date >= date_to:
                break
            if i == limit and limit > 0:
                break

            i += 1

            team1A = tr_obj('td:eq(1) a')[0]
            team2A = tr_obj('td:eq(3) a')[0]

            logger.info('%s - %s' % (team1A.text, team2A.text))

            if proccess_if_no_scores:
                metadata.append((game_date, team1A.text, team2A.text))
                logger.info('%s: %s - %s' % (game_date, team1A.text, team2A.text))
                self.__proccess_team_stats(train_samples,
                                           base_url + team1A.attrib['href'],
                                           base_url + team2A.attrib['href'])

            scores1Str = tr_obj('td:eq(2)').text().strip()
            scores2Str = tr_obj('td:eq(4)').text().strip()

            if scores2Str == '' or scores1Str == '':
                continue

            if not proccess_if_no_scores:
                metadata.append((game_date, team1A.text, team2A.text))
                logger.info('%s: %s - %s' % (game_date, team1A.text, team2A.text))
                self.__proccess_team_stats(train_samples,
                                           base_url + team1A.attrib['href'],
                                           base_url + team2A.attrib['href'])

            Y = 1 if int(scores1Str) - int(scores2Str) >= 0 else 0
            train_Y.append(Y)

            logger.info('class => %s' % (Y))

        return ((train_samples, train_Y), metadata)
