import redis

r = redis.StrictRedis(host='localhost', port=6379)
r.set("foo","bar")
