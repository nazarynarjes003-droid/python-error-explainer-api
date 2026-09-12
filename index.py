from fastapi import FastAPI
from pydantic import BaseModel

import ast

# app = FastAPI()

# @app.get("/")
# def home():
#     return {"message": "Hello API"}





# @app.post("/analyze")
# async def analyze(request: Request):
#     data = await request.json()
#     return data




# @app.get("/users/{user_id}")
# def get_user(user_id: int):
#     return {"user_id": user_id}






# @app.get("/product/{product_id}")
# def get_product(product_id : int):
#     return{"product_id": product_id}





# @app.get("/products")
# def get_product(category: str, max_price = int):
#     return {"category": category,
#             "price" : max_price
#             }



# GET /users?name=ali&age=20


# @app.get("/users")
# def get_users(name: str, age: int):
#     return{
#         "name": name,
#         "age": age}



# @app.get("/products")
# def get_product(name: str, category: str = None):
#     return {"name" :name,
#             "category": category
#             }







# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def home():
#     return {"message": "Hello"}



# @app.get("/product/{product_id}")
# def get_product(product_id: int):

#     if product_id != 1 :
#         raise HTTPException(
#             status_code= 404,
#             detail= "Product not found"
#         )

#     return {
#         "product_id": 1,
#         "name": "Laptop"       
#     }


# class ErrorRequest(BaseModel):
#     code: str
#     error: str

# @app.post("/analyze")
# def analyze(data: ErrorRequest):
#     return data


# ******************************************************************************************************************


# code = '''
# x = "10"
# y = 5
# z = x + y
# '''

# tree = ast.parse(code)

# print(ast.dump(tree)) 



# code = '''
# x = 10
# y = 5
# z = x + y
# '''

# tree = ast.parse(code)

# for node in ast.walk(tree):
#     print(type(node).__name__)


# for node in ast.walk(tree):
#     if isinstance(node, ast.Name):
#         print(node.id)


# code = '''
# x = 10
# y = x + 5
# '''
# tree = ast.parse(code)

# # for node in ast.walk(tree):
# #     if isinstance(node, ast.Name):
# #         print(node.id)

# for node in ast.walk(tree):

#     if isinstance(node, ast.Name):

#         if isinstance(node.ctx, ast.Store):
#             print(node.id, "Store")

#         elif isinstance(node.ctx, ast.Load):
#             print(node.id, "Load")




# code = '''
# x = "hello"
# y = 10
# '''

# tree = ast.parse(code)

# # for node in ast.walk(tree):

# #     if isinstance(node, ast.Assign):
# #         print(node.targets)
# #         print(node.value)

# for node in ast.walk(tree):

#     if isinstance(node, ast.Assign):

#         name = node.targets[0].id
#         value = node.value.value

#         print(name, value, type(value))



# code = '''
# x = 10
# y = 5
# z = x + y
# '''

# tree = ast.parse(code)

# for node in ast.walk(tree):

#     if isinstance(node, ast.Assign):

#         print(node.targets[0].id)
#         print(type(node.value).__name__)

# for node in ast.walk(tree):

#     if isinstance(node, ast.BinOp):

#         print("left:", node.left.id)
#         print("operator:", type(node.op).__name__)
#         print("right:", node.right.id)

# **********************************************************************************************************************

# code = '''
# x = "hello"
# y = 10
# z = x + y
# '''

# tree = ast.parse(code)

# variables = {}

# for node in tree.body:

#     if isinstance(node, ast.Assign):

#         name = node.targets[0].id

#         if isinstance(node.value, ast.Constant):
#             variables[name] = type(node.value.value).__name__

#         if isinstance(node.value, ast.BinOp):

#             left_name = node.value.left.id
#             right_name = node.value.right.id

#             left_type = variables[left_name]
#             right_type = variables[right_name]

#             print(left_name, left_type)
#             print(right_name, right_type)


# # print(variables)



# code = '''
# x = 1
# y = 10
# z = x + y
# '''

# tree = ast.parse(code)

# # جدول متغیرها
# variables = {}

