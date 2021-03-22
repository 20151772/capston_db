import sys
import file_name_changer as fc
import motion_data as md
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.check_box = []
        self.list = []
        self.selected_list = []
        self.setupUI()

    # UI 생성
    def setupUI(self):
        self.setWindowTitle("Motion Capturer")
        self.resize(750, 750)

        # 전체 레이아웃(vertical)
        self.hbox_layout = QHBoxLayout()

        # 좌측 리스트(스크롤>그룹박스>폼레이아웃>체크박스)
        self.form_layout = QFormLayout()
        self.group_box = QGroupBox(self)
        # 리스트에 넣기
        self.setList()
        self.group_box.setLayout(self.form_layout)
        # 스크롤바에 리스트 넣기
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(self.group_box)
        self.scroll_area.setStyleSheet("background-color: white;")
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setWidgetResizable(True)
        self.hbox_layout.addWidget(self.scroll_area)

        # 우측 버튼 레이아웃(horizontal)
        self.vbox_layout = QVBoxLayout()
        # 폴더열기 버튼
        self.file_btn = QPushButton("파일열기", self)
        self.file_btn.clicked.connect(self.fileBtnClicked)
        self.vbox_layout.addWidget(self.file_btn)
        # 실행 버튼
        self.execute_btn = QPushButton("실행", self)
        self.execute_btn.clicked.connect(self.executeBtnClicked)
        self.vbox_layout.addWidget(self.execute_btn)

        # 레이아웃 정리
        self.hbox_layout.addLayout(self.vbox_layout)
        self.setLayout(self.hbox_layout)

    # 리스트 생성
    def setList(self):
        # 체크박스, 폼 레이아웃 초기화
        self.check_box.clear()
        for x in reversed(range(self.form_layout.count())):
            self.form_layout.itemAt(x).widget().setParent(None)

        # 리스트에 따른 체크박스 생성
        for i in range(len(self.list)):
            self.check_box.append(QCheckBox(self.list[i]))
            self.form_layout.addWidget(self.check_box[i])

    # 파일열기 버튼 클릭
    def fileBtnClicked(self):
        # 파일 탐색기
        self.fileDialog = QFileDialog(self)
        self.fileDialog.setFileMode(QFileDialog.ExistingFiles)
        self.fileDialog.setNameFilter(
            self.tr("Videos (*.avi *.mp4 *.wmv *.mpg *.flv *.mov);; All Files(*.*)"))  # 파일 탐색기 확장자 설정
        self.fileDialog.setViewMode(QFileDialog.Detail)
        self.list.clear()
        if self.fileDialog.exec_():
            self.list = self.fileDialog.selectedFiles()
        self.setList()

    # 실행 버튼 클릭
    def executeBtnClicked(self):
        # 체크된 리스트 구함
        self.selected_list.clear()
        for i in range(len(self.list)):
            if self.check_box[i].checkState():
                print(self.list[i])
                self.selected_list.append(self.list[i])

        motion = md.MotionData()
        # 체크된 리스트 내용으로 변환 시작
        for j in range(len(self.selected_list)):
            #self.dialog = QDialog()
            #self.dialog.setWindowTitle("Sign Language Video")
            #self.dialog.show()

            motion.getHolisticData(self.selected_list[j])

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    # AIHub 수화 영상 이름 변경 (필요시 사용)
    '''
    reader = fc.FileNameChanger()
    reader.readCsvFile('./reference/data_anotation.csv', 'D:/sign_language_video', 420)
    print("read csv and video name changed")
    '''

    # UI 실행
    main()
