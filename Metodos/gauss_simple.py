def imprimir_matriz(M):
    for fila in M:
        print(" ", "  ".join(f"{val:9.6f}" for val in fila))
    print()

def gauss_simple(A, b):
    n = len(A)
    # Construir matriz aumentada
    M = [A[i][:] + [b[i]] for i in range(n)]

    print("\n" + "="*60)
    print("          ELIMINACIÓN GAUSSIANA SIMPLE")
    print("="*60)
    print("\nResultados:\n")

    print("Etapa 0\n")
    imprimir_matriz(M)

    for k in range(n - 1):
        for i in range(k + 1, n):
            if M[k][k] == 0:
                print(f"Error: pivote cero en columna {k}. Usa pivoteo.")
                return None
            factor = M[i][k] / M[k][k]
            for j in range(k, n + 1):
                M[i][j] -= factor * M[k][j]

        print(f"Etapa {k + 1}\n")
        imprimir_matriz(M)

    # Sustitución regresiva
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = M[i][n]
        for j in range(i + 1, n):
            x[i] -= M[i][j] * x[j]
        x[i] /= M[i][i]

    print("Después de aplicar sustitución regresiva\n")
    print("x:")
    for val in x:
        print(f"{val:.6f}")

    print("\n" + "="*60)
    return x

def ingresar_matriz(n):
    print(f"\nIngresa la matriz A ({n}x{n}), fila por fila separada por espacios:")
    A = []
    for i in range(n):
        while True:
            try:
                fila = list(map(float, input(f"  Fila {i+1}: ").split()))
                if len(fila) != n:
                    print(f"  Error: ingresa exactamente {n} valores.")
                    continue
                A.append(fila)
                break
            except ValueError:
                print("  Error: ingresa solo números.")
    return A

def ingresar_vector(n):
    print(f"\nIngresa el vector b ({n} valores separados por espacios):")
    while True:
        try:
            b = list(map(float, input("  b: ").split()))
            if len(b) != n:
                print(f"  Error: ingresa exactamente {n} valores.")
                continue
            return b
        except ValueError:
            print("  Error: ingresa solo números.")

def main():
    print("="*60)
    print("    ELIMINACIÓN GAUSSIANA SIMPLE - Entrada de datos")
    print("="*60)

    while True:
        try:
            n = int(input("\nTamaño del sistema n (número de ecuaciones): "))
            if n < 1:
                print("Error: n debe ser mayor a 0.")
                continue
            break
        except ValueError:
            print("Error: ingresa un número entero.")

    A = ingresar_matriz(n)
    b = ingresar_vector(n)

    gauss_simple(A, b)

    input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()