# # قوانین عملگر +
# valid_additions = {
#     ("int", "int"): True,
#     ("float", "float"): True,
#     ("str", "str"): True
# }

# # بررسی دستورات به ترتیب
# for node in tree.body:

#     # پیدا کردن Assign
#     if isinstance(node, ast.Assign):

#         # گرفتن اسم متغیر
#         name = node.targets[0].id

#         # اگر مقدار ساده باشد
#         if isinstance(node.value, ast.Constant):

#             variables[name] = type(node.value.value).__name__

#         # اگر مقدار یک عملیات باشد
#         elif isinstance(node.value, ast.BinOp):

#             # گرفتن اسم متغیر سمت چپ
#             left_name = node.value.left.id

#             # گرفتن اسم متغیر سمت راست
#             right_name = node.value.right.id

#             # پیدا کردن نوع متغیرها
#             left_type = variables[left_name]
#             right_type = variables[right_name]

#             # بررسی اینکه عملگر +
#             if isinstance(node.value.op, ast.Add):

#                 # بررسی مجاز بودن ترکیب نوع‌ها
#                 if (left_type, right_type) in valid_additions:
#                     print("Operation is valid")
#                 else:
#                     print("TypeError")


# print("Variables:", variables)

# *******************************************************************************************************


# code = "len(numbers)"

# tree = ast.parse(code)
# print(ast.dump(tree))

# for node in ast.walk(tree):

#     if isinstance(node, ast.Call):

#         print("function:", node.func.id)
#         print("arguments:", node.args)

# ******************************************************************************************************


# code = "numbers[2]"

# tree = ast.parse(code)
# print(ast.dump(tree))

# for node in ast.walk(tree):

#     if isinstance(node, ast.Subscript):

#         print("value:", node.value.id)
#         print("slice:", node.slice.value)

# ******************************************************************************************************

# code = "user.name"

# tree = ast.parse(code)
# print(ast.dump(tree))

# for node in ast.walk(tree):

#     if isinstance(node, ast.Attribute):

#         print("object:", node.value.id)
#         print("attribute:", node.attr)

# **************************************************************************************************


# code = "x > 10"

# tree = ast.parse(code)
# print(ast.dump(tree))

# for node in ast.walk(tree):

#     if isinstance(node, ast.Compare):

#         print("left:", node.left.id)
#         print("operator:", type(node.ops[0]).__name__)
#         print("right:", node.comparators[0].value)

# *********************************************************************************************

# code = '''
# if x > 10:
#     print(x)
# '''

# tree = ast.parse(code)
# print(ast.dump(tree))

# for node in ast.walk(tree):

#     if isinstance(node, ast.If):

#         print("test:", type(node.test).__name__)
#         print("body:", type(node.body[0]).__name__)

# **************************************************************************************

# code = '''
# def add(a, b):
#     return a + b
# '''

# tree = ast.parse(code)
# print(ast.dump(tree))

# for node in ast.walk(tree):

#     if isinstance(node, ast.FunctionDef):

#         print("function:", node.name)
#         print("arguments:", len(node.args.args))
#         print("first argument:", node.args.args[0].arg)

# *************************************************************************************

# code = '''
# def add(a, b):
#     return a + b
# '''

# tree = ast.parse(code)
# print(ast.dump(tree))

# for node in ast.walk(tree):

#     if isinstance(node, ast.Return):

#         print("return type:", type(node.value).__name__)

# *********************************************************************************

# code = '''
# for x in numbers:
#     print(x)
# '''

# tree = ast.parse(code)
# print(ast.dump(tree))

# for node in ast.walk(tree):

#     if isinstance(node, ast.For):

#         print("target:", node.target.id)
#         print("iter:", node.iter.id)
#         print("body:", type(node.body[0]).__name__)

# *****************************************************************************************

code = '''
while x < 10:
    x += 1
'''

tree = ast.parse(code)
print(ast.dump(tree))

for node in ast.walk(tree):

    if isinstance(node, ast.While):

        print("test:", type(node.test).__name__)
        print("body:", type(node.body[0]).__name__)