class Discipline:
    def __init__(self, name, max_points):
        self.name = name
        self.max_points = max_points
        self.provisional_pts = 0
        self.accumulated_pts = 0
        self.points = []

    # Função para adicionar pontos
    def add_points(self, assessment_type, points):
        if (points >= 0 ):
            self.accumulated_pts += points
            self.points.append({"Type" : assessment_type, "points" : points })

    # Função para calcular a provisória
    def calculate_provisional_pts(self):
        self.provisional_pts = (self.accumulated_pts * 20) / self.max_points
        return self.provisional_pts

    # Funcão para calcular os pontos necessários para atingir a provisória miníma
    def calculate_min_missing_pts(self):
        half = self.max_points / 2
        missing = half - self.accumulated_pts

        if missing < 0:
            missing = 0

        return missing



