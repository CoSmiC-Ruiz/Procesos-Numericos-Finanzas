import math
import re

# Steffensen's method for finding roots of f(x) = 0.
# Applies Aitken's delta-squared (Δ²) acceleration to a fixed-point
# iteration g(x), achieving quadratic convergence without derivatives.
#
# Given g(x) such that x* = g(x*) (i.e. f(x) = x - g(x) = 0),
# three successive iterates are computed:
#   x1 = g(x0),  x2 = g(x1)
# Then the Aitken extrapolation gives the next approximation:
#   x_new = x0 - (x1 - x0)^2 / (x2 - 2*x1 + x0)
#
# Requires: a contractive g(x) with |g'(x*)| < 1 near the root.

def preprocesar(expr):
    funciones = r'(sin|cos|tan|log|ln|exp|sqrt|asin|acos|atan)'
    expr = re.sub(funciones + r'\^(\d+)\s*\(([^()]*)\)', r'\1(\3)**\2', expr)
    expr = expr.replace('^', '**')
    expr = expr.replace('ln(', 'log(')
    return expr

def evaluar(expr, x):
    try:
        expr_proc = preprocesar(expr)
        return eval(expr_proc, {"x": x, **{k: getattr(math, k) for k in dir(math)}})
    except Exception as e:
        raise ValueError(f"Error al evaluar en x={x}: {e}")

def steffensen(f_expr, g_expr, x0, tol, N):
    print("\n" + "="*60)
    print("                  STEFFENSEN")
    print("="*60)
    print("\nTabla de resultados:\n")
    print(f"| {'iter':^4} | {'xi':^14} | {'f(xi)':^10} | {'E':^9} |")
    print("|" + "-"*6 + "|" + "-"*16 + "|" + "-"*12 + "|" + "-"*11 + "|")

    xi  = x0
    fxi = evaluar(f_expr, xi)
    print(f"| {0:^4} | {xi:^14.10f} | {fxi:^10.2e} | {'':^9} |")

    for i in range(1, N + 1):
        # Three fixed-point steps for Aitken's Δ² formula
        x1 = evaluar(g_expr, xi)
        x2 = evaluar(g_expr, x1)

        denominador = x2 - 2 * x1 + xi

        if abs(denominador) < 1e-15:
            print("\nError: denominador cero. El método no puede continuar.")
            return None

        # Aitken's Δ² extrapolation
        xi_new  = xi - (x1 - xi) ** 2 / denominador
        fxi_new = evaluar(f_expr, xi_new)
        E       = abs(xi_new - xi)

        print(f"| {i:^4} | {xi_new:^14.10f} | {fxi_new:^10.2e} | {E:^9.2e} |")

        xi  = xi_new
        fxi = fxi_new

        if E < tol:
            break

    print(f"\nSe encontró una aproximación de la raíz en {xi:.15f}")
    print("="*60)
    return xi

def main():
    print("="*60)
    print("           STEFFENSEN - Entrada de datos")
    print("="*60)
    print("\nEscribe las funciones usando notación matemática estándar.")
    print("Puedes usar: sin, cos, tan, log, ln, exp, sqrt, pi, e, etc.")
    print("Potencias: usa ^ o **   |   Ej: sin^2(x) o sin(x)**2")
    print("\nNota: g(x) debe satisfacer x* = g(x*) y |g'(x*)| < 1.")
    print("Ejemplo f(x):  x**3 - x - 2")
    print("Ejemplo g(x):  (x + 2)**(1/3)\n")

    f_expr = input("f(x) = ").strip()
    g_expr = input("g(x) = ").strip()

    try:
        x0  = float(input("Valor inicial x0: "))
        tol = float(input("Tolerancia Tol (Ej: 1e-7): "))
        N   = int(input("Número máximo de iteraciones N: "))
    except ValueError:
        print("Error: ingresa valores numéricos válidos.")
        return

    try:
        steffensen(f_expr, g_expr, x0, tol, N)
    except ValueError as e:
        print(f"\n{e}")

    input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()
