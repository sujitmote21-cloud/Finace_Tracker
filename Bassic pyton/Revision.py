"""
Unit 2 - Assignment 1 : Part A
Linear/Non-linear equations, Limits, Differentiation, Integration,
Series and Differential Equations - solved using Python (SymPy).

Run this file top to bottom; each question is a separate, clearly
labelled block that prints its own output.
"""

import sympy as sp

x, y, t = sp.symbols('x y t')

print("="*70)
print("LINEAR AND NON-LINEAR EQUATIONS")
print("="*70)

# ---------------------------------------------------------------
# Q1. f = x^2 + y^3 - 3xy . Evaluate f at x = 1, y = 2
# ---------------------------------------------------------------
f = x**2 + y**3 - 3*x*y
val = f.subs({x: 1, y: 2})
print("\nQ1. f(x,y) =", f)
print("f(1,2) =", val)

# ---------------------------------------------------------------
# Q2. Find the expression when x = 1 - y  (substitute into f)
# ---------------------------------------------------------------
f_sub = sp.expand(f.subs(x, 1 - y))
print("\nQ2. f(1-y, y) =", f_sub)

# ---------------------------------------------------------------
# Q3. Expand (x+4)(x+2)
# ---------------------------------------------------------------
expr3 = sp.expand((x + 4) * (x + 2))
print("\nQ3. (x+4)(x+2) expanded =", expr3)

# ---------------------------------------------------------------
# Q4. Factorise x^2 - 16
# ---------------------------------------------------------------
expr4 = sp.factor(x**2 - 16)
print("\nQ4. Factorised x^2 - 16 =", expr4)

# ---------------------------------------------------------------
# Q5. Simplify (x^2 + 2x + 1) / (x + 1)
# ---------------------------------------------------------------
expr5 = sp.simplify((x**2 + 2*x + 1) / (x + 1))
print("\nQ5. Simplified (x^2+2x+1)/(x+1) =", expr5)

# ---------------------------------------------------------------
# Q6. Find the roots of x^2 + x + 1 = 0
# ---------------------------------------------------------------
roots6 = sp.solve(sp.Eq(x**2 + x + 1, 0), x)
print("\nQ6. Roots of x^2+x+1=0 :", roots6)

# ---------------------------------------------------------------
# Q7. Manufacturer problem - simultaneous equations
#     A + B = 120 units, 50A + 100B = 9000
# ---------------------------------------------------------------
A, B = sp.symbols('A B')
eq1 = sp.Eq(A + B, 120)
eq2 = sp.Eq(50*A + 100*B, 9000)
sol7 = sp.solve((eq1, eq2), (A, B))
print("\nQ7. Units of Product A and B produced:", sol7)

print("\n" + "="*70)
print("LIMIT")
print("="*70)

# ---------------------------------------------------------------
# Q8. f(x) = (x^2-4)/(x-2) for x != 2 ; f(x) = 5 for x = 2
#     Check continuity at x = 2 using the limit.
# ---------------------------------------------------------------
f8 = (x**2 - 4) / (x - 2)
f8_simplified = sp.simplify(f8)
limit8 = sp.limit(f8, x, 2)
f_value_at_2 = 5  # given piecewise value at x = 2

print("\nQ8. f(x) =", f8, " -> simplified:", f8_simplified)
print("lim x->2 f(x) =", limit8)
print("f(2) as defined in the piecewise function =", f_value_at_2)

if limit8 == f_value_at_2:
    print("The function IS continuous at x = 2.")
else:
    print("The function is DISCONTINUOUS at x = 2.")
    print(f"Since the limit ({limit8}) exists but does not equal f(2) "
          f"({f_value_at_2}), this is a REMOVABLE discontinuity.")

print("\n" + "="*70)
print("DIFFERENTIATION")
print("="*70)

