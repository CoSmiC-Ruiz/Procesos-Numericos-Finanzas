def imprimir_matriz(M):
    for fila in M:
        print(" ", "  ".join(f"{val:9.6f}" for val in fila))
    print()

def gauss_pivoteo_total(A, b):
    n = len(A)
    M = [A[i][:] + [b[i]] for i in range(n)]
    orden = list(range(n))  # Registro del orden de columnas

    print("\n" + "="*60)
    print("      ELIMINACIÓN GAUSSIANA CON PIVOTEO TOTAL")
    print("="*60)
    print("\nResultados:\n")

    print("Etapa 0\n")
    imprimir_matriz(M)

    for k in range(n - 1):
        # Buscar mayor valor absoluto en la submatriz restante
        max_val = 0
        max_fila, max_col = k, k
        for i in range(k, n):
            for j in range(k, n):
                if abs(M[i][j]) > max_val:
                    max_val = abs(M[i][j])
                    max_fila, max_col = i, j

        # Intercambiar filas
        if max_fila != k:
            M[k], M[max_fila] = M[max_fila], M[k]

        # Intercambiar columnas (sin la columna aumentada)
        if max_col != k:
            for i in range(n):
                M[i][k], M[i][max_col] = M[i][max_col], M[i][k]
            orden[k], orden[max_col] = orden[max_col], orden[k]

        for i in range(k + 1, n):
            if M[k][k] == 0:
                print(f"Error: pivote cero en etapa {k}.")
                return None
            factor = M[i][k] / M[k][k]
            for j in range(k, n + 1):
                M[i][j] -= factor * M[k][j]

        print(f"Etapa {k + 1}\n")
        imprimir_matriz(M)

    # Sustitución regresiva
    x_ord = [0.0] * n
    for i in range(n - 1, -1, -1):
        x_ord[i] = M[i][n]
        for j in range(i + 1, n):
            x_ord[i] -= M[i][j] * x_ord[j]
        x_ord[i] /= M[i][i]

    # Reordenar solución según el orden original de columnas
    x = [0.0] * n
    for i in range(n):
        x[orden[i]] = x_ord[i]

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
    print("  GAUSS PIVOTEO TOTAL - Entrada de datos")
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

    gauss_pivoteo_total(A, b)

    input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()
