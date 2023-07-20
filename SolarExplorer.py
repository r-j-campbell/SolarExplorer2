from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtCore import QSettings
import os
import sys
from design import *
from instruments import *

class SolarExplorer(QWidget):
    def __init__(self):
        super().__init__()
        QSettings().clear()
        self.setWindowTitle("Solar Explorer")
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.appheight = self.screenRect.height()
        self.appwidth = self.screenRect.width()
        self.setGeometry(0,0,int(self.appwidth),int(self.appheight))
        self.settings = QSettings("SolarExplorer", "SolarExplorer")

        self.only_int = QIntValidator()
        self.only_double = QDoubleValidator()

        self.canvas_tabs_list = [None]
        self.increment = 0
        self.click_increment = 0
        self.match = None
        self.reload_flag = False
        self.file_manager_flag = None
        self.dataset_dict = {0: {"file": "first dummy value"}}
        self.file_list = [None]
        self.binary_file_list = [None]

        self.CT_options = ['hsv', 'gray', 'gray_r', 'viridis','bwr', 'bwr_r','hot', 'plasma', 'inferno', 'magma', 'cividis',
                            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn',
                            'binary', 'gist_yarg', 'gist_gray', 'bone',
                            'pink', 'spring', 'summer', 'autumn', 'winter', 'cool',
                            'Wistia', 'afmhot', 'gist_heat', 'copper',
                            'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu',
                            'RdYlGn', 'Spectral', 'coolwarm', 'seismic',
                            'flag', 'prism', 'ocean', 'gist_earth', 'terrain',
                            'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap',
                            'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet',
                            'turbo', 'nipy_spectral', 'gist_ncar']

        self.fontsize_titles = 7
        self.fontsize_axislabels = 7
        self.fontsize_ticklabels = 7
        self.line_widths = 1
        self.primary_line_colour = 'blue'
        self.primary_line_style = 'solid'
        self.secondary_line_colour = 'red'
        self.secondary_line_style = 'dashed'
        self.line_styles = ['solid', 'dotted', 'dashed', 'dashdot']
        self.line_colours = ['black', 'gray', 'blue', 'red', 'green', 'white', 'yellow', 'purple', 'orange', 'magenta', 'cyan']

        self.UI()
        self.show()

    def UI(self):
        widgets(self)
        layouts(self)

    def display(self,instrument_object):
        create_tab(self,instrument_object)
        if self.increment == 0:
            self.increment = 1
    def close(self):
        destroy_tab(self)

    def keyPressEvent(self, event): #called when user presses keys
        if event.key() == Qt.Key_Up or event.key() == Qt.Key_N or event.key() == Qt.Key_Return:
            print("key!")
            if self.file_manager_flag is None:
                self.file_manager_flag = FileManager(self)
                self.file_manager_flag.show()
                self.file_manager_flag.setGeometry(0,0,int(0.2*self.appwidth),int(0.6*self.appheight))
            else:
                self.file_manager_flag.close()
                self.file_manager_flag = None


    def get_all_values(self,nested_dictionary, i, match): #searches nested dictionary for datasets that are already loaded
        for key, value in nested_dictionary.items():
            if type(value) is dict:
                i+=1
                self.get_all_values(value, i, match)
            else:
                if value == match:
                    self.flag=True
                    self.match = i-1
                    return

    def get_dataset(self,file_manager):
        url = QFileDialog.getOpenFileName(self,"Select a .fits file","","All Files(*);;*fits")
        value = str(url[0])
        if value not in self.file_list:
            self.file_list.append(value)
            file_manager.select_dataset_combobox.addItem(value)
        else:
            msg = QMessageBox()
            msg.setText("This file has already been selected.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()

    def display_validation(self,file_manager):
        missing_files = []
        if not os.path.exists(str(file_manager.select_dataset_combobox.currentText())):
            missing_files.append(str(file_manager.select_dataset_combobox.currentText()))
        if len(missing_files) > 0:
            msg = QMessageBox()
            missing_message = ""
            for m in range(0,len(missing_files)):
                missing_message+=missing_files[m]+"\n"
            msg.setText("The following files do not exist:\n"+missing_message)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            return False
        return True

    def load_dataset(self,file_manager):
        if self.display_validation(file_manager):
            self.flag = False
            print(self.dataset_dict)
            self.get_all_values(self.dataset_dict,0,file_manager.select_dataset_combobox.currentText())
            if self.flag: #if match is found
                i=str(self.match)
                print("match found",file_manager.select_dataset_combobox.currentText())
                if self.reload_flag:
                    instrument_object = Spectropolarimetric()
                    self.flag = False
                    self.dataset_dict[i] = {'data_file': file_manager.select_dataset_combobox.currentText(),
                                        'binary_file': file_manager.select_binary_combobox.currentText(),
                                        'instrument_object': instrument_object,
                                        'canvas': self.canvas_tabs_list[-1]
                                         }
                # show(self,self.dataset_dict[i])
                # click(self,self.dataset_dict[i])
                # update_pixel_info(self, self.dataset_dict[i])
            elif not self.flag: #match is not found
                j=str(len(self.dataset_dict))
                self.match = j
                instrument_object = Spectropolarimetric()
                self.display(instrument_object)
                self.dataset_dict[j] = {'data_file': file_manager.select_dataset_combobox.currentText(),
                                    'binary_file': file_manager.select_binary_combobox.currentText(),
                                    'instrument_object': instrument_object,
                                    'canvas': self.canvas_tabs_list[-1]
                                     }
                # show(self,self.dataset_dict[j])
                # click(self,self.dataset_dict[j])
                # update_pixel_info(self, self.dataset_dict[j])
                print("no match found",file_manager.select_dataset_combobox.currentText())
        else:
            pass

    def mouseclicks(self, event): #called when user clicks one of the maps
        self.setFocus()
        if event.xdata is not None and event.ydata is not None:
            i=str(self.match)
            self.dataset_dict[i]["instrument_object"].current_x = event.xdata
            self.dataset_dict[i]["instrument_object"].current_y = event.ydata
            if self.click_increment == 0:
                self.click_increment = 1
            # click(self,self.dataset_dict[i])
            # self.change_canvas()
            # update_pixel_info(self, self.dataset_dict[i])
        else:
            msg = QMessageBox()
            msg.setText("You must click one of the maps.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()

class FileManager(QWidget):
    def __init__(self,se):
        super().__init__()
        file_manager_layout_and_widgets(self,se)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SolarExplorer()
    window.show()
    sys.exit(app.exec_())
