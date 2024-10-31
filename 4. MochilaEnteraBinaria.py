from pulp import LpMaximize, LpProblem, LpVariable, LpStatus, value

class ProblemaMochila:
    def __init__(self):
        self.pesos = []
        self.valores = []
        self.capacidad = 0
        self.num_objetos = 0
        self.problema = None
        self.variables = []
        self.pasos = []

    def solicitar_datos(self):
        while True:
            try:
                self.num_objetos = self.input_numerico("Ingrese el número de objetos: ", entero=True, minimo=1)
                print("Ingrese los pesos y valores de los objetos:")
                for i in range(self.num_objetos):
                    peso = self.input_numerico(f"Peso del objeto {i+1}: ", minimo=0)
                    valor = self.input_numerico(f"Valor del objeto {i+1}: ", minimo=0)
                    self.pesos.append(peso)
                    self.valores.append(valor)
                self.capacidad = self.input_numerico("Ingrese la capacidad de la mochila: ", minimo=0)
                break
            except ValueError as e:
                print(f"Error: {e}")
                if not self.continuar():
                    return False
        return True

    def input_numerico(self, mensaje, entero=False, minimo=None):
        while True:
            try:
                valor = input(mensaje)
                if valor.lower() == 'q':
                    raise KeyboardInterrupt
                if entero:
                    valor = int(valor)
                else:
                    valor = float(valor)
                if minimo is not None and valor < minimo:
                    raise ValueError(f"El valor debe ser al menos {minimo}")
                return valor
            except ValueError:
                print(f"Por favor, ingrese un valor {'entero' if entero else 'numérico'} válido.")

    def continuar(self):
        return input("¿Desea intentar de nuevo? (s/n): ").lower().startswith('s')

    def resolver(self):
        self.pasos.append("--- Paso 1: Crear el problema de maximización ---")
        self.problema = LpProblem("Problema_de_la_Mochila", LpMaximize)
        
        self.pasos.append("--- Paso 2: Definir las variables de decisión ---")
        self.variables = [LpVariable(f"x_{i+1}", cat='Binary') for i in range(self.num_objetos)]
        self.pasos.append("Variables de decisión definidas (0 = no seleccionado, 1 = seleccionado):")
        for i in range(self.num_objetos):
            self.pasos.append(f"x_{i+1} -> Objeto {i+1}")

        self.pasos.append("--- Paso 3: Definir la función objetivo ---")
        self.problema += sum(self.valores[i] * self.variables[i] for i in range(self.num_objetos)), "Valor_total"
        self.pasos.append("Función objetivo formulada: Maximizar el valor total de los objetos seleccionados.")

        self.pasos.append("--- Paso 4: Definir la restricción de capacidad ---")
        self.problema += sum(self.pesos[i] * self.variables[i] for i in range(self.num_objetos)) <= self.capacidad, "Capacidad_mochila"
        self.pasos.append(f"Restricción de capacidad formulada: La suma de los pesos no debe exceder {self.capacidad} kg.")

        self.pasos.append("--- Paso 5: Resolver el problema ---")
        self.problema.solve()
        self.pasos.append(f"Estado de la solución: {LpStatus[self.problema.status]}")

        self.pasos.append("--- Paso 6: Mostrar los objetos seleccionados ---")
        for i in range(self.num_objetos):
            self.pasos.append(f"Objeto {i+1}: {'Seleccionado' if self.variables[i].varValue == 1 else 'No seleccionado'} (Peso: {self.pesos[i]}, Valor: {self.valores[i]})")

        valor_total = sum(self.valores[i] * self.variables[i].varValue for i in range(self.num_objetos))
        peso_total = sum(self.pesos[i] * self.variables[i].varValue for i in range(self.num_objetos))
        self.pasos.append("--- Paso 7: Resultados finales ---")
        self.pasos.append(f"Valor total en la mochila: {valor_total}")
        self.pasos.append(f"Peso total en la mochila: {peso_total}")

    def mostrar_pasos(self):
        for paso in self.pasos:
            print(paso)

    def exportar_resultados(self):
        try:
            with open("4. MochilaEnteraBinaria.txt", "w") as f:
                for paso in self.pasos:
                    f.write(paso + "\n")
            print("Resultados exportados a '4. MochilaEnteraBinaria.txt'")
            return True
        except Exception as e:
            print(f"Error al exportar resultados: {e}")
            return False

def main():
    problema = ProblemaMochila()
    print("Bienvenido al programa de optimización del problema de la mochila")
    print("En cualquier momento, ingrese 'q' para salir del programa")
    
    try:
        if problema.solicitar_datos():
            problema.resolver()
            problema.mostrar_pasos()
            problema.exportar_resultados()
    except KeyboardInterrupt:
        print("\nPrograma terminado por el usuario.")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        print("Gracias por usar el programa de optimización del problema de la mochila")

if __name__ == "__main__":
    main()