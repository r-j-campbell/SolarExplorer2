from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np
# from canvas_functions import *

def layouts(se):
    se.main_layout = QHBoxLayout()
    se.setLayout(se.main_layout)
    #canvas
    se.canvas_tabs = QTabWidget()
    se.canvas_tabs.setTabsClosable(True)
    se.canvas_tabs.tabCloseRequested.connect(lambda index: destroy_tab(index,se))
    se.main_layout.addWidget(se.canvas_tabs)

def create_tab(se,instrument_object):
    #canvas
    se.canvas_tabs_list.append(QWidget())
    se.canvas_tabs.addTab(se.canvas_tabs_list[-1],"test")

    se.tab_layout = QHBoxLayout() #main tab object
    se.canvas_tabs_list[-1].setLayout(se.tab_layout)

    instrument_object.left_layout = QVBoxLayout() #control panel
    instrument_object.right_layout = QVBoxLayout() #canvas
    se.tab_layout.addLayout(instrument_object.left_layout,20)
    se.tab_layout.addLayout(instrument_object.right_layout,80)
    se.tab_layout.addStretch(1)

    #control panel
    instrument_object.widget_tabs = QTabWidget()
    instrument_object.tab1 = QWidget()
    instrument_object.tab2 = QWidget()
    instrument_object.tab3 = QWidget()
    instrument_object.tab4 = QWidget()
    instrument_object.widget_tabs.addTab(instrument_object.tab1,"Files")
    instrument_object.widget_tabs.addTab(instrument_object.tab2,"Maps")
    instrument_object.widget_tabs.addTab(instrument_object.tab3,"Profiles")
    instrument_object.widget_tabs.addTab(instrument_object.tab4,"Information")
    instrument_object.left_layout.addWidget(instrument_object.widget_tabs)

    #canvas

    #canvas
    instrument_object.maps_widget = QWidget()
    instrument_object.profiles_widget = QWidget()
    instrument_object.maps_widget.setLayout(instrument_object.right_layout)
    instrument_object.profiles_widget.setLayout(instrument_object.right_layout)
    instrument_object.splitter1 = QSplitter(Qt.Vertical)
    instrument_object.splitter1.addWidget(instrument_object.maps_widget)
    instrument_object.splitter1.addWidget(instrument_object.profiles_widget)
    instrument_object.right_layout.addWidget(instrument_object.splitter1)

    instrument_object.maps_layout = QHBoxLayout() #maps
    instrument_object.profiles_layout = QHBoxLayout() #plots
    instrument_object.maps_widget.setLayout(instrument_object.maps_layout)
    instrument_object.profiles_widget.setLayout(instrument_object.profiles_layout)

    #-------widgets for canvas-------#
    instrument_object.sc1 = MplCanvas1(instrument_object, width=5, height=4, dpi=100)
    instrument_object.sc1.fig1.canvas.mpl_connect('button_press_event', se.mouseclicks)
    instrument_object.sc2 = MplCanvas2(instrument_object, width=5, height=4, dpi=100)

    instrument_object.maps_layout.addWidget(instrument_object.sc1)
    instrument_object.sc1.setMinimumSize(1,1)
    instrument_object.profiles_layout.addWidget(instrument_object.sc2)
    instrument_object.sc2.setMinimumSize(1,1)

def destroy_tab(index,se):
    se.canvas_tabs.removeTab(index)

def widgets(se):
    #-------widgets for control panel-------#
    se.display_btn = QPushButton("Display")
    se.display_btn.clicked.connect(lambda checked: se.display())


class MplCanvas1(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=10, height=10, dpi=300):
        self.fig1 = Figure(figsize=(width, height), dpi=dpi,tight_layout=True)
        super(MplCanvas1, self).__init__(self.fig1)
class MplCanvas2(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=10, height=10, dpi=300):
        self.fig2 = Figure(figsize=(width, height), dpi=dpi,tight_layout=True)
        super(MplCanvas2, self).__init__(self.fig2)


def file_manager_layout_and_widgets(self,se):
    #widgets
    self.get_dataset_btn = QPushButton("Search for dataset")
    self.get_dataset_btn.clicked.connect(lambda checked: se.get_dataset(self))
    self.select_dataset_combobox = QComboBox(self)
    self.select_dataset_combobox.addItems(se.file_list)
    self.get_binary_btn = QPushButton("Search for binary map")
    self.get_binary_btn.clicked.connect(lambda checked: se.get_binary(self))
    self.select_binary_combobox = QComboBox(self)
    self.select_binary_combobox.addItems(se.binary_file_list)
    self.binary_checkbutton = QCheckBox("Include binary map",self)
    self.reshape_checkbutton = QCheckBox("Reshape array",self)
    self.load_dataset_btn = QPushButton("Display")
    self.load_dataset_btn.clicked.connect(lambda checked: se.load_dataset(self))
    
    #layout
    self.file_manager_layout = QVBoxLayout()
    self.file_manager_layout.addWidget(self.get_dataset_btn)
    self.file_manager_layout.addWidget(self.select_dataset_combobox)
    self.file_manager_layout.addWidget(self.get_binary_btn)
    self.file_manager_layout.addWidget(self.select_binary_combobox)
    self.file_manager_layout.addWidget(self.binary_checkbutton)
    self.file_manager_layout.addWidget(self.reshape_checkbutton)
    self.file_manager_layout.addWidget(self.load_dataset_btn)
    self.file_manager_layout.addStretch(1)
    self.setLayout(self.file_manager_layout)

def file_search(self,se):
    se.file_manager()