# ---------------------------------------------------------------
# Q9. f(x) = x^4 - 5x^3 + 6x^2 - 2x + 1
#     First and second derivatives
# ---------------------------------------------------------------
f9 = x**4 - 5*x**3 + 6*x**2 - 2*x + 1
f9_prime = sp.diff(f9, x)
f9_double_prime = sp.diff(f9, x, 2)
print("\nQ9. f(x)  =", f9)
print("f'(x)  =", f9_prime)
print("f''(x) =", f9_double_prime)

# ---------------------------------------------------------------
# Q10. f(x) = x^3 - 6x^2 + 9x + 1
#      Critical points, classify as max/min/inflection
# ---------------------------------------------------------------
f10 = x**3 - 6*x**2 + 9*x + 1
f10_prime = sp.diff(f10, x)
f10_double_prime = sp.diff(f10, x, 2)
critical_points = sp.solve(sp.Eq(f10_prime, 0), x)

print("\nQ10. f(x) =", f10)
print("f'(x) =", f10_prime)
print("f''(x) =", f10_double_prime)
print("Critical points:", critical_points)

for cp in critical_points:
    second_val = f10_double_prime.subs(x, cp)
    if second_val > 0:
        nature = "Local Minimum"
    elif second_val < 0:
        nature = "Local Maximum"
    else:
        nature = "Point of Inflection (needs further check)"
    print(f"  x = {cp}: f''(x) = {second_val}  -> {nature}  "
          f"(f({cp}) = {f10.subs(x, cp)})")

# ---------------------------------------------------------------
# Q11. C(x) = x^3 - 6x^2 + 15x + 50
#      Marginal cost = C'(x), evaluate at x = 4
# ---------------------------------------------------------------
C = x**3 - 6*x**2 + 15*x + 50
marginal_cost = sp.diff(C, x)
mc_at_4 = marginal_cost.subs(x, 4)
print("\nQ11. C(x) =", C)
print("Marginal Cost C'(x) =", marginal_cost)
print("Marginal Cost at x = 4 :", mc_at_4)

print("\n" + "="*70)
print("INTEGRATION")
print("="*70)

# ---------------------------------------------------------------
# Q12. Integrate 2x/(x^2+1) twice with respect to x
# ---------------------------------------------------------------
g12 = 2*x / (x**2 + 1)
first_integral = sp.integrate(g12, x)
second_integral = sp.integrate(first_integral, x)
print("\nQ12. g(x) =", g12)
print("First integral  :", first_integral, "+ C1")
print("Second integral :", second_integral, "+ C1*x + C2")

# ---------------------------------------------------------------
# Q13. Slope = 3x^2 + 2x, curve passes through (1,5)
#      Find the equation of the curve
# ---------------------------------------------------------------
slope13 = 3*x**2 + 2*x
C1 = sp.symbols('C1')
y_expr13 = sp.integrate(slope13, x) + C1
C1_value = sp.solve(sp.Eq(y_expr13.subs(x, 1), 5), C1)[0]
curve13 = y_expr13.subs(C1, C1_value)
print("\nQ13. dy/dx =", slope13)
print("y (general) =", y_expr13)
print("Using (1,5): C =", C1_value)
print("Equation of the curve: y =", curve13)

# ---------------------------------------------------------------
# Q14. pdf f(x) = 3x^2, 0 <= x <= 1
#      Total probability (definite integral 0 to 1) + indefinite integral
# ---------------------------------------------------------------
f14 = 3*x**2
definite14 = sp.integrate(f14, (x, 0, 1))
indefinite14 = sp.integrate(f14, x)
print("\nQ14. f(x) =", f14, " for 0<=x<=1")
print("Definite integral (0 to 1) i.e. total probability =", definite14)
print("Indefinite integral =", indefinite14, "+ C")

print("\n" + "="*70)
print("SERIES")
print("="*70)

# ---------------------------------------------------------------
# Q15. Maclaurin series expansion of e^x up to x^5 term
# ---------------------------------------------------------------
series15 = sp.series(sp.exp(x), x, 0, 6)
print("\nQ15. Maclaurin series of e^x up to x^5 term:")
print(series15)

