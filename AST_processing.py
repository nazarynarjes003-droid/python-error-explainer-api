import ast

def parse_code(code):
    tree = ast.parse(code)
    return tree

def get_value_type(value, variables = None):

    if variables is None:
        variables = {}

    if isinstance(value, ast.Constant):

        if isinstance(value.value, str):
            return "String"

        elif isinstance(value.value, bool):
            return "Boolean"

        elif isinstance(value.value, int):
            return "Integer"

        elif isinstance(value.value, float):
            return "Float"

        elif value.value is None:
            return "None"

    elif isinstance(value, ast.List):
        return "List"

    elif isinstance(value, ast.Dict):
        return "Dictionary"

    elif isinstance(value, ast.Tuple):
        return "Tuple"

    elif isinstance(value, ast.Set):
        return "Set"

    elif isinstance(value, ast.Name):
        return variables.get(value.id, {}).get("type","Unknown")

    elif isinstance(value, ast.UnaryOp):
        return get_value_type(value.operand, variables)

    elif isinstance(value, ast.BinOp):
        left_type = get_value_type(value.left, variables)
        right_type = get_value_type(value.right, variables)

        if left_type == right_type:
            return left_type

        return"Unknown"

    elif isinstance(value, ast.Call):

        if isinstance(value.func, ast.Name):

            builtin_return_types = {
                "str": "String",
                "int": "Integer",
                "float": "Float",
                "bool": "Boolean",
                "list": "List",
                "dict": "Dictionary",
                "set": "Set",
                "tuple": "Tuple"
            }

            return builtin_return_types.get(value.func.id, "Unknown")

        return "Unknown"

    elif isinstance(value, ast.Subscript):

        if isinstance(value.value, ast.Name):
            base_type = variables.get(value.value.id, {}).get("type", "Unknown")

            if base_type == "String":
                return "String"

        return "Unknown"

    return "Unknown"


def analyze_variables(tree):

    variables = {}

    for node in ast.walk(tree):

        if isinstance(node, ast.Assign):

            for target in node.targets:

                if isinstance(target, ast.Name):

                    variables[target.id] = {
                        "type": get_value_type(node.value, variables),
                        "value": ast.unparse(node.value)
                    }

                elif isinstance(target, ast.Tuple) and isinstance(node.value, ast.Tuple):
                    for name_node, value_node in zip(target.elts, node.value.elts):

                        if isinstance(name_node, ast.Name):

                            variables[name_node.id] = {
                                "type": get_value_type(value_node, variables),
                                "value": ast.unparse(value_node)
                            }

    return variables


def analyze_oprations(tree):

    oprations = []

    for node in ast.walk(tree):

        if isinstance(node, ast.BinOp):

            if isinstance(node.op, ast.Add):
                opration = "Add"

            elif isinstance(node.op, ast.Sub):
                opration = "Subtract"

            elif isinstance(node.op, ast.Mult):
                opration = "Multiply"

            elif isinstance(node.op, ast.Div):
                opration = "Divide"

            else:
                continue

            oprations.append({
                "operation": opration,
                "expression": ast.unparse(node)
            })

    return oprations

def analyze_comprisons(tree):

    comprisons = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Compare):

            for operator in node.op:

                if isinstance(operator, ast.Gt):
                    comprison = "GreaterThan"

                elif isinstance(operator, ast.Lt):
                    comprison = "LessThan"

                elif isinstance(operator, ast.GtE):
                    comprison = "GreaterThanOrEqual"

                elif isinstance(operator, ast.LtE):
                    comprison = "LessThanOrEqual"

                elif isinstance(operator, ast.Eq):
                    comprison = "Equal"

                elif isinstance(operator, ast.NotEq):
                    comprison = "NotEqual"

                else:
                    continue

                comprisons.append({
                    "comparison" : comprison,
                    "expression" : ast.unparse(node)
                })

    return comprisons

def analyze_conditions(tree):

    conditions = []

    for node in ast.walk(tree):

        if isinstance(node, ast.If):

            conditions.append({
                "type": "If",
                "condition" : ast.unparse(node.test)
            })

    return conditions

def analyze_loops(tree):

    loops = []

    for node in ast.walk(tree):

        if isinstance(node, ast.For):

            loops.append({
                "type": "For",
                "target": ast.unparse(node.target),
                "iterable" : ast.unparse(node.iter)
            })

        elif isinstance(node, ast.While):

            loops.append({
                "type": "While",
                "condition": ast.unparse(node.test)
            })

    return loops

def analyze_functions(tree):

    functions = []

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):

            arguments = []

            for argument in node.args.args:
                arguments.append(argument.arg)

            functions.append({
                "name" :node.name,
                "arguments": arguments
            })

    return functions 

def analyze_returns(tree):

    returns = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Return):

            if node.value is not None:
                returns.append({
                    "value": ast.unparse(node.value)
                })

            else:
                returns.append({
                    "value":"None"
                })

    return returns

def analyze_calls(tree):

    calls = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Call):

            if isinstance(node.func, ast.Name):

                function_name = node.func.id

            elif isinstance(node.func, ast.Attribute):

                function_name = node.func.attr

            else:

                function_name = "Unknown"

            arguments = []

            for argument in node.args:
                arguments.append(ast.unparse(argument))

            calls.append({
                "function": function_name,
                "arguments": arguments
            })

    return calls

def analyze_subscripts(tree):

    subscripts = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Subscript):

            subscripts.append({
                "expression": ast.unparse(node)
            })

    return subscripts


def analyze_attributes(tree):

    attributes = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Attribute):

            attributes.append({
                "object": ast.unparse(node.value),
                "attribute": node.attr
            })

    return attributes


def find_suspicious_patterns(tree, variables):

    suspicious = []

    opration_names = {
        ast.Add: "Add",
        ast.Sub: "Subtract",
        ast.Mult: "Multiply",
        ast.Div: "Divide"        
    }

    for node in ast.walk(tree):

        if isinstance(node, ast.BinOp) and type(node.op) in opration_names:

                left_type = get_value_type(node.left, variables)
                right_type = get_value_type(node.right, variables)

                if left_type != "Unknown" and right_type != "Unknown":

                    if left_type != right_type:

                        suspicious.append({
                        "expression": ast.unparse(node),
                        "possible_error": "TypeError",
                        "description": f"عملیات {opration_names[type(node.op)]} بین دو مقدار با نوع داده {left_type} و {right_type} انجام شده است."  
                        })

    return suspicious

def analyze_code(code):

    tree = parse_code(code)

    variables = analyze_variables(tree)

    result = {
        "variables": variables,
        "operations": analyze_oprations(tree),
        "comparisons": analyze_comprisons(tree),
        "conditions": analyze_conditions(tree),
        "loops": analyze_loops(tree),
        "functions": analyze_functions(tree),
        "returns": analyze_returns(tree),
        "calls": analyze_calls(tree),
        "subscripts": analyze_subscripts(tree),
        "attributes": analyze_attributes(tree),
        "suspicious": find_suspicious_patterns(
            tree,
            variables
        )
    }

    return result