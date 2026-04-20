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
        raise ValueError(f"Error al evaluar f({x}): {e}")

def regla_falsa(f_expr, a, b, tol, N):
    print("\n" + "="*75)
    print("                          REGLA FALSA")
    print("="*75)

    fa = evaluar(f_expr, a)
    fb = evaluar(f_expr, b)

    if fa * fb > 0:
        print("Error: f(a) y f(b) tienen el mismo signo. No se garantiza raíz en [a, b].")
        return None

    print("\nTabla de resultados:\n")
    print(f"| {'iter':^4} | {'a':^13} | {'xr':^13} | {'b':^14} | {'f(Xr)':^10} | {'E':^9} |")
    print("|" + "-"*6 + "|" + "-"*15 + "|" + "-"*15 + "|" + "-"*16 + "|" + "-"*12 + "|" + "-"*11 + "|")

    xr_prev = None

    for i in range(1, N + 1):
        xr = b - fb * (b - a) / (fb - fa)
        fxr = evaluar(f_expr, xr)

        E = abs(xr - xr_prev) if xr_prev is not None else None

        if E is not None:
            print(f"| {i:^4} | {a:^13.10f} | {xr:^13.10f} | {b:^14.10f} | {fxr:^10.2e} | {E:^9.2e} |")
        else:
            print(f"| {i:^4} | {a:^13.10f} | {xr:^13.10f} | {b:^14.10f} | {fxr:^10.2e} | {'':^9} |")

        if E is not None and E < tol:
            break

        if fa * fxr < 0:
            b = xr
            fb = fxr
        else:
            a = xr
            fa = fxr

        xr_prev = xr

    print(f"\nSe encontró una aproximación de la raíz en {xr:.15f}")
    print("="*75)
    return xr

def main():
    print("="*75)
    print("                  REGLA FALSA - Entrada de datos")
    print("="*75)
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
        regla_falsa(f_expr, a, b, tol, N)
    except ValueError as e:
        print(f"\n{e}")

    input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()
