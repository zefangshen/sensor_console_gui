import time
from PyQt6.QtWidgets import (
    QMainWindow, QGridLayout, QLabel, QLineEdit, QToolBar, QTextEdit,
    QStatusBar, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTabWidget,
    QComboBox, QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem,
    QFrame
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize
import pyqtgraph as pg
import numpy as np
import pandas as pd
from ipdb import set_trace

class MainWindow(QMainWindow):
    """main window of the application
    """

    def __init__(self):
        '''Initialise elements
        '''

        super().__init__()

        # self.resize(400, 300)
        # doest not show on mac
        self.setWindowIcon(QIcon('./resources/images/spectra.png'))
        self.setWindowTitle("SpeX")
        # self.setGeometry(100, 100, 500, 300)
        self.setContentsMargins(0, 0, 0, 0)
        # self.resize(600, 450)
        self.setMinimumSize(600, 450)

        # menu bar
        # menubar = self.menuBar()
        # file_menu = menubar.addMenu('&File')

        # add statusbar
        self.setStatusBar(QStatusBar(self))

        # access the statusbar
        self.status_bar = self.statusBar() 
        self.message = 'Welcome to SpeX'
        self.status_bar.showMessage(self.message)

        # create central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_layout = QVBoxLayout()
        central_widget.setLayout(central_layout)
        central_layout.setContentsMargins(0, 2, 0, 0)
        central_layout.setSpacing(0)

        # add tabs
        self.tab_layout = QHBoxLayout()
        self.tab_layout.setContentsMargins(0, 0, 0, 0)
        self.tab_layout.setSpacing(0)

        # tabs
        self.device_tab_btn = QPushButton('Device')
        self.device_tab_btn.setProperty('class', 'tab-button')
        self.device_tab_btn.clicked.connect(self.on_device_tab_clicked)
        self.device_tab_btn.setEnabled(False)  # disabled on landing

        self.data_tab_btn = QPushButton('Data')
        self.data_tab_btn.setProperty('class', 'tab-button')
        self.data_tab_btn.clicked.connect(self.on_data_tab_clicked)

        # self.process_tab_btn = QPushButton('Preprocess')
        # self.process_tab_btn.clicked.connect(self.on_process_tab_clicked)

        self.tab_layout.addWidget(self.device_tab_btn)
        self.tab_layout.addWidget(self.data_tab_btn)
        # self.tab_layout.addWidget(self.process_tab_btn)
        self.tab_layout.addStretch()

        central_layout.addLayout(self.tab_layout)

        # tool section
        tool_widget = QWidget()  # need to be widget to set dimensions
        self.tool_layout = QHBoxLayout()
        self.tool_layout.setContentsMargins(5, 0, 0, 0)
        self.tool_layout.setSpacing(5)
        tool_widget.setLayout(self.tool_layout)
        tool_widget.setFixedHeight(70)
        self.connection_status = False  # initial connection status
        self.devices = ['NeoSpectra', 'trinamiX', 'NIRONE', 'STS-Vis']
        self.selected_device = self.devices[0]
        self.project_name = ''

        # separation line
        hline = QFrame()
        hline.setFrameShape(QFrame.Shape.HLine)
        hline.setStyleSheet('color: lightgrey;')

        # data visualisation
        self.display_layout = QHBoxLayout()
        self.display_layout.setContentsMargins(5, 0, 5, 0)

        list_widget = QListWidget()
        # items = ['p_1', 'p_2', 'p_3']
        items = []
        for item in items:
            list_item = QListWidgetItem(item)
            list_item.setFlags(list_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)  # Make item checkable
            list_item.setCheckState(Qt.CheckState.Unchecked)  # Set initial state to unchecked
            list_widget.addItem(list_item)

        self.display_layout.addWidget(list_widget, 1)

        self.on_device_tab_clicked()
        self._display_default()

        # the whole page
        central_layout.addLayout(self.tab_layout)
        central_layout.addWidget(tool_widget)
        central_layout.addWidget(hline)
        central_layout.addLayout(self.display_layout)

    def update_status(self):
        self.status_bar.showMessage(self.message)
    
    def on_device_tab_clicked(self):
        '''device tab
        '''

        # button control
        self.device_tab_btn.setEnabled(False)
        self.data_tab_btn.setEnabled(True)
        # self.process_tab_btn.setEnabled(True)

        # tool section
        self._clear_tool_section()
        # elements
        if self.connection_status:
            self.connect_btn = QPushButton('Disconnect')
        else:
            self.connect_btn = QPushButton('Connect')
        self.connect_btn.setProperty('class', 'action-button')
        # self.connect_btn.setFixedHeight(self.connect_btn.sizeHint().height() * 2)
        # self.connect_btn.setFixedWidth(85)
        self.connect_btn.clicked.connect(self.on_connect_btn_clicked)
        self.tool_layout.addWidget(self.connect_btn)

        vline = QFrame()
        vline.setFrameShape(QFrame.Shape.VLine)
        vline.setStyleSheet('color: lightgrey;')
        self.tool_layout.addWidget(vline)

        right_layout = QVBoxLayout()
        self.tool_layout.addLayout(right_layout)

        topright_layout = QHBoxLayout()
        topright_layout.setContentsMargins(0,0,0,0)
        botright_layout = QHBoxLayout()
        botright_layout.setContentsMargins(0,0,0,0)
        right_layout.addLayout(topright_layout)
        right_layout.addLayout(botright_layout)

        device_label = QLabel('Device')
        self.device_options = QComboBox()
        self.device_options.addItems(self.devices)
        self.device_options.setCurrentText(self.selected_device)
        self.device_options.currentIndexChanged.connect(self.on_device_option_changed)
        topright_layout.addWidget(device_label)
        topright_layout.addWidget(self.device_options, alignment=Qt.AlignmentFlag.AlignLeft)
        topright_layout.addStretch()
        
        status_label = QLabel('Status')
        if self.connection_status:
            self.device_status_text = QLabel('Connected')
        else:
            self.device_status_text = QLabel('Disconnected')
        botright_layout.addWidget(status_label)
        botright_layout.addWidget(self.device_status_text)
        botright_layout.addStretch()

        self.tool_layout.addStretch()

        # display section do not update
        # self._display_default()

    def on_data_tab_clicked(self):
        # tab buttons control
        self.device_tab_btn.setEnabled(True)
        self.data_tab_btn.setEnabled(False)
        # self.process_tab_btn.setEnabled(True)

        # clear current layout
        self._clear_tool_section()

        # project layout
        project_layout = QVBoxLayout()
        project_label = QLabel('New project name')
        self.project_input = QLineEdit()
        self.project_input.setText(self.project_name)
        # project_input.setFixedWidth(int(project_input.sizeHint().width() * 1.0))
        self.project_input.setFixedWidth(150)
        project_layout.addWidget(project_label)
        project_layout.addWidget(self.project_input)

        self.tool_layout.addLayout(project_layout)

        vline1 = QFrame()
        vline1.setFrameShape(QFrame.Shape.VLine)
        vline1.setStyleSheet('color: lightgrey;')
        self.tool_layout.addWidget(vline1)

        # settings layout
        settings_main_layout = QVBoxLayout()
        self.tool_layout.addLayout(settings_main_layout)

        settings_cali_layout = QHBoxLayout()
        settings_main_layout.addLayout(settings_cali_layout)

        cali_freq_label = QLabel('Calibrate freq.')
        cali_options = QComboBox()
        cali_options.addItems(['3', '5', '10', '15'])
        cali_options.currentIndexChanged.connect(self.on_cali_freq_combobox_changed)

        settings_cali_layout.addWidget(cali_freq_label)
        settings_cali_layout.addWidget(cali_options)

        settings_dur_layout = QHBoxLayout()
        settings_main_layout.addLayout(settings_dur_layout)

        dur_label = QLabel('Seconds/scan')
        dur_options = QComboBox()
        dur_options.addItems(['5', '10', '20', '30', '60'])
        dur_options.currentIndexChanged.connect(self.on_dur_combobox_changed)
        settings_dur_layout.addWidget(dur_label)
        settings_dur_layout.addWidget(dur_options)

        # separation line 
        vline2 = QFrame()
        vline2.setFrameShape(QFrame.Shape.VLine)
        vline2.setStyleSheet('color: lightgrey;')
        self.tool_layout.addWidget(vline2)

        # scan button
        scan_btn = QPushButton('Scan')
        scan_btn.setEnabled(True) if self.connection_status else scan_btn.setEnabled(False)
        # scan_btn.setFixedHeight(scan_btn.sizeHint().height() * 2)
        # scan_btn.setFixedWidth(int(scan_btn.sizeHint().width() * 1.5))
        scan_btn.setProperty('class', 'action-button')
        scan_btn.clicked.connect(self.on_scan_btn_clicked)
        self.tool_layout.addWidget(scan_btn)

        self.tool_layout.addStretch()

        # self._display_default()

    def on_process_tab_clicked(self):

        # button control
        self.device_tab_btn.setEnabled(True)
        self.data_tab_btn.setEnabled(True)
        self.process_tab_btn.setEnabled(False)

        # clear current layout
        # self.tool_widget.resize(250, 50)
        self._clear_tool_section()

        # redraw
        method_layout = QVBoxLayout()
        self.tool_layout.addLayout(method_layout)

        # set preprocessing methods
        method_label = QLabel('Prep. method')
        method_options = QComboBox()
        method_options.addItems(['SNV', 'Abs.'])
        method_options.currentIndexChanged.connect(self.on_prep_combobox_changed)

        method_layout.addWidget(method_label)
        method_layout.addWidget(method_options)

        # separation line
        vline = QFrame()
        vline.setFrameShape(QFrame.Shape.VLine)
        vline.setStyleSheet('color: lightgrey;')
        self.tool_layout.addWidget(vline)

        # run button
        # run_btn = QPushButton('Run')
        run_btn = QPushButton('Run')
        run_btn.setFixedHeight(run_btn.sizeHint().height() * 2)
        run_btn.setFixedWidth(int(run_btn.sizeHint().width() * 1.5))
        self.tool_layout.addWidget(run_btn)

        self.tool_layout.addStretch()

        # update display
        self._clear_display_section(partial=True)

        # plot layout
        plot_layout = QVBoxLayout()
        # add first plot
        plot1_widget = pg.PlotWidget()
        plot_layout.addWidget(plot1_widget)
        # x = np.linspace(0, 4*np.pi)
        # y = np.sin(x)
        plot1_widget.plot([], []) # a blank plot

        # add second plot
        plot2_widget = pg.PlotWidget()
        plot_layout.addWidget(plot2_widget)
        # x = np.linspace(0, 4*np.pi)
        # y = np.sin(x)
        plot2_widget.plot([], []) # a blank plot

        self.display_layout.addLayout(plot_layout, 4)

    def on_connect_btn_clicked(self):
        # connection status

        # disable the button first
        self.connect_btn.setEnabled(False)

        if not self.connection_status:
            # not yet connected

            # sleep
            time.sleep(1)

            # set status
            self.device_status_text.setText('Connected')

            # set status bar message.
            self.status_bar.showMessage(f'Connected to {self.selected_device}')

            # update Button text
            self.connect_btn.setText('Disconnect')

        else: 
            # disconnected

            # sleep
            time.sleep(1)

            # set status
            self.device_status_text.setText('Disconnected')

            # set status bar message.
            self.status_bar.showMessage(f'Disconnected {self.selected_device}')

            # update Button text
            self.connect_btn.setText('Connect')

        # update connection status
        self.connection_status = not self.connection_status

        # enable the button again
        self.connect_btn.setEnabled(True)

    def _display_default(self):
        
        # clear 
        self._clear_display_section(partial=True)

        # add a plot
        plot_widget = pg.PlotWidget()
        self.display_layout.addWidget(plot_widget, 3)
        # x = np.linspace(0, 4*np.pi)
        # y = np.sin(x)
        plot_widget.plot([], []) # a blank plot

        # add a table
        table_widget = QTableWidget()
        table_widget.setRowCount(20)  # Set number of rows
        table_widget.setColumnCount(2)  # Set number of columns
        table_widget.setHorizontalHeaderLabels(["Wavelength", "Intensity"])

        # self.table_data = [
        #     ("Alice", 30),
        #     ("Bob", 25),
        #     ("Charlie", 35),
        #     ("David", 40)
        # ]
        self.table_data = []  # empty table 

        for row_index, row_data in enumerate(self.table_data):
            for column_index, item in enumerate(row_data):
                table_item = QTableWidgetItem(str(item))
                table_widget.setItem(row_index, column_index, table_item)

        self.display_layout.addWidget(table_widget, 1)

    def on_scan_btn_clicked(self):
        # get project name
        self.project_name = self.project_input.text()
        # print(self.project_input.text())

        # read data
        self.df = pd.read_csv('./resources/data/spectra.csv')
        self.df.index = [self.project_input.text() + '_' + str(i) for i in self.df.index] 

        # clear the view
        self._clear_display_section(partial=False)

        # populate list
        self.list_widget = QListWidget()
        items = self.df.index.to_list()
        for i, item in enumerate(items):
            list_item = QListWidgetItem(item)
            list_item.setFlags(list_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)  # Make item checkable
            # if i == 0:
            #     list_item.setCheckState(Qt.CheckState.Checked)  # Set initial state to unchecked
            # else:
            list_item.setCheckState(Qt.CheckState.Unchecked)  # Set initial state to unchecked
            self.list_widget.addItem(list_item)

        # handle item changed
        self.list_widget.itemChanged.connect(self.on_data_item_changed)
        self.display_layout.addWidget(self.list_widget, 1)

        # plot spectra
        self.plot_widget = pg.PlotWidget()
        self.line_plots = {}  # managing checked plots
        self.plot_item = self.plot_widget.getPlotItem()  # for managing checked plots
        self.display_layout.addWidget(self.plot_widget, 3)
        x = self.df.columns.astype(float).to_list()
        for indx in self.df.index:
            y = self.df.loc[indx, :].to_list()
            # add a plot
            # self.plot_widget.plot(x, y.to_list(), pen='lightgrey') # a blank plot
            plt = self.plot_item.plot(x, y, pen='grey') # a blank plot
            self.line_plots[indx] = plt

        # empty table
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(20)  # Set number of rows
        self.table_widget.setColumnCount(2)  # Set number of columns
        self.table_widget.setHorizontalHeaderLabels(["Wavelength", "Intensity"])

        # show the first checked sample
        table_data = [
            # (x, round(y, 3)) for x, y in zip(df.columns, df.iloc[0, :])
        ]  # empty table 

        for row_index, row_data in enumerate(table_data):
            for column_index, item in enumerate(row_data):
                table_item = QTableWidgetItem(str(item))
                self.table_widget.setItem(row_index, column_index, table_item)

        self.display_layout.addWidget(self.table_widget, 1)

    def _clear_display_section(self, partial=True):
        if partial is True:
            while self.display_layout.count() > 1:
                item = self.display_layout.takeAt(1)
                widget = item.widget()
                if widget:
                    # widget.setParent(None)
                    widget.deleteLater()
                elif item.layout():
                    self._remove_layout(item.layout())
        else:
            while self.display_layout.count() > 0:
                item = self.display_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    # widget.setParent(None)
                    widget.deleteLater()
                elif item.layout():
                    self._remove_layout(item.layout())

    def _clear_tool_section(self):
        # another option
        while self.tool_layout.count() > 0:
            item = self.tool_layout.takeAt(0)
            widget = item.widget()
            if widget:
                # widget.setParent(None)
                widget.deleteLater()
            elif item.layout():
                self._remove_layout(item.layout())
    
    def _remove_layout(self, layout):
        '''recursively remove layouts and widgets
        '''
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
            elif item.layout():
                self._remove_layout(item.layout())
        layout.deleteLater()

    def on_device_option_changed(self, index):
        self.selected_device = self.sender().itemText(index)
        # print(f"Selected item: {selected_item}")
    
    def on_data_item_changed(self, item):
        indx = item.text()

        # update plot
        self.plot_item.removeItem(self.line_plots[indx])
        x = self.df.columns.astype(float).to_list()
        if item.checkState() == Qt.CheckState.Checked:
            # replot with a different colour
            plt = self.plot_item.plot(
                x, self.df.loc[indx, :].to_list(), pen='blue'
            )
        else:
            # remove a plot 
            plt = self.plot_item.plot(
                x, self.df.loc[indx, :].to_list(), pen='grey'
            )
        
        self.line_plots[indx] = plt

        # update table
        # display the first checked item 
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)

            # get the first one
            if item.checkState() == Qt.CheckState.Checked:
                self.table_widget.clearContents()
                self.table_widget.setRowCount(len(x))
                spec = self.df.loc[item.text(),]
                table_data = [(col1, round(col2,3)) for col1, col2 in zip(x, spec)]

                # populate the table
                for row_index, row_data in enumerate(table_data):
                    for column_index, item in enumerate(row_data):
                        table_item = QTableWidgetItem(str(item))
                        self.table_widget.setItem(
                            row_index, column_index, table_item
                        )

    def on_cali_freq_combobox_changed(self, index):
        selected_item = self.sender().itemText(index)
        print(f"Selected item: {selected_item}")

    def on_dur_combobox_changed(self, index):
        selected_item = self.sender().itemText(index)
        print(f"Selected item: {selected_item}")
    
    def on_prep_combobox_changed(self, index):
        selected_item = self.sender().itemText(index)

