import redis

class Guest_db:
    def __init__(self, host='localhost', port=6379, db=0, password=None):
        self.r = redis.StrictRedis(host='localhost',port=6379,db=0)


    def get_all(self) -> dict:
        keys = redis.keys()
        values = [self.r.get(key) for key in keys]

        known_guests = dict(zip(keys, values))
        return known_guests
    
    def set_guests(self, new_guests: dict):
        for key, value in new_guests:
            self.r.set(key, value)



