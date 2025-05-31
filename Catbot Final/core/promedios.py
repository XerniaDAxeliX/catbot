def calcular_promedio(idi):
    while True:
        try:
            cantidad = int(input(f"{idi['cuantos_parciales']} "))
            if cantidad <= 0:
                print("❌ El número debe ser mayor que cero.")
                continue
            break
        except ValueError:
            print("❌ Ingresá un número válido.")

    notas = []
    for i in range(cantidad):
        while True:
            try:
                nota = float(input(f"{idi['nota_parcial']} {i+1}: "))
                if 0 <= nota <= 10:
                    notas.append(nota)
                    break
                else:
                    print("❌ Ingresá una nota entre 0 y 10.")
            except ValueError:
                print("❌ Ingresá un número válido.")

    print(idi["tus_notas"], notas)
    return sum(notas) / len(notas)