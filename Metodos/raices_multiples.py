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

def fmt(val):
    if val == 0:
        return f"{'0':^14}"
    if abs(val) < 1e-4 or abs(val) >= 1e10:
        return f"{val:^14.4e}"
    return f"{val:^14.10f}"

def raices_multiples(h_expr, dh_expr, ddh_expr, x0, tol, N):
    print("\n" + "="*60)
    print("               RAÍCES MÚLTIPLES")
    print("="*60)
    print("\nTabla de resultados:\n")
    print(f"| {'iter':^4} | {'xi':^14} | {'f(xi)':^9} | {'E':^9} |")
    print("|" + "-"*6 + "|" + "-"*16 + "|" + "-"*11 + "|" + "-"*11 + "|")

    xi = x0
    hxi = evaluar(h_expr, xi)
    print(f"| {0:^4} |{fmt(xi)}| {hxi:^9.1e} | {'':^9} |")

    for i in range(1, N + 1):
        dhxi  = evaluar(dh_expr, xi)
        ddhxi = evaluar(ddh_expr, xi)

        denominador = dhxi**2 - hxi * ddhxi

        if denominador == 0:
            print("\nError: denominador cero. El método no puede continuar.")
            return None

        xi_new = xi - hxi * dhxi / denominador
        hxi_new = evaluar(h_expr, xi_new)
        E = abs(xi_new - xi)

        print(f"| {i:^4} |{fmt(xi_new)}| {hxi_new:^9.1e} | {E:^9.1e} |")

        xi  = xi_new
        hxi = hxi_new

        if E < tol:
            break

    print(f"\nSe encontró una aproximación de la raíz en {xi:.15f}")
    print("="*60)
    return xi

def main():
    print("="*60)
    print("        RAÍCES MÚLTIPLES - Entrada de datos")
    print("="*60)
    print("\nEscribe las funciones usando notación matemática estándar.")
    print("Puedes usar: sin, cos, tan, log, ln, exp, sqrt, pi, e, etc.")
    print("Potencias: usa ^ o **   |   Ej: sin^2(x) o sin(x)**2")
    print("Ejemplo h(x):   exp(x) - x - 1")
    print("Ejemplo h'(x):  exp(x) - 1")
    print("Ejemplo h''(x): exp(x)\n")

    h_expr   = input("h(x)   = ").strip()
    dh_expr  = input("h'(x)  = ").strip()
    ddh_expr = input("h''(x) = ").strip()

    try:
        x0  = float(input("Valor inicial x0: "))
        tol = float(input("Tolerancia Tol (Ej: 1e-7): "))
        N   = int(input("Número máximo de iteraciones N: "))
    except ValueError:
        print("Error: ingresa valores numéricos válidos.")
        return

    try:
        raices_multiples(h_expr, dh_expr, ddh_expr, x0, tol, N)
    except ValueError as e:
        print(f"\n{e}")

    input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()
