# AutomatasPaint

Aplicacion de escritorio en Python para crear, visualizar y probar automatas finitos deterministas (AFD) y no deterministas (AFN).

## Funciones

- Define el alfabeto, los estados, el estado inicial y los estados de aceptacion.
- Edita una tabla de transiciones; en AFN se aceptan varios destinos separados por comas y epsilon.
- Convierte un AFN a AFD mediante construccion por subconjuntos.
- Evalua una cadena y resalta en el lienzo el recorrido o los conjuntos activos.
- Dibuja los automatas en un lienzo tipo Paint y permite exportar el diagrama en PostScript.

## Ejecucion

Requiere Python 3.10 o superior y Tkinter (incluido normalmente con Python):

```powershell
python main.py
```

## Estructura

- `main.py`: punto de entrada.
- `src/model.py`: modelo, validacion, simulacion y conversion AFN a AFD.
- `src/gui.py`: interfaz de escritorio y lienzo.
- `docs/diagrams`: imagenes PNG de los diagramas de clases y casos de uso.
- `docs/diagrams/informe_automataspaint.pdf`: informe tecnico.
