from pulp import *

class ProblemaEstaciones:
    def __init__(self):
        self.num_ciudades = 0
        self.tiempos = []
        self.modelo = None

    def solicitar_datos(self):
        while True:
            try:
                self.num_ciudades = self.input_numerico("Ingrese el número de ciudades: ", entero=True, minimo=2)
                print(f"Ingrese los tiempos de viaje entre ciudades (en minutos):")
                for i in range(self.num_ciudades):
                    fila = []
                    for j in range(self.num_ciudades):
                        if i != j:
                            tiempo = self.input_numerico(f"Tiempo de viaje entre ciudad {i+1} y ciudad {j+1}: ", minimo=0)
                            fila.append(tiempo)
                        else:
                            fila.append(0)
                    self.tiempos.append(fila)
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

    def crear_modelo(self):
        self.modelo = LpProblem("Problema_Ubicacion_Estaciones", LpMinimize)

        # Variables de decisión
        x = [LpVariable(f"x_{i}", cat='Binary') for i in range(self.num_ciudades)]

        # Función objetivo: minimizar el número de estaciones
        self.modelo += lpSum(x)

        # Restricciones: cada ciudad debe estar a no más de 30 minutos de una estación
        for i in range(self.num_ciudades):
            self.modelo += lpSum(x[j] for j in range(self.num_ciudades) if self.tiempos[i][j] <= 30) >= 1

    def resolver_modelo(self):
        try:
            self.modelo.solve()
            print("\nResultados:")
            print("Estado:", LpStatus[self.modelo.status])
            
            num_estaciones = sum(var.varValue for var in self.modelo.variables())
            print(f"Número mínimo de estaciones: {int(num_estaciones)}")

            print("\nUbicación de las estaciones:")
            for i, var in enumerate(self.modelo.variables()):
                if var.varValue == 1:
                    print(f"Ciudad {i+1}")

            return True
        except Exception as e:
            print(f"Error al resolver el modelo: {e}")
            return False

    def exportar_resultados(self):
        try:
            with open("2. EnteraBinariaEstacionesCiudades.txt", "w", encoding='utf-8') as f:
                f.write("Resultados del problema de ubicación de estaciones\n\n")
                f.write(f"Estado: {LpStatus[self.modelo.status]}\n\n")
                num_estaciones = sum(var.varValue for var in self.modelo.variables())
                f.write(f"Número mínimo de estaciones: {int(num_estaciones)}\n\n")
                f.write("Ubicación de las estaciones:\n")
                for i, var in enumerate(self.modelo.variables()):
                    if var.varValue == 1:
                        f.write(f"Ciudad {i+1}\n")
            print("Resultados exportados a '2. EnteraBinariaEstacionesCiudades.txt'")
            return True
        except Exception as e:
            print(f"Error al exportar resultados: {e}")
            return False

def main():
    problema = ProblemaEstaciones()
    print("Bienvenido al programa de optimización de ubicación de estaciones")
    print("En cualquier momento, ingrese 'q' para salir del programa")
    
    try:
        if problema.solicitar_datos():
            problema.crear_modelo()
            if problema.resolver_modelo():
                problema.exportar_resultados()
    except KeyboardInterrupt:
        print("\nPrograma terminado por el usuario.")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        print("Gracias por usar el programa de optimización de ubicación de estaciones")

if __name__ == "__main__":
    main()