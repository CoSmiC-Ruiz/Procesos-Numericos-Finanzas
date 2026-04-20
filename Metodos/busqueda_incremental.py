import math
import re

def preprocesar(expr):
    # Convierte func^n(args) -> func(args)**n  Ej: sin^2(x) -> sin(x)**2
    funciones = r'(sin|cos|tan|log|ln|exp|sqrt|asin|acos|atan)'
    expr = re.sub(funciones + r'\^(\d+)\s*\(([^()]*)\)', r'\1(\3)**\2', expr)
    # Reemplaza ^ restante por **
    expr = expr.replace('^', '**')
    # ln -> log
    expr = expr.replace('ln(', 'log(')
    return expr

def evaluar_funcion(expr, x):
    try:
        expr_proc = preprocesar(expr)
        return eval(expr_proc, {"x": x, **{k: getattr(math, k) for k in dir(math)}})
    except Exception as e:
        raise ValueError(f"Error al evaluar f({x}): {e}")

def busqueda_incremental(f_expr, x0, delta_x, N):
    print("\n" + "="*60)
    print("         BÚSQUEDA INCREMENTAL")
    print("="*60)
    print("\nResultados:\n")

    raices = []
    a = x0
    fa = evaluar_funcion(f_expr, a)

    for _ in range(N):
        b = a + delta_x
        fb = evaluar_funcion(f_expr, b)

        if fa * fb < 0:
            print(f"  Hay una raiz de f en [{a:.10f},{b:.10f}]")
            raices.append((a, b))

        a = b
        fa = fb

    if not raices:
        print("  No se encontraron raices en el intervalo explorado.")

    print(f"\nTotal de intervalos con raiz: {len(raices)}")
    print("="*60)
    return raices

def main():
    print("="*60)
    print("         BÚSQUEDA INCREMENTAL - Entrada de datos")
    print("="*60)
    print("\nEscribe la función usando notación matemática estándar.")
    print("Puedes usar: sin, cos, tan, log, ln, exp, sqrt, pi, e, etc.")
    print("Potencias: usa ^ o **   |   Ej: sin^2(x) o sin(x)**2")
    print("Ejemplo: log(sin^2(x) + 1) - 1/2\n")

    f_expr = input("f(x) = ").strip()

    try:
        x0      = float(input("Valor inicial x0: "))
        delta_x = float(input("Incremento delta_x: "))
        N       = int(input("Número máximo de iteraciones N: "))
    except ValueError:
        print("Error: ingresa valores numéricos válidos.")
        return

    try:
        busqueda_incremental(f_expr, x0, delta_x, N)
    except ValueError as e:
        print(f"\n{e}")

    input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()
