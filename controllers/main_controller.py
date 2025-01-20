from PySide6.QtWidgets import QDialog, QVBoxLayout, QFrame, QCheckBox, QPushButton, QLabel, QScrollArea, QMessageBox, QFileDialog, QWidget
import pandas as pd

class MainController:
    def __init__(self, view):
        self.view = view
        self.data = None
        self.data_by_file = {}
        self.selected_columns_by_file = {}

        # Conectar los botones a sus métodos
        self.view.get_import_button().clicked.connect(self.import_files)
        self.view.get_filter_button().clicked.connect(self.filter_data)

    def import_files(self):
        """Abre un diálogo para seleccionar archivos Excel y los carga."""
        print("Abriendo el diálogo para seleccionar archivos...")  # Comentario de depuración
        files, _ = QFileDialog.getOpenFileNames(
            self.view, "Seleccionar Archivos Excel", "", "Archivos Excel (*.xlsx;*.xls)"
        )

        # Verificar si se han seleccionado archivos
        if not files:
            print("No se seleccionaron archivos.")  # Comentario de depuración
            QMessageBox.warning(self.view, "Advertencia", "No se seleccionaron archivos.")
            return

        print(f"Archivos seleccionados: {files}")  # Comentario de depuración

        # Cargar los archivos seleccionados
        for file in files:
            df = pd.read_excel(file)
            self.data_by_file[file] = df
            print(f"Archivo cargado: {file}")  # Comentario de depuración

        # Actualizar el estado en la vista
        self.view.update_status("Archivos cargados correctamente.")
        
        # No llamamos a select_columns aquí
        # Solo actualizamos la vista para indicar que los archivos fueron cargados correctamente


    def select_columns(self):
        """Permite al usuario seleccionar columnas de los archivos cargados."""
        if not self.data_by_file:
            QMessageBox.warning(self.view, "Advertencia", "Carga datos primero.")
            return

        # Crear un formulario de selección de columnas
        select_window = self.create_select_columns_window()
        select_window.exec()

    def create_select_columns_window(self):
        """Genera la ventana para seleccionar las columnas de cada archivo."""
        select_window = QDialog(self.view)
        select_window.setWindowTitle("Seleccionar Columnas")

        # Layout principal de la ventana
        layout = QVBoxLayout(select_window)

        # Crear un QWidget para contener el contenido desplazable
        scroll_content = QWidget()

        # Layout del contenido desplazable
        scroll_layout = QVBoxLayout(scroll_content)

        checkboxes = {}
        for file, df in self.data_by_file.items():
            frame = QFrame(scroll_content)
            frame.setLayout(QVBoxLayout())

            label = QLabel(f"Columnas en {file.split('/')[-1]}")
            frame.layout().addWidget(label)

            for col in df.columns:
                checkbox = QCheckBox(col)
                checkboxes[col] = checkbox
                frame.layout().addWidget(checkbox)
            
            scroll_layout.addWidget(frame)

        # Crear un QScrollArea y asignar el widget con el contenido desplazable
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Asegúrate de que el área de desplazamiento se redimensione
        scroll_area.setWidget(scroll_content)  # Asignar el contenido a la zona de desplazamiento

        # Añadir el área de desplazamiento al layout principal
        layout.addWidget(scroll_area)

        # Botón para confirmar selección
        button = QPushButton("Aceptar", select_window)
        button.clicked.connect(lambda: self.confirm_column_selection(select_window, checkboxes))
        layout.addWidget(button)

        return select_window


    def confirm_column_selection(self, window, checkboxes):
        """Confirma la selección de columnas y actualiza los datos."""
        selected_columns = {}
        for file, df in self.data_by_file.items():
            # Obtener las columnas seleccionadas de los checkboxes correspondientes
            file_checkboxes = [checkbox for col, checkbox in checkboxes.items() if col in df.columns]
            selected_columns[file] = [col for col, checkbox in zip(df.columns, file_checkboxes) if checkbox.isChecked()]

        self.selected_columns_by_file = selected_columns
        window.accept()  # Cierra la ventana de selección de columnas
        self.update_table_data()


    def update_table_data(self):
            """Filtra los datos seleccionados y los muestra en la tabla."""
            if not self.selected_columns_by_file:
                QMessageBox.warning(self.view, "Advertencia", "No seleccionaste columnas.")
                return
            
            combined_data = []
            for file, selected_columns in self.selected_columns_by_file.items():
                df = self.data_by_file[file]
                if selected_columns:
                    combined_data.append(df[selected_columns])

            if combined_data:
                self.data = pd.concat(combined_data, ignore_index=True)
                self.view.set_data(self.data)
                self.view.update_status("Datos filtrados correctamente.")
            else:
                QMessageBox.warning(self.view, "Advertencia", "No se seleccionaron columnas para mostrar.")
    
    def filter_data(self):
        """Acción de filtrar los datos."""
        if not self.data_by_file:
            QMessageBox.warning(self.view, "Advertencia", "No has cargado archivos.")
            return

        # Permite al usuario seleccionar columnas de los archivos cargados
        self.select_columns()

