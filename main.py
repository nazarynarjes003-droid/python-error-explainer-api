from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse
from datetime import datetime

import error_analysis
import AST_processing
import LLM

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):

    print("خطای داخلی سرور:", repr(exc))

    return JSONResponse(
        status_code = 500,
        content={"message": "خطای داخلی سرور رخ داده است. لطفاً بعداً دوباره تلاش کنید."}
    )

class ErrorRequest(BaseModel):
    code: str
    error : Optional[str] = None


class FeedbackRequest(BaseModel):
    message: str


@app.get("/")
def get_endpoint():
    return "Python Error Explainer API is running"


@app.post("/feedback")
def receive_feedback(request: FeedbackRequest):
    with open("feedback.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {request.message}\n")
    return {"status": "دریافت شد"}


@app.post("/analyze")
def analyze_error_endpoint(request : ErrorRequest):

    try:
        tree = AST_processing.parse_code(request.code)

        if len(tree.body) == 0:
            return {
                "code": request.code,
                "error_type": None,
                "message": "کد ورودی هیچ دستور قابل اجرایی ندارد (احتمالاً کاملاً کامنت شده یا خالی است).",
                "supported": False,
                "detected_automatically": False,
                "analysis": None,
                "analysis_error": None,
                "llm_explanation": None
            }

        code_analysis = AST_processing.analyze_code(request.code)
        analysis_error_message = None

    except SyntaxError as e:

        analysis_error_message = f"کد ورودی قابل تحلیل نیست: {e.msg} (خط {e.lineno})"

        error_info = error_analysis.analysis_error("SyntaxError")
        error_info["message"] = analysis_error_message

        try:
            llm_explanation = LLM.explain_error(error_info, {"suspicious": []}, raw_code=request.code)

        except Exception as ex:
            print("خطای واقعی:", repr(ex))
            llm_explanation = "در حال حاضر امکان دریافت توضیح از هوش مصنوعی وجود ندارد. "

        return {
            "code": request.code,
            "error_type": error_info["error_type"],
            "message": error_info["message"],
            "supported": error_info["supported"],
            "detected_automatically": False,
            "analysis": None,
            "analysis_error": analysis_error_message,
            "llm_explanation": llm_explanation
        }

    detected_error = request.error
    detected_autmatically = False

    if detected_error is None and code_analysis is not None:
        suspicious_list = code_analysis.get("suspicious", [])

        if suspicious_list:
            detected_error = suspicious_list[0]["possible_error"]
            detected_autmatically = True

    if detected_error is not None:
        error_info = error_analysis.analysis_error(detected_error)

    elif code_analysis is not None and len(code_analysis.get("suspicious",[])) == 0:

        supported_list = ", ".join(error_analysis.SUPPORTED_ERRORS.keys())

        error_info = {
            "error_type": None,
            "message": f"کد بررسی شد و هیچ خطای مشکوکی از نوع TypeError در آن شناسایی نشد. اگر کد شما نوع دیگری از خطا تولید می‌کند، لطفاً آن را در فیلد 'error' مشخص کنید. انواع پشتیبانی‌شده: {supported_list}",
            "supported": False
        }

    else:
        error_info = {
            "error_type": None,
            "message": "نوع خطا مشخص نشد و از روی کد هم قابل تشخیص نبود.",
            "supported": False 
        }



    if code_analysis is not None and error_info["error_type"] is not None and error_info["supported"]:

        try:
            llm_explanation = LLM.explain_error(error_info, code_analysis, raw_code = request.code)

        except Exception as e:
            print("خطای واقعی:", repr(e))
            llm_explanation = "در حال حاضر امکان دریافت توضیح از هوش مصنوعی وجود ندارد. "

    else:
        llm_explanation = None



    return{
        "code" : request.code,
        "error_type" : error_info["error_type"],
        "message": error_info["message"],
        "supported" : error_info["supported"],
        "detected_automatically": detected_autmatically,
        "analysis" : code_analysis,
        "analysis_error" : analysis_error_message,
        "llm_explanation" : llm_explanation
    }
