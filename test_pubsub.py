import redis

def test():
    r = redis.Redis(host='192.168.7.1', port='6379')
    p = r.pubsub()
    p.subscribe('gps')
    while True:
        message = p.get_message()
        if message:
            print "Subscriber: %s" % message['data']

test()
