from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QTableView, QLineEdit, QFrame, QStackedWidget
from PySide6.QtGui import QIcon
from PySide6.QtCore import QAbstractTableModel
import pandas as pd

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configura la ventana principal
        self.setWindowTitle("Analizador de Archivos Excel")
        self.setGeometry(100, 100, 1200, 800)
        self.showMaximized()  # Abrir la ventana maximizada

        # Crear un contenedor principal
        main_layout = QVBoxLayout()

        # Barra lateral (Sidebar)
        sidebar = QFrame()
        sidebar.setFixedWidth(200)  # Establecer un ancho fijo para la barra lateral
        sidebar_layout = QVBoxLayout()
        sidebar.setLayout(sidebar_layout)

        # Estilo solo aplicado al contenedor principal, no a la pestaña de filtrado
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2e2e2e;
                font-family: Arial, sans-serif;
                color: #f0f0f0;
            }

            QLabel {
                font-size: 14px;
                color: #f0f0f0;
                margin: 10px 0;
            }

            QPushButton {
                background-color: #3c4e60;
                color: white;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                margin: 10px 0px;
            }

            QLineEdit {
                border: 1px solid #444;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #f0f0f0;
                background-color: #3c4e60;
            }

            QTableView {
                border: 1px solid #444;
                border-radius: 8px;
                background-color: #333333;
                color: #f0f0f0;
                padding: 10px;
            }

            QFrame {
                background-color: #444;
                border-radius: 8px;
                border: 1px solid #333;
            }
        """)

        # Botones fijos en el sidebar, ajustando el espaciado entre ellos
        self.import_button = QPushButton("Importar Archivos")
        self.import_button.setIcon(QIcon("icons/import_icon.png"))
        self.import_button.setFixedHeight(50)
        self.filter_button = QPushButton("Filtrar Datos")
        self.filter_button.setIcon(QIcon("icons/filter_icon.png"))
        self.filter_button.setFixedHeight(50)

        # Ajustar el espaciado entre botones
        sidebar_layout.addWidget(self.import_button)
        sidebar_layout.addWidget(self.filter_button)

        # Layout para el contenido principal
        content_layout = QHBoxLayout()

        # Contenedor para el contenido principal (tabla y barra de búsqueda)
        main_content = QWidget()
        main_content_layout = QVBoxLayout()
        main_content.setLayout(main_content_layout)

        # Etiqueta de estado
        self.status_label = QLabel("Estado: Esperando acción del usuario.")
        main_content_layout.addWidget(self.status_label)

        # Barra de búsqueda en la parte superior
        search_layout = QHBoxLayout()
        self.search_line_edit = QLineEdit()
        self.search_line_edit.setPlaceholderText("Buscar...")
        self.search_button = QPushButton("Buscar")
        self.search_button.setIcon(QIcon("icons/search_icon.png"))
        self.search_button.clicked.connect(self.filter_search_results)

        # Ajustar el tamaño de la barra de búsqueda para que ocupe solo el espacio restante
        search_layout.addWidget(self.search_line_edit)
        search_layout.addWidget(self.search_button)

        # Añadir la barra de búsqueda al layout principal debajo de la etiqueta de estado
        main_content_layout.addLayout(search_layout)

        # Tabla donde se mostrará la data
        self.table_view = QTableView()
        self.table_view.resizeColumnsToContents()
        main_content_layout.addWidget(self.table_view)

        # Crear un QStackedWidget para manejar las diferentes vistas (contenido principal o filtrado)
        self.stacked_widget = QStackedWidget()

        # Pestaña de contenido principal con estilo aplicado
        self.stacked_widget.addWidget(main_content) 

        # Pestaña de filtrado sin estilo
        self.filter_content = QWidget()  # Esta pestaña no tiene estilos
        self.stacked_widget.addWidget(self.filter_content)

        # Añadir el sidebar y el contenido principal al layout
        content_layout.addWidget(sidebar)
        content_layout.addWidget(self.stacked_widget)

        # Contenedor principal
        container = QWidget()
        container.setLayout(main_layout)
        main_layout.addLayout(content_layout)

        self.setCentralWidget(container)

        # Datos y modelo para la tabla (placeholder)
        self.model = None
        self.data = None
        self.selected_columns = []

    def set_data(self, data):
        """Este método es para configurar los datos a mostrar en la tabla"""
        self.data = data
        self.model = PandasTableModel(data)
        self.table_view.setModel(self.model)

    def update_status(self, message):
        """Método para actualizar el mensaje de estado en la UI"""
        self.status_label.setText(message)

    def get_import_button(self):
        """Retorna el botón de importar archivos"""
        return self.import_button

    def get_filter_button(self):
        """Retorna el botón de filtrar datos"""
        return self.filter_button

    def filter_search_results(self):
        """Filtra los datos según el texto en la barra de búsqueda"""
        search_text = self.search_line_edit.text().lower()
        if search_text:
            filtered_data = self.data[self.data.apply(lambda row: row.astype(str).str.contains(search_text).any(), axis=1)]
            self.set_data(filtered_data)
        else:
            self.set_data(self.data)  # Mostrar los datos sin filtro si no hay texto en la búsqueda


class PandasTableModel(QAbstractTableModel):
    def __init__(self, data_frame):
        super().__init__()
        self.df = data_frame

    def rowCount(self, parent=None):
        return len(self.df)

    def columnCount(self, parent=None):
        return len(self.df.columns)

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self.df.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.df.columns[section]
            else:
                return str(section + 1)
        return None
