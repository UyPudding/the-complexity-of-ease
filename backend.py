# Symbolic Expression Generator (Guaranteed to Equal Simple Result (Demo: Only Equal 1))
# ------------------------------------------------------

# This application generates symbolic mathematical expressions that are
# structurally complex but algebraically equivalent to Simple result.

# Expressions are constructed using controlled symbolic manipulation
# and validated via symbolic simplification to ensure correctness.

# Technologies:
# - Flask: Web framework
# - SymPy: Symbolic mathematics engine

import random
import secrets
import os
import sympy as sp
from flask import Flask, request, jsonify, render_template

# ==========================================================
# INITIALIZATION
# ==========================================================

# Seed randomness using high-entropy source to avoid predictable patterns
random.seed(secrets.randbits(64))

# Define main symbolic variable
x = sp.Symbol('x')

# Store structural representations of generated expressions
# Used to prevent duplicates
generated = set()

# ==========================================================
# UTILITY FUNCTIONS
# ==========================================================

def rand_int(a=-9, b=9):

    # Generate a non-zero random integer in [a, b].
    # Zero is excluded to avoid trivial simplifications.

    n = 0
    while n == 0:
        n = random.randint(a, b)
    return n


def normalize(expr):

    # Convert expression to structural representation.
    # Used for uniqueness checking.
    return sp.srepr(expr)

# ==========================================================
# CORE EXPRESSION BUILDERS
# ==========================================================

# ---------------------------
# LEVEL 1 – Elementary Algebra
# ---------------------------

def build_elementary():

    # Construct a basic arithmetic expression consisting of
    # additions, subtractions, multiplications, and divisions.

    # Evaluation is disabled to preserve structural complexity.

    expr = sp.Integer(rand_int())

    for _ in range(random.randint(2, 4)):
        op = random.choice(['+', '-', '*', '/'])
        num = sp.Integer(rand_int())

        if op == '+':
            expr = sp.Add(expr, num, evaluate=False)
        elif op == '-':
            expr = sp.Add(expr, -num, evaluate=False)
        elif op == '*':
            expr = sp.Mul(expr, num, evaluate=False)
        else:
            # Division implemented as multiplication by inverse
            expr = sp.Mul(expr, sp.Pow(num, -1, evaluate=False), evaluate=False)

    return expr


# ---------------------------
# LEVEL 2 – Polynomial Structures
# ---------------------------

def build_middle():

    # Construct polynomial expressions of degree 1–3.
    # May optionally include polynomial multiplication
    # and radical transformations.

    degree = random.randint(1, 3)
    expr = 0

    for i in range(degree + 1):
        expr = sp.Add(
            expr,
            sp.Mul(rand_int(), x**i, evaluate=False),
            evaluate=False
        )

    # Optional multiplication by another polynomial
    if random.random() < 0.5:
        degree2 = random.randint(1, 2)
        expr2 = 0
        for i in range(degree2 + 1):
            expr2 = sp.Add(
                expr2,
                sp.Mul(rand_int(), x**i, evaluate=False),
                evaluate=False
            )
        expr = sp.Mul(expr, expr2, evaluate=False)

    # Optional structural transformation: sqrt(expr^2)
    if random.random() < 0.5:
        expr = sp.sqrt(sp.Pow(expr, 2, evaluate=False))

    return expr


# ---------------------------
# LEVEL 3 – Recursive Expression Trees
# ---------------------------

def random_tree(depth):

    # Recursively generate a symbolic expression tree.

    # At depth 0:
    #    Choose a base symbolic object.
    # At higher depths:
    #    Combine subtrees via addition, subtraction, or multiplication.

    if depth == 0:
        base = random.choice([
            build_middle(),
            sp.sin(x),
            sp.cos(x),
            sp.exp(x),
            sp.log(sp.Abs(x)),
            x,
            sp.Integer(rand_int())
        ])

        # Optional root-power transformation
        if random.random() < 0.3:
            n = random.randint(2, 6)
            base = sp.Pow(sp.Abs(base), n, evaluate=False)
            base = sp.Pow(base, sp.Rational(1, n), evaluate=False)

        return base

    left = random_tree(depth - 1)
    right = random_tree(depth - 1)

    op = random.choice(['+', '-', '*'])

    if op == '+':
        return sp.Add(left, right, evaluate=False)
    elif op == '-':
        return sp.Add(left, -right, evaluate=False)
    else:
        return sp.Mul(left, right, evaluate=False)


