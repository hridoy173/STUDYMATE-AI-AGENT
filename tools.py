
import ast
import operator


# Allowed mathematical operations
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calculator(expression: str) -> dict:
    """
    Safely calculate a mathematical expression.
    """

    try:
        tree = ast.parse(expression, mode="eval")

        def evaluate(node):

            if isinstance(node, ast.Expression):
                return evaluate(node.body)

            if isinstance(node, ast.Constant):
                if type(node.value) in (int, float):
                    return node.value
                raise ValueError("Invalid number")

            if isinstance(node, ast.BinOp):
                op = OPERATORS.get(type(node.op))

                if op is None:
                    raise ValueError("Unsupported operation")

                left = evaluate(node.left)
                right = evaluate(node.right)

                if isinstance(node.op, ast.Pow) and abs(right) > 10:
                    raise ValueError("Exponent too large")

                result = op(left, right)

                if abs(result) > 1e15:
                    raise ValueError("Result too large")

                return result

            if isinstance(node, ast.UnaryOp):
                op = OPERATORS.get(type(node.op))

                if op is None:
                    raise ValueError("Unsupported operation")

                return op(evaluate(node.operand))

            raise ValueError("Invalid mathematical expression")

        result = evaluate(tree)

        return {
            "success": True,
            "expression": expression,
            "result": result
        }

    except (ValueError, TypeError, SyntaxError, ZeroDivisionError) as e:

        return {
            "success": False,
            "error": str(e)
        }
