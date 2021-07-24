# Creates a GUI for a user to supply model parameters.

import PySimpleGUI as sg
import numpy as np
import matplotlib as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

fig = plt.figure.Figure(figsize=(5,4), dpi=100)
t = np.arange(0,3,0.1)

fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

plt.use("TkAgg")

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

# Define the window layout
layout = [
    [sg.Text("Plot test")],
    [sg.Canvas(key="-CANVAS-")],
    [sg.Button("Ok")],
]

# Create the form and show it without the plot
window = sg.Window(
    "Matplotlib Single Graph",
    layout,
    location=(0, 0),
    finalize=True,
    element_justification="center",
    font="Helvetica 18",
)

# Add the plot to the window
draw_figure(window["-CANVAS-"].TKCanvas, fig)

event, values = window.read()

window.close()