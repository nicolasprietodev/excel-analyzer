from PySide6.QtWidgets import QApplication
from views.main_view import MainView
from controllers.main_controller import MainController

def main():
    app = QApplication([])

    # Crear la vista
    view = MainView()

    # Crear el controlador y pasarle la vista
    controller = MainController(view)

    # Mostrar la ventana
    view.show()  # Asegúrate de que la ventana se muestre correctamente

    app.exec()

if __name__ == "__main__":
    main()
