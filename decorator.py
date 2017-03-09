def retry(func):
    """

    如果捕获异常则重试，最多3次

    """

    retries = 0
    count = {"num": retries}

    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            if count['num'] < 3:
                count['num'] += 1
                return wrapped(*args, **kwargs)
            else:
                raise Exception(err)

    return wrapped