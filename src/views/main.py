import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from src.controllers.DisciplineManager import DisciplineManager
from src.data.StorageJSON import StorageJSON
import charts

class DisciplineApp:
    def __init__(self, master):
        self.master = master
        self.master.title("MyGradesISUTC")
        self.master.geometry("540x520")
        self.master.configure(bg="#f0f4f8")

        self.dark_mode = False

        # Frame para o topo da janela
        top_frame = tk.Frame(self.master, bg="#f0f4f8")
        top_frame.pack(side="top", fill="x")

        # Carregar o logotipo do isu
        try:
            logo = tk.PhotoImage(file="../assets/isutc.png")
            logo_label = tk.Label(top_frame, image=logo, bg="#f0f4f8")
            logo_label.image = logo
            logo_label.pack(side="left", padx=10, pady=10)
        except Exception as e:
            print("Erro ao carregar imagem:", e)

        self.manager = DisciplineManager()

        self.frame = tk.Frame(master, bg="white", bd=2, relief=tk.GROOVE)
        self.frame.pack(padx=20, pady=10, fill="both", expand=True)

        label_style = {"bg": "white", "fg": "#003366", "font": ("Arial", 12, "bold")}

        self.label = tk.Label(self.frame, text="Nome da Cadeira:", **label_style)
        self.label.grid(row=0, column=0, sticky="w", padx=15, pady=8)
        self.entry_name = tk.Entry(self.frame, font=("Arial", 12))
        self.entry_name.grid(row=0, column=1, sticky="ew", padx=15, pady=8)

        self.label2 = tk.Label(self.frame, text="Pontos máximos:", **label_style)
        self.label2.grid(row=1, column=0, sticky="w", padx=15, pady=8)
        self.entry_max = tk.Entry(self.frame, font=("Arial", 12))
        self.entry_max.grid(row=1, column=1, sticky="ew", padx=15, pady=8)

        self.frame.grid_columnconfigure(1, weight=1)

        self.frame_buttons_top = tk.Frame(self.frame, bg="white")
        self.frame_buttons_top.grid(row=2, column=0, columnspan=2, sticky="ew", padx=15, pady=(5, 15))
        self.frame_buttons_top.grid_columnconfigure((0,1,2), weight=1, uniform="group1")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Rounded.TButton', font=("Arial", 11, "bold"), background="#0077cc",
                        foreground="white", padding=10, borderwidth=0, relief="flat")
        style.map('Rounded.TButton', background=[('active', '#005fa3'), ('pressed', '#003f66')])

        self.btn_add = ttk.Button(self.frame_buttons_top, text="Adicionar Cadeira",
                                  command=self.add_discipline, style='Rounded.TButton')
        self.btn_add.grid(row=0, column=0, sticky="ew", padx=5)

        self.btn_add_pts = ttk.Button(self.frame_buttons_top, text="Adicionar Avaliação",
                                      command=self.add_points, style='Rounded.TButton')
        self.btn_add_pts.grid(row=0, column=1, sticky="ew", padx=5)

        self.btn_info = ttk.Button(self.frame_buttons_top, text="Ver Info",
                                   command=self.show_info, style='Rounded.TButton')
        self.btn_info.grid(row=0, column=2, sticky="ew", padx=5)

        self.listbox = tk.Listbox(self.frame, font=("Arial", 11), bd=1, relief=tk.SOLID,
                                  selectbackground="#0077cc", activestyle="none")
        self.listbox.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=15, pady=5)

        self.frame.grid_rowconfigure(3, weight=1)

        self.frame_buttons_bottom = tk.Frame(self.frame, bg="white")
        self.frame_buttons_bottom.grid(row=4, column=0, columnspan=2, sticky="ew", padx=15, pady=15)
        self.frame_buttons_bottom.grid_columnconfigure((0,1,2,3,4), weight=1, uniform="group2")

        self.btn_save = ttk.Button(self.frame_buttons_bottom, text="Guardar",
                                   command=self.save_data, style='Rounded.TButton')
        self.btn_save.grid(row=0, column=0, sticky="ew", padx=5)

        self.btn_load = ttk.Button(self.frame_buttons_bottom, text="Carregar",
                                   command=self.load_data_with_message, style='Rounded.TButton')
        self.btn_load.grid(row=0, column=1, sticky="ew", padx=5)

        self.btn_chart_pizza = ttk.Button(self.frame_buttons_bottom, text="Gráfico Pizza",
                                          command=self.show_chart_pizza, style='Rounded.TButton')
        self.btn_chart_pizza.grid(row=0, column=2, sticky="ew", padx=5)

        self.btn_chart_line = ttk.Button(self.frame_buttons_bottom, text="Gráfico Linha",
                                         command=self.show_chart_line, style='Rounded.TButton')
        self.btn_chart_line.grid(row=0, column=3, sticky="ew", padx=5)

        self.btn_dark_mode = ttk.Button(self.frame_buttons_bottom, text="Modo Escuro",
                                        command=self.toggle_dark_mode, style='Rounded.TButton')
        self.btn_dark_mode.grid(row=0, column=4, sticky="ew", padx=5)

        self.load_data(show_message=False)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode

        bg_color = "#1e1e1e" if self.dark_mode else "#f0f4f8"
        fg_color = "white" if self.dark_mode else "#003366"
        entry_bg = "#2e2e2e" if self.dark_mode else "white"
        entry_fg = "white" if self.dark_mode else "black"

        self.master.configure(bg=bg_color)
        self.frame.configure(bg=bg_color)
        self.frame_buttons_top.configure(bg=bg_color)
        self.frame_buttons_bottom.configure(bg=bg_color)

        widgets = [self.label, self.label2]
        for w in widgets:
            w.configure(bg=bg_color, fg=fg_color)

        for e in [self.entry_name, self.entry_max]:
            e.configure(bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)

        self.listbox.configure(bg=entry_bg, fg=entry_fg, selectbackground="#005fa3")

        self.btn_dark_mode.config(text="Modo Claro" if self.dark_mode else "Modo Escuro")

    def add_discipline(self):
        name = self.entry_name.get().strip()
        if not name:
            messagebox.showerror("Erro", "O nome da disciplina não pode estar vazio.")
            return
        try:
            max_points = float(self.entry_max.get())
            if name in [d.name for d in self.manager.disciplines]:
                messagebox.showwarning("Aviso", "Esta disciplina já existe.")
                return
            self.manager.add_discipline(name, max_points)
            self.update_listbox()
            self.entry_name.delete(0, tk.END)
            self.entry_max.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Erro", "Pontos máximos inválidos!")

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for d in self.manager.disciplines:
            self.listbox.insert(tk.END, f"{d.name} - [MAX: {d.max_points}]")

    def add_points(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Atenção", "Seleccione uma disciplina!")
            return
        index = selection[0]
        discipline = self.manager.disciplines[index]

        tipo = simpledialog.askstring("Tipo de Avaliação", "Ex: Mini Teste , Teste, TP, etc:")
        if not tipo:
            messagebox.showwarning("Aviso", "Tipo de avaliação não pode ser vazio.")
            return

        pontos = simpledialog.askfloat("Pontos", "Quantos pontos?")
        if pontos is None or pontos < 0:
            messagebox.showwarning("Aviso", "Pontos inválidos ou negativos.")
            return

        discipline.add_points(tipo, pontos)
        messagebox.showinfo("Sucesso", "Avaliação adicionada!")

    def show_info(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Atenção", "Seleccione uma disciplina!")
            return

        index = selection[0]
        discipline = self.manager.disciplines[index]

        info_window = tk.Toplevel(self.master)
        info_window.title(f"Detalhes - {discipline.name}")
        info_window.geometry("420x450")
        info_window.configure(bg="#f0f4f8")

        frame = tk.Frame(info_window, bg="white", bd=2, relief=tk.GROOVE)
        frame.pack(expand=True, fill="both", padx=15, pady=15)

        title = tk.Label(frame, text=f"{discipline.name}", font=("Arial", 15, "bold"), bg="white", fg="#003366")
        title.pack(pady=(15, 10))

        prov = discipline.calculate_provisional_pts()
        missing = discipline.calculate_min_missing_pts()

        info_text = (
            f"Pontos Acumulados: {discipline.accumulated_pts}\n"
            f"Média Provisória: {prov:.2f}/20\n"
            f"Pontos Em Falta Para Provisória 10: {missing:.2f}\n"
        )

        lbl_info = tk.Label(frame, text=info_text, font=("Arial", 12), bg="white", justify="left")
        lbl_info.pack(pady=10)

        lbl_avaliacoes = tk.Label(frame, text="Avaliações:", font=("Arial", 13, "bold"), bg="white", fg="#003366")
        lbl_avaliacoes.pack(pady=(10, 5))

        if discipline.points:
            for p in discipline.points:
                lbl = tk.Label(frame, text=f"{p['Type']}: {p['points']} pts", bg="white", font=("Arial", 11), anchor="w", justify="left")
                lbl.pack(anchor="w", padx=25)
        else:
            lbl = tk.Label(frame, text="Sem avaliações ainda.", bg="white", font=("Arial", 11, "italic"))
            lbl.pack(pady=5)

    def save_data(self):
        StorageJSON.save_data("dados.json", self.manager.disciplines)
        messagebox.showinfo("Sucesso", "Dados guardados!")

    def load_data(self, show_message=True):
        from src.models.Discipline import Discipline
        dados = StorageJSON.load_data("dados.json")

        nomes_existentes = [disc.name for disc in self.manager.disciplines]

        for item in dados:
            if item["name"] not in nomes_existentes:
                d = Discipline(item["name"], item["max_points"])
                for p in item["assessments"]:
                    d.add_points(p["Type"], p["points"])
                self.manager.disciplines.append(d)
            else:
                if show_message:
                    messagebox.showinfo("Aviso", f"A Cadeira '{item['name']}' já existe. Não foi adicionada novamente.")

        self.update_listbox()
        if show_message:
            messagebox.showinfo("Sucesso", "Dados carregados!")

    def load_data_with_message(self):
        self.load_data(show_message=True)

    def show_chart_pizza(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Atenção", "Selecciona uma cadeira antes de mostrar o gráfico!")
            return
        index = selection[0]
        discipline = self.manager.disciplines[index]
        charts.show_pizza_for_discipline(discipline.points)

    def show_chart_line(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Atenção", "Selecciona uma cadeira antes de mostrar o gráfico!")
            return
        index = selection[0]
        discipline = self.manager.disciplines[index]
        charts.show_line_chart_for_discipline(discipline.points)


if __name__ == "__main__":
    root = tk.Tk()
    app = DisciplineApp(root)
    root.mainloop()
