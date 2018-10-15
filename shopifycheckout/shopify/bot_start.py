from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from twisted.internet import task
from random import randint


timeout = 3


def run_spider():
    l.stop()
    runner = CrawlerRunner(get_project_settings())
    if randint(0, 9) > 5:
        spider_name = 'search'
    else:
        spider_name = 'search'
    d = runner.crawl(spider_name)
    d.addBoth(lambda _: l.start(timeout, False))


l = task.LoopingCall(run_spider)
l.start(timeout)

reactor.run()