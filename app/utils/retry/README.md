Examples
=========

## retry deco

    from retry import retry


    @retry()
    def make_trouble():
        '''Retry until succeed'''


    @retry(ZeroDivisionError, tries=3, delay=2)
    def make_trouble():
        '''Retry on ZeroDivisionError, raise error after 3 attempts, sleep 2 seconds between attempts.'''


    @retry((ValueError, TypeError), delay=1, backoff=2)
    def make_trouble():
        '''Retry on ValueError or TypeError, sleep 1, 2, 4, 8, ... seconds between attempts.'''


    @retry((ValueError, TypeError), delay=1, backoff=2, max_delay=4)
    def make_trouble():
        '''Retry on ValueError or TypeError, sleep 1, 2, 4, 4, ... seconds between attempts.'''
    

    @retry(ValueError, delay=1, jitter=1)
    def make_trouble():
        '''Retry on ValueError, sleep 1, 2, 3, 4, ... seconds between attempts.'''


    # If you enable logging, you can get warnings like 'ValueError, retrying in
    # 1 seconds'
    if __name__ == '__main__':
        import logging
        logging.basicConfig()
        make_trouble()

## retry_call


    import requests

    from retry.api import retry_call


    def make_trouble(service, info=None):
        if not info:
            info = ''
        r = requests.get(service + info)
        return r.text


    def what_is_my_ip(approach=None):
        if approach == "optimistic":
            tries = 1
        elif approach == "conservative":
            tries = 3
        else:
            # skeptical
            tries = -1
        result = retry_call(make_trouble, fargs=["http://ipinfo.io/"], fkwargs={"info": "ip"}, tries=tries)
        print(result)

    what_is_my_ip("conservative")
