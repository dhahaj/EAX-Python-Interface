from qtpy.QtWidgets import (
    QMainWindow,
    QShortcut,
    QFileDialog,
    QMessageBox,
    QInputDialog,
    QAction,
)
from ui.ui_Editor import Ui_EditorWindow
from qtpy.QtGui import QKeySequence, QTextCursor, QFont
from qtpy.QtCore import QEvent, Qt, QByteArray
from settings import get_instance as get_settings
from imports import from_string


class Editor(QMainWindow, Ui_EditorWindow):

    _current_document: str = "Untitled"

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Untitled[*]")

        self.settings = get_settings()

        # Restore window geometry/state
        self.restoreGeometry(self.settings.app_settings.value("editor/geometry", QByteArray()))
        self.restoreState(self.settings.app_settings.value("editor/windowState", QByteArray()))

        # Set font if saved
        font_str = self.settings.get("editor/font", "")
        if font_str:
            self.plainTextEdit.setFont(from_string(font_str))

        # --- Recent Documents setup ---
        self.max_recent_files = 5
        self.recent_files = []
        # Assumes UI has a QMenu named menuFile
        self.recentMenu = self.menuFile.addMenu("Recent Documents")
        self.recentMenu.setEnabled(False)
        self.load_recent_files()
        self.update_recent_files_menu()

        # Connect actions
        self.actionNew.triggered.connect(self.new_file)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(self.save_file)
        self.actionSaveAs.triggered.connect(self.save_file_as)
        self.actionSelectAll.triggered.connect(self.plainTextEdit.selectAll)
        self.actionCopy.triggered.connect(self.plainTextEdit.copy)
        self.actionPaste.triggered.connect(self.plainTextEdit.paste)
        self.actionCut.triggered.connect(self.plainTextEdit.cut)
        self.actionUndo.triggered.connect(self.plainTextEdit.undo)
        self.actionRedo.triggered.connect(self.plainTextEdit.redo)
        self.actionClose.triggered.connect(self.closeDocument)
        self.actionFind.triggered.connect(self.search)
        self.actionReplace.triggered.connect(self.replace)
        self.actionRefresh.triggered.connect(self.refresh)

        QShortcut(QKeySequence.ZoomIn,  self, activated=self.zoom_in)
        QShortcut(QKeySequence('Ctrl+='),  self, activated=self.zoom_in)
        QShortcut(QKeySequence.ZoomOut, self, activated=self.zoom_out)
        QShortcut(QKeySequence('Ctrl+0'), self, activated=self.zoom_reset)

        self.plainTextEdit.installEventFilter(self)
        self.plainTextEdit.textChanged.connect(self.text_changed)
        self.plainTextEdit.document().modificationChanged.connect(self.update_window_title)
        self.plainTextEdit.undoAvailable.connect(self._on_undo_available)

        self.actionFont.triggered.connect(self.selectFont)

    def load_recent_files(self):
        files = self.settings.app_settings.value("editor/recent/files", [])
        if not files:
            files = []
        if isinstance(files, str):
            files = [files]
        self.recent_files = files

    def update_recent_files_menu(self):
        self.recentMenu.clear()
        if not self.recent_files:
            self.recentMenu.setEnabled(False)
            return
        self.recentMenu.setEnabled(True)
        for path in self.recent_files:
            action = QAction(path.split('/')[-1], self)
            action.setData(path)
            action.triggered.connect(self.open_recent_file)
            self.recentMenu.addAction(action)
        self.recentMenu.addSeparator()
        clear = QAction("Clear Recent Documents", self)
        clear.triggered.connect(self.clear_recent_files)
        self.recentMenu.addAction(clear)

    def add_to_recent(self, file_path: str):
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        self.recent_files.insert(0, file_path)
        self.recent_files = self.recent_files[:self.max_recent_files]
        self.settings.app_settings.setValue("editor/recent/files", self.recent_files)
        self.update_recent_files_menu()

    def open_recent_file(self):
        action = self.sender()
        path = action.data() if action else None
        if not path or not self._ask_save():
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Cannot open {path}:\n{e}")
            self.recent_files.remove(path)
            self.settings.app_settings.setValue("editor/recent/files", self.recent_files)
            self.update_recent_files_menu()
            return
        self.plainTextEdit.setPlainText(content)
        self._current_document = path
        self.setWindowFilePath(path)
        self.setWindowTitle(f"{path.split('/')[-1]}[*]")
        self.plainTextEdit.document().setModified(False)
        self.setWindowModified(False)
        self.statusBar().showMessage(f"Opened {path.split('/')[-1]}")
        self.add_to_recent(path)

    def clear_recent_files(self):
        self.recent_files = []
        self.settings.qsettings.setValue("editor/recent/files", self.recent_files)
        self.update_recent_files_menu()

    def refresh(self):
        if self.isWindowModified():
            if QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save them before refreshing?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.Cancel,
            ) == QMessageBox.Yes:
                self.save_file()
        if self._current_document and self._current_document != "Untitled":
            position = self.plainTextEdit.textCursor().position()
            print(f"Refreshing {self._current_document} at position {position}")
            with open(self._current_document, "r", encoding="utf-8") as file:
                content = file.read()
                self.plainTextEdit.setPlainText(content)
            cursor = self.plainTextEdit.textCursor()
            # clamp position to document length, just in case
            position = min(position, self.plainTextEdit.document().characterCount() - 1)
            cursor.setPosition(position, QTextCursor.MoveAnchor)
            self.plainTextEdit.setTextCursor(cursor)
            self.plainTextEdit.ensureCursorVisible()
            self.plainTextEdit.document().setModified(False)
            self.setWindowModified(False)
            self.statusBar().showMessage(f"Refreshed {self._current_document.split('/')[-1]}")

    def eventFilter(self, obj, event):
        # Catch only wheel‐events on the text-edit with Ctrl held
        if obj is self.plainTextEdit and event.type() == QEvent.Type.Wheel:
            if event.modifiers() & Qt.ControlModifier:
                if event.angleDelta().y() > 0:
                    self.zoom_in()
                else:
                    self.zoom_out()
                return True
        return super().eventFilter(obj, event)

    def zoom_in(self):
        font = self.plainTextEdit.font()
        font.setPointSize(font.pointSize() + 1)
        self.plainTextEdit.setFont(font)

    def zoom_out(self):
        font = self.plainTextEdit.font()
        size = max(font.pointSize() - 1, 1)
        font.setPointSize(size)
        self.plainTextEdit.setFont(font)

    def zoom_reset(self):
        # pick your default size here
        font = self.plainTextEdit.font()
        font.setPointSize(12)
        self.plainTextEdit.setFont(font)

    def selectFont(self):
        """
        Open a font dialog to select a font for the text edit area.
        """
        from qtpy.QtWidgets import QFontDialog
        ok, font = QFontDialog.getFont(self.plainTextEdit.font(), self, "Select Font")
        if ok:
            self.plainTextEdit.setFont(font)
            self.plainTextEdit.setFocus()
            self.settings.setValue("editor/font", font.toString())

    def _on_undo_available(self, can_undo):
        if not can_undo:
            # undo stack empty ⇒ we’re back at the “clean” point
            self.plainTextEdit.document().setModified(False)
            self.setWindowModified(False)

    def set_current_file(self, file_name):
        """
        Set the current file name and update the window title.
        """
        self._current_document = file_name
        if file_name:
            self.setWindowFilePath(file_name)
            self.setWindowTitle(f"{self.windowFilePath().split('/')[-1]}[*]")
            self.statusBar().showMessage(f"Opened {file_name.split('/')[-1]}")
            with open(file_name, "r") as file:
                content = file.read()
                self.plainTextEdit.setPlainText(content)
        else:
            self.setWindowTitle("Untitled[*]")
            self.statusBar().clearMessage()
            self.setWindowFilePath("")

        self.setWindowModified(False)
        self.setWindowFilePath(file_name)

    def text_changed(self):
        """
        Set the flag to indicate that the text has changed.
        """
        self.statusBar().showMessage("Unsaved changes")
        self.setWindowModified(True)
        if self.isWindowModified():
            self.update_window_title()

    def update_window_title(self):
        """
        Update the window title based on the current file name and modification status.
        """
        if self.windowFilePath() == "":
            self.setWindowTitle("Untitled[*]")
        else:
            self.setWindowTitle(f"{self.windowFilePath().split('/')[-1]}[*]")
        if not self.plainTextEdit.document().isModified():
            self.statusBar().clearMessage()
            # self.setWindowTitle(f"{self.windowFilePath().split('/')[-1]}[*]")

    def new_file(self):
        if not self._ask_save():
            return
        self.plainTextEdit.clear()
        self.setWindowModified(False)
        self.setWindowFilePath("")
        self.statusBar().clearMessage()
        self._current_document = "Untitled"
        self.setWindowTitle(f"Untitled{self.windowFilePath().split('/')[-1]}[*]")

    def open_file(self):
        if not self._ask_save():
            return
        fname, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if fname:
            with open(fname, 'r', encoding='utf-8') as f:
                self.plainTextEdit.setPlainText(f.read())
            self._current_document = fname
            self.setWindowFilePath(fname)
            self.setWindowTitle(f"{fname.split('/')[-1]}[*]")
            self.plainTextEdit.document().setModified(False)
            self.setWindowModified(False)
            self.statusBar().showMessage(f"Opened {fname.split('/')[-1]}")
            self.add_to_recent(fname)

    def save_file_as(self):
        fname, _ = QFileDialog.getSaveFileName(self, "Save File As", self._current_document, "All Files (*)")
        if not fname:
            return
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(self.plainTextEdit.toPlainText())
        self._current_document = fname
        self.setWindowFilePath(fname)
        self.setWindowTitle(f"{fname.split('/')[-1]}[*]")
        self.plainTextEdit.document().setModified(False)
        self.setWindowModified(False)
        self.statusBar().showMessage(f"Saved {fname.split('/')[-1]}")
        self.add_to_recent(fname)

    def save_file(self):
        if not self._current_document or self._current_document == "Untitled":
            self.save_file_as()
            return
        file_name = self._current_document
        if file_name:
            with open(file_name, "w") as file:
                content = self.plainTextEdit.toPlainText()
                file.write(content)
            self.plainTextEdit.document().clearUndoRedoStacks()
            self.plainTextEdit.document().setModified(False)
            self.setWindowModified(False)
            self.setWindowFilePath(file_name)
            self.setWindowTitle(f"{self.windowFilePath().split('/')[-1]}[*]")
            self.statusBar().showMessage(f"{self.windowFilePath().split('/')[-1]}")

    def closeEvent(self, event):
        if not self._ask_save():
            event.ignore()
        else:
            event.accept()
        # Save the window geometry and state
        self.settings.app_settings.setValue("editor/geometry", self.saveGeometry())
        self.settings.app_settings.setValue("editor/windowState", self.saveState())

    def closeDocument(self):
        if not self._ask_save():
            return
        self.plainTextEdit.clear()
        self._current_document = "Untitled"
        self.setWindowTitle("Untitled[*]")
        self.setWindowModified(False)
        self.setWindowFilePath("")
        self.statusBar().clearMessage()

    def _ask_save(self):
        """
        Ask the user if they want to save changes before closing the editor.
        """
        if self.plainTextEdit.document().isModified():
            reply = QMessageBox.question(
                self,
                "Message",
                "You have unsaved changes. Do you want to save them?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.Cancel,
            )
            if reply == QMessageBox.Yes:
                self.save_file()
            elif reply == QMessageBox.Cancel:
                return False
        return True

    def search(self):
        """
        Open a search dialog to find text in the editor.
        """
        search_term, ok = QInputDialog.getText(self, "Search", "Enter text to search:", text=self._previous_search_term if hasattr(self, "_previous_search_term") else "")
        if ok and search_term:
            self._previous_search_term = search_term
            cursor = self.plainTextEdit.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.NoMove, QTextCursor.MoveMode.MoveAnchor)
            cursor = self.plainTextEdit.document().find(search_term, cursor)
            if cursor.isNull():
                QMessageBox.information(self, "Search", f"'{search_term}' not found.")
            else:
                self.plainTextEdit.setTextCursor(cursor)
                self.plainTextEdit.ensureCursorVisible()
                self.plainTextEdit.setFocus()

    def replace(self):
        """
        Open a replace‐dialog: ask for “find” and “replace” strings,
        then replace all occurrences in the document.
        """
        find_str, ok = QInputDialog.getText(
            self, "Replace", "Find:", text=getattr(self, "_previous_search_term", "")
        )
        if not ok or not find_str:
            return

        replace_str, ok = QInputDialog.getText(
            self, "Replace", f"Replace '{find_str}' with:"
        )
        if not ok:
            return

        # remember last search for convenience
        self._previous_search_term = find_str

        doc = self.plainTextEdit.document()
        # start from top
        cursor = QTextCursor(doc)
        replaced = 0

        cursor.beginEditBlock()
        while True:
            cursor = doc.find(find_str, cursor)
            if cursor.isNull():
                break
            cursor.insertText(replace_str)
            replaced += 1
        cursor.endEditBlock()

        QMessageBox.information(
            self,
            "Replace",
            f"Replaced {replaced} occurrence{'s' if replaced != 1 else ''} of '{find_str}'."
        )

        self.setWindowModified(True)


if __name__ == "__main__":
    import sys
    from qtpy.QtWidgets import QApplication

    app = QApplication(sys.argv)
    editor = Editor()
    editor.set_current_file('config.yaml')  # Set a default file to open
    editor.show()
    sys.exit(app.exec_())
