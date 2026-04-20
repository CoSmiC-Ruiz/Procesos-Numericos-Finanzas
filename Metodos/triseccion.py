import math
import re

# Trisection method for finding roots of f(x) = 0.
# Divides the interval [a, b] into three equal parts at each iteration
# using points x1 = a + h and x2 = a + 2h where h = (b-a)/3,
# then selects the sub-interval guaranteed to contain a root.
# Reduces the bracket by a factor of 1/3 per iteration (vs 1/2 for Bisection).

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

def triseccion(f_expr, a, b, tol, N):
    print("\n" + "="*80)
    print("                          TRISECCIÓN")
    print("="*80)

    fa = evaluar(f_expr, a)
    fb = evaluar(f_expr, b)

    if fa * fb > 0:
        print("Error: f(a) y f(b) tienen el mismo signo. No se garantiza raíz en [a, b].")
        return None

    print("\nTabla de resultados:\n")
    print(f"| {'iter':^4} | {'a':^13} | {'x1':^13} | {'x2':^13} | {'b':^13} | {'E':^9} |")
    print("|" + "-"*6 + "|" + "-"*15 + "|" + "-"*15 + "|" + "-"*15 + "|" + "-"*15 + "|" + "-"*11 + "|")

    for i in range(1, N + 1):
        x1 = a + (b - a) / 3
        x2 = a + 2 * (b - a) / 3

        fx1 = evaluar(f_expr, x1)
        fx2 = evaluar(f_expr, x2)

        E = b - a

        print(f"| {i:^4} | {a:^13.10f} | {x1:^13.10f} | {x2:^13.10f} | {b:^13.10f} | {E:^9.2e} |")

        if E < tol:
            break

        # Check for exact roots at the trisection points
        if abs(fx1) < 1e-15:
            raiz = x1
            print(f"\nRaíz exacta encontrada en x1 = {raiz:.15f}")
            print("="*80)
            return raiz
        if abs(fx2) < 1e-15:
            raiz = x2
            print(f"\nRaíz exacta encontrada en x2 = {raiz:.15f}")
            print("="*80)
            return raiz

        # Select the sub-interval containing the root
        if fa * fx1 < 0:
            b  = x1
            fb = fx1
        elif fx1 * fx2 < 0:
            a  = x1; fa = fx1
            b  = x2; fb = fx2
        else:
            a  = x2
            fa = fx2

    raiz = (a + b) / 2
    print(f"\nSe encontró una aproximación de la raíz en {raiz:.15f}")
    print("="*80)
    return raiz

def main():
    print("="*80)
    print("                   TRISECCIÓN - Entrada de datos")
    print("="*80)
    print("\nEscribe la función usando notación matemática estándar.")
    print("Puedes usar: sin, cos, tan, log, ln, exp, sqrt, pi, e, etc.")
    print("Potencias: usa ^ o **   |   Ej: sin^2(x) o sin(x)**2")
    print("Ejemplo: ln(sin^2(x) + 1) - 1/2\n")

    f_expr = input("f(x) = ").strip()

    try:
        a   = float(input("Extremo izquierdo a: "))
        b   = float(input("Extremo derecho b: "))
        tol = float(input("Tolerancia Tol (Ej: 1e-7): "))
        N   = int(input("Número máximo de iteraciones N: "))
    except ValueError:
        print("Error: ingresa valores numéricos válidos.")
        return

    try:
        triseccion(f_expr, a, b, tol, N)
    except ValueError as e:
        print(f"\n{e}")

    input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()
