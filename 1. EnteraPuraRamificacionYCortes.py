import pulp
import re
import io
import sys
from typing import List, Tuple

class BranchAndCutSolver:
    def __init__(self):
        self.problem = None
        self.variables = []
        self.constraints = []
        self.objective = None
        self.output = []

    def get_user_input(self):
        # Solicitar variables de decisión
        while True:
            var_input = input("Ingrese las variables de decisión separadas por comas (ej. x1,x2,x3): ")
            if re.match(r'^[a-zA-Z]\d+(,[a-zA-Z]\d+)*$', var_input):
                self.variables = var_input.split(',')
                break
            print("Entrada inválida. Por favor, ingrese variables en el formato x1,x2,x3,... sin saltos.")

        # Solicitar restricciones
        print("Ingrese las restricciones (una por línea). Presione Enter sin escribir nada para finalizar.")
        print("Formato: 2*x1 + 3*x2 <= 10 o 2*x1 + 3*x2 >= 10 o 2*x1 + 3*x2 = 10")
        while True:
            constraint = input("Restricción: ")
            if constraint == "":
                break
            if self.validate_constraint(constraint):
                self.constraints.append(constraint)
            else:
                print("Restricción inválida. Por favor, intente de nuevo.")

        # Solicitar objetivo
        while True:
            self.objective = input("¿Desea maximizar o minimizar? (max/min): ").lower()
            if self.objective in ['max', 'min']:
                break
            else:
                print("Entrada inválida. Por favor, escriba 'max' o 'min'.")

        # Solicitar función objetivo
        while True:
            obj_function = input("Ingrese la función objetivo (ej. 70*x1 + 100*x2 o 70x1 + 100x2): ")
            if self.validate_expression(obj_function):
                self.objective_function = obj_function
                break
            else:
                print("Función objetivo inválida. Por favor, intente de nuevo.")

    def validate_constraint(self, constraint: str) -> bool:
        pattern = r'^(\s*-?\s*\d*\.?\d*\s*\*?\s*[a-zA-Z]\d+\s*[+\-]?\s*)*\s*[<>=]=\s*-?\d+\.?\d*$'
        return re.match(pattern, constraint) is not None

    def validate_expression(self, expr: str) -> bool:
        pattern = r'^(\s*-?\s*\d*\.?\d*\s*\*?\s*[a-zA-Z]\d+\s*[+\-]?\s*)*\s*\d*\.?\d*\s*\*?\s*[a-zA-Z]\d+$'
        return re.match(pattern, expr) is not None

    def create_problem(self):
        self.problem = pulp.LpProblem("Branch_and_Cut_Problem", 
                                      pulp.LpMaximize if self.objective == 'max' else pulp.LpMinimize)

        lp_vars = {var: pulp.LpVariable(var, lowBound=0, cat='Integer') for var in self.variables}

        self.problem += pulp.LpAffineExpression(self.parse_expression(self.objective_function, lp_vars))

        for constraint in self.constraints:
            parts = re.split(r'\s*([<>=]=)\s*', constraint)
            if len(parts) != 3:
                print(f"Error en la restricción: {constraint}")
                continue
            lhs, operator, rhs = parts
            sense = pulp.LpConstraintLE if operator == '<=' else pulp.LpConstraintGE if operator == '>=' else pulp.LpConstraintEQ
            self.problem += pulp.LpConstraint(
                e=pulp.LpAffineExpression(self.parse_expression(lhs, lp_vars)),
                sense=sense,
                rhs=float(rhs)
            )

    def parse_expression(self, expr: str, lp_vars: dict) -> List[Tuple[pulp.LpVariable, float]]:
        terms = re.findall(r'(-?\s*\d*\.?\d*\s*\*?\s*[a-zA-Z]\d+)', expr)
        parsed_terms = []
        for term in terms:
            if '*' in term:
                coeff, var = term.split('*')
            else:
                coeff, var = re.match(r'(-?\s*\d*\.?\d*\s*)([a-zA-Z]\d+)', term).groups()
            coeff = float(coeff.strip()) if coeff.strip() != '' else 1.0
            var = var.strip()
            parsed_terms.append((lp_vars[var], coeff))
        return parsed_terms

    def solve(self):
        self.output.append("Resolviendo el problema usando el algoritmo de ramificación y cortes...")
        
        # Configurar el solucionador con opciones específicas
        solver = pulp.PULP_CBC_CMD(msg=1, presolve=True, cuts=True, strong=True)
        
        status = self.problem.solve(solver)
    
        self.output.append("\nEstado de la solución:")
        self.output.append(f"Estado: {pulp.LpStatus[status]}")
        self.output.append(f"Valor objetivo: {pulp.value(self.problem.objective)}")
        self.output.append("\nValores de las variables:")
        for var in self.problem.variables():
            self.output.append(f"{var.name} = {var.varValue}")

    def export_output(self):
        with open("1. EnteraPuraRamificacionYCortes.txt", "w", encoding='utf-8') as f:
            f.write("\n".join(self.output))
        print("\n".join(self.output))

    def run(self):
        self.get_user_input()
        self.create_problem()
        self.solve()
        self.export_output()

if __name__ == "__main__":
    solver = BranchAndCutSolver()
    solver.run()