def build_high():

    # Construct advanced symbolic expressions by:
    # - Generating a recursive tree
    # - Wrapping it with derivative, integral, or transcendental functions

    expr = random_tree(3)

    wrapper = random.choice([
        lambda e: sp.Derivative(e, x),
        lambda e: sp.Integral(e, x),
        lambda e: sp.sin(e),
        lambda e: sp.exp(e)
    ])

    return wrapper(expr)


# ==========================================================
# FORCE EXPRESSION TO EQUAL 1
# ==========================================================

def force_equal_one(expr, level): 

    # Transform a core expression into a mathematically
    # equivalent form that simplifies to 1.

    # Different strategies are used depending on difficulty level.

    expr = sp.sympify(expr)

    if level == 1:
        # Multiplicative inverse identity: f(x) * f(x)^(-1) = 1
        return sp.Mul(expr, sp.Pow(expr, -1, evaluate=False), evaluate=False)

    elif level == 2:
        choice = random.choice(["mul_inverse", "shifted"])

        if choice == "mul_inverse":
            return sp.Mul(expr, sp.Pow(expr, -1, evaluate=False), evaluate=False)
        else:
            # (f(x) + 1) * (f(x) + 1)^(-1) = 1
            num = sp.Add(expr, 1, evaluate=False)
            return sp.Mul(num, sp.Pow(num, -1, evaluate=False), evaluate=False)

    else:
        choice = random.choice([
            "mul_inverse",
            "exp_zero",
            "trig_identity",
            "root_power",
            "limit_safe"
        ])

        if choice == "mul_inverse":
            return sp.Mul(expr, sp.Pow(expr, -1, evaluate=False), evaluate=False)

        elif choice == "exp_zero":
            # e^(f(x) - f(x)) = e^0 = 1
            zero_part = sp.Add(expr, -expr, evaluate=False)
            return sp.exp(zero_part)

        elif choice == "root_power":
            n = random.randint(2, 6)
            base = sp.Pow(sp.Abs(expr), n, evaluate=False)
            root = sp.Pow(base, sp.Rational(1, n), evaluate=False)
            return sp.Mul(root, sp.Pow(root, -1, evaluate=False), evaluate=False)

        elif choice == "limit_safe":
            # Construct a limit expression that evaluates to 1
            point = random.choice([0, 1, -1, 2])

            limit_form = random.choice([
                "ratio",
                "exp_zero",
                "trig_identity"
            ])

            if limit_form == "ratio":
                core = sp.Mul(expr, sp.Pow(expr, -1, evaluate=False), evaluate=False)

            elif limit_form == "exp_zero":
                zero_part = sp.Add(expr, -expr, evaluate=False)
                core = sp.exp(zero_part)

            else:
                # sin^2(x) + cos^2(x) = 1
                core = sp.Add(
                    sp.Pow(sp.sin(expr), 2, evaluate=False),
                    sp.Pow(sp.cos(expr), 2, evaluate=False),
                    evaluate=False
                )

            return sp.Limit(core, x, point)

        else:
            return sp.Add(
                sp.Pow(sp.sin(expr), 2, evaluate=False),
                sp.Pow(sp.cos(expr), 2, evaluate=False),
                evaluate=False
            )


# ==========================================================
# GENERATION PIPELINE
# ==========================================================

def generate_expression(level):
   # Generate a structurally unique expression that simplifies to 1.

    # Validation process:
    # 1. Build core expression
    # 2. Transform to force equality to 1
    # 3. Symbolically simplify
    # 4. Verify exact equality
    # 5. Ensure structural uniqueness

    for _ in range(50):  # Prevent infinite generation loop

        if level == 1:
            core = build_elementary()
        elif level == 2:
            core = build_middle()
        else:
            core = build_high()

        expr = force_equal_one(core, level)

        try:
            evaluated = sp.simplify(expr)
        except:
            continue

        # Ensure exact symbolic equality to 1
        if sp.simplify(sp.Add(evaluated, -1)) != 0:
            continue

        key = normalize(expr)
        if key in generated:
            continue

        generated.add(key)
        return expr

    raise ValueError("Failed to generate expression")


# ==========================================================
# FLASK WEB LAYER
# ==========================================================

app = Flask(__name__)

@app.route("/")
def home():
    # Render main interface page.
 
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    # API endpoint for expression generation.

    # equest JSON:
    #   { "level": 1 | 2 | 3 }

    #Response JSON:
      #  - expr  : string representation
      #  - latex : LaTeX formatted expression
      #  - level : difficulty level

    level = int(request.json.get("level"))

    expr = generate_expression(level)
    latex_expr = sp.latex(expr)

    return jsonify({
        "expr": str(expr),
        "latex": latex_expr,
        "level": level
    })


if __name__ == "__main__":
    app.run(debug=True)



# ---- THANKS FOR READING =))) ----
