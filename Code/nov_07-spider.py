import scrapy
from slugify import slugify

class TeamMatches(scrapy.Spider):
    name = "team-matches"

    def start_requests(self):
        urls = [
            #'https://www.betstudy.com/soccer-stats/c/england/premier-league/d/results/2017-2018/',
            'https://www.betstudy.com/soccer-stats/c/england/premier-league/d/results/2016-2017/',
            #'https://www.betstudy.com/soccer-stats/c/england/premier-league/d/results/2015-2016/',
            #'https://www.betstudy.com/soccer-stats/c/england/premier-league/d/results/2014-2015/',
            #'https://www.betstudy.com/soccer-stats/c/england/premier-league/d/results/2013-2014/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_fixtures_page)

    def parse_fixtures_page(self, response):
        for info_button in response.css('ul.action-list').css('a::attr(href)'):
            url = response.urljoin(info_button.extract())
            yield scrapy.Request(url, callback=self.parse_match_page)

    def parse_match_page(self, response):

        home_team, away_team = response.css('div.player h2 a::text').extract()

        home_goals, away_goals = response.css('div.info strong.score::text').extract_first().split('-')

        date = response.css('em.date').css('span.timestamp::text').extract_first()

        match_number = response.request.url.split('-')[-1].split('/')[0]

        yield {
            'match number': int(match_number),
            'info': {
                'date': date,
                'home team': slugify(home_team),
                'away team': slugify(away_team),
                'home goals': int(home_goals),
                'away goals': int(away_goals),
            }
        }
