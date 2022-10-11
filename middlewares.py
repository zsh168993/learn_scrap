# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html



# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random
from scrapy import signals
from fake_useragent import UserAgent
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from w3lib.http import basic_auth_header
from zhonghua.settings import user_agent_list

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class ZhonghuaSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
# IP代理池
class ZhonghuaHttpProxyMiddleware(HttpProxyMiddleware):
    def __init__(self, ip=""):
        self.ip = ip

    def process_request(self, request, spider):
        try:
            proxy = "f883.kdltps.com:15818"
            # proxy = "117.69.176.71:15818"

            request.meta['proxy'] = "http://%(proxy)s" % {'proxy': proxy}
            # 用户名密码认证
            request.headers['Proxy-Authorization'] = basic_auth_header('t16519297283463', 'kx87b6yx')  # 白名单认证可注释此行
            request.headers["Connection"] = "close"
            return None
        except:
            spider.logger.error('some proxy error happended!')

    # def process_response(self, request, response, spider):
    #     spider.logger.info(request.url)
    #     spider.logger.info(request.headers)
    #     spider.logger.info(response.headers)
    #     spider.logger.info(response.body.decode(response.encoding))


# 用户代理池
class ZhonghuaUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent=""):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        try:
            request.headers.setdefault('User-Agent', random.choice(user_agent_list))
        except:
            spider.logger.error('some User-Agent error happended!')

#延时
class ZhonghuaDownloadTimeoutMiddleware:
    def __init__(self, timeout=180):
        self._timeout = timeout

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings.getfloat('DOWNLOAD_TIMEOUT'))
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def spider_opened(self, spider):
        self._timeout = getattr(spider, 'download_timeout', self._timeout)

    def process_request(self, request, spider):
        if self._timeout:
            request.meta.setdefault('download_timeout', self._timeout)
        if self._timeout>180:
            #reason = response_status_message(response.status)
            try:
                proxy = "f883.kdltps.com:15818"
                # proxy = "117.69.176.71:15818"
                request.meta['proxy'] = "http://%(proxy)s" % {'proxy': proxy}
                # 用户名密码认证
                request.headers['Proxy-Authorization'] = basic_auth_header('t16519297283463', 'kx87b6yx')  # 白名单认证可注释此行
                request.headers["Connection"] = "close"
                request.headers.setdefault('User-Agent', random.choice(user_agent_list))
                # proxy_ip_port = random.choice(self.proxy_list)
                # request.meta['proxy'] = 'http://' + proxy_ip_port
            except:
                spider.logger.error('some User-Agent error happended!')
#重试
class ZhonghuaRetryMiddleware(RetryMiddleware):
    # def __init__(self, crawler):
    #     self.proxy_list = crawler.settings.PROXY_LIST
    #     self.ua_list = crawler.settings.USER_AGENT_LIST

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response

        if response.status in self.retry_http_codes:
            #reason = response_status_message(response.status)
            try:
                proxy = "f883.kdltps.com:15818"
                request.meta['proxy'] = "http://%(proxy)s" % {'proxy': proxy}
                # 用户名密码认证
                request.headers['Proxy-Authorization'] = basic_auth_header('t16519297283463', 'kx87b6yx')  # 白名单认证可注释此行
                request.headers["Connection"] = "close"
                request.headers.setdefault('User-Agent',random.choice(user_agent_list))
                return request
                # proxy_ip_port = random.choice(self.proxy_list)
                # request.meta['proxy'] = 'http://' + proxy_ip_port
            except:
                spider.logger.error('some User-Agent error happended!')
        return response

class ZhonghuaDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        referer = request.url
        if referer:
            request.headers["referer"] = referer
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest


        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

