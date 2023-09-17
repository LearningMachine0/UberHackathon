from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
import sys

def main():
    # Create the PyQt6 application
    app = QApplication(sys.argv)

    # Create a main window
    window = QMainWindow()
    window.setWindowTitle("PyQt6 Application")
    window.setGeometry(100, 100, 400, 200)

    # Create a label and add it to the main window
    label = QLabel("Hello, PyQt6!", window)
    label.setGeometry(50, 50, 300, 100)

    # Show the main window
    window.show()

    # Start the application event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()