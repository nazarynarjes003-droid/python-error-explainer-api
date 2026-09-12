SUPPORTED_ERRORS = {
    "TypeError": "نوع داده‌های استفاده‌شده برای این عملیات با یکدیگر سازگار نیستند.",
    "ValueError": "مقدار واردشده برای این عملیات معتبر نیست.",
    "IndexError": "اندیس موردنظر خارج از محدوده موجود است.",
    "KeyError": "کلید موردنظر در دیکشنری وجود ندارد.",
    "SyntaxError": "ساختار دستوری کد Python نادرست است.",
    "AttributeError": "شیء موردنظر دارای این ویژگی یا متد نیست."
}


def analysis_error(error_type):

    if error_type in SUPPORTED_ERRORS:
        return {
            "error_type" : error_type,
            "message" : SUPPORTED_ERRORS[error_type],
            "supported" : True
        }

    return {
        "error_type" : error_type,
        "message" : "این نوع خطا در سیستم پشتیبانی نمیشود.",
        "supported" : False
    }