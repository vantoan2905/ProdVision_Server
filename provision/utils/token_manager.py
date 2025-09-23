import redis
import random

r = redis.StrictRedis(host='localhost', port=6379, db=0)

class OTPManager:
    @staticmethod
    def generate_otp(user_id, length=6, expire_seconds=300):
        otp = random.randint(10**(length-1), 10**length-1)
        try:
            r.setex(f"otp:{user_id}", expire_seconds, otp)  
        except Exception as e:
            print(e)
        return otp

    @staticmethod
    def verify_otp(user_id, otp):
        key = f"otp:{user_id}"
        stored_otp = r.get(key)
        if not stored_otp:
            return False
        if str(stored_otp.decode()) == str(otp):
            r.delete(key)
            return True
        return False
