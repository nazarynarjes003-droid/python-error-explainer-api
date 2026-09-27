class Error:

    def __init__(self, error_type, message):

        self.error_type = error_type
        self.message = message


    def to_dict(self):
        return{
            "error_type": self.error_type,
            "message": self.message,
            "supported": True            
        }


type_error = Error("TypeError", "نوع داده‌های استفاده‌شده برای این عملیات با یکدیگر سازگار نیستند.")
value_error = Error("ValueError", "مقدار واردشده برای این عملیات معتبر نیست.")
index_error = Error("IndexError", "اندیس موردنظر خارج از محدوده موجود است.")
key_error = Error("KeyError", "کلید موردنظر در دیکشنری وجود ندارد.")
syntax_error = Error("SyntaxError", "ساختار دستوری کد Python نادرست است.")
attribute_error = Error("AttributeError", "شیء موردنظر دارای این ویژگی یا متد نیست.")
zero_division_error = Error("ZeroDivisionError", "تقسیم بر صفر مجاز نیست.")
name_error = Error("NameError", "متغیر یا نامی که استفاده شده تعریف نشده است.")
import_error = Error("ImportError", "امکان وارد کردن (import) این ماژول یا نام از آن وجود ندارد.")
module_not_found_error = Error("ModuleNotFoundError", "ماژول موردنظر یافت نشد؛ ممکن است نصب نشده باشد یا نام آن اشتباه باشد.")
indentation_error = Error("IndentationError", "تورفتگی (فاصله‌گذاری ابتدای خط) کد نادرست است.")
recursion_error = Error("RecursionError", "تعداد فراخوانی‌های بازگشتی تابع از حد مجاز پایتون بیشتر شده است (احتمالاً حالت پایان بازگشت وجود ندارد).")
file_not_found_error = Error("FileNotFoundError", "فایل موردنظر یافت نشد؛ ممکن است مسیر یا نام فایل اشتباه باشد.")
permission_error = Error("PermissionError", "دسترسی لازم برای خواندن یا نوشتن این فایل وجود ندارد.")
unbound_local_error = Error("UnboundLocalError", "متغیر محلی قبل از مقداردهی در تابع استفاده شده است.")



all_errors = [
    type_error,
    value_error,
    index_error,
    key_error,
    syntax_error,
    attribute_error,
    zero_division_error,
    name_error,
    import_error,
    module_not_found_error,
    indentation_error,
    recursion_error,
    file_not_found_error,
    permission_error,
    unbound_local_error
]


def analysis_error(error_type):

    for error_obj in all_errors:

        if error_obj.error_type == error_type:
            return error_obj.to_dict()

    return{
        "error_type": error_type,
        "message": "این نوع خطا در سیستم پشتیبانی نمیشود.",
        "supported": False        
    }