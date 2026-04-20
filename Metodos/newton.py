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

def newton(f_expr, df_expr, x0, tol, N):
    print("\n" + "="*60)
    print("                    NEWTON")
    print("="*60)
    print("\nTabla de resultados:\n")
    print(f"| {'iter':^4} | {'xi':^13} | {'f(xi)':^10} | {'E':^9} |")
    print("|" + "-"*6 + "|" + "-"*15 + "|" + "-"*12 + "|" + "-"*11 + "|")

    xi = x0
    fxi = evaluar(f_expr, xi)
    print(f"| {0:^4} | {xi:^13.10f} | {fxi:^10.2e} | {'':^9} |")

    for i in range(1, N + 1):
        dfxi = evaluar(df_expr, xi)

        if dfxi == 0:
            print("\nError: la derivada es cero. El método no puede continuar.")
            return None

        xi_new = xi - fxi / dfxi
        fxi_new = evaluar(f_expr, xi_new)
        E = abs(xi_new - xi)

        print(f"| {i:^4} | {xi_new:^13.10f} | {fxi_new:^10.2e} | {E:^9.2e} |")

        xi = xi_new
        fxi = fxi_new

        if E < tol:
            break

    print(f"\nSe encontró una aproximación de la raíz en {xi:.15f}")
    print("="*60)
    return xi

def main():
    print("="*60)
    print("             NEWTON - Entrada de datos")
    print("="*60)
    print("\nEscribe las funciones usando notación matemática estándar.")
    print("Puedes usar: sin, cos, tan, log, ln, exp, sqrt, pi, e, etc.")
    print("Potencias: usa ^ o **   |   Ej: sin^2(x) o sin(x)**2")
    print("Ejemplo f(x):  ln(sin^2(x) + 1) - 1/2")
    print("Ejemplo f'(x): 2*sin(x)*cos(x) / (sin^2(x) + 1)\n")

    f_expr  = input("f(x)  = ").strip()
    df_expr = input("f'(x) = ").strip()

    try:
        x0  = float(input("Valor inicial x0: "))
        tol = float(input("Tolerancia Tol (Ej: 1e-7): "))
        N   = int(input("Número máximo de iteraciones N: "))
    except ValueError:
        print("Error: ingresa valores numéricos válidos.")
        return

    try:
        newton(f_expr, df_expr, x0, tol, N)
    except ValueError as e:
        print(f"\n{e}")

    input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()
