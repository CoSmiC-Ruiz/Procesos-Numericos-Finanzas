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

def secante(f_expr, x0, x1, tol, N):
    print("\n" + "="*60)
    print("                   SECANTE")
    print("="*60)
    print("\nTabla de resultados:\n")
    print(f"| {'iter':^4} | {'xi':^14} | {'f(xi)':^10} | {'E':^9} |")
    print("|" + "-"*6 + "|" + "-"*16 + "|" + "-"*12 + "|" + "-"*11 + "|")

    fx0 = evaluar(f_expr, x0)
    fx1 = evaluar(f_expr, x1)

    print(f"| {0:^4} | {x0:^14.10f} | {fx0:^10.2e} | {'':^9} |")
    print(f"| {1:^4} | {x1:^14.10f} | {fx1:^10.2e} | {'':^9} |")

    for i in range(2, N + 1):
        if fx1 - fx0 == 0:
            print("\nError: división por cero (f(x1) - f(x0) = 0).")
            return None

        xi_new = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        fxi_new = evaluar(f_expr, xi_new)
        E = abs(xi_new - x1)

        print(f"| {i:^4} | {xi_new:^14.10f} | {fxi_new:^10.2e} | {E:^9.2e} |")

        x0, fx0 = x1, fx1
        x1, fx1 = xi_new, fxi_new

        if E < tol:
            break

    print(f"\nSe encontró una aproximación de la raíz en {x1:.15f}")
    print("="*60)
    return x1

def main():
    print("="*60)
    print("            SECANTE - Entrada de datos")
    print("="*60)
    print("\nEscribe la función usando notación matemática estándar.")
    print("Puedes usar: sin, cos, tan, log, ln, exp, sqrt, pi, e, etc.")
    print("Potencias: usa ^ o **   |   Ej: sin^2(x) o sin(x)**2")
    print("Ejemplo: ln(sin^2(x) + 1) - 1/2\n")

    f_expr = input("f(x) = ").strip()

    try:
        x0  = float(input("Valor inicial x0: "))
        x1  = float(input("Valor inicial x1: "))
        tol = float(input("Tolerancia Tol (Ej: 1e-7): "))
        N   = int(input("Número máximo de iteraciones N: "))
    except ValueError:
        print("Error: ingresa valores numéricos válidos.")
        return

    try:
        secante(f_expr, x0, x1, tol, N)
    except ValueError as e:
        print(f"\n{e}")

    input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()
