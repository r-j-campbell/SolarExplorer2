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

def create_tab(se):
    #canvas
    se.canvas_tabs_list.append(QWidget())
    se.canvas_tabs.addTab(se.canvas_tabs_list[-1],"test")

    se.tab_layout = QHBoxLayout() #control panel
    se.canvas_tabs_list[-1].setLayout(se.tab_layout)

    se.left_layout = QVBoxLayout() #control panel
    se.right_layout = QVBoxLayout() #canvas
    se.tab_layout.addLayout(se.left_layout,20)
    se.tab_layout.addLayout(se.right_layout,80)
    se.tab_layout.addStretch(1)

    #control panel
    se.widget_tabs = QTabWidget()
    se.tab1 = QWidget()
    se.tab2 = QWidget()
    se.tab3 = QWidget()
    se.tab4 = QWidget()
    se.widget_tabs.addTab(se.tab1,"Files")
    se.widget_tabs.addTab(se.tab2,"Maps")
    se.widget_tabs.addTab(se.tab3,"Profiles")
    se.widget_tabs.addTab(se.tab4,"Information")
    se.left_layout.addWidget(se.widget_tabs)

    #control panel
    se.widget_tabs2 = QTabWidget()
    se.tab12 = QWidget()
    se.tab22 = QWidget()
    se.tab32 = QWidget()
    se.tab42 = QWidget()
    se.widget_tabs2.addTab(se.tab12,"Files")
    se.widget_tabs2.addTab(se.tab22,"Maps")
    se.widget_tabs2.addTab(se.tab32,"Profiles")
    se.widget_tabs2.addTab(se.tab42,"Information")
    se.right_layout.addWidget(se.widget_tabs2)

def destroy_tab(index,se):
    se.canvas_tabs.removeTab(index)


def widgets(se):
    #-------widgets for control panel-------#
    se.display_btn = QPushButton("Display")
    se.display_btn.clicked.connect(lambda checked: se.display())

def file_manager_layout_and_widgets(self,se):
    #widgets
    self.get_dataset_btn = QPushButton("Search for files")
    self.get_dataset_btn.clicked.connect(lambda checked: se.get_dataset(self))
    self.select_dataset_combobox = QComboBox(self)
    self.reshape_checkbutton = QCheckBox("Reshape array?",self)
    self.load_dataset_btn = QPushButton("Display")
    self.load_dataset_btn.clicked.connect(lambda checked: se.load_dataset(self))
    
    #layout
    self.file_manager_layout = QVBoxLayout()
    self.file_manager_layout.addWidget(self.get_dataset_btn)
    self.file_manager_layout.addWidget(self.select_dataset_combobox)
    self.file_manager_layout.addWidget(self.reshape_checkbutton)
    self.file_manager_layout.addWidget(self.load_dataset_btn)
    self.file_manager_layout.addStretch(1)
    self.setLayout(self.file_manager_layout)

def file_search(self,se):
    se.file_manager()


