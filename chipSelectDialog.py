from qtpy.QtWidgets import QInputDialog
import constants
from settings import get_instance


class ChipSelectDialog(QInputDialog):
    def __init__(self, parent):
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

    def accept(self):
        # grab the textValue just before closing
        self.selected_chip = self.textValue()
        super().accept()

    @staticmethod
    def get_chip(parent):
        dlg = ChipSelectDialog(parent)
        if dlg.exec_() == QInputDialog.Accepted:
            get_instance().setValue(
                constants.KEY_CHIP_PART,
                dlg.selected_chip
            )
            return dlg.selected_chip
        return None
