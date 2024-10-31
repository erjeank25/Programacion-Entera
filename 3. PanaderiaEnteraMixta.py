from pulp import *

class Panaderia:
    def __init__(self):
        self.hornos = []
        self.demanda = 0
        self.modelo = None

    def solicitar_datos(self):
        while True:
            try:
                n_hornos = self.input_numerico("Ingrese el número de hornos: ", entero=True, minimo=1)
                for i in range(n_hornos):
                    print(f"\nDatos para el horno {i+1}:")
                    capacidad = self.input_numerico("Capacidad: ", entero=True, minimo=1)
                    costo_fijo = self.input_numerico("Costo fijo diario: ", minimo=0)
                    costo_variable = self.input_numerico("Costo por barra: ", minimo=0)
                    self.hornos.append((capacidad, costo_fijo, costo_variable))
                
                self.demanda = self.input_numerico("Ingrese la demanda total de pan: ", entero=True, minimo=1)
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
        self.modelo = LpProblem("Problema_Panaderia", LpMinimize)
        
        x = [LpVariable(f"x{i}", lowBound=0, cat='Integer') for i in range(len(self.hornos))]
        y = [LpVariable(f"y{i}", cat='Binary') for i in range(len(self.hornos))]
        
        self.modelo += lpSum([self.hornos[i][1] * y[i] + self.hornos[i][2] * x[i] for i in range(len(self.hornos))])
        
        self.modelo += lpSum(x) == self.demanda, "Demanda_Total"
        for i in range(len(self.hornos)):
            self.modelo += x[i] <= self.hornos[i][0] * y[i], f"Capacidad_Horno_{i+1}"

    def resolver_modelo(self):
        try:
            self.modelo.solve()
            print("\nResultados:")
            print("Estado:", LpStatus[self.modelo.status])
            
            for v in self.modelo.variables():
                print(f"{v.name} = {v.varValue}")
            
            print(f"Costo total = {value(self.modelo.objective)}")
            return True
        except Exception as e:
            print(f"Error al resolver el modelo: {e}")
            return False

    def exportar_resultados(self):
        try:
            with open("3. PanaderiaEnteraMixta.txt", "w", encoding='utf-8') as f:
                f.write("Resultados del problema de la panadería\n\n")
                f.write(f"Estado: {LpStatus[self.modelo.status]}\n\n")
                for v in self.modelo.variables():
                    f.write(f"{v.name} = {v.varValue}\n")
                f.write(f"\nCosto total = {value(self.modelo.objective)}")
            print("Resultados exportados a '3. PanaderiaEnteraMixta.txt'")
            return True
        except Exception as e:
            print(f"Error al exportar resultados: {e}")
            return False

def main():
    panaderia = Panaderia()
    print("Bienvenido al programa de optimización de panadería")
    print("En cualquier momento, ingrese 'q' para salir del programa")
    
    try:
        if panaderia.solicitar_datos():
            panaderia.crear_modelo()
            if panaderia.resolver_modelo():
                panaderia.exportar_resultados()
    except KeyboardInterrupt:
        print("\nPrograma terminado por el usuario.")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        print("Gracias por usar el programa de optimización de panadería")

if __name__ == "__main__":
    main()