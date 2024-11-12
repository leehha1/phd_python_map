import osmnx as ox
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QWidget, QSlider, QVBoxLayout, QLabel, QPushButton, QFileDialog, QComboBox)
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
        self.current_region = 'Ukraine'
        # Кнопка для сохранения координат
        self.save_button = QPushButton("Save coordinates", self)
        self.save_button.clicked.connect(self.save_coordinates)

        # Кнопка для сохранения в txt
        self.save_txt_button = QPushButton("Save to TXT", self)
        self.save_txt_button.clicked.connect(self.save_to_txt)

        self.vertices_count_label = QLabel("Amount of points: 0", self)

        self.layout.addWidget(self.vertices_count_label)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.save_txt_button)  # Добавляем кнопку
        self.update_map(0)

    def save_to_txt(self):
        """Сохраняет координаты в txt-файл с заданным форматом."""
        defaultFileName = f"{self.current_region}_ansys_data_simplification_{self.current_precision}.txt"
        filter = "Text Files (*.txt);;All Files (*)"

        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Save to TXT", defaultFileName, filter, options=options)

        if fileName:
            simplified_map = self.ox_map.geometry.simplify(self.current_precision / SIMPL_COOF, preserve_topology=True)
            with open(fileName, 'w') as file:
                # Записываем заголовок
                file.write("/NOPR   ! Suppress printing of UNDO process\n")
                file.write("/PMACRO ! Echo following commands to log\n")
                file.write("FINISH  ! Make sure we are at BEGIN level\n")
                file.write("/CLEAR,NOSTART  ! Clear model since no SAVE found\n")
                file.write("! WE SUGGEST YOU REMOVE THIS LINE AND THE FOLLOWING STARTUP LINES\n")
                file.write("/input,menust,tmp,''\n")
                file.write("/GRA,POWER\n")
                file.write("/GST,ON\n")
                file.write("/PLO,INFO,3\n")
                file.write("/GRO,CURL,ON\n")
                file.write("/CPLANE,1\n")
                file.write("/REPLOT,RESIZE\n")
                file.write("WPSTYLE,,,,,,,,0\n")
                file.write("/GOP    ! Resume printing after UNDO process\n")
                file.write(")! We suggest a save at this point\n")
                file.write("/PREP7\n")

                # Записываем координаты
                k_index = 1
                for poly in simplified_map:
                    if hasattr(poly, 'exterior'):
                        for coord in poly.exterior.coords:
                            if k_index >= len(poly.exterior.coords):
                                break
                            file.write(f"K,{k_index},{coord[0]},{coord[1]},,\n")
                            k_index += 1

                k_index = 1
                for poly in simplified_map:
                    if hasattr(poly, 'exterior'):
                        for coord in poly.exterior.coords:
                            if k_index >= len(poly.exterior.coords):
                                break
                            if k_index == len(poly.exterior.coords) - 1:
                                file.write(f"LSTR, {k_index}, 1\n")
                            else:
                                file.write(f"LSTR, {k_index}, {k_index + 1}\n")
                            k_index += 1

                file.write(f"FLST,2,{k_index-1},4\n")

                k_index = 1
                for poly in simplified_map:
                    if hasattr(poly, 'exterior'):
                        for coord in poly.exterior.coords:
                            if k_index >= len(poly.exterior.coords):
                                break
                            file.write(f"FITEM,2,{k_index}\n")
                            k_index += 1

                file.write("AL,P51X\n")

    def load_map(self, region_name):
        if region_name == 'All':
            regions = ['Ukraine', 'Belarus', 'Pskov Oblast, Russia', 'Novgorod Oblast, Russia']
            combined_map = pd.concat([ox.geocode_to_gdf(region) for region in regions])
            return combined_map
        else:
            return ox.geocode_to_gdf(region_name)

    def save_coordinates(self):
        defaultFileName = f"{self.current_region}_coordinates_simplification_{self.current_precision}.csv"
        filter = "CSV Files (*.csv);;All Files (*)"

        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Save coordinates", defaultFileName, filter, options=options)

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
        total_vertices = sum(len(poly.exterior.coords) for poly in simplified_map if hasattr(poly, 'exterior'))
        self.vertices_count_label.setText(f"Amount of points: {total_vertices}")

    def change_region(self, region):
        self.current_region = region
        self.ox_map = self.load_map(region)
        self.update_map(self.current_precision)

    def change_combined_region(self, combined_map):
        """Меняет карту на объединённую версию нескольких областей."""
        self.ox_map = combined_map
        self.update_map(self.current_precision)


class CoordinateSimplificationWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.map_widget = MapWidget()
        self.labeled_slider = QLabeledSlider(minimum=0, maximum=100, initial_value=0, parent=self)

        self.region_selector = QComboBox(self)
        self.region_selector.addItems(['Ukraine', 'Belarus', 'Pskov Oblast and Novgorod Oblast', 'All'])
        self.region_selector.currentTextChanged.connect(self.change_region)

        layout = QVBoxLayout()
        layout.addWidget(self.region_selector)
        layout.addWidget(self.map_widget)
        layout.addWidget(self.labeled_slider)
        self.setLayout(layout)

    def update_map(self, value):
        self.map_widget.update_map(value)

    def change_region(self, region):
        if region == 'Pskov Oblast and Novgorod Oblast':
            # Загружаем карты обеих областей
            pskov_map = ox.geocode_to_gdf('Pskov Oblast, Russia')
            novgorod_map = ox.geocode_to_gdf('Novgorod Oblast, Russia')

            # Объединяем геометрию
            combined_geometry = pskov_map.geometry.unary_union.union(novgorod_map.geometry.unary_union)
            combined_map = pskov_map.copy()
            combined_map.geometry = [combined_geometry]

            self.map_widget.change_combined_region(combined_map)
            self.map_widget.current_region = region
        elif region == 'All':
            # Загружаем все регионы и объединяем
            regions = ['Ukraine', 'Belarus', 'Pskov Oblast, Russia', 'Novgorod Oblast, Russia']
            all_maps = [ox.geocode_to_gdf(region) for region in regions]

            # Объединяем все карты
            combined_geometry = all_maps[0].geometry.unary_union
            for region_map in all_maps[1:]:
                combined_geometry = combined_geometry.union(region_map.geometry.unary_union)

            combined_map = all_maps[0].copy()
            combined_map.geometry = [combined_geometry]

            self.map_widget.change_combined_region(combined_map)
            self.map_widget.current_region = region
        else:
            self.map_widget.change_region(region)


