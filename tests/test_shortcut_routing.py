import sys
from pathlib import Path

from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QKeyEvent, QKeySequence

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import meshmill


class DummyWindow:
    def __init__(self):
        self.calls = []
        self.vtk_widget = object()
        self.source_poly = object()
        self.busy = False
        self.crop_start = None
        self.crop_candidate = None
        self.crop_points = []
        self.measure_points = []
        self.measure_hover_world = None
        self.selection_count = 1
        self.shortcuts = {
            shortcut_id: QKeySequence(default).toString(
                QKeySequence.SequenceFormat.PortableText
            )
            for shortcut_id, (_label, default) in meshmill.SHORTCUT_DEFINITIONS.items()
        }

    def isActiveWindow(self):
        return True

    def _selection_shortcut(self, action):
        self.calls.append(action)

    def _save_shortcut_activated(self):
        self.calls.append("save")

    def _undo_working_mesh(self):
        self.calls.append("undo")

    def _redo_working_mesh(self):
        self.calls.append("redo")

    def _selected_triangle_count(self):
        return self.selection_count

    def _clear_selection(self, message=None):
        self.calls.append("clear")

    def _clear_selection_and_ruler(self):
        self.calls.append("clear")

    def _keyboard_navigate(self, direction, control, shift):
        mode = (
            "zoom"
            if control and shift and direction in ("up", "down")
            else "roll"
            if control and shift
            else "pan"
            if control
            else "orbit"
        )
        self.calls.append(f"{mode}-{direction}")

    def _set_display_shortcut(self, mode):
        self.calls.append(f"display-{mode}")

    def _set_standard_view(self, direction):
        self.calls.append(f"view-{direction}")

    def _set_current_view_as(self, direction):
        self.calls.append(f"set-view-{direction}")

    def _diagnostic(self, _event_name, **_details):
        pass

    def _shortcut_callback(self, action):
        return meshmill.MainWindow._shortcut_callback(self, action)


cases = [
    (Qt.Key.Key_Space, Qt.KeyboardModifier.ControlModifier, "optimize"),
    (Qt.Key.Key_X, Qt.KeyboardModifier.ControlModifier, "crop"),
    (Qt.Key.Key_C, Qt.KeyboardModifier.ControlModifier, "add"),
    (Qt.Key.Key_Z, Qt.KeyboardModifier.ControlModifier, "undo"),
    (Qt.Key.Key_Y, Qt.KeyboardModifier.ControlModifier, "redo"),
    (
        Qt.Key.Key_Z,
        Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier,
        "redo",
    ),
    (Qt.Key.Key_S, Qt.KeyboardModifier.ControlModifier, "save"),
    (Qt.Key.Key_Delete, Qt.KeyboardModifier.NoModifier, "delete"),
    (Qt.Key.Key_Escape, Qt.KeyboardModifier.NoModifier, "clear"),
    (Qt.Key.Key_F1, Qt.KeyboardModifier.NoModifier, "display-Shaded"),
    (Qt.Key.Key_F2, Qt.KeyboardModifier.NoModifier, "display-Density"),
    (Qt.Key.Key_F3, Qt.KeyboardModifier.NoModifier, "display-Wireframe"),
    (Qt.Key.Key_F4, Qt.KeyboardModifier.NoModifier, "display-Vertices"),
    (Qt.Key.Key_Insert, Qt.KeyboardModifier.NoModifier, "view-left"),
    (Qt.Key.Key_Home, Qt.KeyboardModifier.NoModifier, "view-front"),
    (Qt.Key.Key_PageUp, Qt.KeyboardModifier.NoModifier, "view-right"),
    (Qt.Key.Key_End, Qt.KeyboardModifier.NoModifier, "view-back"),
    (Qt.Key.Key_PageDown, Qt.KeyboardModifier.NoModifier, "view-bottom"),
    (Qt.Key.Key_Insert, Qt.KeyboardModifier.ControlModifier, "set-view-left"),
    (Qt.Key.Key_Home, Qt.KeyboardModifier.ControlModifier, "set-view-front"),
    (Qt.Key.Key_PageUp, Qt.KeyboardModifier.ControlModifier, "set-view-right"),
    (Qt.Key.Key_Delete, Qt.KeyboardModifier.ControlModifier, "set-view-top"),
    (Qt.Key.Key_End, Qt.KeyboardModifier.ControlModifier, "set-view-back"),
    (Qt.Key.Key_PageDown, Qt.KeyboardModifier.ControlModifier, "set-view-bottom"),
    (Qt.Key.Key_Left, Qt.KeyboardModifier.NoModifier, "orbit-left"),
    (Qt.Key.Key_Right, Qt.KeyboardModifier.ControlModifier, "pan-right"),
    (
        Qt.Key.Key_Up,
        Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier,
        "zoom-up",
    ),
    (
        Qt.Key.Key_Left,
        Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier,
        "roll-left",
    ),
]

physical_navigation_cases = [
    (Qt.Key.Key_Home, "set-view-front"),
    (Qt.Key.Key_Insert, "set-view-left"),
    (Qt.Key.Key_PageUp, "set-view-right"),
    (Qt.Key.Key_Delete, "set-view-top"),
    (Qt.Key.Key_End, "set-view-back"),
    (Qt.Key.Key_PageDown, "set-view-bottom"),
]

window = DummyWindow()
for key, modifiers, expected in cases:
    override = QKeyEvent(QEvent.Type.ShortcutOverride, key, modifiers)
    assert meshmill.MainWindow.eventFilter(window, None, override) is True
    assert override.isAccepted()
    assert window.calls == []
    press = QKeyEvent(QEvent.Type.KeyPress, key, modifiers)
    assert meshmill.MainWindow.eventFilter(window, None, press) is True
    assert window.calls.pop() == expected

for key, expected in physical_navigation_cases:
    modifiers = (
        Qt.KeyboardModifier.ControlModifier
        | Qt.KeyboardModifier.KeypadModifier
    )
    override = QKeyEvent(QEvent.Type.ShortcutOverride, key, modifiers)
    assert meshmill.MainWindow.eventFilter(window, None, override) is True
    assert override.isAccepted()
    press = QKeyEvent(QEvent.Type.KeyPress, key, modifiers)
    assert meshmill.MainWindow.eventFilter(window, None, press) is True
    assert window.calls.pop() == expected

repeat = QKeyEvent(
    QEvent.Type.KeyPress,
    Qt.Key.Key_Left,
    Qt.KeyboardModifier.NoModifier,
    "",
    True,
    1,
)
assert meshmill.MainWindow.eventFilter(window, None, repeat) is True
assert window.calls.pop() == "orbit-left"

window.selection_count = 0
press = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_Delete, Qt.KeyboardModifier.NoModifier)
assert meshmill.MainWindow.eventFilter(window, None, press) is True
assert window.calls.pop() == "view-top"

print(
    f"shortcut routing ok: {len(cases) + len(physical_navigation_cases)} commands"
)
