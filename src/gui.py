from __future__ import annotations

import math
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from .model import Automaton, EPSILON


class AutomataApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AutomatasPaint - AFD y AFN")
        self.root.geometry("1200x760")
        self.root.minsize(980, 620)
        self.entries: dict[tuple[str, str], ttk.Entry] = {}
        self.current_path: list[set[str]] = []
        self.step = 0
        self._build()
        self.load_example()

    def _build(self):
        top = ttk.Frame(self.root, padding=10)
        top.pack(fill="x")
        self.kind = tk.StringVar(value="AFD")
        for value in ("AFD", "AFN"):
            ttk.Radiobutton(top, text=value, variable=self.kind, value=value, command=self.refresh_table).pack(side="left", padx=5)
        self.alphabet = self._field(top, "Alfabeto (coma):", "0,1")
        self.states = self._field(top, "Estados (coma):", "q0,q1")
        self.initial = self._field(top, "Inicial:", "q0")
        self.finals = self._field(top, "Aceptacion (coma):", "q1")
        ttk.Button(top, text="Actualizar tabla", command=self.refresh_table).pack(side="left", padx=8)

        main = ttk.PanedWindow(self.root, orient="horizontal")
        main.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        left = ttk.Frame(main, padding=5)
        right = ttk.Frame(main, padding=5)
        main.add(left, weight=1)
        main.add(right, weight=2)
        ttk.Label(left, text="Tabla de transiciones", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        self.table = ttk.Frame(left)
        self.table.pack(fill="both", expand=True, pady=6)
        buttons = ttk.Frame(left)
        buttons.pack(fill="x")
        ttk.Button(buttons, text="Convertir AFN a AFD", command=self.convert).pack(fill="x", pady=2)
        ttk.Button(buttons, text="Cargar ejemplo", command=self.load_example).pack(fill="x", pady=2)
        ttk.Button(buttons, text="Exportar diagrama", command=self.export_png).pack(fill="x", pady=2)
        ttk.Separator(left).pack(fill="x", pady=10)
        ttk.Label(left, text="Probar cadena", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.text = ttk.Entry(left)
        self.text.pack(fill="x", pady=4)
        ttk.Button(left, text="Evaluar", command=self.evaluate).pack(fill="x")
        self.result = ttk.Label(left, text="", wraplength=310)
        self.result.pack(anchor="w", pady=8)
        self.path_label = ttk.Label(left, text="", wraplength=310)
        self.path_label.pack(anchor="w")

        ttk.Label(right, text="Lienzo del automata", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        self.canvas = tk.Canvas(right, bg="white", highlightthickness=1, highlightbackground="#aab2bd")
        self.canvas.pack(fill="both", expand=True, pady=6)
        self.canvas.bind("<Configure>", lambda _: self.draw())

    def _field(self, parent, label, default):
        ttk.Label(parent, text=label).pack(side="left", padx=(10, 3))
        entry = ttk.Entry(parent, width=15)
        entry.insert(0, default)
        entry.pack(side="left")
        return entry

    @staticmethod
    def tokens(value: str) -> list[str]:
        return [x.strip() for x in value.split(",") if x.strip()]

    def refresh_table(self):
        for child in self.table.winfo_children(): child.destroy()
        self.entries.clear()
        states, alphabet = self.tokens(self.states.get()), self.tokens(self.alphabet.get())
        if self.kind.get() == "AFN": alphabet.append(EPSILON)
        ttk.Label(self.table, text="Estado", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        for col, symbol in enumerate(alphabet, 1):
            ttk.Label(self.table, text=symbol, font=("Segoe UI", 9, "bold")).grid(row=0, column=col, sticky="ew", padx=2, pady=2)
        for row, state in enumerate(states, 1):
            ttk.Label(self.table, text=state).grid(row=row, column=0, sticky="w", padx=2, pady=2)
            for col, symbol in enumerate(alphabet, 1):
                item = ttk.Entry(self.table, width=12)
                item.grid(row=row, column=col, sticky="ew", padx=2, pady=2)
                self.entries[(state, symbol)] = item

    def build_automaton(self) -> Automaton:
        states, alphabet = self.tokens(self.states.get()), self.tokens(self.alphabet.get())
        trans = {}
        for key, entry in self.entries.items():
            values = set(self.tokens(entry.get()))
            if values: trans[key] = values
        automaton = Automaton(alphabet, states, self.initial.get().strip(), set(self.tokens(self.finals.get())), trans, self.kind.get())
        automaton.validate()
        return automaton

    def fill_from(self, automaton: Automaton):
        self.kind.set(automaton.kind)
        self.alphabet.delete(0, "end"); self.alphabet.insert(0, ",".join(automaton.alphabet))
        self.states.delete(0, "end"); self.states.insert(0, ",".join(automaton.states))
        self.initial.delete(0, "end"); self.initial.insert(0, automaton.initial)
        self.finals.delete(0, "end"); self.finals.insert(0, ",".join(sorted(automaton.finals)))
        self.refresh_table()
        for key, destinations in automaton.transitions.items():
            if key in self.entries: self.entries[key].insert(0, ",".join(sorted(destinations)))
        self.current_path = []; self.draw()

    def load_example(self):
        example = Automaton(["0", "1"], ["q0", "q1"], "q0", {"q1"}, {("q0", "0"): {"q0"}, ("q0", "1"): {"q1"}, ("q1", "0"): {"q0"}, ("q1", "1"): {"q1"}}, "AFD")
        self.fill_from(example)
        self.result.config(text="Ejemplo: cadenas que terminan en 1.")

    def convert(self):
        try:
            converted = self.build_automaton().to_dfa()
            if self.kind.get() == "AFD":
                self.result.config(text="El automata ya es determinista.")
            else:
                self.fill_from(converted); self.result.config(text="Conversion completada mediante subconjuntos.")
        except ValueError as error: messagebox.showerror("Datos invalidos", str(error))

    def evaluate(self):
        try:
            accepted, self.current_path, error = self.build_automaton().simulate(self.text.get().strip())
            if error: self.result.config(text=error)
            else: self.result.config(text="CADENA ACEPTADA" if accepted else "CADENA RECHAZADA")
            self.path_label.config(text="Recorrido: " + " -> ".join("{" + ",".join(sorted(x)) + "}" for x in self.current_path))
            self.step = len(self.current_path) - 1; self.draw()
        except ValueError as error: messagebox.showerror("Datos invalidos", str(error))

    def draw(self):
        self.canvas.delete("all")
        try: automaton = self.build_automaton()
        except ValueError: return
        width, height = max(self.canvas.winfo_width(), 500), max(self.canvas.winfo_height(), 300)
        center, radius = (width / 2, height / 2), min(width, height) * .32
        positions = {}
        for i, state in enumerate(automaton.states):
            angle = -math.pi / 2 + i * (2 * math.pi / max(len(automaton.states), 1))
            positions[state] = (center[0] + radius * math.cos(angle), center[1] + radius * math.sin(angle))
        grouped = {}
        for (origin, symbol), targets in automaton.transitions.items():
            for target in targets: grouped[(origin, target)] = grouped.get((origin, target), []) + [symbol]
        for (origin, target), labels in grouped.items():
            x1, y1 = positions[origin]; x2, y2 = positions[target]
            if origin == target:
                self.canvas.create_arc(x1-42, y1-62, x1+42, y1+22, start=35, extent=285, style="arc", width=2)
                self.canvas.create_text(x1+45, y1-47, text=",".join(labels), fill="#243b53")
            else:
                self.canvas.create_line(x1, y1, x2, y2, arrow="last", width=2, fill="#52616b")
                self.canvas.create_text((x1+x2)/2, (y1+y2)/2-13, text=",".join(labels), fill="#243b53")
        active = self.current_path[self.step] if self.current_path else set()
        for state, (x, y) in positions.items():
            color = "#b8f2c2" if state in active else "#ffffff"
            if state in automaton.finals: self.canvas.create_oval(x-27, y-27, x+27, y+27, outline="#0b6e4f", width=2)
            self.canvas.create_oval(x-23, y-23, x+23, y+23, fill=color, outline="#172b4d", width=2)
            self.canvas.create_text(x, y, text=state)
        x, y = positions[automaton.initial]
        self.canvas.create_line(x-78, y, x-27, y, arrow="last", width=2, fill="#172b4d")

    def export_png(self):
        name = filedialog.asksaveasfilename(defaultextension=".ps", filetypes=[("PostScript", "*.ps")])
        if name: self.canvas.postscript(file=name, colormode="color")

    def run(self): self.root.mainloop()
