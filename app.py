import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                           QVBoxLayout, QWidget, QFileDialog, QComboBox, 
                           QHBoxLayout, QFrame, QSizePolicy)
from PyQt5.QtGui import QPixmap, QImage, QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QSize
from rembg import remove, new_session
from PIL import Image
import io

class MinimalistRemoverApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BG Remover")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(600, 400)
        
        # Setup model
        os.environ['U2NET_HOME'] = os.path.abspath('models')
        self.available_models = {
            'u2net': 'u2net.onnx',
            'u2netp': 'u2netp.onnx',
            'u2net_human_seg': 'u2net_human_seg.onnx',
            'u2net_cloth_seg': 'u2net_cloth_seg.onnx',
            'silueta': 'silueta.onnx',
            'isnet-general-use': 'isnet-general-use.onnx',
            'isnet-anime': 'isnet-anime.onnx',
            'sam': 'sam.onnx',
            'birefnet-general': 'birefnet-general.onnx',
            'birefnet-general-lite': 'birefnet-general-lite.onnx',
            'birefnet-portrait': 'birefnet-portrait.onnx',
            'birefnet-dis': 'birefnet-dis.onnx',
            'birefnet-hrsod': 'birefnet-hrsod.onnx',
            'birefnet-cod': 'birefnet-cod.onnx',
            'birefnet-massive': 'birefnet-massive.onnx'
        }
        
        # Setup UI
        self.init_ui()
        self.check_local_models()
        
        # Variabel gambar
        self.input_image = None
        self.output_image = None

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Layout utama
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header
        title = QLabel("Background Remover")
        title.setFont(QFont('Arial', 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Control panel
        control_layout = QHBoxLayout()
        control_layout.setSpacing(10)
        
        # Model selection
        self.model_combobox = QComboBox()
        self.model_combobox.addItems(self.available_models.keys())
        self.model_combobox.setFixedHeight(35)
        self.model_combobox.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 5px;
                min-width: 120px;
            }
        """)
        
        # Tombol
        btn_style = """
            QPushButton {
                padding: 8px 15px;
                border: none;
                border-radius: 5px;
                background-color: #4CAF50;
                color: white;
                min-width: 100px;
            }
            QPushButton:hover { background-color: #45a049; }
            QPushButton:disabled { background-color: #cccccc; }
        """
        
        self.upload_btn = QPushButton("Upload Image")
        self.upload_btn.setFixedHeight(35)
        self.upload_btn.clicked.connect(self.upload_image)
        
        self.remove_btn = QPushButton("Remove BG")
        self.remove_btn.setFixedHeight(35)
        self.remove_btn.clicked.connect(self.remove_background)
        self.remove_btn.setEnabled(False)
        
        self.save_btn = QPushButton("Save")
        self.save_btn.setFixedHeight(35)
        self.save_btn.clicked.connect(self.save_image)
        self.save_btn.setEnabled(False)
        
        # Terapkan style ke tombol
        for btn in [self.upload_btn, self.remove_btn, self.save_btn]:
            btn.setStyleSheet(btn_style)
        
        control_layout.addWidget(self.model_combobox)
        control_layout.addWidget(self.upload_btn)
        control_layout.addWidget(self.remove_btn)
        control_layout.addWidget(self.save_btn)
        main_layout.addLayout(control_layout)
        
        # Image display area
        self.image_frame = QFrame()
        self.image_frame.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border: 2px dashed #ddd;
                border-radius: 10px;
            }
        """)
        self.image_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setText("Upload an image to start")
        self.image_label.setFont(QFont('Arial', 12))
        self.image_label.setStyleSheet("color: #888;")
        
        frame_layout = QVBoxLayout(self.image_frame)
        frame_layout.addWidget(self.image_label)
        
        main_layout.addWidget(self.image_frame)
        
        # Status bar
        self.status_bar = QLabel()
        self.status_bar.setStyleSheet("color: #666; font-size: 12px;")
        main_layout.addWidget(self.status_bar)

    def check_local_models(self):
        missing = [name for name, file in self.available_models.items() 
                 if not os.path.exists(os.path.join('models', file))]
        if missing:
            self.show_status(f"Missing models: {', '.join(missing)}", "error")

    def show_status(self, message, type="info"):
        color_map = {
            "info": "#2196F3",
            "success": "#4CAF50",
            "error": "#f44336"
        }
        self.status_bar.setText(message)
        self.status_bar.setStyleSheet(f"color: {color_map[type]}; font-size: 12px;")

    def upload_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg)")
        
        if file_name:
            try:
                self.input_image = Image.open(file_name)
                pixmap = QPixmap(file_name)
                self.display_image(pixmap)
                self.remove_btn.setEnabled(True)
                self.save_btn.setEnabled(False)
                self.show_status("Image loaded successfully", "success")
            except Exception as e:
                self.show_status(f"Error loading image: {str(e)}", "error")

    def display_image(self, pixmap):
        scaled = pixmap.scaled(
            self.image_frame.size() - QSize(40, 40),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.image_label.setPixmap(scaled)
        self.image_label.setText("")

    def remove_background(self):
        if self.input_image:
            try:
                model_name = self.model_combobox.currentText()
                model_file = self.available_models[model_name]
                model_path = os.path.join('models', model_file)
                
                if not os.path.exists(model_path):
                    self.show_status(f"Model file {model_file} not found!", "error")
                    return
                
                self.show_status("Processing...", "info")
                QApplication.processEvents()  # Update UI
                
                session = new_session(model_name)
                self.output_image = remove(self.input_image, session=session)
                
                # Convert to QPixmap
                byte_arr = io.BytesIO()
                self.output_image.save(byte_arr, format='PNG')
                pixmap = QPixmap()
                pixmap.loadFromData(byte_arr.getvalue())
                
                self.display_image(pixmap)
                self.save_btn.setEnabled(True)
                self.show_status("Background removed successfully", "success")
                
            except Exception as e:
                self.show_status(f"Error processing image: {str(e)}", "error")

    def save_image(self):
        if self.output_image:
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Save Image", "", "PNG Files (*.png)")
            
            if file_name:
                try:
                    self.output_image.save(file_name, 'PNG')
                    self.show_status(f"Image saved to {file_name}", "success")
                except Exception as e:
                    self.show_status(f"Error saving image: {str(e)}", "error")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Set style
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(255, 255, 255))
    palette.setColor(QPalette.WindowText, QColor(53, 53, 53))
    app.setPalette(palette)
    
    window = MinimalistRemoverApp()
    window.show()
    sys.exit(app.exec_())