from PySide6.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QDialogButtonBox

class ColumnSelectionDialog(QDialog):
    def __init__(self, columns, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleccionar Columnas")

        self.selected_columns = []

        # Crear el layout para las casillas de verificación
        layout = QVBoxLayout(self)

        # Crear las casillas de verificación para cada columna
        self.checkboxes = {}
        for col in columns:
            checkbox = QCheckBox(col)
            layout.addWidget(checkbox)
            self.checkboxes[col] = checkbox

        # Botones de aceptar y cancelar
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_selected_columns(self):
        """Devuelve la lista de columnas seleccionadas."""
        self.selected_columns = [col for col, checkbox in self.checkboxes.items() if checkbox.isChecked()]
        return self.selected_columns
