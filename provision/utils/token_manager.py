import random
import time

class OTPManager:
    # Lưu OTP trong RAM: {user_id: (otp_code, expire_time)}
    otp_store = {}

    @staticmethod
    def generate_otp(user_id, length=6, expire_seconds=300):
        """Tạo OTP cho từng user riêng biệt"""
        otp = random.randint(10**(length-1), 10**length - 1)
        expire_time = time.time() + expire_seconds
        OTPManager.otp_store[user_id] = (otp, expire_time)
        return otp

    @staticmethod
    def verify_otp(user_id, otp):
        """Xác thực OTP theo user"""
        if user_id not in OTPManager.otp_store:
            return False
        stored_otp, expire_time = OTPManager.otp_store[user_id]
        if time.time() > expire_time:
            del OTPManager.otp_store[user_id]  # OTP hết hạn
            return False
        if stored_otp == otp:
            del OTPManager.otp_store[user_id]  # Xác thực xong xóa luôn
            return True
        return False
