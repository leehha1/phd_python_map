import osmnx as ox
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QWidget, QSlider, QVBoxLayout, QLabel, QPushButton, QFileDialog)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

SIMPL_COOF = 500

class QLabeledSlider(QWidget):
    def __init__(self, minimum, maximum, initial_value, parent=None):
        super(QLabeledSlider, self).__init__(parent)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(minimum)
        self.slider.setMaximum(maximum)
        self.slider.setValue(initial_value)

        self.label = QLabel(str(initial_value), self)
        self.label.setAlignment(Qt.AlignCenter)

        # Добавляем метку для описания
        self.description_label = QLabel("Map simplification level:", self)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.slider.valueChanged.connect(self.value_changed)
        self.slider.sliderReleased.connect(self.slider_released)

        layout = QVBoxLayout(self)
        layout.addWidget(self.description_label)
        layout.addWidget(self.slider)
        layout.addWidget(self.label)

    def value_changed(self, value):
        self.label.setText(str(value))

    def slider_released(self):
        # Получаем текущее значение слайдера
        value = self.slider.value()
        self.parent().update_map(value)


class MapWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.current_precision = 0

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.canvas)

        self.ox_map = ox.geocode_to_gdf('Ukraine')

        self.save_button = QPushButton("Save coordinates", self)
        self.save_button.clicked.connect(self.save_coordinates)
        self.vertices_count_label = QLabel("Amount of points: 0", self)

        self.layout.addWidget(self.vertices_count_label)
        self.layout.addWidget(self.save_button)
        self.update_map(0)

    def save_coordinates(self):
        defaultFileName = f"Ukraine_coordinates_simplification_{self.current_precision}.csv"
        filter = "CSV Files (*.csv);;All Files (*)"

        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Save coordinates", defaultFileName, filter,
                                                  options=options)

        if fileName:
            simplified_map = self.ox_map.geometry.simplify(self.current_precision / SIMPL_COOF, preserve_topology=True)
            coords = []
            for poly in simplified_map:
                if hasattr(poly, 'exterior'):
                    coords.extend(poly.exterior.coords)
            df = pd.DataFrame(coords, columns=['Longitude', 'Latitude'])
            df.to_csv(fileName, index=False)

    def update_map(self, precision):
        self.current_precision = precision
        self.ax.clear()
        simplified_map = self.ox_map.geometry.simplify(precision / SIMPL_COOF, preserve_topology=True)
        simplified_map.plot(ax=self.ax, color='blue')
        self.canvas.draw()
        # Подсчет вершин в упрощенной карте
        total_vertices = sum(len(poly.exterior.coords) for poly in simplified_map if hasattr(poly, 'exterior'))
        self.vertices_count_label.setText(f"Amount of points: {total_vertices}")


class CoordinateSimplificationWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.map_widget = MapWidget()
        self.labeled_slider = QLabeledSlider(minimum=0, maximum=100, initial_value=0, parent=self)

        layout = QVBoxLayout()
        layout.addWidget(self.map_widget)
        layout.addWidget(self.labeled_slider)
        self.setLayout(layout)

    # Добавляем метод update_map сюда
    def update_map(self, value):
        self.map_widget.update_map(value)

