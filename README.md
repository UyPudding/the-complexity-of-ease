# 🧠 The Complexity of Ease (TCOE)

> Complex structure. Trivial truth.  
> A symbolic mathematics engine that generates highly non-trivial expressions — all guaranteed to simplify to exactly **1**.

🌐 **Live Website:**  
https://the-complexity-of-ease.onrender.com (Deployed by <i>Render.com</i>)

---

## 📖 Overview

**The Complexity of Ease (TCOE)** is a web-based symbolic expression generator built with Python and Flask.

The system constructs mathematically sophisticated expressions across multiple difficulty levels — including polynomials, recursive expression trees, derivatives, integrals, transcendental functions, and limits — while guaranteeing that every generated expression simplifies to:

\[
1
\]

This project explores the paradox:

> How complex can a mathematical structure become while preserving a trivial invariant?

---

## 🎯 Core Concept

Each expression is generated in two phases:

### 1️⃣ Structural Construction
A non-trivial symbolic expression is created using:
- Recursive expression trees
- Polynomial composition
- Trigonometric functions
- Exponential and logarithmic functions
- Derivatives and integrals
- Radical transformations
- Limit constructions

### 2️⃣ Identity Enforcement
The expression is transformed using rigorous mathematical identities such as:

- Multiplicative inverse  
  `f(x) * f(x)^(-1) = 1`

- Exponential cancellation  
  `exp(f(x) - f(x)) = 1`

- Trigonometric identity  
  `sin²(x) + cos²(x) = 1`

- Root-power symmetry  
  `√(|f(x)|^n) * ( √(|f(x)|^n) )^(-1) = 1`

Each result is symbolically validated to ensure exact equality to **1**.

---

## 🧩 Difficulty Levels

| Level        | Description |
|--------------|------------|
| Elementary   | Basic arithmetic constructions |
| Middle       | Polynomial structures and radical transformations |
| High         | Recursive symbolic trees, derivatives, integrals, transcendental and limit constructions |

All levels are guaranteed to simplify to **1**.

---

## 🏗 Architecture

### Backend
- Python
- Flask
- SymPy (Symbolic Mathematics Engine)

### Frontend
- HTML
- CSS
- JavaScript

### Deployment
- Cloud Web Service (Render)

---

## 🔬 Expression Validation Pipeline

Every generated expression undergoes:

1. Core structure generation  
2. Identity transformation  
3. Symbolic simplification  
4. Exact equality verification  
5. Structural uniqueness check  

If validation fails, regeneration occurs automatically.

---

## 🚀 Run Locally

```bash
pip install -r requirements.txt
python app.py
```

<span style="text-align: center;">THANKS FOR VISITING! 🍪</span>
