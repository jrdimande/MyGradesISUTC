from src.models.Discipline import Discipline
class DisciplineManager:
    def __init__(self):
        self.disciplines = []

    # Função para adicionar cadeiras
    def add_discipline(self, name, max_points):
        discipline = Discipline(name, max_points)
        self.disciplines.append(discipline)

    # Função para remover cadeiras
    def rm_discipline(self, name):
        for disipline in self.disciplines:
            if disipline.name == name:
                self.disciplines.remove(disipline)

    # Função para Listar cadeiras
    def ls_disciplines(self):
        for discipline in self.disciplines:
            print(f"{discipline.name.title()}")


