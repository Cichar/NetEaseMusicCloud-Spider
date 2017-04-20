# encoding: utf-8
def retry(func):
    """

    如果捕获异常则重试，最多3次

    """

    retries = 0
    err_503 = 0
    count = {"num": retries, 'err_503': err_503}

    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            if '503' in str(err):
                print('** 警告：服务器已进行限制 **')
                if count['err_503'] < 3:
                    count['err_503'] += 1
                else:
                    exit()
            if count['num'] < 3:
                count['num'] += 1
                print('** retry : {0} 重试 {1} 次 **'.format(str(err), count['num']))
                return wrapped(*args, **kwargs)
            else:
                print('** retry : %s **' % str(err))
    return wrapped
