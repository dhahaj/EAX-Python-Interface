from qtpy.QtWidgets import QInputDialog
import constants
from settings import get_instance


class ChipSelectDialog(QInputDialog):
    """
    A dialog for selecting a chip part from a predefined list.
    Inherits from QInputDialog and presents a combo box populated with chip options defined in `constants.CHIP_OPTIONS`.
    The currently selected chip is initialized from the application settings using `get_instance()`.
    When accepted, the selected chip is stored and can be retrieved.
    Args:
        parent (QWidget): The parent widget for the dialog.
    Attributes:
        selected_chip (str or None): The chip selected by the user, or None if no selection was made.
    Methods:
        accept():
            Stores the currently selected chip value before closing the dialog.
        get_chip(parent):
            Static method to display the dialog, update the application setting with the selected chip,
            and return the selected chip string. Returns None if the dialog is cancelled.
    """

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setWindowTitle('Select Chip')
        self.setLabelText('Chip:')
        self.setComboBoxItems(constants.CHIP_OPTIONS)
        self.setOption(QInputDialog.UseListViewForComboBoxItems)
        current = get_instance().get(
            constants.KEY_CHIP_PART,
            constants.DEFAULT_SETTINGS[constants.KEY_CHIP_PART],
        )
        self.setTextValue(current)
        self.selected_chip = None

    def accept(self) -> None:
        # grab the textValue just before closing
        self.selected_chip = self.textValue()
        super().accept()

    @staticmethod
    def get_chip(parent) -> str | None:
        dlg = ChipSelectDialog(parent)
        if dlg.exec_() == QInputDialog.Accepted:
            get_instance().setValue(
                constants.KEY_CHIP_PART,
                dlg.selected_chip
            )
            return dlg.selected_chip
        return None
