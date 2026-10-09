from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PySide6.QtCore import QEvent, Qt, QTimer
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QApplication, QMessageBox

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import meshmill as mm

SCAN = Path(__file__).resolve().parents[1] / "samples" / "sample-scan.stl"
KEYS = {
    "left": Qt.Key.Key_Insert,
    "front": Qt.Key.Key_Home,
    "right": Qt.Key.Key_PageUp,
    "top": Qt.Key.Key_Delete,
    "back": Qt.Key.Key_End,
    "bottom": Qt.Key.Key_PageDown,
}


def normalized_camera_frame(camera):
    focal = np.asarray(camera.GetFocalPoint(), dtype=float)
    position = np.asarray(camera.GetPosition(), dtype=float)
    view = position - focal
    view /= np.linalg.norm(view)
    up = np.asarray(camera.GetViewUp(), dtype=float)
    up -= view * float(up @ view)
    up /= np.linalg.norm(up)
    right = np.cross(up, view)
    right /= np.linalg.norm(right)
    return focal, position, np.column_stack((right, up, view))


def projected_sample(points, frame):
    sample = points[np.linspace(0, len(points) - 1, min(20_000, len(points)), dtype=np.int64)]
    return (sample - sample.mean(axis=0)) @ frame


app = QApplication.instance() or QApplication([])
window = mm.MainWindow()
window.resize(1500, 850)
window.show()
window.activateWindow()
window.raise_()
app.processEvents()

triangle_count = mm.binary_stl_triangle_count(SCAN)
assert triangle_count is not None
poly, points, faces = mm.load_binary_stl_overview(SCAN, triangle_count, 160_000)
window._finish_load(
    window.load_generation,
    SCAN,
    poly,
    points,
    faces,
    {"overview": True, "total_triangles": triangle_count},
    None,
)
app.processEvents()
camera = window.renderer.GetActiveCamera()


def accept_confirmation():
    modal = QApplication.activeModalWidget()
    if isinstance(modal, QMessageBox):
        assert modal.defaultButton() is modal.button(QMessageBox.StandardButton.Save)
        from PySide6.QtTest import QTest
        QTest.keyClick(modal, Qt.Key.Key_Return)
    else:
        QTimer.singleShot(5, accept_confirmation)


def send_physical(direction, control=False):
    modifiers = Qt.KeyboardModifier.KeypadModifier
    if control:
        modifiers |= Qt.KeyboardModifier.ControlModifier
        QTimer.singleShot(5, accept_confirmation)
    key = KEYS[direction]
    for event_type in (QEvent.Type.ShortcutOverride, QEvent.Type.KeyPress):
        event = QKeyEvent(event_type, key, modifiers)
        QApplication.sendEvent(window, event)
        assert event.isAccepted(), (direction, control, event_type)
    app.processEvents()


saved = {}


def calibrate(direction, azimuth, elevation, roll):
    send_physical(direction)
    camera.Azimuth(azimuth)
    camera.Elevation(elevation)
    camera.Roll(roll)
    camera.OrthogonalizeViewUp()
    window.renderer.ResetCameraClippingRange()
    window.vtk_widget.GetRenderWindow().Render()
    app.processEvents()
    focal, _position, frame = normalized_camera_frame(camera)
    saved[direction] = {
        "focal": focal,
        "view": frame[:, 2].copy(),
        "up": frame[:, 1].copy(),
        "projection": projected_sample(window.source_points, frame),
    }
    opposite = mm.OPPOSITE_VIEWS[direction]
    opposite_frame = frame.copy()
    opposite_frame[:, 0] *= -1.0
    opposite_frame[:, 2] *= -1.0
    saved[opposite] = {
        "focal": focal.copy(),
        "view": -frame[:, 2].copy(),
        "up": frame[:, 1].copy(),
        "projection": projected_sample(window.source_points, opposite_frame),
    }
    send_physical(direction, control=True)
    assert direction in window.saved_standard_views
    assert opposite in window.saved_standard_views
    assert window.view_buttons[direction].isChecked()
    assert np.allclose(window.orientation_indicator._orientation, (0.0, 0.0, 0.0))


def recall_and_verify(direction):
    send_physical(direction)
    focal, _position, frame = normalized_camera_frame(camera)
    expected = saved[direction]
    view_error = float(np.linalg.norm(frame[:, 2] - expected["view"]))
    up_error = float(np.linalg.norm(frame[:, 1] - expected["up"]))
    focal_error = float(np.linalg.norm(focal - expected["focal"]))
    projection = projected_sample(window.source_points, frame)
    projection_error = float(np.sqrt(np.mean((projection[:, :2] - expected["projection"][:, :2]) ** 2)))
    assert view_error < 1e-10, (direction, "view", view_error)
    assert up_error < 1e-10, (direction, "up", up_error)
    assert focal_error < 1e-6, (direction, "focal", focal_error)
    assert projection_error < 1e-6, (direction, "projection", projection_error)
    assert window.view_buttons[direction].isChecked(), direction
    assert sum(button.isChecked() for button in window.view_buttons.values()) == 1
    assert np.allclose(window.orientation_indicator._orientation, (0.0, 0.0, 0.0))
    print(
        f"{direction:6s} view={view_error:.3e} up={up_error:.3e} "
        f"focal={focal_error:.3e} projection={projection_error:.3e}"
    )


# From both vertical views, the model's Front direction (+Y) is screen-up.
send_physical("top")
_, _, top_frame = normalized_camera_frame(camera)
assert np.allclose(top_frame[:, 2], (0.0, 0.0, 1.0))
assert np.allclose(top_frame[:, 1], (0.0, 1.0, 0.0))
send_physical("bottom")
_, _, bottom_frame = normalized_camera_frame(camera)
assert np.allclose(bottom_frame[:, 2], (0.0, 0.0, -1.0))
assert np.allclose(bottom_frame[:, 1], (0.0, 1.0, 0.0))

# Initial calibrations deliberately include yaw, pitch, and roll so this checks
# complete camera frames rather than only the displayed Z correction.
calibrate("front", 7.0, -4.0, 175.0)
calibrate("left", -5.0, 6.0, -35.0)
calibrate("top", 4.0, -8.0, 23.0)
calibrate("right", -9.0, 3.0, -51.0)
calibrate("back", 6.0, 5.0, 142.0)
calibrate("bottom", -3.0, -7.0, 68.0)

for direction in (
    "front", "left", "front", "top", "left", "right", "back", "front",
    "bottom", "top", "right", "left", "bottom", "back", "front",
):
    recall_and_verify(direction)

# Overwrite two existing calibrations and prove the new positions replace the
# old ones while every other saved view remains unchanged.
calibrate("front", -11.0, 9.0, -27.0)
for direction in ("left", "front", "back", "front", "top", "front"):
    recall_and_verify(direction)
calibrate("left", 13.0, -6.0, 41.0)
for direction in ("front", "left", "right", "left", "bottom", "front", "left"):
    recall_and_verify(direction)

print("orientation stress test passed")
window.close()
