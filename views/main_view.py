from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QTableView, QLineEdit, QFrame, QStackedWidget, QDialog, QCheckBox, QDialogButtonBox, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import QAbstractTableModel
import pandas as pd
from column_selection_dialog import ColumnSelectionDialog

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
        self.recommendations_button = QPushButton("Generar Recomendaciones")
        self.recommendations_button.setFixedHeight(50)

        # Ajustar el espaciado entre botones
        sidebar_layout.addWidget(self.import_button)
        sidebar_layout.addWidget(self.filter_button)
        sidebar_layout.addWidget(self.recommendations_button)

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

        # Ajustar el tamaño de la barra de búsqueda para que ocupe solo el espacio restante
        search_layout.addWidget(self.search_line_edit)
        search_layout.addWidget(self.search_button)

        # Añadir la barra de búsqueda al layout principal
        main_content_layout.addLayout(search_layout)

        # Tabla para mostrar los datos
        self.table_view = QTableView()
        main_content_layout.addWidget(self.table_view)

        # Añadir todo al layout principal
        content_layout.addWidget(sidebar)
        content_layout.addWidget(main_content)

        # Crear un widget principal
        main_widget = QWidget()
        main_widget.setLayout(content_layout)
        self.setCentralWidget(main_widget)

    def filter_columns(self):
        """Permite al usuario seleccionar las columnas que desea ver."""
        if not self.data:
            QMessageBox.warning(self, "Advertencia", "No hay datos cargados para seleccionar columnas.")
            return

        # Crear un cuadro de diálogo para seleccionar columnas
        column_dialog = ColumnSelectionDialog(self.data.columns.tolist())
        if column_dialog.exec() == QDialog.Accepted:
            selected_columns = column_dialog.get_selected_columns()
            self.set_data(self.data[selected_columns])

    def update_status(self, message):
        """Método para actualizar el mensaje de estado en la UI"""
        self.status_label.setText(message)

    def set_data(self, data):
        """Método para mostrar datos en la tabla"""
        self.data = data
        model = PandasModel(data)
        self.table_view.setModel(model)

    def get_import_button(self):
        return self.import_button

    def get_filter_button(self):
        return self.filter_button

    def get_recommendations_button(self):
        return self.recommendations_button
