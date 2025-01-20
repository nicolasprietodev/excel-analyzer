from PySide6.QtWidgets import QMessageBox, QFileDialog
import pandas as pd

class MainController:
    def __init__(self, view):
        self.view = view
        self.sales_data = None
        self.purchases_data = None
        self.data_by_file = {}

        # Conectar los botones a sus métodos
        self.view.get_import_button().clicked.connect(self.import_files)
        self.view.get_filter_button().clicked.connect(self.filter_data)
        self.view.get_recommendations_button().clicked.connect(self.generate_recommendations)

    def import_files(self):
        """Abre un diálogo para seleccionar archivos Excel y los carga."""
        files, _ = QFileDialog.getOpenFileNames(
            self.view, "Seleccionar Archivos Excel", "", "Archivos Excel (*.xlsx;*.xls)"
        )

        if not files:
            QMessageBox.warning(self.view, "Advertencia", "No se seleccionaron archivos.")
            return

        # Cargar los archivos seleccionados
        for file in files:
            df = pd.read_excel(file)
            self.data_by_file[file] = df

        # Actualizar el estado en la vista
        self.view.update_status("Archivos cargados correctamente.")
        self.process_data()

    def process_data(self):
        """Procesa los datos de ventas y compras para extraer información relevante."""
        for file, df in self.data_by_file.items():
            if "ÍTEM - NOMBRE" in df.columns and "ÍTEM - CANTIDAD" in df.columns:
                # Si es un archivo de ventas
                if "Ventas" in file:
                    self.sales_data = df
                # Si es un archivo de compras
                elif "Compras" in file:
                    self.purchases_data = df

        if self.sales_data is not None:
            self.view.update_status("Datos de ventas cargados y procesados.")
        if self.purchases_data is not None:
            self.view.update_status("Datos de compras cargados y procesados.")
        
        # Si ambos archivos están cargados, hacer el análisis de ventas
        if self.sales_data is not None and self.purchases_data is not None:
            self.analyze_data()

    def analyze_data(self):
        """Realiza un análisis de las ventas y compras, encontrando los productos más y menos vendidos."""
        if self.sales_data is not None:
            # Agrupar por nombre de ítem y sumar las cantidades
            grouped_sales = self.sales_data.groupby("ÍTEM - NOMBRE")["ÍTEM - CANTIDAD"].sum()
            most_sold = grouped_sales.idxmax()
            most_sold_qty = grouped_sales.max()
            least_sold = grouped_sales.idxmin()
            least_sold_qty = grouped_sales.min()

            # Mostrar las recomendaciones de ventas
            recommendation_text = (
                f"Producto más vendido: {most_sold} ({most_sold_qty} unidades)\n"
                f"Producto menos vendido: {least_sold} ({least_sold_qty} unidades)"
            )
            self.view.update_status(recommendation_text)
        else:
            self.view.update_status("No se han cargado datos de ventas.")

    def generate_recommendations(self):
        """Genera recomendaciones basadas en los datos de ventas y las muestra."""
        if self.sales_data is None:
            QMessageBox.warning(self.view, "Advertencia", "No se han cargado datos de ventas.")
            return

        # Verificar si las columnas necesarias están presentes
        required_columns = ["ÍTEM - NOMBRE", "ÍTEM - CANTIDAD"]
        if not all(col in self.sales_data.columns for col in required_columns):
            QMessageBox.warning(self.view, "Error", "El archivo de ventas no contiene las columnas requeridas.")
            return

        # Procesar las recomendaciones
        grouped_sales = self.sales_data.groupby("ÍTEM - NOMBRE")["ÍTEM - CANTIDAD"].sum()
        most_sold = grouped_sales.idxmax()
        most_sold_qty = grouped_sales.max()
        least_sold = grouped_sales.idxmin()
        least_sold_qty = grouped_sales.min()

        # Mostrar las recomendaciones
        recommendation_text = (
            f"Producto más vendido: {most_sold} ({most_sold_qty} unidades)\n"
            f"Producto menos vendido: {least_sold} ({least_sold_qty} unidades)"
        )
        self.view.update_status(recommendation_text)

    def filter_data(self):
        """Filtra y muestra los datos seleccionados."""
        if not self.data_by_file:
            QMessageBox.warning(self.view, "Advertencia", "No se han cargado archivos para filtrar.")
            return

        # Llamar a los datos filtrados de alguna forma (puedes agregar filtros adicionales aquí)
        # Ejemplo simple: tomar los datos del primer archivo cargado
        first_file_data = next(iter(self.data_by_file.values()))
        self.view.set_data(first_file_data)
        