import math
import re

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

def punto_fijo(f_expr, g_expr, x0, tol, N):
    print("\n" + "="*60)
    print("                  PUNTO FIJO")
    print("="*60)
    print("\nTabla de resultados:\n")
    print(f"| {'iter':^4} | {'xi':^14} | {'f(xi)':^9} | {'E':^9} |")
    print("|" + "-"*6 + "|" + "-"*16 + "|" + "-"*11 + "|" + "-"*11 + "|")

    xi = x0
    fxi = evaluar(f_expr, xi)
    print(f"| {0:^4} | {xi:^14.10f} | {fxi:^9.2e} | {'':^9} |")

    for i in range(1, N + 1):
        xi_new = evaluar(g_expr, xi)
        fxi_new = evaluar(f_expr, xi_new)
        E = abs(xi_new - xi)

        print(f"| {i:^4} | {xi_new:^14.10f} | {fxi_new:^9.2e} | {E:^9.2e} |")

        xi = xi_new
        fxi = fxi_new

        if E < tol:
            break

    print(f"\nSe encontró una aproximación de la raíz en {xi:.15f}")
    print("="*60)
    return xi

def main():
    print("="*60)
    print("           PUNTO FIJO - Entrada de datos")
    print("="*60)
    print("\nEscribe las funciones usando notación matemática estándar.")
    print("Puedes usar: sin, cos, tan, log, ln, exp, sqrt, pi, e, etc.")
    print("Potencias: usa ^ o **   |   Ej: sin^2(x) o sin(x)**2")
    print("Ejemplo f(x):  ln(sin^2(x) + 1) - 1/2 - x")
    print("Ejemplo g(x):  ln(sin^2(x) + 1) - 1/2\n")

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
        punto_fijo(f_expr, g_expr, x0, tol, N)
    except ValueError as e:
        print(f"\n{e}")

    input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()