print("\n" + "="*70)
print("DIFFERENTIAL EQUATIONS")
print("="*70)

# ---------------------------------------------------------------
# Q16. Solve dy/dx + 2y = 3  WITHOUT the inbuilt dsolve command
#      (first order linear ODE - integrating factor method),
#      then compare with the inbuilt command.
# ---------------------------------------------------------------
print("\nQ16. dy/dx + 2y = 3")
print("-- Manual solution (integrating factor method) --")
Cc = sp.symbols('C')
yf = sp.Function('y')
IF = sp.exp(sp.integrate(2, x))                     # integrating factor e^(2x)
rhs = sp.integrate(3 * IF, x) + Cc                  # y * IF = integral(3*IF dx) + C
y_manual = sp.simplify(rhs / IF)
print("Integrating factor =", IF)
print("Manual general solution: y =", y_manual)

print("-- Using SymPy's inbuilt dsolve --")
ode16 = sp.Eq(sp.diff(yf(x), x) + 2*yf(x), 3)
sol16 = sp.dsolve(ode16, yf(x))
print("dsolve result:", sol16)

# ---------------------------------------------------------------
# Q17. Solve y'' + y = e^x ;  y(0) = 1
# ---------------------------------------------------------------
print("\nQ17. y'' + y = e^x ,  y(0) = 1")
ode17 = sp.Eq(sp.diff(yf(x), x, 2) + yf(x), sp.exp(x))
sol17 = sp.dsolve(ode17, yf(x), ics={yf(0): 1})
print("Solution:", sol17)

# ---------------------------------------------------------------
# Q18. Solve y'' + y = 0 ;  y(0) = 0 ,  y'(0) = 1
# ---------------------------------------------------------------
print("\nQ18. y'' + y = 0 ,  y(0) = 0 , y'(0) = 1")
ode18 = sp.Eq(sp.diff(yf(x), x, 2) + yf(x), 0)
sol18 = sp.dsolve(ode18, yf(x), ics={yf(0): 0, sp.diff(yf(x), x).subs(x, 0): 1})
print("Solution:", sol18)

# ---------------------------------------------------------------
# Q19. Solve d^2y/dx^2 - y = 0  WITHOUT the inbuilt dsolve command
#      (auxiliary/characteristic equation method)
# ---------------------------------------------------------------
print("\nQ19. d^2y/dx^2 - y = 0  (manual, characteristic equation method)")
m = sp.symbols('m')
char_eq = sp.Eq(m**2 - 1, 0)
roots19 = sp.solve(char_eq, m)
C1s, C2s = sp.symbols('C1 C2')
y_manual19 = C1s * sp.exp(roots19[0]*x) + C2s * sp.exp(roots19[1]*x)
print("Characteristic equation: m^2 - 1 = 0  -> roots:", roots19)
print("Manual general solution: y =", y_manual19)

print("-- Using SymPy's inbuilt dsolve for comparison --")
ode19 = sp.Eq(sp.diff(yf(x), x, 2) - yf(x), 0)
sol19 = sp.dsolve(ode19, yf(x))
print("dsolve result:", sol19)

# ---------------------------------------------------------------
# Q20. Bacterial growth: dB/dt = k*B , B(0) = 500
#      Solve using SymPy and apply the initial condition.
# ---------------------------------------------------------------
print("\nQ20. Bacterial growth: dB/dt = k*B ,  B(0) = 500")
k = sp.symbols('k', positive=True)
Bf = sp.Function('B')
ode20 = sp.Eq(sp.diff(Bf(t), t), k * Bf(t))
sol20_general = sp.dsolve(ode20, Bf(t))
print("General solution:", sol20_general)

sol20_particular = sp.dsolve(ode20, Bf(t), ics={Bf(0): 500})
print("Particular solution using B(0) = 500:", sol20_particular)

print("\n" + "="*70)
print("END OF ASSIGNMENT")
print("="*70)