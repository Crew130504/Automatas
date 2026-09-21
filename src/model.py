from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field

EPSILON = "ε"


@dataclass
class Automaton:
    alphabet: list[str]
    states: list[str]
    initial: str
    finals: set[str]
    transitions: dict[tuple[str, str], set[str]] = field(default_factory=dict)
    kind: str = "AFD"

    def validate(self) -> None:
        if not self.states:
            raise ValueError("Debe definir al menos un estado.")
        if any(len(symbol) != 1 for symbol in self.alphabet):
            raise ValueError("Cada simbolo del alfabeto debe tener un solo caracter.")
        if self.initial not in self.states:
            raise ValueError("El estado inicial debe pertenecer a los estados definidos.")
        if not self.finals.issubset(self.states):
            raise ValueError("Hay estados de aceptacion no definidos.")
        symbols = set(self.alphabet) | ({EPSILON} if self.kind == "AFN" else set())
        for (origin, symbol), destinations in self.transitions.items():
            if origin not in self.states or symbol not in symbols or not destinations.issubset(self.states):
                raise ValueError("La tabla contiene una transicion invalida.")
            if self.kind == "AFD" and len(destinations) > 1:
                raise ValueError("Un AFD no puede tener varios destinos para el mismo simbolo.")

    def epsilon_closure(self, states: set[str]) -> set[str]:
        closure = set(states)
        pending = list(states)
        while pending:
            state = pending.pop()
            for target in self.transitions.get((state, EPSILON), set()):
                if target not in closure:
                    closure.add(target)
                    pending.append(target)
        return closure

    def move(self, states: set[str], symbol: str) -> set[str]:
        targets: set[str] = set()
        for state in states:
            targets.update(self.transitions.get((state, symbol), set()))
        return self.epsilon_closure(targets) if self.kind == "AFN" else targets

    def simulate(self, text: str) -> tuple[bool, list[set[str]], str | None]:
        self.validate()
        active = self.epsilon_closure({self.initial}) if self.kind == "AFN" else {self.initial}
        path = [active]
        for symbol in text:
            if symbol not in self.alphabet:
                return False, path, f"El simbolo '{symbol}' no pertenece al alfabeto."
            active = self.move(active, symbol)
            path.append(active)
        return bool(active & self.finals), path, None

    def to_dfa(self) -> "Automaton":
        if self.kind == "AFD":
            return self
        self.validate()
        start = frozenset(self.epsilon_closure({self.initial}))
        queue = deque([start])
        seen = {start}
        transitions: dict[tuple[str, str], set[str]] = {}

        def label(group: frozenset[str]) -> str:
            # El separador vertical conserva cada subconjunto como un solo estado
            # en los campos de interfaz, que usan comas para separar estados.
            return "{" + "|".join(sorted(group)) + "}" if group else "∅"

        while queue:
            group = queue.popleft()
            for symbol in self.alphabet:
                target = frozenset(self.move(set(group), symbol))
                transitions[(label(group), symbol)] = {label(target)}
                if target not in seen:
                    seen.add(target)
                    queue.append(target)
        states = [label(group) for group in seen]
        finals = {label(group) for group in seen if set(group) & self.finals}
        return Automaton(self.alphabet, states, label(start), finals, transitions, "AFD")
