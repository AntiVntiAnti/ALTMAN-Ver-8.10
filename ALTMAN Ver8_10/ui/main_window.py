import datetime
from PyQt6 import QtWidgets
from PyQt6.QtCore import QDate, QSettings, QTime, Qt, QByteArray, QDateTime, QAbstractTableModel
from PyQt6.QtGui import QCloseEvent
from typing import Any, Optional
import tracker_config as tkc
from ui.main_ui.gui import Ui_MainWindow
from logger_setup import logger
from navigation.master_navigation import change_stack_page
from utility.app_operations.show_hide import toggle_views
from database.altman_add_data import add_altmans_data

# ////////////////////////////////////////////////////////////////////////////////////////
# UI
# ////////////////////////////////////////////////////////////////////////////////////////

# ////////////////////////////////////////////////////////////////////////////////////////
# LOGGER
# ////////////////////////////////////////////////////////////////////////////////////////

# ////////////////////////////////////////////////////////////////////////////////////////
# NAVIGATION
# ////////////////////////////////////////////////////////////////////////////////////////

# Window geometry and frame
from utility.app_operations.frameless_window import (
    FramelessWindow)
from utility.app_operations.window_controls import (
    WindowController)

# Database connections
from database.database_manager import (
    DataManager)

# Delete Records
from database.database_utility.delete_records import (
    delete_selected_rows)

# setup Models
from database.database_utility.model_setup import (
    create_and_set_model)
# ////////////////////////////////////////////////////////////////////////////////////////
# ADD DATA MODULES
# ////////////////////////////////////////////////////////////////////////////////////////


