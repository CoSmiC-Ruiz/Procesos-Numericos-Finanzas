import math

# Thomas Algorithm - Tridiagonal Gaussian Elimination.
# Solves a tridiagonal system of the form:
#   b[0]*x[0] + c[0]*x[1]                            = d[0]
#   a[i]*x[i-1] + b[i]*x[i] + c[i]*x[i+1]           = d[i]
#                       a[n-1]*x[n-2] + b[n-1]*x[n-1] = d[n-1]
#
# Forward sweep eliminates the lower diagonal (Thomas algorithm),
# then back-substitution solves for x.
# Time complexity: O(n) — optimal for tridiagonal systems.

def imprimir_tridiagonal(a, b, c, d, n):
    for i in range(n):
        fila = [0.0] * (n + 1)
        fila[i] = b[i]
        if i > 0:
            fila[i - 1] = a[i]
        if i < n - 1:
            fila[i + 1] = c[i]
        fila[n] = d[i]
        print(" ", "  ".join(f"{val:9.6f}" for val in fila))
    print()

def gauss_tridiagonal(a, b, c, d):
    n = len(b)

    # Work on copies to preserve the original inputs
    b = b[:]
    d = d[:]

    print("\n" + "="*65)
    print("          ELIMINACIÓN GAUSSIANA TRIDIAGONAL")
    print("="*65)
    print("\nResultados:\n")

    print("Etapa 0 (Sistema original)\n")
    imprimir_tridiagonal(a, b, c, d, n)

    # Forward sweep (Thomas algorithm)
    for i in range(1, n):
        if b[i - 1] == 0:
            print(f"Error: pivote cero en posición {i-1}.")
            return None
        w    = a[i] / b[i - 1]
        b[i] = b[i] - w * c[i - 1]
        d[i] = d[i] - w * d[i - 1]
        a[i] = 0.0

        # Check if the new pivot became zero after elimination
        if b[i] == 0:
            print(f"Error: pivote cero tras eliminación en posición {i}.")
            return None

        print(f"Etapa {i}\n")
        imprimir_tridiagonal(a, b, c, d, n)

    # Back substitution
    x = [0.0] * n
    x[n - 1] = d[n - 1] / b[n - 1]
    for i in range(n - 2, -1, -1):
        x[i] = (d[i] - c[i] * x[i + 1]) / b[i]

    print("Después de aplicar sustitución regresiva\n")
    print("x:")
    for val in x:
        print(f"{val:.6f}")

    print("\n" + "="*65)
    return x

def ingresar_diagonal(nombre, n):
    print(f"\nIngresa la diagonal {nombre} ({n} valores separados por espacios):")
    while True:
        try:
            vals = list(map(float, input(f"  {nombre}: ").split()))
            if len(vals) != n:
                print(f"  Error: ingresa exactamente {n} valores.")
                continue
            return vals
        except ValueError:
            print("  Error: ingresa solo números.")

def main():
    print("="*65)
    print("   GAUSS TRIDIAGONAL (Thomas) - Entrada de datos")
    print("="*65)
    print("\nEl sistema tiene la forma:")
    print("  diagonal inferior (a): n-1 valores  [a1, a2, ..., an-1]")
    print("  diagonal principal (b): n valores   [b0, b1, ..., bn-1]")
    print("  diagonal superior (c): n-1 valores  [c0, c1, ..., cn-2]")
    print("  vector independiente (d): n valores\n")

    while True:
        try:
            n = int(input("Tamaño del sistema n: "))
            if n < 2:
                print("Error: n debe ser al menos 2.")
                continue
            break
        except ValueError:
            print("Error: ingresa un número entero.")

    b = ingresar_diagonal("b (diagonal principal)", n)
    c = ingresar_diagonal("c (diagonal superior)", n - 1)
    a_raw = ingresar_diagonal("a (diagonal inferior)", n - 1)
    d = ingresar_diagonal("d (vector independiente)", n)

    # a[0] = 0.0 (padding): row 0 has no lower-diagonal element
    a = [0.0] + a_raw

    gauss_tridiagonal(a, b, c, d)

    input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()
