import atexit

import os

import tempfile

from PyQt5.QtGui import QColor
from PyQt5.QtWebEngineWidgets import QWebEngineView
from matplotlib import colors
from qtrangeslider.qtcompat import QtCore

from .coordinates_simplification import CoordinateSimplificationWidget
from ..from_ui import Ui_MainWindow

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QFileDialog, QProgressDialog
from loguru import logger
import pandas as pd
import folium
import matplotlib.pyplot as plt

from superqt import QLabeledRangeSlider


class StartWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.temp_files = []
        self.setupUi(self)
        self.label.setScaledContents(True)
        # self._init_widgets()
        self._connect_all()
        self.cmap = plt.get_cmap('viridis')
        self.init_RS_years()
        self.TE_warning.setTextColor(QColor(255, 0, 0))
        coordinate_simplification = CoordinateSimplificationWidget()
        self.verticalLayout.addWidget(coordinate_simplification)
        atexit.register(self.clean_temp_files)

    def clean_temp_files(self):
        for temp_file in self.temp_files:
            os.remove(temp_file)

    def _connect_all(self):
        logger.debug("_connect_all")
        self.PB_open_file.clicked.connect(self._PB_open_clicked)
        self.PB_show_by_year.clicked.connect(self._PB_show_by_year_clicked)

    def _PB_open_clicked(self):
        self.file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose File",
            "",
            "files (*.csv)",
        )
        if self.file_path:
            self.LE_file_path.setText(self.file_path)
        self._read_csv()
        self.original_min_year = self.original_df['founded'].min()
        self.original_max_year = self.original_df['founded'].max()

        # self.set_SB_min_max(self.original_min_year, self.original_max_year, self.original_min_year, self.original_max_year)

        self.set_RS_years(self.original_min_year, self.original_max_year, self.original_min_year, self.original_max_year)

        self.init_map(self.original_df, self.original_min_year, self.original_max_year)

    def _PB_show_by_year_clicked(self):
        # current_min = self.SB_min_year.value()
        # current_max = self.SB_max_year.value()
        current_min, current_max = self.RS_years.sliderPosition()
        print(current_min, current_max)
        df = self._get_df_by_year(current_min, current_max)

        min_year = df['founded'].min()
        max_year = df['founded'].max()
        # self.set_SB_min_max(self.original_min_year, self.original_max_year, min_year, max_year)
        # self.set_RS_years(self.original_min_year, self.original_max_year, min_year, max_year)
        self.init_map(df, min_year, max_year)

    def init_RS_years(self):
        self.RS_years = QLabeledRangeSlider(QtCore.Qt.Horizontal)
        self.RS_years.setContentsMargins(0, 0, 0, 0)
        self.RS_years.setMaximumHeight(50)
        self.horizontalLayout_3.addWidget(self.RS_years)

    def set_RS_years(self, min_value: int, max_value: int, current_min: int, current_max: int):
        self.RS_years.setMinimum(min_value)
        self.RS_years.setMaximum(max_value)
        self.RS_years.setValue((current_min, current_max))

    # def set_SB_min_max(self, min_value: int, max_value: int, current_min: int, current_max: int):
    #     self.SB_min_year.setMinimum(min_value)
    #     self.SB_max_year.setMinimum(min_value)
    #
    #     self.SB_min_year.setMaximum(max_value)
    #     self.SB_max_year.setMaximum(max_value)
    #
    #     self.SB_min_year.setValue(current_min)
    #     self.SB_max_year.setValue(current_max)

    def _get_df_by_year(self, current_min: int | float, current_max: int | float):
        df = self.original_df[
            (self.original_df['founded'] >= int(current_min)) &
            (self.original_df['founded'] <= int(current_max))
        ]
        return df

    def _read_csv(self):
        self.original_df = pd.read_csv(self.file_path)


    def init_map(
            self,
            df,
            min_year: int | float | None = None,
            max_year: int | float | None = None
    ):
        map = folium.Map(location=[48.3794, 31.1656], zoom_start=6, tiles="cartodb positron")

        if not min_year or not max_year:
            min_year = df['founded'].min()
            max_year = df['founded'].max()

        def get_color(year):
            norm = (year - min_year) / (max_year - min_year)
            rgba_color = self.cmap(norm)
            hex_color = colors.rgb2hex(rgba_color[:3])
            return hex_color
        len_df = len(df.axes[0])
        progress_dialog = self.start_loading(pr_max=len_df)

        for index, row in df.iterrows():
            tooltip_content = f'<div style="font-size: 18px; font-weight: bold;">{row["city"]} - {row["founded"]}</div>'

            folium.CircleMarker(
                location=(row['latitude'], row['longitude']),
                radius=2,
                color=get_color(row['founded']),
                fill=True,
                fill_color=get_color(row['founded']),
                tooltip=tooltip_content
            ).add_to(map)
            progress_dialog = self.plus_one_step_loading(progress_dialog)

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
        map.save(temp_file.name)
        temp_file.close()
        self.temp_files.append(temp_file.name)
        if hasattr(self, 'view_map'):
            self.view_map.load(QUrl.fromLocalFile(temp_file.name))
        else:
            self.view_map = QWebEngineView()
            self.view_map.load(QUrl.fromLocalFile(temp_file.name))
            self.verticalLayout_5.addWidget(self.view_map)
        self.finish_loading(progress_dialog, len_df)

    def start_loading(self, pr_min: int = 0, pr_max: int = 100):
        progress_dialog = QProgressDialog("Loading data...", "Abort", pr_min, pr_max, self)
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setMinimumDuration(0)
        progress_dialog.value()
        return progress_dialog

    def plus_one_step_loading(self, progress_dialog):
        current_value = progress_dialog.value()
        progress_dialog.setValue(current_value+1)
        if progress_dialog.wasCanceled():
            return
        return progress_dialog

    def finish_loading(self, progress_dialog, pr_max):
        progress_dialog.setValue(pr_max)
        return progress_dialog


# if __name__ == '__main__':
#     logger.add(
#         "logs/logs.log",
#         level="DEBUG",
#         format="{time} {level} {message}",
#         rotation="10 MB",  # Ротация лог-файла по размеру
#         compression="zip",  # Сжатие старых лог-файлов в zip-архивы
#         enqueue=True,  # Записывать сообщения асинхронно
#     )
#     QCoreApplication.setApplicationName("Finder")
#
#     app = QtWidgets.QApplication(sys.argv)
#     app.setStyle('Fusion')
#
#     capture_window = StartWindow()
#     capture_window.show()
#     sys.exit(app.exec_())
