import cv2
from PIL import Image
from PySide6.QtWidgets import QWidget, QApplication, QFileDialog
from ...components import PhotoViewer
from .page_screen_ui import Ui_Form


class PageScreen(QWidget,Ui_Form):
    _page = None
    def __init__(self):
        super(PageScreen,self).__init__()
        self.setupUi(self)
        self._config_page()
        self._set_image(self._get_image())



    def _config_page(self):
        self._page = PhotoViewer(self.page_container)
        self.page_container.layout().addWidget(self._page)

    def _set_image(self,path: str):
        image = Image.fromarray(cv2.imread(path))
        self._page.set_image(image.toqpixmap())

    def _get_image(self) -> str | None:
        # Configurar a caixa de diálogo
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Selecionar Imagem")
        file_dialog.setNameFilter("Imagens (*.png *.jpg *.jpeg *.bmp *.gif)")

        # Executar o diálogo e obter o resultado
        if file_dialog.exec():
            arquivos_selecionados = file_dialog.selectedFiles()
            if arquivos_selecionados:
                caminho_imagem = arquivos_selecionados[0]
                return caminho_imagem
                # Aqui você pode usar o caminho da imagem como necessário



if __name__ == "__main__":
    app = QApplication()
    test = PageScreen()
    test.show()
    app.exec()