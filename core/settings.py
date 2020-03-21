# # -*- coding: utf-8 -*-

# # Scrapy settings for scrapy-example-pagination project
# #
# # For simplicity, this file contains only settings considered important or
# # commonly used. You can find more settings consulting the documentation:
# #
# #     http://doc.scrapy.org/en/latest/topics/settings.html
# #     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# #     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

# BOT_NAME = 'scrapy-example-pagination'

# SPIDER_MODULES = ['core.spiders']
# NEWSPIDER_MODULE = 'core.spiders'

# # Feed Export Settings
# #FEED_FORMAT = 'csv'
# #FEED_EXPORT_FIELDS = ["short_desc","detail_desc","expiry_date","pdp_url","img_url"]

# # Obey robots.txt rules
# #ROBOTSTXT_OBEY = True
# #ROBOTSTXT_OBEY = False

# # Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 1

# # Configure a delay for requests for the same website (default: 0)
# # See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# # See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# # The download delay setting will honor only one of:
# #CONCURRENT_REQUESTS_PER_DOMAIN = 16
# #CONCURRENT_REQUESTS_PER_IP = 16

# # Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# # Enable or disable downloader middlewares
# # See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#     'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 399,
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware': 401,
#     'scrapy_proxies.RandomProxy': 398,
# }

# # Logging
# LOG_LEVEL = 'INFO'
# #LOG_LEVEL = 'DEBUG'

# # Settings for scrapy-proxies
# RETRY_TIMES = 10
# RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]
# PROXY_LIST = 'list.txt'    # Proxy list contains rotating IPs
# PROXY_MODE = 1

# # Settings for fake-user-agent
# RANDOM_UA_PER_PROXY = True


BOT_NAME = 'tutorial'

SPIDER_MODULES = ['core.spiders']
NEWSPIDER_MODULE = 'core.spiders'

# DOWNLOADER_MIDDLEWARES = {
#     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
#     # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#     'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 399,
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware': 401,
#     'scrapy_proxies.RandomProxy': 398,
# }

CONCURRENT_REQUESTS = 200


# Retry many times since proxies often fail
# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]
RETRY_TIMES = 10000000
PROXY_LIST = 'list.txt'    # Proxy list contains rotating IPs
PROXY_MODE = 1

DOWNLOAD_TIMEOUT = 20000
# DUPEFILTER_DEBUG=True
# REDIRECT_ENABLED=True
# COOKIES_ENABLED = False
# HTTPCACHE_ENABLED=True
# AJAXCRAWL_ENABLED=True
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36"


# CONCURRENT_REQUESTS=1
# CONCURRENT_REQUESTS_PER_DOMAIN=1
# CONCURRENT_ITEMS=1
# CONCURRENT_REQUESTS_PER_IP = 5
# RANDOM_DOWNLOAD_DELAY = True
# DOWNLOAD_DELAY = 3
# AUTOTHROTTLE_ENABLED=True

# ITEM_PIPELINES = {'tutorial.pipelines.TutorialPipeline': 300 }
