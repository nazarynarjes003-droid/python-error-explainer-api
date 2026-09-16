from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    api_key = os.getenv("OPENROUTER_API_KEY"),
    base_url = "https://openrouter.ai/api/v1"
)


def build_prompt(error_result, code_result, raw_code = None):
    error_type = error_result["error_type"]
    error_message = error_result["message"]
    suspicious = code_result.get("suspicious", [])

    suspicious_text = ""
    for item in suspicious:
        suspicious_text += f"- عبارت: {item['expression']} | خطای احتمالی: {item['possible_error']} | توضیح: {item['description']}\n"

    if not suspicious_text:
        suspicious_text = "هیچ الگوی مشکوکی در کد شناسایی نشد.\n"

    code_section = ""
    if raw_code:
        code_section = f"""
متن کامل کد کاربر:
{raw_code}
"""

    prompt = f"""یک قطعه کد پایتون با خطای زیر مواجه شده است:

نوع خطا: {error_type}
توضیح کلی خطا: {error_message}
{code_section}
بخش‌های مشکوک شناسایی‌شده در کد:
{suspicious_text}

فقط و فقط یک آبجکت JSON با دقیقاً این ساختار برگردان، بدون هیچ متن اضافه، بدون توضیح قبل یا بعد از آن، بدون ```json و بدون بک‌تیک. مقادیر تمام فیلدها (explanation, possible_causes, solution) باید کاملاً به زبان فارسی نوشته شوند، حتی اگر کد یا پیام خطا به انگلیسی باشد. در فیلد solution از فرمت مارک‌داون (مثل بک‌تیک سه‌تایی یا python) استفاده نکن؛ اگر نیاز به نمایش کد نمونه بود، آن را به‌صورت متن ساده و بدون بک‌تیک بنویس:

{{
  "error_type": "نوع خطا",
  "explanation": "علت وقوع خطا در یک یا دو جمله ساده",
  "possible_causes": ["دلیل احتمالی اول", "دلیل احتمالی دوم"],
  "solution": "راهکار مشخص برای رفع خطا، همراه یک قطعه کد کوتاه در صورت لزوم"
}}
"""
    return prompt



def explain_error(error_result, code_result, raw_code = None):

    prompt = build_prompt(error_result, code_result, raw_code)

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[{"role": "user", "content": prompt}]        
    )

    raw_content = response.choices[0].message.content.strip()

    if raw_content.startswith("```"):
        raw_content = raw_content.strip("`")
        raw_content = raw_content.replace("json", "", 1).strip()

    try:
        structured_result = json.loads(raw_content)

    except json.JSONDecodeError:
        structured_result ={
            "error_type": error_result.get("error_type"),
            "explanation": "پاسخ دریافتی از هوش مصنوعی قابل تبدیل به فرمت استاندارد نبود.",
            "possible_causes": [],
            "solution": "لطفاً دوباره تلاش کنید."           
        }

    return structured_result