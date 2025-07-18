import matplotlib.pyplot as plt

# Função para mostrar grafico de pizza
def show_pizza_for_discipline(assessments):
    labels = [a['Type'] for a in assessments]
    points = [a['points'] for a in assessments]

    plt.pie(points, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title("Distribuição das Avaliações")
    plt.show()

# Função para mostrar gráfico de linha
def show_line_chart_for_discipline(assessments):
    labels = [a['Type'] for a in assessments]
    points = [a['points'] for a in assessments]

    plt.plot(labels, points, marker='o', linestyle='-', color='b')
    plt.title("Desempenho por Avaliação")
    plt.xlabel("Tipo de Avaliação")
    plt.ylabel("Pontos Obtidos")
    plt.grid(True)
    plt.show()
