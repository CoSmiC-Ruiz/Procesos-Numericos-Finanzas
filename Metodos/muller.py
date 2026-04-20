import math
import cmath
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

def muller(f_expr, x0, x1, x2, tol, N):
    print("\n" + "="*60)
    print("                    MÜLLER")
    print("="*60)
    print("\nTabla de resultados:\n")
    print(f"| {'iter':^4} | {'xi':^14} | {'f(xi)':^10} | {'E':^9} |")
    print("|" + "-"*6 + "|" + "-"*16 + "|" + "-"*12 + "|" + "-"*11 + "|")

    fx0 = evaluar(f_expr, x0)
    fx1 = evaluar(f_expr, x1)
    fx2 = evaluar(f_expr, x2)

    print(f"| {0:^4} | {x0:^14.10f} | {fx0:^10.2e} | {'':^9} |")
    print(f"| {1:^4} | {x1:^14.10f} | {fx1:^10.2e} | {'':^9} |")
    print(f"| {2:^4} | {x2:^14.10f} | {fx2:^10.2e} | {'':^9} |")

    for i in range(3, N + 1):
        h0 = x1 - x0
        h1 = x2 - x1

        if h0 == 0 or h1 == 0:
            print("\nError: dos puntos iniciales son iguales.")
            return None

        d0 = (fx1 - fx0) / h0
        d1 = (fx2 - fx1) / h1

        a = (d1 - d0) / (h1 + h0)
        b = a * h1 + d1
        c = fx2

        discriminante = cmath.sqrt(b**2 - 4*a*c)

        # Elegir el denominador de mayor magnitud
        denom1 = b + discriminante
        denom2 = b - discriminante
        denom = denom1 if abs(denom1) >= abs(denom2) else denom2

        if denom == 0:
            print("\nError: denominador cero.")
            return None

        x3 = x2 - (2 * c) / denom
        x3 = x3.real  # Tomar parte real

        fx3 = evaluar(f_expr, x3)
        E = abs(x3 - x2)

        print(f"| {i:^4} | {x3:^14.10f} | {fx3:^10.2e} | {E:^9.2e} |")

        x0, fx0 = x1, fx1
        x1, fx1 = x2, fx2
        x2, fx2 = x3, fx3

        if E < tol:
            break

    print(f"\nSe encontró una aproximación de la raíz en {x2:.15f}")
    print("="*60)
    return x2

def main():
    print("="*60)
    print("              MÜLLER - Entrada de datos")
    print("="*60)
    print("\nEscribe la función usando notación matemática estándar.")
    print("Puedes usar: sin, cos, tan, log, ln, exp, sqrt, pi, e, etc.")
    print("Potencias: usa ^ o **   |   Ej: sin^2(x) o sin(x)**2")
    print("Ejemplo: ln(sin^2(x) + 1) - 1/2\n")

    f_expr = input("f(x) = ").strip()

    try:
        x0  = float(input("Valor inicial x0: "))
        x1  = float(input("Valor inicial x1: "))
        x2  = float(input("Valor inicial x2: "))
        tol = float(input("Tolerancia Tol (Ej: 1e-7): "))
        N   = int(input("Número máximo de iteraciones N: "))
    except ValueError:
        print("Error: ingresa valores numéricos válidos.")
        return

    try:
        muller(f_expr, x0, x1, x2, tol, N)
    except ValueError as e:
        print(f"\n{e}")

    input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()