class MainWindow(FramelessWindow, QtWidgets.QMainWindow, Ui_MainWindow):
    """
    The main window of the application.

    This class represents the main window of the application. It inherits from `FramelessWindow`,
    `QtWidgets.QMainWindow`, and `Ui_MainWindow`. It provides methods for handling various actions
    and events related to the main window.

    Attributes:
        becks_model (Optional[QAbstractTableModel]): The model for the mental mental table.
        ui (Ui_MainWindow): The user interface object for the main window.

    """
    
    def __init__(self,
                 *args: Any,
                 **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.altmans_model = None
        self.becks_model: Optional[QAbstractTableModel] = None
        self.ui: Ui_MainWindow = Ui_MainWindow()
        self.setupUi(self)
        # Database init
        self.db_manager: DataManager = DataManager()
        self.setup_models()
        # QSettings settings_manager setup
        self.settings: QSettings = QSettings(tkc.ORGANIZATION_NAME, tkc.APPLICATION_NAME)
        self.window_controller: WindowController = WindowController()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.app_operations()
        self.restore_state()
        # self.slider_set_spinbox()
        self.stack_navigation()
        self.delete_group()
        self.update_altmans_summary()
        self.altman_table_commit()
        self.forward_backward_btn_set()

    def next_page(self):
        """
        Switches to the next page in the AltmanQuestionStack.

        This method increments the current index of the AltmanQuestionStack by 1 and sets the current index to the next page.
        If the current index is at the last page, it wraps around to the first page.

        Parameters:
        - None

        Returns:
        - None
        """
        try:
            current_index = self.altmanQuestionStack.currentIndex()
            next_index = (current_index + 1) % self.altmanQuestionStack.count()
            self.altmanQuestionStack.setCurrentIndex(next_index)
        except Exception as e:
            logger.error(f"Error in next_page: {e}")
            
    def prev_page(self):
        """
        Go to the previous page in the Altman question stack.

        Raises:
            Exception: If an error occurs while navigating to the previous page.
        """
        try:
            current_index = self.altmanQuestionStack.currentIndex()
            prev_index = (current_index - 1) % self.altmanQuestionStack.count()
            self.altmanQuestionStack.setCurrentIndex(prev_index)
        except Exception as e:
            logger.error(f"Error in prev_page: {e}")
    
    def go_home(self):
        """
        Go to the home page of the application.

        This method sets the current index of the `altmanQuestionStack` to 0, effectively navigating to the home page.

        Raises:
            Exception: If an error occurs while setting the current index.

        """
        try:
            self.altmanQuestionStack.setCurrentIndex(0)
        except Exception as e:
            logger.error(f"Error in go_home: {e}")
            
    def see_measure(self):
        try:
            self.altmanQuestionStack.setCurrentIndex(5)
        except Exception as e:
            logger.error(f"Error in see_measure: {e}")
            
    # ////////////////////////////////////////////////////////////////////////////////////////
    # APP-OPERATIONS setup
    # ////////////////////////////////////////////////////////////////////////////////////////
    def app_operations(self) -> None:
        """
        Performs the necessary operations for setting up the application.

        This method connects signals and slots, sets the initial state of the UI elements,
        and handles various actions triggered by the user.

        Raises:
            Exception: If an error occurs while setting up the app_operations.

        """
        try:
            
            # app switch pages
            self.actionShowAltmanExam.triggered.connect(self.switchone)
            self.actionShowAltmanTable.triggered.connect(self.switchtwo)
            # auto date time
            self.altman_time.setTime(QTime.currentTime())
            self.altman_date.setDate(QDate.currentDate())
            # nav actions
        except Exception as e:
            logger.error(f"Error occurred while setting up app_operations : {e}", exc_info=True)
    
    def forward_backward_btn_set(self):
        """
        Sets up the connections for the forward and backward buttons.

        This method connects the `triggered` signals of the `actionNext`, `actionPrev`,
        `actionHome`, and `actionMeasureView` actions to their respective slots:
        - `next_page`
        - `prev_page`
        - `go_home`
        - `see_measure`

        If any error occurs during the setup, an error message is logged.

        Raises:
            Exception: If an error occurs during the setup.

        """
        try:
            self.actionNext.triggered.connect(self.next_page)
            self.actionPrev.triggered.connect(self.prev_page)
            self.actionHome.triggered.connect(self.go_home)
            self.actionMeasureView.triggered.connect(self.see_measure)
        except Exception as e:
            logger.error(f"Error occurred while setting up forward_backward_btn_set : {e}", exc_info=True)
        
    def switchone(self) -> None:


        """
        Switches the current widget to the 'onepage' widget and resizes the main window.

        Parameters:
            None

        Returns:
            None
        """
        try:
            self.mainStack.setCurrentWidget(self.mainStack)
            self.setFixedSize(475, 170)
        except Exception as e:
            logger.error(f"error switching to question stack {e}", exc_info=True)
            
    def switchtwo(self) -> None:
        """
        Switches the current widget to the 'twopage' widget and resizes the main window to a fixed size of 800x460.
        """
        try:
            self.mainStack.setCurrentWidget(self.mainStack)
            self.setFixedSize(900, 460)
        except Exception as e:
            logger.error(f"{e}", exc_info=True)
    
    def stack_navigation(self) -> None:
        """
        Connects the triggered signals of certain actions to change the stack pages.

        The method creates a dictionary `change_stack_pages` that maps actions to their corresponding page index.
        It then iterates over the dictionary and connects the `triggered` signal of each action to a lambda function
        that calls the `change_stack_page` method with the corresponding page index.

        Raises:
            Exception: If an error occurs during the connection of signals.

        """
        try:
            change_stack_pages = {
                self.actionShowAltmanExam: 0,
                self.actionShowAltmanTable: 1,
            }
            
            for action, page in change_stack_pages.items():
                action.triggered.connect(lambda _, p=page: change_stack_page(self.mainStack, p))
        
        except Exception as e:
            logger.error(f"An error has occurred: {e}", exc_info=True)
    
    def altman_table_commit(self) -> None:
        """
        Connects the 'commit' action to the 'add_mentalsolo_data' function and inserts data into the altman_table.

        This method connects the 'commit' action to the 'add_mentalsolo_data' function, which inserts data into the altman_table.
        The data to be inserted is obtained from various widgets in the UI and passed as arguments to the 'add_altmans_data' function.
        The 'add_altmans_data' function is called with the appropriate arguments and the 'insert_into_altman_table' method of the 'db_manager' object.

        Raises:
            Exception: If an error occurs during the process.
        """
        try:
            self.actionCommit.triggered.connect(
                lambda: add_altmans_data(
                    self, {
                        "altman_date": "altman_date",
                        "altman_time": "altman_time",
                        "altman_question": "altman_question",
                        "altman_question_2": "altman_question_2",
                        "altman_question_3": "altman_question_3",
                        "altman_question_4": "altman_question_4",
                        "altman_question_5": "altman_question_5",
                        "altmans_summary": "altmans_summary",
                        "model": "altmans_model"
                    },
                    self.db_manager.insert_into_altman_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
        
        self.altmans_summary.setEnabled(False)
        for slider in [
            self.altman_question, self.altman_question_2, self.altman_question_3, self.
                altman_question_4, self.altman_question_5, ]:
            slider.setRange(0, 4)
        
        self.altman_question.valueChanged.connect(self.update_altmans_summary)
        self.altman_question_2.valueChanged.connect(self.update_altmans_summary)
        self.altman_question_3.valueChanged.connect(self.update_altmans_summary)
        self.altman_question_4.valueChanged.connect(self.update_altmans_summary)
        self.altman_question_5.valueChanged.connect(self.update_altmans_summary)
    
    def update_altmans_summary(self) -> None:
        """
        Updates the averages of the sliders in the wellbeing and pain module such that
        the overall is the average of the whole.

        :return: None
        """
        try:
            values = [slider.value() for slider in
                      [self.altman_question, self.altman_question_2, self.altman_question_3, self.altman_question_4,
                       self.altman_question_5] if slider.value() > 0]

            altmans_sum = sum(values)

            self.altmans_summary.setValue(int(altmans_sum))

        except Exception as e:
            logger.error(f"{e}", exc_info=True)
            
    def delete_group(self) -> None:
        """
        Connects the delete action to the delete_selected_rows function.

        This method connects the delete action to the delete_selected_rows function,
        passing the necessary arguments to delete the selected rows in the altman_table.

        Args:
            self: The instance of the main window.

        Returns:
            None
        """
        self.actionDelete.triggered.connect(
            lambda: delete_selected_rows(
                self,
                'altmans_table',
                'altmans_model'
            )
        )
        
    def setup_models(self) -> None:
        """
        Set up the models for the main window.

        This method creates and sets the becks_model using the altman_table.

        Returns:
            None
        """
        self.altmans_model = create_and_set_model(
            "altman_refined_table",
            self.altmans_table
        )
        
    def save_state(self) -> None:
            """
            Saves the window geometry state and window state.

            This method saves the current geometry and state of the window
            using the QSettings object. It saves the window geometry state
            and the window state separately.

            Raises:
                Exception: If there is an error saving the window geometry state
                           or the window state.

            """
            try:
                self.settings.setValue("geometry", self.saveGeometry())
            except Exception as e:
                logger.error(f"Error saving the minds_module geo{e}", exc_info=True)
            try:
                self.settings.setValue("windowState", self.saveState())
            except Exception as e:
                logger.error(f"Error saving the minds_module geo{e}", exc_info=True)
    
    def restore_state(self) -> None:
        """
        Restores the window geometry and state.

        This method restores the previous geometry and state of the window
        by retrieving the values from the settings. If an error occurs during
        the restoration process, an error message is logged.

        Raises:
            Exception: If an error occurs while restoring the window geometry or state.
        """
        try:
            # restore window geometry state
            self.restoreGeometry(self.settings.value("geometry", QByteArray()))
        except Exception as e:
            logger.error(f"Error restoring the minds module : stress state {e}")
        
        try:
            self.restoreState(self.settings.value("windowState", QByteArray()))
        except Exception as e:
            logger.error(f"Error restoring WINDOW STATE {e}", exc_info=True)
    
    def closeEvent(self, event: QCloseEvent) -> None:
            """
            Event handler for the close event of the window.

            Saves the state before closing the window.

            Args:
                event (QCloseEvent): The close event object.

            Returns:
                None
            """
            try:
                self.save_state()
            except Exception as e:
                logger.error(f"error saving state during closure: {e}", exc_info=True)
