from __future__ import annotations

# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 MeshMill contributors

import argparse
import ctypes
import json
import math
import multiprocessing
import os
import struct
import sys
import threading
import time
import traceback
import warnings
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import fast_simplification

from PySide6.QtCore import (
    QEvent,
    QKeyCombination,
    QObject,
    QPoint,
    QPointF,
    QLocale,
    QRect,
    QSettings,
    QSignalBlocker,
    Qt,
    QTimer,
    QUrl,
    Signal,
)
from PySide6.QtGui import (
    QColor,
    QCursor,
    QDesktopServices,
    QIcon,
    QImage,
    QKeySequence,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QPolygonF,
    QRegion,
)
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QProgressBar,
    QKeySequenceEdit,
    QScrollArea,
    QSlider,
    QSpinBox,
    QToolTip,
    QVBoxLayout,
    QWidget,
)

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray, vtk_to_numpy
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkFiltersCore import (
    vtkDecimatePro,
    vtkPolyDataNormals,
    vtkQuadricDecimation,
    vtkTriangleFilter,
)
from vtkmodules.vtkIOGeometry import vtkSTLReader, vtkSTLWriter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkCamera,
    vtkCoordinate,
    vtkHardwarePicker,
    vtkPolyDataMapper,
    vtkPolyDataMapper2D,
    vtkRenderer,
    vtkWindowToImageFilter,
)
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401


# Conservative allowance for source arrays, VTK objects, render data, and temporary work buffers.
ESTIMATED_BYTES_PER_TRIANGLE = 220

from localization import DEFAULT_LOCALE, locale_manager, tr


APP_NAME = "MeshMill"
APP_VERSION = "0.1.0"
REPOSITORY_URL = ""
PRESETS = {"light": 50_000, "balanced": 200_000, "detailed": 400_000}
UNIT_MM = {"mm": 1.0, "cm": 10.0, "m": 1000.0, "in": 25.4, "ft": 304.8}
SMART_DIVISORS = {"Draft": 160.0, "Balanced": 500.0, "Fine": 800.0}
ALGORITHMS = ["Fast QEM", "Density balanced", "Shape preserving", "Preserve topology"]
DISPLAY_MODES = ["Shaded", "Density", "Wireframe", "Vertices"]
STANDARD_VIEWS = {
    "top": ((0, 0, 1), (0, 1, 0)),
    "bottom": ((0, 0, -1), (0, 1, 0)),
    "front": ((0, 1, 0), (0, 0, 1)),
    "back": ((0, -1, 0), (0, 0, 1)),
    "left": ((1, 0, 0), (0, 0, 1)),
    "right": ((-1, 0, 0), (0, 0, 1)),
}
OPPOSITE_VIEWS = {
    "left": "right",
    "right": "left",
    "front": "back",
    "back": "front",
    "top": "bottom",
    "bottom": "top",
}
SHORTCUT_DEFINITIONS = {
    "save": ("Save", "Ctrl+S"),
    "undo": ("Undo", "Ctrl+Z"),
    "redo": ("Redo", "Ctrl+Y"),
    "redo_alt": ("Redo (alternate)", "Ctrl+Shift+Z"),
    "selection_optimize": ("Optimize selection", "Ctrl+Space"),
    "selection_crop": ("Crop selection", "Ctrl+X"),
    "selection_add": ("Add selection", "Ctrl+C"),
    "selection_delete": ("Delete selection", "Delete"),
    "selection_clear": ("Clear selection", "Esc"),
    "display_shaded": ("Display: Shaded", "F1"),
    "display_density": ("Display: Density", "F2"),
    "display_wireframe": ("Display: Wireframe", "F3"),
    "display_vertices": ("Display: Vertices", "F4"),
    "view_left": ("View: Left", "Insert"),
    "view_front": ("View: Front", "Home"),
    "view_right": ("View: Right", "PgUp"),
    "view_top": ("View: Top", "Delete"),
    "view_back": ("View: Back", "End"),
    "view_bottom": ("View: Bottom", "PgDown"),
    "set_view_left": ("Set view: Left", "Ctrl+Insert"),
    "set_view_front": ("Set view: Front", "Ctrl+Home"),
    "set_view_right": ("Set view: Right", "Ctrl+PgUp"),
    "set_view_top": ("Set view: Top", "Ctrl+Delete"),
    "set_view_back": ("Set view: Back", "Ctrl+End"),
    "set_view_bottom": ("Set view: Bottom", "Ctrl+PgDown"),
    "orbit_left": ("Orbit left", "Left"),
    "orbit_right": ("Orbit right", "Right"),
    "orbit_up": ("Orbit up", "Up"),
    "orbit_down": ("Orbit down", "Down"),
    "pan_left": ("Pan left", "Ctrl+Left"),
    "pan_right": ("Pan right", "Ctrl+Right"),
    "pan_up": ("Pan up", "Ctrl+Up"),
    "pan_down": ("Pan down", "Ctrl+Down"),
    "zoom_in": ("Zoom in", "Ctrl+Shift+Up"),
    "zoom_out": ("Zoom out", "Ctrl+Shift+Down"),
    "roll_counterclockwise": ("Roll counterclockwise", "Ctrl+Shift+Left"),
    "roll_clockwise": ("Roll clockwise", "Ctrl+Shift+Right"),
}
CLI_ALGORITHMS = {
    "fast": "Fast QEM",
    "density": "Density balanced",
    "shape": "Shape preserving",
    "topology": "Preserve topology",
}
warnings.filterwarnings("ignore", message="Call to deprecated method.*", category=DeprecationWarning)


def resource_path(relative: str) -> Path:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base / relative


def localize_widget_tree(root: QWidget) -> None:
    """Apply the active catalog to static widget labels and tooltips."""
    widgets = [root, *root.findChildren(QWidget)]
    for widget in widgets:
        title = widget.windowTitle()
        if title:
            source = widget.property("i18n_window_title") or title
            widget.setProperty("i18n_window_title", source)
            widget.setWindowTitle(tr(str(source)))
        tooltip = widget.toolTip()
        if tooltip:
            source = widget.property("i18n_tooltip") or tooltip
            widget.setProperty("i18n_tooltip", source)
            widget.setToolTip(tr(str(source)))
        if isinstance(widget, (QLabel, QPushButton, QCheckBox)):
            text = widget.text()
            if text:
                source = widget.property("i18n_text") or text
                widget.setProperty("i18n_text", source)
                widget.setText(tr(str(source)))
    direction = locale_manager.manifest.get("languages", {}).get(
        locale_manager.locale, {}
    ).get("direction", "ltr")
    root.setLayoutDirection(
        Qt.LayoutDirection.RightToLeft if direction == "rtl" else Qt.LayoutDirection.LeftToRight
    )


APP_STYLESHEET = """
QMainWindow, QWidget#mainRoot { background: #F7F5F1; }
QWidget { color: #0B1B34; font-family: "Segoe UI"; font-size: 12px; }
QFrame#toolSection { background: #FBFAF8; border: 1px solid #E4E1DC; border-radius: 8px; }
QLabel#sectionTitle { color: #0B1B34; font-size: 12px; font-weight: 700;
                      border-bottom: 2px solid #D9F99D; padding-bottom: 3px; }
QLabel#fileCard { background: #FFFFFF; border: 1px solid #E4E1DC; border-left: 3px solid #2563FF;
                  border-radius: 7px; padding: 7px; color: #24324A; }
QPushButton { background: #FFFFFF; border: 1px solid #D8DCE5; border-radius: 6px; padding: 6px 10px; }
QPushButton:hover { border-color: #2563FF; background: #F1F5FF; }
QPushButton:pressed { background: #E2EAFF; }
QPushButton:disabled { color: #9CA3AF; background: #EEEDEA; border-color: #E4E1DC; }
QPushButton[accent="true"] { color: white; background: #2563FF; border-color: #2563FF; font-weight: 600; }
QPushButton[accent="true"]:hover { background: #1B4ED8; }
QPushButton[accent="true"]:disabled { color: #9CA3AF; background: #EEEDEA; border-color: #E4E1DC; }
QPushButton[quiet="true"] { background: transparent; }
QComboBox, QSpinBox { background: #FFFFFF; border: 1px solid #D8DCE5; border-radius: 6px;
                      padding: 5px 8px; min-height: 18px; }
QComboBox:hover, QSpinBox:hover { border-color: #2563FF; }
QComboBox::drop-down { border: 0; width: 22px; }
QSlider::groove:horizontal { height: 5px; border-radius: 2px; background: #DCE2EC; }
QSlider::sub-page:horizontal { background: #2563FF; border-radius: 2px; }
QSlider::handle:horizontal { width: 15px; margin: -5px 0; border-radius: 7px;
                             background: #FFFFFF; border: 2px solid #2563FF; }
QCheckBox::indicator { width: 16px; height: 16px; }
QCheckBox::indicator:checked { background: #2563FF; border: 1px solid #2563FF; border-radius: 3px; }
QProgressBar { border: 1px solid #D8DCE5; border-radius: 5px; background: #ECEAE6;
               text-align: center; min-height: 16px; }
QProgressBar::chunk { background: #2563FF; border-radius: 4px; }
QToolTip { background: #0B1B34; color: #F7F5F1; border: 1px solid #2563FF; padding: 5px; }
"""


class ResultBridge(QObject):
    done = Signal(int, object, object, object)


class LoadBridge(QObject):
    done = Signal(int, object, object, object, object, object, object)


class EditBridge(QObject):
    done = Signal(int, object)


class DensityBridge(QObject):
    done = Signal(int, object, object, object)


class OperationCancelled(Exception):
    pass


@dataclass
class MeshHistoryState:
    poly: vtkPolyData
    points: np.ndarray
    faces: np.ndarray
    actor: vtkActor | None
    modified: bool
    preview_poly: vtkPolyData | None
    preview_actor: vtkActor | None
    dimension_drift: np.ndarray | None
    showing_original: bool
    preview_dirty: bool
    committed_optimization: bool


class _PdhValueUnion(ctypes.Union):
    _fields_ = [
        ("longValue", ctypes.c_long),
        ("doubleValue", ctypes.c_double),
        ("largeValue", ctypes.c_longlong),
    ]


class _PdhCounterValue(ctypes.Structure):
    _anonymous_ = ("value",)
    _fields_ = [("CStatus", ctypes.c_ulong), ("value", _PdhValueUnion)]


class _PdhValueItem(ctypes.Structure):
    _fields_ = [("szName", ctypes.c_wchar_p), ("FmtValue", _PdhCounterValue)]


class WindowsGpuCounters:
    """Read the same Windows GPU Engine counters used by Task Manager."""

    PDH_FMT_DOUBLE = 0x00000200
    PDH_MORE_DATA = 0x800007D2

    def __init__(self) -> None:
        self.available = False
        self.query = ctypes.c_void_p()
        self.engine_counter = ctypes.c_void_p()
        self.memory_counter = ctypes.c_void_p()
        if os.name != "nt":
            return
        try:
            self.pdh = ctypes.WinDLL("pdh")
            self.pdh.PdhOpenQueryW.argtypes = [ctypes.c_wchar_p, ctypes.c_size_t, ctypes.c_void_p]
            self.pdh.PdhAddEnglishCounterW.argtypes = [
                ctypes.c_void_p,
                ctypes.c_wchar_p,
                ctypes.c_size_t,
                ctypes.c_void_p,
            ]
            self.pdh.PdhCollectQueryData.argtypes = [ctypes.c_void_p]
            self.pdh.PdhGetFormattedCounterArrayW.argtypes = [
                ctypes.c_void_p,
                ctypes.c_ulong,
                ctypes.POINTER(ctypes.c_ulong),
                ctypes.POINTER(ctypes.c_ulong),
                ctypes.c_void_p,
            ]
            self.pdh.PdhOpenQueryW.restype = ctypes.c_ulong
            self.pdh.PdhAddEnglishCounterW.restype = ctypes.c_ulong
            self.pdh.PdhCollectQueryData.restype = ctypes.c_ulong
            self.pdh.PdhGetFormattedCounterArrayW.restype = ctypes.c_ulong
            if self.pdh.PdhOpenQueryW(None, 0, ctypes.byref(self.query)) != 0:
                return
            engine_status = self.pdh.PdhAddEnglishCounterW(
                self.query,
                r"\GPU Engine(*)\Utilization Percentage",
                0,
                ctypes.byref(self.engine_counter),
            )
            memory_status = self.pdh.PdhAddEnglishCounterW(
                self.query,
                r"\GPU Adapter Memory(*)\Dedicated Usage",
                0,
                ctypes.byref(self.memory_counter),
            )
            if engine_status != 0:
                return
            self.available = True
            self.has_memory_counter = memory_status == 0
            self.pdh.PdhCollectQueryData(self.query)
        except (AttributeError, OSError):
            self.available = False

    def _values(self, counter: ctypes.c_void_p) -> list[tuple[str, float]]:
        size = ctypes.c_ulong(0)
        count = ctypes.c_ulong(0)
        status = self.pdh.PdhGetFormattedCounterArrayW(
            counter, self.PDH_FMT_DOUBLE, ctypes.byref(size), ctypes.byref(count), None
        )
        if status != self.PDH_MORE_DATA or size.value == 0:
            return []
        buffer = ctypes.create_string_buffer(size.value)
        status = self.pdh.PdhGetFormattedCounterArrayW(
            counter,
            self.PDH_FMT_DOUBLE,
            ctypes.byref(size),
            ctypes.byref(count),
            buffer,
        )
        if status != 0:
            return []
        items = ctypes.cast(buffer, ctypes.POINTER(_PdhValueItem))
        return [
            (items[index].szName or "", float(items[index].FmtValue.doubleValue))
            for index in range(count.value)
            if items[index].FmtValue.CStatus in (0, 1)
        ]

    @staticmethod
    def _adapter_key(instance: str) -> str:
        normalized = instance.lower()
        luid = normalized.find("luid_")
        if luid >= 0:
            normalized = normalized[luid:]
        return normalized.split("_eng_", 1)[0]

    def sample(self) -> tuple[float, float]:
        if not self.available or self.pdh.PdhCollectQueryData(self.query) != 0:
            raise OSError("Windows GPU performance counters are unavailable")
        engines: dict[str, float] = {}
        for instance, value in self._values(self.engine_counter):
            normalized = instance.lower()
            luid = normalized.find("luid_")
            engine = normalized[luid:] if luid >= 0 else normalized
            engines[engine] = engines.get(engine, 0.0) + max(0.0, value)
        loads: dict[str, float] = {}
        for engine, value in engines.items():
            key = self._adapter_key(engine)
            loads[key] = max(loads.get(key, 0.0), value)
        memory: dict[str, float] = {}
        if self.has_memory_counter:
            for instance, value in self._values(self.memory_counter):
                memory[self._adapter_key(instance)] = max(0.0, value)
        if not loads:
            raise OSError("Windows returned no GPU engine samples")
        adapter = max(loads, key=lambda key: (loads[key], memory.get(key, 0.0)))
        return max(0.0, min(100.0, loads[adapter])), memory.get(adapter, 0.0)

    def close(self) -> None:
        if getattr(self, "query", None):
            try:
                self.pdh.PdhCloseQuery(self.query)
            except (AttributeError, OSError):
                pass
            self.query = ctypes.c_void_p()


class ViewButton(QPushButton):
    orientationRequested = Signal()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._orientation_press = False

    def mousePressEvent(self, event) -> None:  # noqa: N802
        owner = self.window()
        control_held = bool(
            (event.modifiers() | QApplication.keyboardModifiers())
            & Qt.KeyboardModifier.ControlModifier
        ) or bool(getattr(owner, "control_key_held", False))
        if (
            event.button() == Qt.MouseButton.LeftButton
            and control_held
        ):
            self._orientation_press = True
            self.setDown(True)
            self.orientationRequested.emit()
            event.accept()
            return
        self._orientation_press = False
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton and self._orientation_press:
            self._orientation_press = False
            self.setDown(False)
            event.accept()
            return
        super().mouseReleaseEvent(event)


class DraggableOverlayFrame(QFrame):
    """Viewport panel that can be moved without interfering with child controls."""

    movedByUser = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._drag_global_offset: QPoint | None = None

    def mousePressEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_global_offset = event.globalPosition().toPoint() - self.pos()
            self.raise_()
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:  # noqa: N802
        if self._drag_global_offset is not None and bool(event.buttons() & Qt.MouseButton.LeftButton):
            parent = self.parentWidget()
            if parent is not None:
                proposed = event.globalPosition().toPoint() - self._drag_global_offset
                x = max(8, min(proposed.x(), max(8, parent.width() - self.width() - 8)))
                y = max(8, min(proposed.y(), max(8, parent.height() - self.height() - 8)))
                self.move(x, y)
                self.movedByUser.emit()
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton and self._drag_global_offset is not None:
            self._drag_global_offset = None
            event.accept()
            return
        super().mouseReleaseEvent(event)


class OrientationIndicator(QWidget):
    """Compact world-axis view indicator for the active camera."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setFixedSize(180, 104)
        self.setToolTip("Camera rotation relative to the mesh's current X, Y, and Z axes.")
        self._right = np.array((1.0, 0.0, 0.0))
        self._up = np.array((0.0, 1.0, 0.0))
        self._forward = np.array((0.0, 0.0, -1.0))
        self._orientation = (0.0, 0.0, 0.0)

    def set_camera(self, position, focal, view_up, orientation) -> None:
        forward = np.asarray(focal, dtype=float) - np.asarray(position, dtype=float)
        forward /= max(float(np.linalg.norm(forward)), 1e-12)
        up = np.asarray(view_up, dtype=float)
        up -= forward * float(up @ forward)
        up /= max(float(np.linalg.norm(up)), 1e-12)
        right = np.cross(forward, up)
        right /= max(float(np.linalg.norm(right)), 1e-12)
        self._right = right
        self._up = up
        self._forward = forward
        self._orientation = tuple(float(value) for value in orientation)
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor("#425A78"), 1.0))
        painter.setBrush(QColor(11, 27, 52, 225))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 9, 9)
        center_x = self.width() / 2.0
        center = QPointF(center_x, 47.0)

        cube = QPolygonF(
            [
                QPointF(center_x, 19),
                QPointF(center_x + 21, 31),
                QPointF(center_x, 43),
                QPointF(center_x - 21, 31),
            ]
        )
        painter.setPen(QPen(QColor("#AFC5E6"), 1.2))
        painter.setBrush(QColor(42, 65, 96, 220))
        painter.drawPolygon(cube)
        painter.drawLine(QPointF(center_x - 21, 31), QPointF(center_x - 21, 55))
        painter.drawLine(QPointF(center_x + 21, 31), QPointF(center_x + 21, 55))
        painter.drawLine(QPointF(center_x, 43), QPointF(center_x, 67))
        painter.drawLine(QPointF(center_x - 21, 55), QPointF(center_x, 67))
        painter.drawLine(QPointF(center_x + 21, 55), QPointF(center_x, 67))

        axes = (
            ("X", np.array((1.0, 0.0, 0.0)), QColor("#FF5A5F")),
            ("Y", np.array((0.0, 1.0, 0.0)), QColor("#B8F35A")),
            ("Z", np.array((0.0, 0.0, 1.0)), QColor("#4DA3FF")),
        )
        projected = []
        for label, axis, color in axes:
            screen = np.array((float(axis @ self._right), -float(axis @ self._up)))
            depth = float(axis @ self._forward)
            projected.append((depth, label, screen, color))
        for depth, label, screen, color in sorted(projected):
            end = center + QPointF(float(screen[0] * 29.0), float(screen[1] * 29.0))
            pen = QPen(color, 3.0 if depth >= 0 else 1.5)
            if depth < 0:
                pen.setStyle(Qt.PenStyle.DashLine)
            painter.setPen(pen)
            painter.drawLine(center, end)
            painter.setPen(color)
            painter.drawText(QRect(int(end.x() - 8), int(end.y() - 9), 16, 18), Qt.AlignmentFlag.AlignCenter, label)

        x, y, z = (round(value) for value in self._orientation)
        painter.setPen(QColor("#D8E5F7"))
        angle_font = painter.font()
        angle_font.setPointSizeF(8.5)
        painter.setFont(angle_font)
        painter.drawText(
            QRect(6, 77, self.width() - 12, 20),
            Qt.AlignmentFlag.AlignCenter,
            f"X {x:+d}°  Y {y:+d}°  Z {z:+d}°",
        )


class ViewportScaleBar(QWidget):
    """Camera-aware scale ruler drawn over the viewport."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setFixedSize(200, 46)
        self._label = ""
        self._pixels = 120.0
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        # QVTKRenderWindowInteractor is a native OpenGL surface. Transparent
        # child-widget updates can leave previous scale-bar frames behind while
        # zooming, so this small overlay clears itself with the viewport color.
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, True)

    def set_scale(self, label: str, pixels: float) -> None:
        clamped_pixels = max(24.0, min(170.0, float(pixels)))
        if label == self._label and abs(clamped_pixels - self._pixels) < 0.25:
            return
        self._label = label
        self._pixels = clamped_pixels
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#0B1B34"))
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor(235, 242, 252, 235), 2.0))
        right = self.width() - 12.0
        left = right - self._pixels
        y = 31.0
        painter.drawLine(QPointF(left, y), QPointF(right, y))
        painter.drawLine(QPointF(left, y - 5), QPointF(left, y + 5))
        painter.drawLine(QPointF(right, y - 5), QPointF(right, y + 5))
        painter.setPen(QColor(235, 242, 252, 245))
        painter.drawText(
            QRect(int(left), 4, int(self._pixels), 20),
            Qt.AlignmentFlag.AlignCenter,
            self._label,
        )


class ArrowComboBox(QComboBox):
    """Combo box with a theme-independent dropdown chevron."""

    def paintEvent(self, event) -> None:  # noqa: N802
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#0B1B34" if self.isEnabled() else "#9CA3AF"))
        center_x = self.width() - 13
        center_y = self.height() // 2 + 1
        painter.drawPolygon(
            QPolygonF(
                [
                    QPointF(center_x - 4, center_y - 2),
                    QPointF(center_x + 4, center_y - 2),
                    QPointF(center_x, center_y + 3),
                ]
            )
        )


class DeferredTooltipFilter(QObject):
    """Quiet, two-second, movement-sensitive help without changing the cursor."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.widget: QWidget | None = None
        self.position = QPoint()
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.setInterval(2000)
        self.timer.timeout.connect(self._show)

    def eventFilter(self, watched, event) -> bool:  # noqa: N802
        if not isinstance(watched, QWidget) or not watched.toolTip():
            return False
        kind = event.type()
        if kind == QEvent.Type.ToolTip:
            return True
        if kind == QEvent.Type.Enter:
            self._arm(watched, QCursor.pos())
        elif kind == QEvent.Type.MouseMove:
            QToolTip.hideText()
            position = event.globalPosition().toPoint() if hasattr(event, "globalPosition") else QCursor.pos()
            self._arm(watched, position)
        elif kind in (QEvent.Type.Leave, QEvent.Type.Hide, QEvent.Type.FocusOut):
            if watched is self.widget:
                self.timer.stop()
                QToolTip.hideText()
                self.widget = None
        return False

    def _arm(self, widget: QWidget, position: QPoint) -> None:
        self.widget = widget
        self.position = position
        self.timer.start()

    def _show(self) -> None:
        if self.widget is not None and self.widget.underMouse():
            QToolTip.showText(self.position + QPoint(12, 18), self.widget.toolTip(), self.widget)


class CropPolygonOverlay(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.points: list[QPoint] = []
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    def set_points(self, points: list[QPoint]) -> None:
        self.points = [QPoint(point) for point in points]
        self.update()
        self.show()
        self.raise_()

    def paintEvent(self, _event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Source)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 0))
        if len(self.points) < 3:
            return
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        polygon = QPolygonF([QPointF(point) for point in self.points])
        painter.setBrush(QColor(40, 155, 255, 18))
        pen = QPen(QColor(125, 215, 255, 245), 3)
        pen.setStyle(Qt.PenStyle.DashLine)
        painter.setPen(pen)
        painter.drawPolygon(polygon)
        painter.setPen(QPen(QColor(8, 35, 55, 255), 2))
        painter.setBrush(QColor(145, 225, 255, 245))
        for point in self.points:
            painter.drawEllipse(QPointF(point), 6, 6)


class GeometryActivityGraph(QWidget):
    """Rolling CPU/GPU history with marked geometry-processing intervals."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.samples: list[tuple[float, float, bool]] = []
        self.operation = "Idle"
        self.geometry_text = "No mesh loaded"
        self.setFixedHeight(112)

    def add_sample(
        self,
        cpu: float,
        gpu: float,
        processing: bool,
        operation: str,
        points: int,
        triangles: int,
    ) -> None:
        cpu = max(0.0, min(100.0, cpu))
        gpu = max(0.0, min(100.0, gpu))
        self.samples.append((cpu, gpu, processing))
        self.samples = self.samples[-120:]
        self.operation = operation
        self.geometry_text = (
            f"{fmt_count(points)} vertices / {fmt_count(triangles)} triangles"
            if points or triangles
            else "No mesh loaded"
        )
        self.update()

    def paintEvent(self, _event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.fillRect(self.rect(), QColor("#FFFFFF"))
        painter.setPen(QColor("#0B1B34"))
        painter.drawText(8, 15, f"Geometry activity · {self.operation} · {self.geometry_text}")

        left, top, right, bottom = 8, 23, self.width() - 8, self.height() - 19
        width = max(1, right - left)
        height = max(1, bottom - top)
        painter.setPen(QPen(QColor("#E4E1DC"), 1))
        for fraction in (0.25, 0.5, 0.75):
            y = top + height * fraction
            painter.drawLine(left, round(y), right, round(y))

        if self.samples:
            step = width / max(1, len(self.samples) - 1)
            active_color = QColor(37, 99, 255, 30)
            for index, (_, _, active) in enumerate(self.samples):
                if active:
                    x = left + index * step
                    painter.fillRect(
                        round(x - max(1.0, step) / 2),
                        top,
                        max(2, round(step) + 1),
                        height,
                        active_color,
                    )

            def draw_line(values: list[float], color: str) -> None:
                points = QPolygonF(
                    [
                        QPointF(left + index * step, bottom - height * value / 100.0)
                        for index, value in enumerate(values)
                    ]
                )
                painter.setPen(QPen(QColor(color), 1.8))
                painter.drawPolyline(points)

            draw_line([sample[0] for sample in self.samples], "#2563FF")
            draw_line([sample[1] for sample in self.samples], "#8FCB33")

        painter.setPen(QColor("#2563FF"))
        painter.drawText(8, self.height() - 5, "CPU")
        painter.setPen(QColor("#8FCB33"))
        painter.drawText(38, self.height() - 5, "GPU")
        painter.setPen(QColor("#6B7280"))
        painter.drawText(70, self.height() - 5, "geometry processing")


def fmt_count(value: int) -> str:
    return f"{value:,}"


def fmt_bytes(value: int) -> str:
    if value >= 1024 ** 3:
        return f"{value / 1024 ** 3:.2f} GB"
    if value >= 1024 ** 2:
        return f"{value / 1024 ** 2:.1f} MB"
    if value >= 1024:
        return f"{value / 1024:.1f} KB"
    return f"{value} bytes"


def binary_stl_size(triangle_count: int) -> int:
    return 84 + 50 * triangle_count


def bounds_size(bounds: tuple[float, ...]) -> tuple[float, float, float]:
    return bounds[1] - bounds[0], bounds[3] - bounds[2], bounds[5] - bounds[4]


def fmt_size(size: tuple[float, float, float]) -> str:
    return " x ".join(f"{v:,.3f}" for v in size)


def polydata_arrays(poly: vtkPolyData) -> tuple[np.ndarray, np.ndarray]:
    points = np.asarray(vtk_to_numpy(poly.GetPoints().GetData()), dtype=np.float64)
    raw = np.asarray(vtk_to_numpy(poly.GetPolys().GetData()))
    if raw.size % 4 or np.any(raw[0::4] != 3):
        raise ValueError("The STL did not resolve to a triangle-only mesh.")
    faces = np.asarray(raw.reshape(-1, 4)[:, 1:], dtype=np.int32)
    return points, faces


def arrays_polydata(points: np.ndarray, faces: np.ndarray) -> vtkPolyData:
    vtk_points = vtkPoints()
    vtk_points.SetData(numpy_to_vtk(np.ascontiguousarray(points), deep=True))
    packed = np.empty((len(faces), 4), dtype=np.int64)
    packed[:, 0] = 3
    packed[:, 1:] = faces
    cells = vtkCellArray()
    cells.SetCells(len(faces), numpy_to_vtkIdTypeArray(packed.ravel(), deep=True))
    poly = vtkPolyData()
    poly.SetPoints(vtk_points)
    poly.SetPolys(cells)
    return poly


def load_stl(path: Path) -> tuple[vtkPolyData, np.ndarray, np.ndarray]:
    reader = vtkSTLReader()
    reader.SetFileName(os.fspath(path))
    reader.MergingOn()
    reader.Update()
    triangle = vtkTriangleFilter()
    triangle.SetInputConnection(reader.GetOutputPort())
    triangle.Update()
    poly = vtkPolyData()
    poly.DeepCopy(triangle.GetOutput())
    if poly.GetNumberOfPolys() == 0:
        raise ValueError("No triangles were found in the file.")
    points, faces = polydata_arrays(poly)
    return poly, points, faces


def binary_stl_triangle_count(path: Path) -> int | None:
    size = path.stat().st_size
    if size < 84:
        return None
    with path.open("rb") as stream:
        header = stream.read(84)
    count = struct.unpack_from("<I", header, 80)[0]
    return count if 84 + 50 * count == size else None


def load_binary_stl_overview(
    path: Path, triangle_count: int, triangle_limit: int
) -> tuple[vtkPolyData, np.ndarray, np.ndarray]:
    sample_count = min(max(1, triangle_limit), triangle_count)
    record_dtype = np.dtype(
        [("normal", "<f4", (3,)), ("vertices", "<f4", (3, 3)), ("attribute", "<u2")]
    )
    records = np.memmap(path, dtype=record_dtype, mode="r", offset=84, shape=(triangle_count,))
    indices = np.linspace(0, triangle_count - 1, sample_count, dtype=np.int64)
    points = np.ascontiguousarray(records[indices]["vertices"].reshape(-1, 3), dtype=np.float64)
    del records
    faces = np.arange(len(points), dtype=np.int32).reshape(-1, 3)
    return arrays_polydata(points, faces), points, faces


def load_stl_smart(
    path: Path,
    mode: str,
    memory_budget_bytes: int,
    overview_triangle_limit: int,
) -> tuple[vtkPolyData, np.ndarray, np.ndarray, dict]:
    triangle_count = binary_stl_triangle_count(path)
    estimated_memory = (
        triangle_count * ESTIMATED_BYTES_PER_TRIANGLE
        if triangle_count is not None
        else path.stat().st_size * 5
    )
    use_overview = mode == "overview" or (
        mode == "auto" and estimated_memory > memory_budget_bytes
    )
    if use_overview:
        if triangle_count is None:
            raise MemoryError(
                "This STL is too large for the current memory budget, and bounded overview "
                "loading currently requires a binary STL. Increase the budget, choose Full mesh, "
                "or convert the file to binary STL."
            )
        poly, points, faces = load_binary_stl_overview(
            path, triangle_count, overview_triangle_limit
        )
        return poly, points, faces, {
            "overview": True,
            "total_triangles": triangle_count,
            "estimated_memory": estimated_memory,
        }
    poly, points, faces = load_stl(path)
    return poly, points, faces, {
        "overview": False,
        "total_triangles": len(faces),
        "estimated_memory": estimated_memory,
    }


def available_physical_memory() -> int:
    if os.name == "nt":
        class MemoryStatus(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        status = MemoryStatus()
        status.dwLength = ctypes.sizeof(MemoryStatus)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            return int(status.ullAvailPhys)
    else:
        try:
            return int(os.sysconf("SC_AVPHYS_PAGES") * os.sysconf("SC_PAGE_SIZE"))
        except (AttributeError, OSError, ValueError):
            pass
    return 4 * 1024**3


def dedicated_vram_capacity() -> int:
    if os.name != "nt":
        return 0

    class Guid(ctypes.Structure):
        _fields_ = [
            ("Data1", ctypes.c_ulong),
            ("Data2", ctypes.c_ushort),
            ("Data3", ctypes.c_ushort),
            ("Data4", ctypes.c_ubyte * 8),
        ]

    class AdapterDesc1(ctypes.Structure):
        _fields_ = [
            ("Description", ctypes.c_wchar * 128),
            ("VendorId", ctypes.c_uint),
            ("DeviceId", ctypes.c_uint),
            ("SubSysId", ctypes.c_uint),
            ("Revision", ctypes.c_uint),
            ("DedicatedVideoMemory", ctypes.c_size_t),
            ("DedicatedSystemMemory", ctypes.c_size_t),
            ("SharedSystemMemory", ctypes.c_size_t),
            ("AdapterLuid", ctypes.c_longlong),
            ("Flags", ctypes.c_uint),
        ]

    iid = Guid(
        0x770AAE78,
        0xF26F,
        0x4DBA,
        (ctypes.c_ubyte * 8)(0xA8, 0x29, 0x25, 0x3C, 0x83, 0xD1, 0xB3, 0x87),
    )
    factory = ctypes.c_void_p()

    def method(pointer: ctypes.c_void_p, index: int, prototype):
        table = ctypes.cast(pointer, ctypes.POINTER(ctypes.POINTER(ctypes.c_void_p))).contents
        return prototype(table[index])

    try:
        create_factory = ctypes.WinDLL("dxgi").CreateDXGIFactory1
        create_factory.argtypes = [ctypes.POINTER(Guid), ctypes.POINTER(ctypes.c_void_p)]
        create_factory.restype = ctypes.c_long
        if create_factory(ctypes.byref(iid), ctypes.byref(factory)) < 0 or not factory.value:
            return 0

        enum_adapter = method(
            factory,
            12,
            ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(ctypes.c_void_p)),
        )
        capacities: list[int] = []
        index = 0
        while True:
            adapter = ctypes.c_void_p()
            if enum_adapter(factory, index, ctypes.byref(adapter)) < 0 or not adapter.value:
                break
            get_desc = method(
                adapter,
                10,
                ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_void_p, ctypes.POINTER(AdapterDesc1)),
            )
            release_adapter = method(
                adapter, 2, ctypes.WINFUNCTYPE(ctypes.c_ulong, ctypes.c_void_p)
            )
            desc = AdapterDesc1()
            if get_desc(adapter, ctypes.byref(desc)) >= 0 and not (desc.Flags & 2):
                capacities.append(int(desc.DedicatedVideoMemory))
            release_adapter(adapter)
            index += 1
        return max(capacities, default=0)
    except (AttributeError, OSError, ValueError):
        return 0
    finally:
        if factory.value:
            release_factory = method(
                factory, 2, ctypes.WINFUNCTYPE(ctypes.c_ulong, ctypes.c_void_p)
            )
            release_factory(factory)


def save_stl(poly: vtkPolyData, path: Path) -> None:
    writer = vtkSTLWriter()
    writer.SetFileName(os.fspath(path))
    writer.SetFileTypeToBinary()
    writer.SetInputData(poly)
    if writer.Write() != 1:
        raise OSError(f"VTK could not save {path}")


class MeshInteractorStyle(vtkInteractorStyleTrackballCamera):
    """CAD-style navigation: middle-drag orbit, Shift+middle-drag pan, wheel zoom."""

    def __init__(
        self, widget: QWidget, loupe_callback, crop_callback, keyboard_nav_callback,
        measurement_callback,
    ) -> None:
        super().__init__()
        self._widget = widget
        self._loupe_callback = loupe_callback
        self._crop_callback = crop_callback
        self._keyboard_nav_callback = keyboard_nav_callback
        self._measurement_callback = measurement_callback
        self._right_down = False
        self._crop_down = False
        self._crop_edit_down = False
        self._crop_right_consumed = False
        self._consume_left_release = False
        self._middle_mode: str | None = None
        self._zoom_picker = vtkHardwarePicker()
        self.invert_horizontal = False
        self.invert_vertical = False
        self.invert_zoom = False
        self.AddObserver("MiddleButtonPressEvent", self._middle_press)
        self.AddObserver("MiddleButtonReleaseEvent", self._middle_release)
        self.AddObserver("RightButtonPressEvent", self._right_press)
        self.AddObserver("RightButtonReleaseEvent", self._right_release)
        self.AddObserver("LeftButtonPressEvent", self._left_press)
        self.AddObserver("LeftButtonReleaseEvent", self._left_release)
        self.AddObserver("MouseMoveEvent", self._mouse_move)
        self.AddObserver("MouseWheelForwardEvent", self._wheel_forward)
        self.AddObserver("MouseWheelBackwardEvent", self._wheel_backward)
        self.AddObserver("KeyPressEvent", self._key_press)
        self.AddObserver("KeyReleaseEvent", self._key_release)

    def _left_press(self, _obj, _event) -> None:
        if self.GetInteractor().GetShiftKey() and not self.GetInteractor().GetControlKey():
            if self._measurement_callback("click", self.GetInteractor().GetEventPosition()):
                self._consume_left_release = True
                return
        if self.GetInteractor().GetControlKey():
            self._crop_down = True
            self._widget.setCursor(Qt.CursorShape.CrossCursor)
            self._crop_callback("start", self.GetInteractor().GetEventPosition())
        elif self._crop_callback("left_press", self.GetInteractor().GetEventPosition()):
            self._crop_edit_down = True
            self._consume_left_release = True
            return
        else:
            self.OnLeftButtonDown()

    def _left_release(self, _obj, _event) -> None:
        if self._consume_left_release:
            self._consume_left_release = False
            if self._crop_edit_down:
                self._crop_edit_down = False
                self._crop_callback("left_release", self.GetInteractor().GetEventPosition())
            return
        if self._crop_down:
            self._crop_down = False
            self._crop_callback("finish", self.GetInteractor().GetEventPosition())
            self._widget.setCursor(Qt.CursorShape.ArrowCursor)
        else:
            self.OnLeftButtonUp()

    def _middle_press(self, _obj, _event) -> None:
        self._crop_callback("navigation", None)
        if self.GetInteractor().GetShiftKey():
            self._middle_mode = "pan"
            self._widget.setCursor(Qt.CursorShape.SizeAllCursor)
            self.StartPan()
        else:
            self._middle_mode = "rotate"
            self._widget.setCursor(Qt.CursorShape.ClosedHandCursor)
            self.StartRotate()

    def _middle_release(self, _obj, _event) -> None:
        if self._middle_mode == "pan":
            self.EndPan()
        elif self._middle_mode == "rotate":
            self.EndRotate()
        self._middle_mode = None
        self._widget.setCursor(Qt.CursorShape.ArrowCursor)

    def _right_press(self, _obj, _event) -> None:
        if self._crop_callback("right_press", self.GetInteractor().GetEventPosition()):
            self._crop_right_consumed = True
            return
        self._right_down = True
        self._widget.setCursor(Qt.CursorShape.CrossCursor)
        self._loupe_callback(True)

    def _right_release(self, _obj, _event) -> None:
        if self._crop_right_consumed:
            self._crop_right_consumed = False
            return
        self._right_down = False
        self._loupe_callback(False)
        self._widget.setCursor(Qt.CursorShape.ArrowCursor)

    def _mouse_move(self, _obj, _event) -> None:
        if self._crop_down:
            self._crop_callback("move", self.GetInteractor().GetEventPosition())
        elif self._crop_edit_down:
            self._crop_callback("edit_move", self.GetInteractor().GetEventPosition())
        elif self._right_down:
            self._loupe_callback(True)
        elif self.GetInteractor().GetShiftKey() and self._middle_mode is None:
            self._measurement_callback("move", self.GetInteractor().GetEventPosition())
        else:
            self._measurement_callback("hide", None)
            # Continue VTK's active rotate/pan/dolly interaction.
            interactor = self.GetInteractor()
            if (
                (self.invert_horizontal or self.invert_vertical)
                and self._middle_mode in ("rotate", "pan")
            ):
                current_x, current_y = interactor.GetEventPosition()
                last_x, last_y = interactor.GetLastEventPosition()
                mapped_x = 2 * last_x - current_x if self.invert_horizontal else current_x
                mapped_y = 2 * last_y - current_y if self.invert_vertical else current_y
                interactor.SetEventPosition(mapped_x, mapped_y)
                self.OnMouseMove()
                interactor.SetEventPosition(current_x, current_y)
            else:
                self.OnMouseMove()
            self._measurement_callback("refresh", None)

    @staticmethod
    def _display_to_world(renderer: vtkRenderer, x: float, y: float, depth: float) -> np.ndarray:
        renderer.SetDisplayPoint(x, y, depth)
        renderer.DisplayToWorld()
        world = np.asarray(renderer.GetWorldPoint(), dtype=float)
        if abs(world[3]) > 1e-12:
            world = world / world[3]
        return world[:3]

    def _zoom_at_cursor(self, factor: float) -> None:
        interactor = self.GetInteractor()
        x, y = interactor.GetEventPosition()
        self.FindPokedRenderer(x, y)
        renderer = self.GetCurrentRenderer()
        if renderer is None:
            return
        camera = renderer.GetActiveCamera()

        renderer.ResetCameraClippingRange()
        bounds = np.asarray(renderer.ComputeVisiblePropBounds(), dtype=float)
        valid_bounds = (
            bounds.shape == (6,)
            and np.all(np.isfinite(bounds))
            and np.all(bounds[[1, 3, 5]] >= bounds[[0, 2, 4]])
        )
        picked = self._zoom_picker.Pick(x, y, 0.0, renderer)
        anchor = np.asarray(self._zoom_picker.GetPickPosition(), dtype=float) if picked else None
        if anchor is None or anchor.shape != (3,) or not np.all(np.isfinite(anchor)):
            plane_point = (
                (bounds[[0, 2, 4]] + bounds[[1, 3, 5]]) * 0.5
                if valid_bounds
                else np.asarray(camera.GetFocalPoint(), dtype=float)
            )
            near_point = self._display_to_world(renderer, x, y, 0.0)
            far_point = self._display_to_world(renderer, x, y, 1.0)
            cursor_ray = far_point - near_point
            plane_normal = np.asarray(camera.GetDirectionOfProjection(), dtype=float)
            denominator = float(cursor_ray @ plane_normal)
            if abs(denominator) > 1e-12:
                amount = float((plane_point - near_point) @ plane_normal) / denominator
                anchor = near_point + cursor_ray * amount
            else:
                anchor = plane_point

        if camera.GetParallelProjection():
            camera.SetParallelScale(camera.GetParallelScale() / factor)
            renderer.SetWorldPoint(*anchor, 1.0)
            renderer.WorldToDisplay()
            anchor_depth = renderer.GetDisplayPoint()[2]
            cursor_world = self._display_to_world(renderer, x, y, anchor_depth)
            offset = anchor - cursor_world
            focal_offset = offset
        else:
            position = np.asarray(camera.GetPosition(), dtype=float)
            ray = anchor - position
            distance = float(np.linalg.norm(ray))
            if valid_bounds:
                diagonal = float(np.linalg.norm(bounds[[1, 3, 5]] - bounds[[0, 2, 4]]))
            else:
                diagonal = 0.0
            minimum_step = max(diagonal * 0.0015, 1e-6)
            view_direction = np.asarray(camera.GetDirectionOfProjection(), dtype=float)
            view_direction /= max(float(np.linalg.norm(view_direction)), 1e-12)
            forward_depth = float(ray @ view_direction)
            if distance <= 1e-12 or forward_depth <= minimum_step:
                # Once the cursor surface reaches the camera, continue through it in the current
                # viewing direction. Following a point behind the camera would reverse the axis.
                ray = view_direction
                distance = 0.0
            else:
                ray /= distance
            proportional_step = distance * abs(1.0 - 1.0 / factor)
            direction = 1.0 if factor > 1.0 else -1.0
            offset = ray * direction * max(proportional_step, minimum_step)
            # Move the focal point only by the sideways part of the cursor-ray movement. The
            # forward part changes camera distance, preventing the fixed-distance stall while the
            # lateral part keeps the selected screen position anchored under the pointer.
            focal_offset = offset - view_direction * float(offset @ view_direction)
            safe_focal_distance = max(diagonal * 0.002, 1e-5)
            remaining_focal_distance = camera.GetDistance() - float(offset @ view_direction)
            if remaining_focal_distance < safe_focal_distance:
                # Carry the focal point forward only as much as needed to preserve camera
                # orientation. This prevents VTK from flipping the view when zoom passes through
                # a surface while retaining the minimum useful movement per wheel step.
                focal_offset += view_direction * (
                    safe_focal_distance - remaining_focal_distance
                )
        if np.all(np.isfinite(offset)):
            camera.SetPosition(*(np.asarray(camera.GetPosition(), dtype=float) + offset))
            camera.SetFocalPoint(*(np.asarray(camera.GetFocalPoint(), dtype=float) + focal_offset))
        renderer.ResetCameraClippingRange()
        interactor.Render()

    def _wheel_forward(self, _obj, _event) -> None:
        self._crop_callback("navigation", None)
        if self.GetInteractor().GetControlKey():
            self._roll_at_view_center(-5.0 if not self.invert_horizontal else 5.0)
            return
        self._zoom_at_cursor(1.0 / 1.20 if self.invert_zoom else 1.20)
        self._measurement_callback("refresh", None)

    def _wheel_backward(self, _obj, _event) -> None:
        self._crop_callback("navigation", None)
        if self.GetInteractor().GetControlKey():
            self._roll_at_view_center(5.0 if not self.invert_horizontal else -5.0)
            return
        self._zoom_at_cursor(1.20 if self.invert_zoom else 1.0 / 1.20)
        self._measurement_callback("refresh", None)

    def _roll_at_view_center(self, degrees: float) -> None:
        interactor = self.GetInteractor()
        x, y = interactor.GetEventPosition()
        self.FindPokedRenderer(x, y)
        renderer = self.GetCurrentRenderer()
        if renderer is None:
            return
        camera = renderer.GetActiveCamera()
        camera.Roll(degrees)
        camera.OrthogonalizeViewUp()
        renderer.ResetCameraClippingRange()
        interactor.Render()

    def _key_press(self, _obj, _event) -> None:
        key = self.GetInteractor().GetKeySym().lower()
        if key in ("return", "enter") and self._crop_callback("confirm", None):
            return
        if key == "escape" and self._crop_callback("cancel", None):
            return
        if self._keyboard_nav_callback(
            key,
            bool(self.GetInteractor().GetControlKey()),
            bool(self.GetInteractor().GetShiftKey()),
        ):
            return
        self.OnKeyPress()

    def _key_release(self, _obj, _event) -> None:
        if self.GetInteractor().GetKeySym().lower() in ("shift_l", "shift_r", "shift"):
            self._measurement_callback("hide", None)
        self.OnKeyRelease()


def mesh_surface_area(points: np.ndarray, faces: np.ndarray) -> float:
    a = points[faces[:, 0]]
    b = points[faces[:, 1]]
    c = points[faces[:, 2]]
    return float((0.5 * np.linalg.norm(np.cross(b - a, c - a), axis=1)).sum())


def smart_target(points: np.ndarray, faces: np.ndarray, quality: str) -> int:
    bounds_min = points.min(axis=0)
    bounds_max = points.max(axis=0)
    diagonal = float(np.linalg.norm(bounds_max - bounds_min))
    if diagonal <= 0:
        return min(50_000, len(faces))
    desired_edge = diagonal / SMART_DIVISORS[quality]
    ideal_triangle_area = (math.sqrt(3.0) / 4.0) * desired_edge * desired_edge
    estimate = round(mesh_surface_area(points, faces) / ideal_triangle_area)
    # The surface-area estimate remains the driver, while the quality bands
    # prevent a noisy scan from making every preset nearly full density.
    quality_cap = {"Draft": 0.15, "Balanced": 0.50, "Fine": 0.75}[quality]
    upper = min(750_000, max(1_000, round(len(faces) * quality_cap)))
    return max(10_000, min(upper, estimate))


def point_density_colors(
    points: np.ndarray,
    faces: np.ndarray,
    cancel_event: threading.Event | None = None,
) -> np.ndarray:
    """Return RGB colors from smoothed local spacing and robust log-density z-scores."""
    point_count = len(points)
    incident_count = np.bincount(faces.ravel(), minlength=point_count).astype(np.float32)
    incident_area = np.zeros(point_count, dtype=np.float32)
    chunk_size = 250_000
    for start in range(0, len(faces), chunk_size):
        if cancel_event is not None and cancel_event.is_set():
            raise OperationCancelled
        chunk = faces[start:start + chunk_size]
        a = points[chunk[:, 0]]
        b = points[chunk[:, 1]]
        c = points[chunk[:, 2]]
        area = 0.5 * np.linalg.norm(np.cross(b - a, c - a), axis=1)
        incident_area += np.bincount(
            chunk.ravel(), weights=np.repeat(area, 3), minlength=point_count
        ).astype(np.float32, copy=False)

    valid = (incident_count > 0) & (incident_area > 0)
    log_density = np.zeros(point_count, dtype=np.float32)
    # Vertices per incident surface area is the local sampling density. Work in log space so
    # scan-density outliers remain visible without allowing them to dominate the color range.
    log_density[valid] = np.log(
        np.maximum(incident_count[valid] / incident_area[valid], np.float32(1e-30))
    )

    # One-ring smoothing makes regional density visible at normal zoom while retaining
    # narrow oversampled bands. Each face contributes its other two vertices as neighbors.
    neighbor_sum = np.zeros(point_count, dtype=np.float32)
    neighbor_count = np.zeros(point_count, dtype=np.float32)
    for start in range(0, len(faces), chunk_size):
        if cancel_event is not None and cancel_event.is_set():
            raise OperationCancelled
        chunk = faces[start:start + chunk_size]
        face_mean = log_density[chunk].mean(axis=1)
        destinations = chunk.ravel()
        neighbor_sum += np.bincount(
            destinations, weights=np.repeat(face_mean, 3), minlength=point_count
        ).astype(np.float32, copy=False)
        neighbor_count += np.bincount(destinations, minlength=point_count).astype(
            np.float32, copy=False
        )
    smoothed = np.divide(
        log_density + neighbor_sum,
        1.0 + neighbor_count,
        out=log_density.copy(),
        where=(1.0 + neighbor_count) > 0,
    )

    normalized = np.zeros(point_count, dtype=np.float64)
    if np.any(valid):
        values = smoothed[valid]
        median = float(np.median(values))
        mad = float(np.median(np.abs(values - median)))
        robust_sigma = max(1.4826 * mad, 1e-12)
        robust_z = np.clip((smoothed - median) / robust_sigma, -8.0, 8.0)
        # 1.702*z closely approximates a normal CDF without adding a heavy statistics dependency.
        bell_curve = 1.0 / (1.0 + np.exp(-1.702 * robust_z))
        # Retain rank contrast for multimodal scans while allowing statistical outliers to flare red.
        low, high = np.percentile(values, (0.5, 99.5))
        rank_contrast = np.clip((smoothed - low) / max(high - low, 1e-12), 0.0, 1.0)
        normalized = np.maximum(bell_curve, 0.80 * rank_contrast)
        normalized[~valid] = 0.0

    stops = np.asarray(
        [[18, 48, 112], [25, 154, 214], [87, 224, 184], [250, 204, 21], [226, 55, 48]],
        dtype=np.float64,
    )
    scaled = normalized * (len(stops) - 1)
    lower = np.minimum(scaled.astype(np.int32), len(stops) - 2)
    blend = (scaled - lower)[:, None]
    return np.ascontiguousarray(
        np.rint(stops[lower] * (1.0 - blend) + stops[lower + 1] * blend).astype(np.uint8)
    )


def point_density_cell_colors(
    point_colors: np.ndarray,
    faces: np.ndarray,
    cancel_event: threading.Event | None = None,
) -> np.ndarray:
    """Convert point density colors to stable per-triangle colors for surface rendering."""
    colors = np.empty((len(faces), 3), dtype=np.uint8)
    chunk_size = 250_000
    for start in range(0, len(faces), chunk_size):
        if cancel_event is not None and cancel_event.is_set():
            raise OperationCancelled
        chunk = faces[start:start + chunk_size]
        colors[start:start + len(chunk)] = np.rint(
            point_colors[chunk].astype(np.float32).mean(axis=1)
        ).astype(np.uint8)
    return colors


def density_balance_arrays(
    points: np.ndarray, faces: np.ndarray, target: int, aggressiveness: float
) -> tuple[np.ndarray, np.ndarray]:
    """Use conservative QEM so redundant flat sampling collapses before geometric detail."""
    # QEM already incorporates local surface curvature in its accumulated plane error. The old
    # voxel-average prepass moved vertices before measuring that error and visibly distorted scans.
    quality_aggressiveness = min(5.0, max(0.0, aggressiveness * 0.70))
    return fast_simplification.simplify(
        points,
        faces,
        target_count=target,
        agg=quality_aggressiveness,
        verbose=False,
        preserve_border=True,
    )


def simplify_arrays(
    points: np.ndarray,
    faces: np.ndarray,
    target: int,
    algorithm: str,
    aggressiveness: float = 7.0,
) -> tuple[np.ndarray, np.ndarray]:
    reduction = 1.0 - target / len(faces)
    if algorithm == "Fast QEM":
        return fast_simplification.simplify(
            points, faces, target_reduction=reduction, agg=aggressiveness, verbose=False
        )
    if algorithm == "Density balanced":
        return density_balance_arrays(points, faces, target, aggressiveness)
    source = arrays_polydata(points, faces)
    if algorithm == "Shape preserving":
        decimator = vtkQuadricDecimation()
        decimator.SetInputData(source)
        decimator.SetTargetReduction(reduction)
        decimator.VolumePreservationOn()
    elif algorithm == "Preserve topology":
        decimator = vtkDecimatePro()
        decimator.SetInputData(source)
        decimator.SetTargetReduction(reduction)
        decimator.PreserveTopologyOn()
        decimator.SplittingOff()
        decimator.BoundaryVertexDeletionOff()
    else:
        raise ValueError(f"Unknown optimization algorithm: {algorithm}")
    decimator.Update()
    return polydata_arrays(decimator.GetOutput())


def simplify_process_job(points, faces, target: int, algorithm: str):
    """Run native simplification outside the UI process."""
    try:
        p_out, f_out = simplify_arrays(points, faces, target, algorithm)
        return p_out, f_out, None
    except Exception:
        return None, None, traceback.format_exc()


def cli_main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="MeshMillCLI",
        description="Optimize an STL locally without changing its coordinate scale.",
    )
    parser.add_argument("input", type=Path, help="Input STL file")
    parser.add_argument("-o", "--output", type=Path, help="Output STL filename")
    choice = parser.add_mutually_exclusive_group()
    choice.add_argument("-t", "--target", type=int, help="Target triangle count")
    choice.add_argument(
        "-p", "--preset", choices=sorted(PRESETS), default="balanced",
        help="light=50k, balanced=200k, detailed=400k (default: balanced)",
    )
    parser.add_argument(
        "-a", "--aggressiveness", type=float, default=7.0,
        help="0 favors quality, 7 is balanced, 10 favors speed (default: 7)",
    )
    parser.add_argument(
        "--algorithm", choices=sorted(CLI_ALGORITHMS), default="fast",
        help="fast, density, shape, or topology (default: fast)",
    )
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing output file")
    args = parser.parse_args(argv)

    source = args.input.expanduser().resolve()
    if not source.is_file():
        parser.error(f"input file does not exist: {source}")
    if source.suffix.lower() != ".stl":
        parser.error("input must be an STL file")
    target = args.target if args.target is not None else PRESETS[args.preset]
    if target < 1_000:
        parser.error("target must be at least 1000 triangles")
    if not 0 <= args.aggressiveness <= 10:
        parser.error("aggressiveness must be between 0 and 10")
    output = args.output
    if output is None:
        output = source.with_name(f"{source.stem}_{target // 1000}k.stl")
    else:
        output = output.expanduser().resolve()
    if output == source:
        parser.error("output must differ from input")
    if output.exists() and not args.overwrite:
        parser.error(f"output already exists: {output} (use --overwrite to replace it)")
    output.parent.mkdir(parents=True, exist_ok=True)

    print(f"Loading: {source}", flush=True)
    poly, points, faces = load_stl(source)
    original_count = len(faces)
    original_size = np.asarray(bounds_size(poly.GetBounds()))
    print(f"Original: {original_count:,} triangles", flush=True)
    print(f"Dimensions: {fmt_size(tuple(original_size))}", flush=True)
    if target >= original_count:
        parser.error(f"target {target:,} is not smaller than the source ({original_count:,})")

    print(
        f"Optimizing to about {target:,} triangles "
        f"(aggressiveness {args.aggressiveness:g})...",
        flush=True,
    )
    reduced_points, reduced_faces = simplify_arrays(
        points, faces, target, CLI_ALGORITHMS[args.algorithm], args.aggressiveness
    )
    reduced = arrays_polydata(reduced_points, reduced_faces)
    reduced_size = np.asarray(bounds_size(reduced.GetBounds()))
    drift = np.abs(reduced_size - original_size)
    save_stl(reduced, output)
    print(f"Result: {len(reduced_faces):,} triangles", flush=True)
    print(f"Dimensions: {fmt_size(tuple(reduced_size))}", flush=True)
    print(f"Dimension drift: {fmt_size(tuple(drift))}", flush=True)
    print(f"Saved: {output}", flush=True)
    return 0


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.settings = QSettings("MeshMill", "MeshMill")
        self.settings.remove("rendering/gpu_preference")
        self.locale_preference = str(self.settings.value("interface/locale", "system"))
        self.locale_code = locale_manager.select(self._resolved_locale(self.locale_preference))
        self.shortcuts = {
            shortcut_id: QKeySequence(
                str(self.settings.value(f"shortcuts/{shortcut_id}", default_sequence))
            ).toString(QKeySequence.SequenceFormat.PortableText)
            for shortcut_id, (_label, default_sequence) in SHORTCUT_DEFINITIONS.items()
        }
        self.setWindowTitle(APP_NAME)
        self.setStyleSheet(APP_STYLESHEET)
        icon_path = resource_path("assets/meshmill-mark.svg")
        if icon_path.exists():
            self.setWindowIcon(QIcon(os.fspath(icon_path)))
        self.resize(1180, 780)
        self.tools_side = str(self.settings.value("interface/tools_side", "Right"))
        units_default_version = self.settings.value("interface/units_default_version", 0, type=int)
        self.default_units = (
            "cm"
            if units_default_version < 2
            else str(self.settings.value("interface/default_units", "cm"))
        )
        if self.default_units not in UNIT_MM:
            self.default_units = "cm"
        self.settings.setValue("interface/default_units", self.default_units)
        self.settings.setValue("interface/units_default_version", 2)
        self.large_mesh_mode = str(self.settings.value("performance/large_mesh_mode", "auto"))
        if self.large_mesh_mode not in {"auto", "full", "overview"}:
            self.large_mesh_mode = "auto"
        saved_memory_percent = self.settings.value(
            "performance/memory_percent", 50, type=int
        )
        self.large_mesh_memory_percent = max(
            20, min(80, round(saved_memory_percent / 5) * 5)
        )
        self.overview_triangle_limit = max(
            50_000,
            min(2_000_000, self.settings.value("performance/overview_triangles", 250_000, type=int)),
        )
        legacy_mouse = self.settings.value("navigation/invert_mouse", False, type=bool)
        legacy_keyboard = self.settings.value("navigation/invert_keyboard", False, type=bool)
        legacy_horizontal = self.settings.value(
            "navigation/invert_horizontal", False, type=bool
        )
        legacy_vertical = self.settings.value("navigation/invert_vertical", False, type=bool)
        legacy_zoom = self.settings.value("navigation/invert_zoom", False, type=bool)
        self.mouse_horizontal = self.settings.value(
            "navigation/mouse_horizontal", legacy_mouse or legacy_horizontal, type=bool
        )
        self.mouse_vertical = self.settings.value(
            "navigation/mouse_vertical", legacy_mouse or legacy_vertical, type=bool
        )
        self.mouse_zoom = self.settings.value(
            "navigation/mouse_zoom", legacy_mouse or legacy_zoom, type=bool
        )
        self.keyboard_horizontal = self.settings.value(
            "navigation/keyboard_horizontal", legacy_keyboard or legacy_horizontal, type=bool
        )
        self.keyboard_vertical = self.settings.value(
            "navigation/keyboard_vertical", legacy_keyboard or legacy_vertical, type=bool
        )
        self.keyboard_zoom = self.settings.value(
            "navigation/keyboard_zoom", legacy_keyboard or legacy_zoom, type=bool
        )
        self.source_path: Path | None = None
        self.loaded_triangle_count = 0
        self.source_poly: vtkPolyData | None = None
        self.source_points: np.ndarray | None = None
        self.source_faces: np.ndarray | None = None
        self.preview_poly: vtkPolyData | None = None
        self.preview_actor: vtkActor | None = None
        self.source_actor: vtkActor | None = None
        self.simplified_actor: vtkActor | None = None
        self.previous_view_poly: vtkPolyData | None = None
        self.previous_view_actor: vtkActor | None = None
        self.active_actor: vtkActor | None = None
        self.loupe_renderer: vtkRenderer | None = None
        self.loupe_actor: vtkActor | None = None
        self.loupe_frame: QFrame | None = None
        self.loupe_widget: QVTKRenderWindowInteractor | None = None
        self.loupe_label: QLabel | None = None
        self.showing_original = False
        self.showing_previous = False
        self.dimension_drift_model_units: np.ndarray | None = None
        self.generation = 0
        self.busy = False
        self.loading = False
        self.active_operation = ""
        self.operation_snapshot: dict | None = None
        self.operation_cancel_event: threading.Event | None = None
        self.operation_future = None
        self.operation_uses_process = False
        self.load_generation = 0
        self.edit_generation = 0
        self.density_generation = 0
        self.density_cache: dict[int, np.ndarray] = {}
        self.pending_density_poly: vtkPolyData | None = None
        self.load_started_at = 0.0
        self.geometry_activity_until = 0.0
        self.geometry_activity_label = "Idle"
        self.pending_target: int | None = None
        self.running_target: int | None = None
        self.preview_dirty = True
        self.pass_ready = False
        self.preview_is_selection = False
        self.mesh_modified = False
        self.control_key_held = False
        self.saved_standard_views: dict[str, tuple[np.ndarray, np.ndarray]] = {}
        self.has_committed_optimization = False
        self.overview_mode = False
        self.overview_total_triangles = 0
        self.crop_start: QPoint | None = None
        self.crop_candidate: tuple[vtkPolyData, np.ndarray, np.ndarray, np.ndarray] | None = None
        self.crop_info_frame: QFrame | None = None
        self.crop_info_label: QLabel | None = None
        self.selection_undo_button: QPushButton | None = None
        self.crop_info_user_positioned = False
        self.crop_points: list[QPoint] = []
        self.crop_drag_index: int | None = None
        self.crop_selection_actor: vtkActor | None = None
        self.crop_overlay_actors: list[vtkActor2D] = []
        self.measure_points: list[np.ndarray] = []
        self.measure_hover_world: np.ndarray | None = None
        self.measure_pending_position: tuple[int, int] | None = None
        self.measure_overlay_actor: vtkActor2D | None = None
        self.measure_info_frame: QFrame | None = None
        self.measure_info_label: QLabel | None = None
        self.measure_units: ArrowComboBox | None = None
        self.measure_units_overridden = False
        self.measure_picker: vtkHardwarePicker | None = None
        self.selected_face_mask: np.ndarray | None = None
        self.selection_undo_stack: list[np.ndarray | None] = []
        self.selection_base_quality: str | None = None
        self.selection_base_algorithm: str | None = None
        self.selection_base_target: int | None = None
        self.selection_target: int | None = None
        self.undo_stack: list[MeshHistoryState] = []
        self.redo_stack: list[MeshHistoryState] = []
        self.undo_bytes = 0
        self.redo_bytes = 0
        self.undo_limit_bytes = 1_000_000_000
        self.logical_cpu_count = max(1, os.cpu_count() or 1)
        self.vram_capacity_bytes = dedicated_vram_capacity()
        self._last_cpu_times: tuple[int, int, int] | None = None
        self.gpu_counters = WindowsGpuCounters()
        self.verification_screenshot: Path | None = None
        self.diagnostic_log_path: Path | None = None
        self._last_diagnostic_camera_time = 0.0
        self.executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="mesh-reducer")
        self.optimization_executor = ProcessPoolExecutor(
            max_workers=1, mp_context=multiprocessing.get_context("spawn")
        )
        self.bridge = ResultBridge()
        self.bridge.done.connect(self._finish_simplify)
        self.load_bridge = LoadBridge()
        self.load_bridge.done.connect(self._finish_load)
        self.edit_bridge = EditBridge()
        self.edit_bridge.done.connect(self._finish_mesh_edit)
        self.density_bridge = DensityBridge()
        self.density_bridge.done.connect(self._finish_density_analysis)
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.setInterval(650)
        self.timer.timeout.connect(self.preview)
        self.measure_pick_timer = QTimer(self)
        self.measure_pick_timer.setSingleShot(True)
        self.measure_pick_timer.setInterval(35)
        self.measure_pick_timer.timeout.connect(self._update_measure_hover)

        root = QWidget()
        root.setObjectName("mainRoot")
        self.setCentralWidget(root)
        outer = QHBoxLayout(root)
        self.outer_layout = outer

        controls = QScrollArea(root)
        self.controls_widget = controls
        controls.setWidgetResizable(True)
        controls.setFrameShape(QFrame.Shape.NoFrame)
        controls.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        controls.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        controls.setFixedWidth(352)
        controls_content = QWidget(controls)
        self.controls_content = controls_content
        self._busy_control_states: dict[QWidget, bool] = {}
        controls_content.setObjectName("controlsContent")
        controls.setWidget(controls_content)
        panel = QVBoxLayout(controls_content)
        panel.setAlignment(Qt.AlignmentFlag.AlignTop)

        def field_label(text: str, help_text: str) -> QLabel:
            label = QLabel(text)
            label.setToolTip(help_text)
            return label

        brand_row = QHBoxLayout()
        brand_row.addStretch(1)
        brand_logo = QLabel()
        brand_logo.setFixedSize(310, 78)
        brand_logo.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        logo_path = resource_path("assets/meshmill-logo.svg")
        if logo_path.exists():
            brand_logo.setPixmap(
                QPixmap(os.fspath(logo_path)).scaled(
                    310,
                    78,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        brand_row.addWidget(brand_logo)
        panel.addLayout(brand_row)

        self.open_button = QPushButton("Open STL…")
        self.open_button.setProperty("accent", True)
        self.open_button.clicked.connect(self.open_file)

        self.reload_button = QPushButton("Reload Original Mesh")
        self.reload_button.setProperty("quiet", True)
        self.reload_button.setEnabled(False)
        self.reload_button.clicked.connect(self._reload_original)

        self.undo_button = QPushButton("Undo")
        self.undo_button.setProperty("quiet", True)
        self.undo_button.setEnabled(False)
        self.undo_button.clicked.connect(self._undo_working_mesh)
        self.cancel_preview_button = QPushButton("Cancel")
        self.cancel_preview_button.setProperty("quiet", True)
        self.cancel_preview_button.setEnabled(False)
        self.cancel_preview_button.setToolTip(
            "Discard the optimized result and return to the original mesh."
        )
        self.cancel_preview_button.clicked.connect(self._cancel_optimized_preview)
        self.redo_button = QPushButton("Redo")
        self.redo_button.setProperty("quiet", True)
        self.redo_button.setEnabled(False)
        self.redo_button.clicked.connect(self._redo_working_mesh)
        self.history_actions = QFrame()
        history_row = QHBoxLayout(self.history_actions)
        history_row.setContentsMargins(0, 0, 0, 0)
        history_row.addWidget(self.undo_button)
        history_row.addWidget(self.cancel_preview_button)
        history_row.addWidget(self.redo_button)

        def tool_section(title_text: str) -> QVBoxLayout:
            frame = QFrame(controls_content)
            frame.setObjectName("toolSection")
            layout = QVBoxLayout(frame)
            layout.setContentsMargins(9, 7, 9, 9)
            layout.setSpacing(6)
            heading = QLabel(title_text, frame)
            heading.setObjectName("sectionTitle")
            layout.addWidget(heading)
            panel.addWidget(frame)
            return layout

        optimization_panel = tool_section("OPTIMIZATION")
        stats_panel = tool_section("STATS")
        general_panel = tool_section("GENERAL")

        self.file_label = QLabel("No file loaded")
        self.file_label.setObjectName("fileCard")
        self.file_label.setWordWrap(True)
        self.file_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        file_row = QHBoxLayout()
        file_row.setSpacing(4)
        file_row.addWidget(self.file_label, 1)
        self.open_file_folder_button = QPushButton("📁")
        self.open_file_folder_button.setFixedWidth(30)
        self.open_file_folder_button.setEnabled(False)
        self.open_file_folder_button.setToolTip("Open the folder containing this STL.")
        self.open_file_folder_button.clicked.connect(self._open_source_folder)
        file_row.addWidget(self.open_file_folder_button)
        self.copy_file_path_button = QPushButton("⧉")
        self.copy_file_path_button.setFixedWidth(30)
        self.copy_file_path_button.setEnabled(False)
        self.copy_file_path_button.setToolTip("Copy the full STL path to the clipboard.")
        self.copy_file_path_button.clicked.connect(self._copy_source_path)
        file_row.addWidget(self.copy_file_path_button)
        stats_panel.addLayout(file_row)

        stats = QGridLayout()
        stats.addWidget(field_label("Original triangles:", "Triangle count before the pending optimization is applied."), 0, 0)
        self.original_count = QLabel("—")
        stats.addWidget(self.original_count, 0, 1)
        stats.addWidget(field_label("Original vertices:", "Vertex count before the pending optimization is applied."), 1, 0)
        self.original_vertices = QLabel("—")
        stats.addWidget(self.original_vertices, 1, 1)
        stats.addWidget(field_label("Optimized triangles:", "Triangle count in the optimized result."), 2, 0)
        self.preview_count = QLabel("—")
        stats.addWidget(self.preview_count, 2, 1)
        stats.addWidget(field_label("Optimized vertices:", "Vertex count in the optimized result."), 3, 0)
        self.preview_vertices = QLabel("—")
        stats.addWidget(self.preview_vertices, 3, 1)
        self.dimensions_caption = QLabel("Dimensions (mm):")
        self.dimensions_caption.setToolTip("Overall X × Y × Z size of the original mesh.")
        stats.addWidget(self.dimensions_caption, 4, 0, Qt.AlignmentFlag.AlignTop)
        self.dimensions = QLabel("—")
        self.dimensions.setWordWrap(True)
        stats.addWidget(self.dimensions, 4, 1)
        stats.addWidget(
            field_label(
                "Dimension drift:",
                "Absolute change in the optimized result's X, Y, and Z bounding-box dimensions.",
            ),
            5,
            0,
        )
        self.drift = QLabel("—")
        stats.addWidget(self.drift, 5, 1)
        stats.addWidget(
            field_label(
                "Reduction:",
                "Percentage of the original STL triangles removed from the current mesh.",
            ),
            6,
            0,
        )
        self.optimization_ratio = QLabel("—")
        stats.addWidget(self.optimization_ratio, 6, 1)
        stats.addWidget(field_label("Original file:", "Size of the STL file opened from disk."), 7, 0)
        self.original_file_size = QLabel("—")
        stats.addWidget(self.original_file_size, 7, 1)
        stats.addWidget(field_label("Estimated output:", "Estimated binary STL size at the current target."), 8, 0)
        self.estimated_file_size = QLabel("—")
        stats.addWidget(self.estimated_file_size, 8, 1)
        stats_panel.addLayout(stats)

        units_row = QHBoxLayout()
        units_row.addWidget(field_label("Model units", "Units used to display dimensions. STL coordinates are unchanged."))
        self.units = ArrowComboBox()
        self.units.addItems(["mm", "cm", "m", "in", "ft"])
        self.units.currentTextChanged.connect(self._units_changed)
        self.units.setCurrentText(self.default_units)
        self._units_changed(self.default_units)
        units_row.addWidget(self.units, 1)
        stats_panel.addLayout(units_row)

        self.preview_button = QPushButton("Optimize")
        self.preview_button.setProperty("accent", True)
        self._set_primary_action(False, False)
        self.preview_button.clicked.connect(self._primary_optimize_action)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 1000)
        self.slider.setValue(500)
        self.slider.valueChanged.connect(self._slider_changed)
        optimization_panel.addWidget(self.slider)

        optimization_panel.addWidget(field_label("Target triangles", "Requested triangle count for whole-mesh or selected-region optimization."))
        self.target = QSpinBox()
        self.target.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self.target.setRange(1_000, 5_000_000)
        self.target.setSingleStep(10_000)
        self.target.setValue(200_000)
        self.target.valueChanged.connect(self._target_changed)
        optimization_panel.addWidget(self.target)

        presets = QHBoxLayout()
        self.preset_buttons: list[QPushButton] = []
        for _ in range(4):
            button = QPushButton("—")
            button.setProperty("preset_value", 1000)
            button.clicked.connect(
                lambda _=False, b=button: self.target.setValue(int(b.property("preset_value")))
            )
            presets.addWidget(button)
            self.preset_buttons.append(button)
        optimization_panel.addLayout(presets)

        smart_row = QHBoxLayout()
        smart_row.addWidget(field_label("Smart quality", "Automatic density level used when calculating a target."))
        self.smart_quality = ArrowComboBox()
        self.smart_quality.addItems(list(SMART_DIVISORS))
        self.smart_quality.setCurrentText("Balanced")
        self.smart_quality.currentTextChanged.connect(self._apply_smart_target)
        smart_row.addWidget(self.smart_quality, 1)
        self.smart_button = QPushButton("Auto target")
        self.smart_button.clicked.connect(self._apply_smart_target)
        smart_row.addWidget(self.smart_button)
        optimization_panel.addLayout(smart_row)

        algorithm_row = QHBoxLayout()
        algorithm_row.addWidget(field_label("Algorithm", "Geometry optimization method used for the next operation."))
        self.algorithm = ArrowComboBox()
        self.algorithm.addItems(ALGORITHMS)
        self.algorithm.currentTextChanged.connect(self._algorithm_changed)
        algorithm_row.addWidget(self.algorithm, 1)
        optimization_panel.addLayout(algorithm_row)

        self.display_type = ArrowComboBox(self)
        for mode in DISPLAY_MODES:
            shortcut = self.shortcuts[f"display_{mode.lower()}"]
            self.display_type.addItem(f"{mode} ({shortcut})", mode)
        saved_display = str(self.settings.value("display/type", "Shaded"))
        saved_display = {
            "Point matrix": "Vertices",
            "Point density matrix": "Density",
        }.get(saved_display, saved_display)
        saved_index = self.display_type.findData(saved_display)
        if saved_index >= 0:
            self.display_type.setCurrentIndex(saved_index)
        self.display_type.currentIndexChanged.connect(
            lambda _index: self._apply_display_mode(self._display_mode())
        )
        display_row = QHBoxLayout()
        display_row.addWidget(
            field_label("Display type", "Choose how mesh geometry and point density are drawn.")
        )
        display_row.addWidget(self.display_type, 1)
        optimization_panel.addLayout(display_row)
        general_panel.addWidget(self.open_button)
        general_panel.addWidget(self.reload_button)

        # Selection removal stays keyboard-driven (Delete and Escape). Keep internal controls for
        # shared enabled-state handling without adding redundant disabled buttons to the toolbox.
        self.delete_selection_button = QPushButton("Delete selected", self.controls_content)
        self.delete_selection_button.setEnabled(False)
        self.delete_selection_button.clicked.connect(self._delete_selected)
        self.delete_selection_button.hide()
        self.clear_selection_button = QPushButton("Clear selection", self.controls_content)
        self.clear_selection_button.setEnabled(False)
        self.clear_selection_button.clicked.connect(self._clear_selection)
        self.clear_selection_button.hide()
        optimization_panel.addWidget(self.history_actions)

        self.toggle_mesh_button = QPushButton("Show original")
        self.toggle_mesh_button.setEnabled(False)
        self.toggle_mesh_button.clicked.connect(self._toggle_mesh)

        self.previous_mesh_button = QPushButton("Show previous")
        self.previous_mesh_button.setEnabled(False)
        self.previous_mesh_button.clicked.connect(self._toggle_previous_mesh)

        self.comparison_actions = QFrame()
        comparison_row = QHBoxLayout(self.comparison_actions)
        comparison_row.setContentsMargins(0, 0, 0, 0)
        comparison_row.addWidget(self.toggle_mesh_button)
        comparison_row.addWidget(self.previous_mesh_button)

        self.status = QLabel("Open STL")
        self.status.setWordWrap(True)
        self.status.setStyleSheet("color: #5E6B80;")
        optimization_panel.addWidget(self.status)

        optimization_panel.addWidget(self.preview_button)
        optimization_panel.addWidget(self.comparison_actions)

        self.save_button = QPushButton("Save current mesh…")
        self.save_button.setProperty("accent", True)
        self.save_button.setEnabled(self.mesh_modified)
        self.save_button.clicked.connect(self.save_file)
        general_panel.addWidget(self.save_button)
        self._update_action_row_visibility()
        info_row = QHBoxLayout()
        self.settings_button = QPushButton("Settings")
        self.settings_button.setProperty("quiet", True)
        self.settings_button.clicked.connect(self._show_settings)
        info_row.addWidget(self.settings_button)
        self.about_button = QPushButton("About")
        self.about_button.setProperty("quiet", True)
        self.about_button.clicked.connect(self._show_about)
        info_row.addWidget(self.about_button)
        self.repository_button = QPushButton("GitHub")
        self.repository_button.setProperty("quiet", True)
        self.repository_button.setEnabled(bool(REPOSITORY_URL))
        self.repository_button.clicked.connect(self._open_repository)
        info_row.addWidget(self.repository_button)
        general_panel.addLayout(info_row)
        panel.addStretch(1)

        viewport_column = QWidget(root)
        self.viewport_column = viewport_column
        viewport_layout = QVBoxLayout(viewport_column)
        viewport_layout.setContentsMargins(0, 0, 0, 0)
        viewport_layout.setSpacing(6)
        self.vtk_widget = QVTKRenderWindowInteractor(viewport_column)
        viewport_layout.addWidget(self.vtk_widget, 1)
        self._create_loading_panel()
        self._create_metrics_panel(viewport_layout)
        self._apply_tools_side(self.tools_side)
        self.renderer = vtkRenderer()
        self.renderer.SetBackground(0.043, 0.106, 0.204)
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.vtk_widget.GetRenderWindow().SetMultiSamples(8)
        self.vtk_widget.Initialize()
        self.navigation_style = MeshInteractorStyle(
            self.vtk_widget, self._show_loupe, self._crop_interaction, self._keyboard_navigate,
            self._measurement_interaction,
        )
        self.measure_picker = vtkHardwarePicker()
        self.navigation_style.invert_horizontal = self.mouse_horizontal
        self.navigation_style.invert_vertical = self.mouse_vertical
        self.navigation_style.invert_zoom = self.mouse_zoom
        self.vtk_widget.GetRenderWindow().GetInteractor().SetInteractorStyle(self.navigation_style)
        self._create_view_pad()
        self._create_density_legend()
        QTimer.singleShot(0, self._position_view_pad)
        self.metrics_timer = QTimer(self)
        self.metrics_timer.setInterval(1000)
        self.metrics_timer.timeout.connect(self._update_system_metrics)
        self.metrics_timer.start()
        self.loading_timer = QTimer(self)
        self.loading_timer.setInterval(250)
        self.loading_timer.timeout.connect(self._update_loading_panel)
        self._update_system_metrics()
        self._install_help_tooltips()
        localize_widget_tree(self)
        # Route application commands before focused editors consume standard text shortcuts.
        # The filter is active only while this MeshMill window is active.
        QApplication.instance().installEventFilter(self)

    @staticmethod
    def _resolved_locale(preference: str) -> str:
        if preference != "system":
            return preference
        system_name = QLocale.system().name().replace("_", "-")
        available = {code for code, _name in locale_manager.available_locales()}
        if system_name in available:
            return system_name
        language = system_name.split("-", 1)[0].lower()
        return next(
            (code for code in available if code.lower().split("-", 1)[0] == language),
            DEFAULT_LOCALE,
        )

    def eventFilter(self, watched, event) -> bool:  # noqa: N802
        if event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Control:
            self.control_key_held = True
        elif event.type() == QEvent.Type.KeyRelease and event.key() == Qt.Key.Key_Control:
            self.control_key_held = False
        elif event.type() == QEvent.Type.ApplicationDeactivate:
            self.control_key_held = False
        if watched is self.vtk_widget and event.type() == QEvent.Type.Resize:
            QTimer.singleShot(0, self._position_viewport_overlays)
            return super().eventFilter(watched, event)
        if event.type() == QEvent.Type.EnabledChange and watched in (
            self.undo_button,
            self.cancel_preview_button,
            self.redo_button,
            self.toggle_mesh_button,
            self.previous_mesh_button,
            self.reload_button,
            self.save_button,
            self.preview_button,
            self.open_file_folder_button,
            self.copy_file_path_button,
        ):
            QTimer.singleShot(0, self._update_action_row_visibility)
        if (
            event.type() not in (QEvent.Type.ShortcutOverride, QEvent.Type.KeyPress)
            or not self.isActiveWindow()
        ):
            return super().eventFilter(watched, event)

        modifiers = event.modifiers()
        raw_modifiers = int(modifiers.value)
        if event.key() in {
            Qt.Key.Key_Insert,
            Qt.Key.Key_Home,
            Qt.Key.Key_PageUp,
            Qt.Key.Key_Delete,
            Qt.Key.Key_End,
            Qt.Key.Key_PageDown,
        }:
            # Windows reports the six-key navigation cluster as keypad keys on
            # some keyboards. Treat that hardware flag as irrelevant so the
            # physical keys match the displayed shortcuts.
            modifiers &= ~Qt.KeyboardModifier.KeypadModifier
        combination = QKeyCombination(modifiers, Qt.Key(event.key()))
        sequence = QKeySequence(combination).toString(QKeySequence.SequenceFormat.PortableText)
        matching_actions = [
            shortcut_id for shortcut_id, configured in self.shortcuts.items() if configured == sequence
        ]
        action = None
        callback = None
        for candidate in matching_actions:
            candidate_callback = self._shortcut_callback(candidate)
            if candidate_callback is not None:
                action = candidate
                callback = candidate_callback
                break
        self._diagnostic(
            "key_event",
            event_type=event.type().name,
            key=int(event.key()),
            raw_modifiers=raw_modifiers,
            normalized_sequence=sequence,
            matching_actions=matching_actions,
            resolved_action=action,
            watched=type(watched).__name__ if watched is not None else None,
            focus=type(QApplication.focusWidget()).__name__ if QApplication.focusWidget() else None,
        )
        if action is None or callback is None:
            return super().eventFilter(watched, event)
        navigation_actions = {
            "orbit_left", "orbit_right", "orbit_up", "orbit_down",
            "pan_left", "pan_right", "pan_up", "pan_down",
            "zoom_in", "zoom_out", "roll_counterclockwise", "roll_clockwise",
        }
        if event.isAutoRepeat() and action not in navigation_actions:
            event.accept()
            return True
        if event.type() == QEvent.Type.ShortcutOverride:
            event.accept()
            return True
        callback()
        event.accept()
        return True

    def _update_action_row_visibility(self) -> None:
        if hasattr(self, "history_actions"):
            self.history_actions.setVisible(
                any(
                    button.isEnabled()
                    for button in (
                        self.undo_button, self.cancel_preview_button, self.redo_button
                    )
                )
            )
        if hasattr(self, "comparison_actions"):
            self.comparison_actions.setVisible(
                self.toggle_mesh_button.isEnabled() or self.previous_mesh_button.isEnabled()
            )
        for name in (
            "reload_button",
            "save_button",
            "preview_button",
            "open_file_folder_button",
            "copy_file_path_button",
        ):
            button = getattr(self, name, None)
            if button is not None:
                button.setVisible(button.isEnabled())

    def _shortcut_callback(self, action: str):
        callbacks = {
            "save": self._save_shortcut_activated,
            "undo": self._undo_working_mesh,
            "redo": self._redo_working_mesh,
            "redo_alt": self._redo_working_mesh,
            "selection_optimize": lambda: self._selection_shortcut("optimize"),
            "selection_crop": lambda: self._selection_shortcut("crop"),
            "selection_add": lambda: self._selection_shortcut("add"),
            "selection_delete": (
                (lambda: self._selection_shortcut("delete"))
                if self._selected_triangle_count()
                else None
            ),
            "selection_clear": (
                self._clear_selection_and_ruler
                if self._selected_triangle_count() or self.measure_points or self.measure_hover_world is not None
                else None
            ),
            "display_shaded": lambda: self._set_display_shortcut("Shaded"),
            "display_wireframe": lambda: self._set_display_shortcut("Wireframe"),
            "display_vertices": lambda: self._set_display_shortcut("Vertices"),
            "display_density": lambda: self._set_display_shortcut("Density"),
            "view_left": lambda: self._set_standard_view("left"),
            "view_front": lambda: self._set_standard_view("front"),
            "view_right": lambda: self._set_standard_view("right"),
            "view_top": lambda: self._set_standard_view("top"),
            "view_back": lambda: self._set_standard_view("back"),
            "view_bottom": lambda: self._set_standard_view("bottom"),
            "set_view_left": lambda: self._set_current_view_as("left"),
            "set_view_front": lambda: self._set_current_view_as("front"),
            "set_view_right": lambda: self._set_current_view_as("right"),
            "set_view_top": lambda: self._set_current_view_as("top"),
            "set_view_back": lambda: self._set_current_view_as("back"),
            "set_view_bottom": lambda: self._set_current_view_as("bottom"),
        }
        if action in callbacks:
            return callbacks[action]
        if (
            self.source_poly is None
            or self.busy
            or self.crop_start is not None
        ):
            return None
        navigation = {
            "orbit_left": ("left", False, False),
            "orbit_right": ("right", False, False),
            "orbit_up": ("up", False, False),
            "orbit_down": ("down", False, False),
            "pan_left": ("left", True, False),
            "pan_right": ("right", True, False),
            "pan_up": ("up", True, False),
            "pan_down": ("down", True, False),
            "zoom_in": ("up", True, True),
            "zoom_out": ("down", True, True),
            "roll_counterclockwise": ("left", True, True),
            "roll_clockwise": ("right", True, True),
        }
        if action not in navigation:
            return None
        direction, control, shift = navigation[action]
        return lambda: self._keyboard_navigate(direction, control, shift)

    def _set_display_shortcut(self, mode: str) -> None:
        index = self.display_type.findData(mode)
        if index >= 0:
            self.display_type.setCurrentIndex(index)
        self.settings.setValue("display/type", mode)
        self.status.setText(f"Display: {mode}")

    def _display_mode(self) -> str:
        return str(self.display_type.currentData() or "Shaded")

    def _refresh_display_mode_labels(self) -> None:
        current_mode = self._display_mode()
        with QSignalBlocker(self.display_type):
            for index, mode in enumerate(DISPLAY_MODES):
                shortcut = self.shortcuts[f"display_{mode.lower()}"]
                self.display_type.setItemText(index, f"{mode} ({shortcut})")
            current_index = self.display_type.findData(current_mode)
            if current_index >= 0:
                self.display_type.setCurrentIndex(current_index)

    def _apply_tools_side(self, side: str) -> None:
        self.tools_side = "Left" if side == "Left" else "Right"
        self.outer_layout.removeWidget(self.controls_widget)
        self.outer_layout.removeWidget(self.viewport_column)
        if self.tools_side == "Left":
            self.outer_layout.addWidget(self.controls_widget)
            self.outer_layout.addWidget(self.viewport_column, 1)
        else:
            self.outer_layout.addWidget(self.viewport_column, 1)
            self.outer_layout.addWidget(self.controls_widget)

    def _show_settings(self) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle("MeshMill Settings")
        dialog.setModal(True)
        dialog.resize(620, 760)
        outer = QVBoxLayout(dialog)
        scroll = QScrollArea(dialog)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        content = QWidget(scroll)
        layout = QVBoxLayout(content)
        layout.setSpacing(12)

        def section(title: str) -> QVBoxLayout:
            frame = QFrame(content)
            frame.setObjectName("settingsSection")
            frame.setStyleSheet(
                "QFrame#settingsSection { border: 1px solid #D6DCE5; border-radius: 8px; "
                "background: #FFFFFF; }"
            )
            section_layout = QVBoxLayout(frame)
            section_layout.setContentsMargins(14, 12, 14, 12)
            heading = QLabel(title, frame)
            heading.setStyleSheet("font-weight: 700; border: 0;")
            section_layout.addWidget(heading)
            layout.addWidget(frame)
            return section_layout

        interface_layout = section("Interface")
        form = QFormLayout()

        language = ArrowComboBox(dialog)
        language.addItem("System default", "system")
        for code, name in locale_manager.available_locales():
            language.addItem(name, code)
        locale_index = language.findData(self.locale_preference)
        language.setCurrentIndex(max(0, locale_index))
        language.setToolTip("Application language.")
        form.addRow("Language", language)

        tools_side = ArrowComboBox(dialog)
        tools_side.addItems(["Right", "Left"])
        tools_side.setCurrentText(self.tools_side)
        tools_side.setToolTip("Choose which side of the window contains the tools pane.")
        form.addRow("Tools pane", tools_side)

        default_units = ArrowComboBox(dialog)
        default_units.addItems(list(UNIT_MM))
        default_units.setCurrentText(self.default_units)
        default_units.setToolTip("Units selected when MeshMill starts. STL coordinates are unchanged.")
        form.addRow("Default units", default_units)

        interface_layout.addLayout(form)

        performance_layout = section("Large meshes")
        performance_form = QFormLayout()
        large_mesh_mode = ArrowComboBox(dialog)
        large_mesh_mode.addItem("Auto", "auto")
        large_mesh_mode.addItem("Full mesh", "full")
        large_mesh_mode.addItem("Overview only", "overview")
        large_mesh_mode.setCurrentIndex(max(0, large_mesh_mode.findData(self.large_mesh_mode)))
        large_mesh_mode.setToolTip(
            "Auto checks estimated memory before loading. Oversized binary STL files open as a "
            "bounded overview instead of exhausting system memory."
        )
        performance_form.addRow("Loading", large_mesh_mode)

        memory_percent_control = QWidget(dialog)
        memory_percent_layout = QVBoxLayout(memory_percent_control)
        memory_percent_layout.setContentsMargins(0, 0, 0, 0)
        memory_percent_layout.setSpacing(3)
        memory_percent = QSlider(Qt.Orientation.Horizontal, memory_percent_control)
        memory_percent.setRange(20, 80)
        memory_percent.setSingleStep(5)
        memory_percent.setPageStep(10)
        memory_percent.setTickInterval(10)
        memory_percent.setTickPosition(QSlider.TickPosition.TicksBelow)
        memory_percent.setValue(self.large_mesh_memory_percent)
        memory_percent.setToolTip(
            "Share of currently available RAM that Auto may use for loading a full mesh."
        )
        memory_scale = QHBoxLayout()
        memory_minimum = QLabel("20%", memory_percent_control)
        memory_value = QLabel(memory_percent_control)
        memory_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        memory_value.setStyleSheet("font-weight: 600; color: #2563FF;")
        memory_maximum = QLabel("80%", memory_percent_control)
        memory_scale.addWidget(memory_minimum)
        memory_scale.addStretch(1)
        memory_scale.addWidget(memory_value)
        memory_scale.addStretch(1)
        memory_scale.addWidget(memory_maximum)

        def update_memory_budget(value: int) -> None:
            value = max(20, min(80, round(value / 5) * 5))
            if memory_percent.value() != value:
                with QSignalBlocker(memory_percent):
                    memory_percent.setValue(value)
            budget = round(available_physical_memory() * value / 100.0)
            memory_value.setText(f"{value}%  ({fmt_bytes(budget)})")

        memory_percent.valueChanged.connect(update_memory_budget)
        update_memory_budget(memory_percent.value())
        memory_percent_layout.addWidget(memory_percent)
        memory_percent_layout.addLayout(memory_scale)
        performance_form.addRow("Memory budget", memory_percent_control)

        overview_triangles = QSpinBox(dialog)
        overview_triangles.setRange(50_000, 2_000_000)
        overview_triangles.setSingleStep(50_000)
        overview_triangles.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        overview_triangles.setValue(self.overview_triangle_limit)
        overview_triangles.setToolTip(
            "Triangle sample used for navigation when the complete binary STL exceeds the budget."
        )
        performance_form.addRow("Overview triangles", overview_triangles)
        performance_layout.addLayout(performance_form)

        invert_layout = section("Invert")
        invert_grid = QGridLayout()
        invert_grid.setColumnStretch(0, 1)
        mouse_heading = QLabel("Mouse", dialog)
        mouse_heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        invert_grid.addWidget(mouse_heading, 0, 1)
        keyboard_heading = QLabel("Keyboard", dialog)
        keyboard_heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        invert_grid.addWidget(keyboard_heading, 0, 2)
        inversion_checks: dict[str, tuple[QCheckBox, QCheckBox]] = {}
        inversion_values = {
            "Horizontal": (self.mouse_horizontal, self.keyboard_horizontal),
            "Vertical": (self.mouse_vertical, self.keyboard_vertical),
            "Zoom": (self.mouse_zoom, self.keyboard_zoom),
        }

        def inversion_diagram(input_kind: str, axis: str, inverted: bool) -> str:
            if input_kind == "Mouse" and axis == "Horizontal":
                result = "→ / ←" if inverted else "← / →"
                return f"Drag ← / →   View {result}"
            if input_kind == "Mouse" and axis == "Vertical":
                result = "↓ / ↑" if inverted else "↑ / ↓"
                return f"Drag ↑ / ↓   View {result}"
            if input_kind == "Mouse":
                result = "− / +" if inverted else "+ / −"
                return f"Wheel ↑ / ↓   Zoom {result}"
            if axis == "Horizontal":
                result = "→ / ←" if inverted else "← / →"
                return f"Press ← / →   View {result}"
            if axis == "Vertical":
                result = "↓ / ↑" if inverted else "↑ / ↓"
                return f"Press ↑ / ↓   View {result}"
            result = "− / +" if inverted else "+ / −"
            return f"Press ↑ / ↓   Zoom {result}"

        def input_icon(input_kind: str, axis: str) -> QPixmap:
            pixmap = QPixmap(25, 23)
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setPen(QPen(QColor("#334155"), 1.5))
            if input_kind == "Mouse":
                painter.drawRoundedRect(QRect(7, 2, 11, 18), 5, 5)
                painter.drawLine(12, 3, 12, 8)
                painter.drawLine(8, 9, 17, 9)
                if axis == "Zoom":
                    painter.drawLine(12, 4, 12, 7)
                    painter.drawLine(10, 5, 12, 3)
                    painter.drawLine(14, 5, 12, 3)
            else:
                first = QRect(1, 4, 11, 15)
                second = QRect(13, 4, 11, 15)
                painter.drawRoundedRect(first, 2, 2)
                painter.drawRoundedRect(second, 2, 2)
                arrows = ("←", "→") if axis == "Horizontal" else ("↑", "↓")
                painter.drawText(first, Qt.AlignmentFlag.AlignCenter, arrows[0])
                painter.drawText(second, Qt.AlignmentFlag.AlignCenter, arrows[1])
            painter.end()
            return pixmap

        def inversion_control(
            input_kind: str, axis: str, checked: bool, tooltip: str
        ) -> tuple[QWidget, QCheckBox]:
            cell = QWidget(dialog)
            cell_layout = QHBoxLayout(cell)
            cell_layout.setContentsMargins(4, 1, 4, 1)
            cell_layout.setSpacing(7)
            check = QCheckBox(cell)
            check.setChecked(checked)
            check.setAccessibleName(f"{input_kind} {axis.lower()}")
            check.setToolTip(tooltip)
            icon = QLabel(cell)
            icon.setFixedSize(25, 23)
            icon.setPixmap(input_icon(input_kind, axis))
            icon.setToolTip(tooltip)
            diagram = QLabel(cell)
            diagram.setMinimumWidth(145)
            diagram.setStyleSheet("color: #334155; font-size: 11px;")
            diagram.setToolTip(tooltip)

            def refresh(value: bool) -> None:
                diagram.setText(inversion_diagram(input_kind, axis, value))
                diagram.setStyleSheet(
                    "color: #2563FF; font-size: 11px; font-weight: 600;"
                    if value
                    else "color: #334155; font-size: 11px;"
                )

            refresh(checked)
            check.toggled.connect(refresh)
            cell_layout.addWidget(check)
            cell_layout.addWidget(icon)
            cell_layout.addWidget(diagram, 1)
            return cell, check

        for row, (axis, values) in enumerate(inversion_values.items(), start=1):
            invert_grid.addWidget(QLabel(axis, dialog), row, 0)
            mouse_tooltip = {
                "Horizontal": "Reverse horizontal mouse orbit, pan, and Ctrl+wheel roll.",
                "Vertical": "Reverse vertical mouse orbit and pan.",
                "Zoom": "Reverse scroll-wheel zoom direction.",
            }[axis]
            mouse_cell, mouse_check = inversion_control(
                "Mouse", axis, values[0], mouse_tooltip
            )
            invert_grid.addWidget(mouse_cell, row, 1)
            keyboard_tooltip = {
                "Horizontal": "Reverse horizontal orbit, pan, and roll shortcut directions.",
                "Vertical": "Reverse vertical orbit and pan shortcut directions.",
                "Zoom": "Reverse keyboard zoom-in and zoom-out directions.",
            }[axis]
            keyboard_cell, keyboard_check = inversion_control(
                "Keyboard", axis, values[1], keyboard_tooltip
            )
            invert_grid.addWidget(keyboard_cell, row, 2)
            inversion_checks[axis] = (mouse_check, keyboard_check)
        invert_layout.addLayout(invert_grid)

        shortcuts_layout = section("Keyboard shortcuts")
        shortcut_grid = QGridLayout()
        shortcut_grid.setColumnStretch(1, 1)
        shortcut_grid.addWidget(QLabel("Action", dialog), 0, 0)
        shortcut_grid.addWidget(QLabel("Shortcut", dialog), 0, 1)
        shortcut_edits: dict[str, QKeySequenceEdit] = {}
        for row, (shortcut_id, (label, default_sequence)) in enumerate(
            SHORTCUT_DEFINITIONS.items(), start=1
        ):
            shortcut_grid.addWidget(QLabel(label, dialog), row, 0)
            editor = QKeySequenceEdit(QKeySequence(self.shortcuts[shortcut_id]), dialog)
            editor.setMaximumSequenceLength(1)
            editor.setClearButtonEnabled(True)
            shortcut_grid.addWidget(editor, row, 1)
            reset_button = QPushButton("Reset", dialog)
            reset_button.setProperty("quiet", True)
            reset_button.setFixedWidth(64)
            reset_button.clicked.connect(
                lambda _=False, e=editor, default=default_sequence: e.setKeySequence(
                    QKeySequence(default)
                )
            )
            shortcut_grid.addWidget(reset_button, row, 2)
            shortcut_edits[shortcut_id] = editor
        shortcuts_layout.addLayout(shortcut_grid)

        reset_layout = section("Reset")
        reset_all_button = QPushButton("Reset all settings", dialog)
        reset_all_button.setProperty("quiet", True)
        reset_layout.addWidget(reset_all_button)
        reset_all_requested = {"value": False}

        def reset_all() -> None:
            answer = QMessageBox.question(
                dialog,
                "Reset all settings",
                "Reset interface, navigation, display, and keyboard shortcut settings?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Cancel,
            )
            if answer != QMessageBox.StandardButton.Yes:
                return
            reset_all_requested["value"] = True
            language.setCurrentIndex(language.findData("system"))
            tools_side.setCurrentText("Right")
            default_units.setCurrentText("cm")
            large_mesh_mode.setCurrentIndex(large_mesh_mode.findData("auto"))
            memory_percent.setValue(50)
            overview_triangles.setValue(250_000)
            for mouse_check, keyboard_check in inversion_checks.values():
                mouse_check.setChecked(False)
                keyboard_check.setChecked(False)
            for shortcut_id, (_label, default_sequence) in SHORTCUT_DEFINITIONS.items():
                shortcut_edits[shortcut_id].setKeySequence(QKeySequence(default_sequence))

        reset_all_button.clicked.connect(reset_all)
        layout.addStretch(1)
        scroll.setWidget(content)
        outer.addWidget(scroll, 1)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel,
            parent=dialog,
        )
        def accept_settings() -> None:
            assignments: dict[str, set[str]] = {}
            for shortcut_id, editor in shortcut_edits.items():
                sequence = editor.keySequence().toString(QKeySequence.SequenceFormat.PortableText)
                if sequence:
                    assignments.setdefault(sequence, set()).add(shortcut_id)
            conflicts = [
                ids
                for ids in assignments.values()
                if len(ids) > 1 and ids != {"selection_delete", "view_top"}
            ]
            if conflicts:
                QMessageBox.warning(dialog, APP_NAME, "Each shortcut must be unique.")
                return
            dialog.accept()

        buttons.accepted.connect(accept_settings)
        buttons.rejected.connect(dialog.reject)
        outer.addWidget(buttons)
        localize_widget_tree(dialog)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        if reset_all_requested["value"]:
            self.settings.clear()
        self.locale_preference = str(language.currentData() or "system")
        self.locale_code = locale_manager.select(self._resolved_locale(self.locale_preference))
        self.default_units = default_units.currentText()
        self.large_mesh_mode = str(large_mesh_mode.currentData())
        self.large_mesh_memory_percent = memory_percent.value()
        self.overview_triangle_limit = overview_triangles.value()
        self.mouse_horizontal = inversion_checks["Horizontal"][0].isChecked()
        self.keyboard_horizontal = inversion_checks["Horizontal"][1].isChecked()
        self.mouse_vertical = inversion_checks["Vertical"][0].isChecked()
        self.keyboard_vertical = inversion_checks["Vertical"][1].isChecked()
        self.mouse_zoom = inversion_checks["Zoom"][0].isChecked()
        self.keyboard_zoom = inversion_checks["Zoom"][1].isChecked()
        self.navigation_style.invert_horizontal = self.mouse_horizontal
        self.navigation_style.invert_vertical = self.mouse_vertical
        self.navigation_style.invert_zoom = self.mouse_zoom
        self.units.setCurrentText(self.default_units)
        self._apply_tools_side(tools_side.currentText())
        self.shortcuts = {
            shortcut_id: editor.keySequence().toString(QKeySequence.SequenceFormat.PortableText)
            for shortcut_id, editor in shortcut_edits.items()
        }
        self._refresh_view_button_tooltips()
        self._refresh_display_mode_labels()

        self.settings.setValue("interface/tools_side", self.tools_side)
        self.settings.setValue("interface/locale", self.locale_preference)
        self.settings.remove("rendering/gpu_preference")
        self.settings.setValue("interface/default_units", self.default_units)
        self.settings.setValue("interface/units_default_version", 2)
        self.settings.setValue("performance/large_mesh_mode", self.large_mesh_mode)
        self.settings.setValue("performance/memory_percent", self.large_mesh_memory_percent)
        self.settings.setValue("performance/overview_triangles", self.overview_triangle_limit)
        self.settings.setValue("navigation/mouse_horizontal", self.mouse_horizontal)
        self.settings.setValue("navigation/mouse_vertical", self.mouse_vertical)
        self.settings.setValue("navigation/mouse_zoom", self.mouse_zoom)
        self.settings.setValue("navigation/keyboard_horizontal", self.keyboard_horizontal)
        self.settings.setValue("navigation/keyboard_vertical", self.keyboard_vertical)
        self.settings.setValue("navigation/keyboard_zoom", self.keyboard_zoom)
        self.settings.remove("navigation/invert_mouse")
        self.settings.remove("navigation/invert_keyboard")
        self.settings.remove("navigation/invert_horizontal")
        self.settings.remove("navigation/invert_vertical")
        self.settings.remove("navigation/invert_zoom")
        self.settings.remove("optimization/automatic")
        self.settings.remove("display/show_edges")
        self.settings.setValue("display/type", self._display_mode())
        for shortcut_id, sequence in self.shortcuts.items():
            self.settings.setValue(f"shortcuts/{shortcut_id}", sequence)
        self.settings.sync()
        localize_widget_tree(self)

    def _install_help_tooltips(self) -> None:
        help_text = {
            self.open_button: "Open an STL mesh.",
            self.reload_button: "Reload source STL and discard edits.",
            self.undo_button: "Undo one mesh action.",
            self.redo_button: "Redo one mesh action.",
            self.units: "Dimension display units.",
            self.target: "Target triangle count.",
            self.preview_button: "Optimize the mesh or apply the completed result.",
            self.smart_quality: "Automatic target density: Draft 15%, Balanced 50%, Fine 75% maximum.",
            self.smart_button: "Calculate target from mesh size and surface area.",
            self.algorithm: "Mesh optimization algorithm.",
            self.slider: "Triangle target density.",
            self.display_type: "Choose shaded, wireframe, point, or color-mapped point-density display.",
            self.toggle_mesh_button: "Switch between the original and optimized meshes.",
            self.previous_mesh_button: "Switch between the current mesh and its previous undo state.",
            self.save_button: "Save the current mesh as a binary STL.",
            self.settings_button: "Open app settings.",
            self.metrics_toggle: "Show or hide CPU, memory, GPU, and mesh metrics.",
            self.about_button: "Version and license information.",
            self.repository_button: (
                "Open the project repository."
                if REPOSITORY_URL
                else "Project repository unavailable."
            ),
        }
        for widget, description in help_text.items():
            widget.setToolTip(description)
            widget.setMouseTracking(True)
        for widget in self.findChildren(QWidget):
            if widget.toolTip():
                widget.setMouseTracking(True)
        self.tooltip_filter = DeferredTooltipFilter(self)
        QApplication.instance().installEventFilter(self.tooltip_filter)

    def _create_metrics_panel(self, parent_layout: QVBoxLayout) -> None:
        self.metrics_toggle = QPushButton("Metrics  ▲")
        self.metrics_toggle.setCheckable(True)
        self.metrics_toggle.setChecked(False)
        self.metrics_toggle.setStyleSheet(
            "QPushButton { background: #FBFAF8; color: #0B1B34; border: 1px solid #D8DCE5; "
            "border-radius: 5px; padding: 4px 12px; text-align: left; } "
            "QPushButton:hover { border-color: #2563FF; background: #F1F5FF; }"
        )
        self.metrics_toggle.toggled.connect(self._toggle_metrics)
        parent_layout.addWidget(self.metrics_toggle)

        frame = QFrame()
        self.metrics_frame = frame
        frame.setObjectName("metricsPanel")
        frame.setStyleSheet(
            "QFrame#metricsPanel { background: #FBFAF8; border: 1px solid #D8DCE5; "
            "border-radius: 7px; } QLabel { color: #0B1B34; } "
            "QProgressBar { border: 1px solid #D8DCE5; border-radius: 4px; "
            "background: #ECEAE6; text-align: center; color: #0B1B34; min-height: 16px; } "
            "QProgressBar::chunk { background: #2563FF; border-radius: 3px; }"
        )
        grid = QGridLayout(frame)
        grid.setContentsMargins(10, 7, 10, 7)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(4)
        self.metric_labels: dict[str, QLabel] = {}
        self.metric_bars: dict[str, QProgressBar] = {}
        for column, (key, title) in enumerate((("cpu", "CPU"), ("ram", "RAM"), ("gpu", "GPU"))):
            heading = QLabel(title)
            heading.setStyleSheet("font-weight: 600;")
            value = QLabel("Reading…")
            bar = QProgressBar()
            bar.setRange(0, 100)
            bar.setValue(0)
            bar.setFormat("%p% used")
            grid.addWidget(heading, 0, column)
            grid.addWidget(bar, 1, column)
            grid.addWidget(value, 2, column)
            self.metric_labels[key] = value
            self.metric_bars[key] = bar
        self.live_mesh_metric = QLabel("Mesh: no file loaded")
        self.live_mesh_metric.setStyleSheet("color: #6B7280;")
        grid.addWidget(self.live_mesh_metric, 3, 0, 1, 3)
        self.capacity_metric = QLabel("Capacity: calculating…")
        self.capacity_metric.setStyleSheet("color: #6B7280;")
        self.capacity_metric.setWordWrap(True)
        self.capacity_metric.setToolTip(
            "Estimated from currently available memory, the configured memory budget, CPU "
            "count, and overview chunk size. Geometry operations currently run one at a time."
        )
        grid.addWidget(self.capacity_metric, 4, 0, 1, 3)
        self.geometry_activity_graph = GeometryActivityGraph(frame)
        self.geometry_activity_graph.setToolTip("CPU, GPU, and geometry activity.")
        grid.addWidget(self.geometry_activity_graph, 5, 0, 1, 3)
        parent_layout.addWidget(frame)
        frame.hide()

    def _toggle_metrics(self, visible: bool) -> None:
        self.metrics_frame.setVisible(visible)
        self.metrics_toggle.setText("Hide metrics  ▼" if visible else "Metrics  ▲")
        self._refresh_viewport_layout()
        # Windows can defer resizing the native VTK child in a maximized window. Repeat
        # after Qt has processed the visibility and layout requests.
        QTimer.singleShot(0, self._refresh_viewport_layout)
        QTimer.singleShot(75, self._refresh_viewport_layout)

    def _refresh_viewport_layout(self) -> None:
        root = self.centralWidget()
        layouts = (
            root.layout() if root is not None else None,
            self.viewport_column.layout(),
            self.metrics_frame.layout(),
        )
        for layout in layouts:
            if layout is not None:
                layout.invalidate()
                layout.activate()
        if root is not None:
            root.updateGeometry()
        self.viewport_column.updateGeometry()
        self.metrics_frame.updateGeometry()
        self.vtk_widget.updateGeometry()
        QApplication.sendPostedEvents(None, QEvent.Type.LayoutRequest)
        self._position_viewport_overlays()
        render_window = self.vtk_widget.GetRenderWindow()
        if render_window is not None and self.vtk_widget.width() > 0 and self.vtk_widget.height() > 0:
            render_window.SetSize(self.vtk_widget.width(), self.vtk_widget.height())
            render_window.Render()

    def _position_viewport_overlays(self) -> None:
        self._position_view_pad()
        self._position_orientation_overlays()
        self._position_loading_panel()
        if hasattr(self, "density_legend"):
            self.density_legend.move(
                max(14, self.vtk_widget.width() - self.density_legend.width() - 14),
                14,
            )
        if self.measure_info_frame is not None and self.measure_info_frame.isVisible():
            self.measure_info_frame.adjustSize()
            self.measure_info_frame.move(
                14,
                max(
                    14,
                    self.vtk_widget.height()
                    - self.measure_info_frame.height()
                    - (self.view_pad.height() if hasattr(self, "view_pad") else 0)
                    - 28,
                ),
            )
            self._apply_rounded_mask(self.measure_info_frame, 5)
        if self.crop_info_frame is not None and self.crop_info_frame.isVisible():
            x = max(8, min(self.crop_info_frame.x(), max(8, self.vtk_widget.width() - self.crop_info_frame.width() - 8)))
            y = max(8, min(self.crop_info_frame.y(), max(8, self.vtk_widget.height() - self.crop_info_frame.height() - 8)))
            self.crop_info_frame.move(x, y)
        self._update_measure_overlay(render=False)
        self._update_scale_bar()

    @staticmethod
    def _apply_rounded_mask(widget: QWidget, radius: float) -> None:
        if widget.width() <= 0 or widget.height() <= 0:
            return
        path = QPainterPath()
        path.addRoundedRect(
            0.0, 0.0, float(widget.width()), float(widget.height()), radius, radius
        )
        widget.setMask(QRegion(path.toFillPolygon().toPolygon()))

    def _create_density_legend(self) -> None:
        self.density_legend = QLabel(self.vtk_widget)
        self.density_legend.setText(
            "POINT DENSITY   <span style='color:#123070'>Sparse</span>  "
            "<span style='color:#199AD6'>●</span> "
            "<span style='color:#57E0B8'>●</span> "
            "<span style='color:#FACC15'>●</span> "
            "<span style='color:#E23730'>● Dense</span>"
        )
        self.density_legend.setTextFormat(Qt.TextFormat.RichText)
        self.density_legend.setStyleSheet(
            "background: rgba(247,245,241,232); color: #0B1B34; border: 1px solid #657384; "
            "border-radius: 6px; padding: 7px 10px; font-weight: 600;"
        )
        self.density_legend.adjustSize()
        self.density_legend.hide()

    @staticmethod
    def _filetime_value(value) -> int:
        return (int(value.dwHighDateTime) << 32) | int(value.dwLowDateTime)

    def _update_system_metrics(self) -> None:
        cpu = float(self.metric_bars["cpu"].value())
        gpu = float(self.metric_bars["gpu"].value())
        available_memory = available_physical_memory()
        total_memory = 0
        if os.name == "nt":
            class FILETIME(ctypes.Structure):
                _fields_ = [("dwLowDateTime", ctypes.c_ulong), ("dwHighDateTime", ctypes.c_ulong)]

            idle, kernel, user = FILETIME(), FILETIME(), FILETIME()
            if ctypes.windll.kernel32.GetSystemTimes(
                ctypes.byref(idle), ctypes.byref(kernel), ctypes.byref(user)
            ):
                current = tuple(self._filetime_value(v) for v in (idle, kernel, user))
                if self._last_cpu_times is not None:
                    idle_delta = current[0] - self._last_cpu_times[0]
                    total_delta = (current[1] - self._last_cpu_times[1]) + (current[2] - self._last_cpu_times[2])
                    cpu = 100.0 * (1.0 - idle_delta / total_delta) if total_delta else 0.0
                    cpu = max(0.0, min(100.0, cpu))
                    self.metric_bars["cpu"].setValue(round(cpu))
                    self.metric_labels["cpu"].setText(
                        f"{cpu:.0f}% used  •  {100-cpu:.0f}% remaining  •  "
                        f"{self.logical_cpu_count} logical processors"
                    )
                self._last_cpu_times = current

            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]
            memory = MEMORYSTATUSEX()
            memory.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory)):
                used = int(memory.dwMemoryLoad)
                available_memory = int(memory.ullAvailPhys)
                total_memory = int(memory.ullTotalPhys)
                self.metric_bars["ram"].setValue(used)
                self.metric_labels["ram"].setText(
                    f"{used}% used  •  {100-used}% remaining  •  "
                    f"{fmt_bytes(available_memory)} free / {fmt_bytes(total_memory)} total"
                )

        try:
            load, dedicated_bytes = self.gpu_counters.sample()
            gpu = load
            self.metric_bars["gpu"].setValue(round(load))
            self.metric_bars["gpu"].setFormat("%p% used")
            if self.vram_capacity_bytes > 0:
                memory_text = (
                    f"  •  {fmt_bytes(round(dedicated_bytes))} / "
                    f"{fmt_bytes(self.vram_capacity_bytes)} VRAM"
                )
            elif dedicated_bytes > 0:
                memory_text = f"  •  {fmt_bytes(round(dedicated_bytes))} VRAM in use"
            else:
                memory_text = ""
            self.metric_labels["gpu"].setText(
                f"Windows GPU engines  •  {load:.0f}% load  •  {100-load:.0f}% idle{memory_text}"
            )
        except (OSError, ValueError, IndexError):
            self.metric_bars["gpu"].setValue(0)
            self.metric_bars["gpu"].setFormat("Unavailable")
            self.metric_labels["gpu"].setText("Windows GPU performance counters unavailable")

        memory_budget = max(1, round(available_memory * self.large_mesh_memory_percent / 100.0))
        estimated_triangles = max(1, memory_budget // ESTIMATED_BYTES_PER_TRIANGLE)
        estimated_vertices = estimated_triangles // 2
        chunk_memory = max(1, self.overview_triangle_limit * ESTIMATED_BYTES_PER_TRIANGLE)
        parallel_cube_budget = max(
            1, min(self.logical_cpu_count, memory_budget // chunk_memory)
        )
        self.capacity_metric.setText(
            f"Capacity estimate  •  Full mesh: ~{fmt_count(estimated_triangles)} triangles / "
            f"~{fmt_count(estimated_vertices)} vertices / "
            f"{fmt_bytes(binary_stl_size(estimated_triangles))} binary STL  •  "
            f"Geometry jobs: 1  •  Parallel cube budget: ~{parallel_cube_budget}"
        )

        if self.source_faces is None:
            self.live_mesh_metric.setText("Mesh: no file loaded")
        else:
            preview = self.preview_poly.GetNumberOfPolys() if self.preview_poly is not None else 0
            operation = (
                self.active_operation
                if self.active_operation
                else "Optimizing"
                if self.busy
                else "Selection awaiting action"
                if self.crop_candidate
                else "Ready"
            )
            preview_text = fmt_count(preview) if preview else "not generated"
            if self.overview_mode:
                working_text = (
                    f"Overview: {fmt_count(len(self.source_faces))} sampled / "
                    f"{fmt_count(self.overview_total_triangles)} total triangles"
                )
            else:
                working_text = (
                    f"Original: {fmt_count(len(self.source_points))} vertices / "
                    f"{fmt_count(len(self.source_faces))} triangles"
                )
            self.live_mesh_metric.setText(
                f"{operation}  •  {working_text}  •  Optimized: {preview_text} triangles"
            )

        processing = self.busy or time.monotonic() < self.geometry_activity_until
        operation = (
            self.active_operation
            if self.active_operation
            else self.geometry_activity_label
            if processing
            else "Idle"
        )
        point_count = len(self.source_points) if self.source_points is not None else 0
        triangle_count = len(self.source_faces) if self.source_faces is not None else 0
        self.geometry_activity_graph.add_sample(
            cpu,
            gpu,
            processing,
            operation,
            point_count,
            triangle_count,
        )

    def _mark_geometry_activity(self, label: str, seconds: float = 2.0) -> None:
        self.geometry_activity_label = label
        self.geometry_activity_until = max(self.geometry_activity_until, time.monotonic() + seconds)

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        if self.crop_points:
            self._update_crop_overlay()
        QTimer.singleShot(0, self._position_view_pad)
        QTimer.singleShot(0, self._position_loading_panel)

    def _create_loading_panel(self) -> None:
        self.loading_frame = QFrame(self.vtk_widget)
        self.loading_frame.setObjectName("loadingPanel")
        self.loading_frame.setFixedWidth(430)
        self.loading_frame.setStyleSheet(
            "QFrame#loadingPanel { background: rgba(247, 245, 241, 245); "
            "border: 1px solid #B8C7DF; border-radius: 12px; } "
            "QLabel { background: transparent; color: #0B1B34; } "
            "QProgressBar { min-height: 10px; max-height: 10px; border: 0; "
            "border-radius: 5px; background: #DCE2EC; } "
            "QProgressBar::chunk { background: #2563FF; border-radius: 5px; }"
        )
        layout = QVBoxLayout(self.loading_frame)
        layout.setContentsMargins(22, 18, 22, 18)
        layout.setSpacing(8)
        self.loading_heading = QLabel("Preparing mesh")
        self.loading_heading.setStyleSheet("font-size: 18px; font-weight: 700;")
        layout.addWidget(self.loading_heading)
        self.loading_file_label = QLabel("Reading STL…")
        self.loading_file_label.setWordWrap(True)
        layout.addWidget(self.loading_file_label)
        self.loading_detail_label = QLabel("Reading triangles and welding shared vertices.")
        self.loading_detail_label.setStyleSheet("color: #5E6B80;")
        self.loading_detail_label.setWordWrap(True)
        layout.addWidget(self.loading_detail_label)
        self.loading_progress = QProgressBar()
        self.loading_progress.setRange(0, 0)
        self.loading_progress.setTextVisible(False)
        layout.addWidget(self.loading_progress)
        self.loading_elapsed_label = QLabel("Starting…")
        self.loading_elapsed_label.setStyleSheet("color: #6B7280; font-size: 11px;")
        layout.addWidget(self.loading_elapsed_label)
        self.progress_cancel_button = QPushButton("Cancel", self.loading_frame)
        self.progress_cancel_button.setToolTip(
            "Cancel this operation and restore the preceding mesh, selection, and settings."
        )
        self.progress_cancel_button.clicked.connect(self._cancel_mesh_operation)
        self.progress_cancel_button.setEnabled(False)
        layout.addWidget(self.progress_cancel_button)
        self.loading_frame.adjustSize()
        self._apply_rounded_mask(self.loading_frame, 12)
        self.loading_frame.hide()

    def _position_loading_panel(self) -> None:
        if not hasattr(self, "loading_frame"):
            return
        self.loading_frame.adjustSize()
        self._apply_rounded_mask(self.loading_frame, 12)
        x = max(12, (self.vtk_widget.width() - self.loading_frame.width()) // 2)
        y = max(12, (self.vtk_widget.height() - self.loading_frame.height()) // 2)
        self.loading_frame.move(x, y)
        if self.loading_frame.isVisible():
            self.loading_frame.raise_()

    def _update_loading_panel(self) -> None:
        if not self.busy:
            return
        elapsed = max(0.0, time.monotonic() - self.load_started_at)
        self.loading_elapsed_label.setText(f"Elapsed: {elapsed:.1f} s")

    def _set_controls_busy(self, busy: bool) -> None:
        interactive_types = (QPushButton, QCheckBox, QComboBox, QSpinBox, QSlider)
        if busy:
            self._busy_control_states = {
                widget: widget.isEnabled()
                for widget in self.controls_content.findChildren(QWidget)
                if isinstance(widget, interactive_types)
            }
            for widget in self._busy_control_states:
                widget.setEnabled(False)
            self.progress_cancel_button.setEnabled(True)
            return
        for widget, enabled in self._busy_control_states.items():
            widget.setEnabled(enabled)
        self._busy_control_states.clear()
        self.progress_cancel_button.setEnabled(False)

    def _capture_operation_snapshot(self) -> None:
        self.operation_snapshot = {
            "quality": self.smart_quality.currentText(),
            "algorithm": self.algorithm.currentText(),
            "target": self.target.value(),
            "display": self._display_mode(),
            "units": self.units.currentText(),
            "status": self.status.text(),
            "selection": (
                self.selected_face_mask.copy() if self.selected_face_mask is not None else None
            ),
            "selection_undo_stack": [
                mask.copy() if mask is not None else None for mask in self.selection_undo_stack
            ],
            "crop_candidate": self.crop_candidate,
            "crop_points": [QPoint(point) for point in self.crop_points],
            "selection_target": self.selection_target,
            "selection_base_quality": self.selection_base_quality,
            "selection_base_algorithm": self.selection_base_algorithm,
            "selection_base_target": self.selection_base_target,
            "preview_dirty": self.preview_dirty,
            "pass_ready": self.pass_ready,
            "button_states": {
                widget: widget.isEnabled()
                for widget in (
                    self.preview_button,
                    self.save_button,
                    self.toggle_mesh_button,
                    self.previous_mesh_button,
                    self.reload_button,
                    self.undo_button,
                    self.cancel_preview_button,
                    self.redo_button,
                    self.delete_selection_button,
                    self.clear_selection_button,
                )
            },
        }
        self.operation_cancel_event = threading.Event()

    def _cancel_mesh_operation(self) -> None:
        if not self.busy:
            return
        cancelled_title = self.active_operation or "Operation"
        if self.operation_cancel_event is not None:
            self.operation_cancel_event.set()
        if self.operation_future is not None:
            self.operation_future.cancel()

        if self.operation_uses_process:
            processes = list(getattr(self.optimization_executor, "_processes", {}).values())
            for process in processes:
                if process.is_alive():
                    process.terminate()
            self.optimization_executor.shutdown(wait=False, cancel_futures=True)
            self.optimization_executor = ProcessPoolExecutor(
                max_workers=1, mp_context=multiprocessing.get_context("spawn")
            )

        self.generation += 1
        self.edit_generation += 1
        self.load_generation += 1
        self.density_generation += 1
        self.pending_target = None
        self.running_target = None
        self.loading = False

        # Native mesh routines may not expose an interruption hook. Retire their worker so a
        # cancelled native call cannot block the next requested operation.
        retired_executor = self.executor
        retired_executor.shutdown(wait=False, cancel_futures=True)
        self.executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="mesh-reducer")

        snapshot = self.operation_snapshot
        self._end_mesh_operation()
        if snapshot is not None:
            with QSignalBlocker(self.smart_quality):
                self.smart_quality.setCurrentText(snapshot["quality"])
            with QSignalBlocker(self.algorithm):
                self.algorithm.setCurrentText(snapshot["algorithm"])
            with QSignalBlocker(self.target):
                self.target.setValue(snapshot["target"])
            with QSignalBlocker(self.display_type):
                display_index = self.display_type.findData(snapshot["display"])
                if display_index >= 0:
                    self.display_type.setCurrentIndex(display_index)
            with QSignalBlocker(self.units):
                self.units.setCurrentText(snapshot["units"])
            self.selected_face_mask = snapshot["selection"]
            self.selection_undo_stack = snapshot["selection_undo_stack"]
            self.crop_candidate = snapshot["crop_candidate"]
            self.crop_points = snapshot["crop_points"]
            self.selection_target = snapshot["selection_target"]
            self.selection_base_quality = snapshot["selection_base_quality"]
            self.selection_base_algorithm = snapshot["selection_base_algorithm"]
            self.selection_base_target = snapshot["selection_base_target"]
            self.preview_dirty = snapshot["preview_dirty"]
            self._set_primary_action(
                snapshot["pass_ready"], snapshot["button_states"][self.preview_button]
            )
            for widget, enabled in snapshot["button_states"].items():
                widget.setEnabled(enabled)
            if self.crop_candidate is not None:
                self._show_crop_highlight(self.crop_candidate[0])
                self._update_crop_overlay()
            elif self.selected_face_mask is not None and self.selected_face_mask.any():
                self._refresh_persistent_selection()
            for actor in (self.source_actor, self.simplified_actor):
                if actor is not None:
                    self._set_actor_display_mode(actor)
            self._update_dimension_labels()
            self._sync_slider_from_target()
            if self._selected_triangle_count():
                self._show_selection_primary_action()
            self.vtk_widget.GetRenderWindow().Render()
        self.status.setText(f"{cancelled_title} cancelled • previous state restored")

    def _begin_mesh_operation(self, title: str, detail: str) -> int:
        self.timer.stop()
        self._capture_operation_snapshot()
        self._mark_geometry_activity(title, 2.0)
        self.edit_generation += 1
        self.busy = True
        self.operation_uses_process = False
        self.active_operation = title
        self.load_started_at = time.monotonic()
        self._set_controls_busy(True)
        self.loading_heading.setText(title)
        self.loading_file_label.setText(detail)
        self.loading_detail_label.setText("Processing mesh data")
        self.loading_elapsed_label.setText("Starting…")
        self.loading_frame.show()
        self._position_loading_panel()
        self.loading_frame.raise_()
        self.loading_timer.start()
        QApplication.processEvents()
        return self.edit_generation

    def _end_mesh_operation(self) -> None:
        self.loading_timer.stop()
        self.loading_frame.hide()
        self._set_controls_busy(False)
        self.busy = False
        self.active_operation = ""
        self.operation_snapshot = None
        self.operation_cancel_event = None
        self.operation_future = None
        self.operation_uses_process = False

    def _create_view_pad(self) -> None:
        self.view_pad = QFrame(self.vtk_widget)
        self.view_pad.setObjectName("viewPad")
        self.view_pad.setStyleSheet(
            "QFrame#viewPad { background: rgba(251, 250, 248, 245); border: 1px solid #D8DCE5; "
            "border-radius: 7px; } QPushButton { min-width: 58px; min-height: 27px; "
            "padding: 2px 6px; background: #FFFFFF; color: #0B1B34; border: 1px solid #D8DCE5; "
            "border-radius: 4px; } QPushButton:hover { background: #F1F5FF; border-color: #2563FF; } "
            "QPushButton:checked { background: #2563FF; color: #FFFFFF; border-color: #1D4ED8; }"
        )
        grid = QGridLayout(self.view_pad)
        grid.setContentsMargins(7, 7, 7, 7)
        grid.setHorizontalSpacing(5)
        grid.setVerticalSpacing(5)
        layout = [
            ("Left", "left", 0, 0),
            ("Front", "front", 0, 1),
            ("Right", "right", 0, 2),
            ("Top", "top", 1, 0),
            ("Back", "back", 1, 1),
            ("Bottom", "bottom", 1, 2),
        ]
        self.view_buttons: dict[str, ViewButton] = {}
        for label, direction, row, column in layout:
            button = ViewButton(label, self.view_pad)
            button.setCheckable(True)
            button.clicked.connect(lambda _=False, d=direction: self._set_standard_view(d))
            button.orientationRequested.connect(lambda d=direction: self._set_current_view_as(d))
            grid.addWidget(button, row, column)
            self.view_buttons[direction] = button
        orientation_help = QLabel("Click: view  •  Ctrl+click: set this view", self.view_pad)
        orientation_help.setAlignment(Qt.AlignmentFlag.AlignCenter)
        orientation_help.setStyleSheet("color: #6B7280; padding: 1px 3px;")
        grid.addWidget(orientation_help, 2, 0, 1, 3)
        self._refresh_view_button_tooltips()
        self.orientation_indicator = OrientationIndicator(self.vtk_widget)
        self.orientation_indicator.show()
        self.orientation_indicator.raise_()
        self.scale_bar = ViewportScaleBar(self.vtk_widget)
        self.scale_bar.hide()
        self.scale_bar.raise_()
        camera = self.renderer.GetActiveCamera()
        camera.AddObserver("ModifiedEvent", self._update_orientation_indicator)
        camera.AddObserver("ModifiedEvent", self._diagnostic_camera_modified)
        self._update_orientation_indicator()
        self.view_pad.adjustSize()
        self.view_pad.raise_()

    def _refresh_view_button_tooltips(self) -> None:
        if not hasattr(self, "view_buttons"):
            return
        for direction, button in self.view_buttons.items():
            shortcut = self.shortcuts.get(f"view_{direction}", "")
            set_shortcut = self.shortcuts.get(f"set_view_{direction}", "")
            shortcut_text = f" View shortcut: {shortcut}." if shortcut else ""
            set_shortcut_text = f" Set shortcut: {set_shortcut}." if set_shortcut else ""
            button.setToolTip(
                f"View {direction}.{shortcut_text} Ctrl+click sets the current view as {direction}."
                f"{set_shortcut_text}"
            )

    def _update_orientation_indicator(self, *_args) -> None:
        if not hasattr(self, "orientation_indicator"):
            return
        camera = self.renderer.GetActiveCamera()
        self._update_active_view_button(camera)
        orientation = camera.GetOrientation()
        if any(button.isChecked() for button in self.view_buttons.values()):
            orientation = (0.0, 0.0, 0.0)
        self.orientation_indicator.set_camera(
            camera.GetPosition(),
            camera.GetFocalPoint(),
            camera.GetViewUp(),
            orientation,
        )
        self._update_scale_bar(camera)

    def _update_scale_bar(self, camera=None) -> None:
        if not hasattr(self, "scale_bar") or self.source_poly is None:
            if hasattr(self, "scale_bar"):
                self.scale_bar.hide()
            return
        height = max(1, self.vtk_widget.height())
        camera = camera or self.renderer.GetActiveCamera()
        if camera.GetParallelProjection():
            world_per_pixel = (2.0 * float(camera.GetParallelScale())) / height
        else:
            position = np.asarray(camera.GetPosition(), dtype=float)
            focal = np.asarray(camera.GetFocalPoint(), dtype=float)
            distance = max(float(np.linalg.norm(position - focal)), 1e-9)
            visible_height = 2.0 * distance * math.tan(math.radians(camera.GetViewAngle()) * 0.5)
            world_per_pixel = visible_height / height
        unit = self.units.currentText() if hasattr(self, "units") else "mm"
        raw_value = world_per_pixel * 130.0 / UNIT_MM[unit]
        if raw_value <= 0 or not math.isfinite(raw_value):
            self.scale_bar.hide()
            return
        exponent = math.floor(math.log10(raw_value))
        scale = 10.0 ** exponent
        normalized = raw_value / scale
        nice = (5.0 if normalized >= 5.0 else 2.0 if normalized >= 2.0 else 1.0) * scale
        pixels = nice * UNIT_MM[unit] / world_per_pixel
        decimals = max(0, -exponent)
        label = f"{nice:,.{min(decimals, 3)}f} {unit}"
        self.scale_bar.set_scale(label, pixels)
        self.scale_bar.show()
        self.scale_bar.raise_()

    def _update_active_view_button(self, camera=None) -> None:
        if not hasattr(self, "view_buttons"):
            return
        camera = camera or self.renderer.GetActiveCamera()
        position = np.asarray(camera.GetPosition(), dtype=float)
        focal = np.asarray(camera.GetFocalPoint(), dtype=float)
        view = position - focal
        view /= max(float(np.linalg.norm(view)), 1e-12)
        up = np.asarray(camera.GetViewUp(), dtype=float)
        up -= view * float(up @ view)
        up /= max(float(np.linalg.norm(up)), 1e-12)
        active = None
        for direction, (expected_view, expected_up) in STANDARD_VIEWS.items():
            expected_view, expected_up = self.saved_standard_views.get(
                direction,
                (np.asarray(expected_view, dtype=float), np.asarray(expected_up, dtype=float)),
            )
            if (
                float(view @ expected_view) > 0.99999
                and float(up @ expected_up) > 0.99999
            ):
                active = direction
                break
        for direction, button in self.view_buttons.items():
            button.setChecked(direction == active)

    def _position_view_pad(self) -> None:
        if not hasattr(self, "view_pad"):
            return
        margin = 14
        self.view_pad.adjustSize()
        x = margin
        y = max(margin, self.vtk_widget.height() - self.view_pad.height() - margin)
        if self.view_pad.pos() == QPoint(x, y):
            self.view_pad.raise_()
            return
        self.view_pad.hide()
        QApplication.processEvents()
        self.vtk_widget.GetRenderWindow().Render()
        self.view_pad.move(x, y)
        self.view_pad.show()
        self.view_pad.raise_()

    def _position_orientation_overlays(self) -> None:
        if hasattr(self, "orientation_indicator"):
            self.orientation_indicator.move(14, 14)
            self.orientation_indicator.raise_()
        if hasattr(self, "scale_bar"):
            self.scale_bar.move(
                max(14, self.vtk_widget.width() - self.scale_bar.width() - 14),
                max(14, self.vtk_widget.height() - self.scale_bar.height() - 14),
            )
            self.scale_bar.raise_()

    def _set_standard_view(self, direction: str) -> None:
        if direction not in STANDARD_VIEWS:
            return
        self._detach_selection_polygon_for_navigation()
        if self.active_actor is not None:
            bounds = self.active_actor.GetBounds()
        elif self.source_poly is not None:
            bounds = self.source_poly.GetBounds()
        else:
            return
        center = np.asarray(
            ((bounds[0] + bounds[1]) / 2, (bounds[2] + bounds[3]) / 2, (bounds[4] + bounds[5]) / 2)
        )
        diagonal = float(np.linalg.norm((bounds[1] - bounds[0], bounds[3] - bounds[2], bounds[5] - bounds[4])))
        distance = max(1.0, diagonal * 2.0)
        self._diagnostic("recall_view_begin", direction=direction, camera=self._camera_state())
        canonical_view, canonical_up = STANDARD_VIEWS[direction]
        view_direction, view_up = self.saved_standard_views.get(
            direction,
            (np.asarray(canonical_view, dtype=float), np.asarray(canonical_up, dtype=float)),
        )
        camera = self.renderer.GetActiveCamera()
        camera.SetFocalPoint(*center)
        camera.SetPosition(*(center + distance * view_direction))
        camera.SetViewUp(*view_up)
        camera.OrthogonalizeViewUp()
        self.renderer.ResetCamera(*bounds)
        camera.SetViewUp(*view_up)
        camera.OrthogonalizeViewUp()
        self.renderer.ResetCameraClippingRange()
        self.vtk_widget.GetRenderWindow().Render()
        self._update_active_view_button(camera)
        self.view_pad.raise_()
        self._diagnostic(
            "recall_view_complete",
            direction=direction,
            used_saved_view=direction in self.saved_standard_views,
            camera=self._camera_state(),
        )

    def _set_current_view_as(self, direction: str) -> None:
        if self.source_poly is None:
            return
        self._detach_selection_polygon_for_navigation()
        camera = self.renderer.GetActiveCamera()
        old_position = np.asarray(camera.GetPosition(), dtype=float).copy()
        old_focal = np.asarray(camera.GetFocalPoint(), dtype=float).copy()
        current_view = old_position - old_focal
        current_view /= max(float(np.linalg.norm(current_view)), 1e-12)
        current_up = np.asarray(camera.GetViewUp(), dtype=float).copy()
        current_up -= current_view * float(current_up @ current_view)
        current_up /= max(float(np.linalg.norm(current_up)), 1e-12)
        self._diagnostic("save_view_requested", direction=direction, camera=self._camera_state())
        answer = QMessageBox.question(
            self,
            "Confirm viewport orientation",
            f"Set the current camera angle as {direction.title()}?\n\n"
            f"The current X, Y, and Z corrections become zero for {direction.title()}. "
            "Other saved views remain unchanged.",
            QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Save,
        )
        if answer != QMessageBox.StandardButton.Save:
            self._diagnostic("save_view_cancelled", direction=direction)
            return
        self.saved_standard_views[direction] = (current_view.copy(), current_up.copy())
        opposite = OPPOSITE_VIEWS[direction]
        self.saved_standard_views[opposite] = (-current_view.copy(), current_up.copy())
        self._update_active_view_button(camera)
        self._update_orientation_indicator()
        self.vtk_widget.GetRenderWindow().Render()
        self.view_pad.raise_()
        self.status.setText(f"{direction.title()} view saved")
        self._diagnostic(
            "save_view_complete",
            direction=direction,
            opposite_direction=opposite,
            saved_view=current_view.tolist(),
            saved_up=current_up.tolist(),
            camera=self._camera_state(),
        )

    def _camera_state(self) -> dict:
        camera = self.renderer.GetActiveCamera()
        return {
            "position": list(camera.GetPosition()),
            "focal_point": list(camera.GetFocalPoint()),
            "view_up": list(camera.GetViewUp()),
            "orientation": list(camera.GetOrientation()),
            "parallel_scale": float(camera.GetParallelScale()),
            "active_view": next(
                (
                    direction
                    for direction, button in getattr(self, "view_buttons", {}).items()
                    if button.isChecked()
                ),
                None,
            ),
        }

    def _diagnostic(self, event_name: str, **details) -> None:
        path = self.diagnostic_log_path
        if path is None:
            return
        record = {"time": time.time(), "event": event_name, **details}
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8") as stream:
                stream.write(json.dumps(record, separators=(",", ":")) + "\n")
        except OSError:
            pass

    def _diagnostic_camera_modified(self, *_args) -> None:
        now = time.monotonic()
        if now - self._last_diagnostic_camera_time < 0.08:
            return
        self._last_diagnostic_camera_time = now
        self._diagnostic("camera_modified", camera=self._camera_state())

    @staticmethod
    def _orientation_rotation(
        current_view: np.ndarray,
        current_up: np.ndarray,
        target_view: np.ndarray,
        target_up: np.ndarray,
    ) -> np.ndarray:
        """Return the proper rotation mapping one complete camera frame to another."""
        source_view = np.asarray(current_view, dtype=float)
        source_view /= max(float(np.linalg.norm(source_view)), 1e-12)
        source_up = np.asarray(current_up, dtype=float)
        source_up -= source_view * float(source_up @ source_view)
        source_up /= max(float(np.linalg.norm(source_up)), 1e-12)
        source_right = np.cross(source_up, source_view)
        source_right /= max(float(np.linalg.norm(source_right)), 1e-12)

        destination_view = np.asarray(target_view, dtype=float)
        destination_view /= max(float(np.linalg.norm(destination_view)), 1e-12)
        destination_up = np.asarray(target_up, dtype=float)
        destination_up -= destination_view * float(destination_up @ destination_view)
        destination_up /= max(float(np.linalg.norm(destination_up)), 1e-12)
        destination_right = np.cross(destination_up, destination_view)
        destination_right /= max(float(np.linalg.norm(destination_right)), 1e-12)

        source_frame = np.column_stack((source_right, source_up, source_view))
        target_frame = np.column_stack((destination_right, destination_up, destination_view))
        rotation = target_frame @ source_frame.T
        u, _singular_values, vh = np.linalg.svd(rotation)
        rotation = u @ vh
        if np.linalg.det(rotation) < 0:
            u[:, -1] *= -1
            rotation = u @ vh
        return rotation

    @staticmethod
    def _anchored_orientation_rotation(
        current_view: np.ndarray, target_view: np.ndarray, anchor_view: np.ndarray
    ) -> np.ndarray:
        """Map a view onto its target using rotation only around an established axis."""
        axis = np.asarray(anchor_view, dtype=float)
        axis /= max(float(np.linalg.norm(axis)), 1e-12)
        source = np.asarray(current_view, dtype=float) - axis * float(current_view @ axis)
        target = np.asarray(target_view, dtype=float) - axis * float(target_view @ axis)
        source_length = float(np.linalg.norm(source))
        target_length = float(np.linalg.norm(target))
        if source_length <= 1e-9 or target_length <= 1e-9:
            return np.eye(3)
        source /= source_length
        target /= target_length
        sine = float(axis @ np.cross(source, target))
        cosine = max(-1.0, min(1.0, float(source @ target)))
        angle = math.atan2(sine, cosine)
        x, y, z = axis
        cross = np.asarray(((0.0, -z, y), (z, 0.0, -x), (-y, x, 0.0)))
        return np.eye(3) + math.sin(angle) * cross + (1.0 - math.cos(angle)) * (cross @ cross)

    def _keyboard_navigate(self, key: str, control: bool, shift: bool) -> bool:
        self._detach_selection_polygon_for_navigation()
        if key in ("left", "right") and self.keyboard_horizontal:
            key = {"left": "right", "right": "left"}[key]
        elif key in ("up", "down"):
            invert_axis = self.keyboard_zoom if control and shift else self.keyboard_vertical
            if invert_axis:
                key = {"up": "down", "down": "up"}[key]
        camera = self.renderer.GetActiveCamera()
        if control and shift and key == "up":
            camera.Dolly(1.12)
        elif control and shift and key == "down":
            camera.Dolly(1.0 / 1.12)
        elif control and shift and key == "left":
            camera.Roll(5.0)
        elif control and shift and key == "right":
            camera.Roll(-5.0)
        elif key in ("left", "right", "up", "down"):
            if control:
                position = np.asarray(camera.GetPosition(), dtype=float)
                focal = np.asarray(camera.GetFocalPoint(), dtype=float)
                view_up = np.asarray(camera.GetViewUp(), dtype=float)
                forward = focal - position
                distance = float(np.linalg.norm(forward))
                if distance <= 0:
                    return True
                forward /= distance
                view_up /= max(float(np.linalg.norm(view_up)), 1e-12)
                right = np.cross(forward, view_up)
                right /= max(float(np.linalg.norm(right)), 1e-12)
                amount = distance * 0.035
                if key == "left":
                    offset = -right * amount
                elif key == "right":
                    offset = right * amount
                elif key == "up":
                    offset = view_up * amount
                else:
                    offset = -view_up * amount
                camera.SetPosition(*(position + offset))
                camera.SetFocalPoint(*(focal + offset))
            else:
                if key == "left":
                    camera.Azimuth(-5.0)
                elif key == "right":
                    camera.Azimuth(5.0)
                elif key == "up":
                    camera.Elevation(5.0)
                else:
                    camera.Elevation(-5.0)
                camera.OrthogonalizeViewUp()
        else:
            return False
        self.renderer.ResetCameraClippingRange()
        self.vtk_widget.GetRenderWindow().Render()
        return True

    def closeEvent(self, event) -> None:  # noqa: N802
        self.executor.shutdown(wait=False, cancel_futures=True)
        self.optimization_executor.shutdown(wait=False, cancel_futures=True)
        self.gpu_counters.close()
        self.vtk_widget.Finalize()
        super().closeEvent(event)

    def open_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Open scan", "", "STL mesh (*.stl)")
        if path:
            self.load_path(Path(path))

    def _open_source_folder(self) -> None:
        if self.source_path is None:
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(os.fspath(self.source_path.parent)))

    def _copy_source_path(self) -> None:
        if self.source_path is None:
            return
        QApplication.clipboard().setText(os.fspath(self.source_path))
        self.status.setText("STL path copied")

    def load_path(self, path: Path) -> None:
        if self.busy:
            self.status.setText("Finish the current operation before loading another mesh.")
            return
        try:
            file_size = path.stat().st_size
        except Exception as exc:
            QMessageBox.critical(self, APP_NAME, f"Could not load the STL:\n\n{exc}")
            self.status.setText("Load failed.")
            return

        self._capture_operation_snapshot()
        self._cancel_crop(None)
        self.timer.stop()
        self.load_generation += 1
        token = self.load_generation
        self.loading = True
        self.busy = True
        self.active_operation = "Loading"
        self._mark_geometry_activity("Loading geometry", 2.0)
        self.load_started_at = time.monotonic()
        self._set_controls_busy(True)
        self.loading_heading.setText("Preparing mesh")
        self.loading_file_label.setText(f"{path.name}  •  {fmt_bytes(file_size)}")
        self.loading_detail_label.setText("Reading triangles and welding vertices")
        self.loading_elapsed_label.setText("Starting…")
        self.loading_frame.show()
        self._position_loading_panel()
        self.loading_frame.raise_()
        self.loading_timer.start()
        self.status.setText(f"Loading {path.name}…")

        memory_budget = round(
            available_physical_memory() * self.large_mesh_memory_percent / 100.0
        )
        future = self.executor.submit(
            load_stl_smart,
            path,
            self.large_mesh_mode,
            memory_budget,
            self.overview_triangle_limit,
        )
        self.operation_future = future

        def completed(result_future) -> None:
            try:
                poly, points, faces, metadata = result_future.result()
                error = None
            except Exception as exc:  # noqa: BLE001
                poly = points = faces = None
                metadata = None
                error = exc
            self.load_bridge.done.emit(token, path, poly, points, faces, metadata, error)

        future.add_done_callback(completed)

    def _finish_load(
        self,
        token: int,
        path: Path,
        poly: vtkPolyData | None,
        points: np.ndarray | None,
        faces: np.ndarray | None,
        metadata: dict | None,
        error: Exception | None,
    ) -> None:
        if token != self.load_generation:
            return
        self.loading = False
        self._end_mesh_operation()
        if error is not None or poly is None or points is None or faces is None:
            QMessageBox.critical(self, APP_NAME, f"Could not load the STL:\n\n{error}")
            self.status.setText("Load failed")
            return

        self.source_path = path
        self.source_poly = poly
        self.source_points = points
        self.source_faces = faces
        self.overview_mode = bool(metadata and metadata.get("overview"))
        self.overview_total_triangles = int(
            metadata.get("total_triangles", len(faces)) if metadata else len(faces)
        )
        self.preview_poly = None
        self.preview_is_selection = False
        self.density_cache.clear()
        self.measure_points.clear()
        self.measure_hover_world = None
        if self.measure_info_frame is not None:
            self.measure_info_frame.hide()
        self.mesh_modified = False
        self.saved_standard_views.clear()
        self.has_committed_optimization = False
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.undo_bytes = 0
        self.redo_bytes = 0
        self.undo_button.setEnabled(False)
        self.redo_button.setEnabled(False)
        self._reset_previous_view()
        self.selected_face_mask = None
        self.selection_undo_stack.clear()
        self.crop_info_user_positioned = False
        self.delete_selection_button.setEnabled(False)
        self.clear_selection_button.setEnabled(False)
        self.source_actor = None
        self.simplified_actor = None
        self.file_label.setText(os.fspath(path))
        self.open_file_folder_button.setEnabled(True)
        self.copy_file_path_button.setEnabled(True)
        self.loaded_triangle_count = self.overview_total_triangles
        self._update_save_button_label()
        self.original_count.setText(
            f"{fmt_count(len(faces))} overview / {fmt_count(self.overview_total_triangles)} total"
            if self.overview_mode
            else fmt_count(len(faces))
        )
        self.original_vertices.setText(
            f"{fmt_count(len(points))} overview" if self.overview_mode else fmt_count(len(points))
        )
        self.preview_count.setText("—")
        self.preview_vertices.setText("—")
        self.original_file_size.setText(fmt_bytes(path.stat().st_size))
        self._update_dimension_labels()
        self.drift.setText("—")
        self.optimization_ratio.setText("—")
        self.dimension_drift_model_units = None
        with QSignalBlocker(self.target):
            self.target.setRange(1_000, max(1_000, len(faces)))
        self._update_dynamic_presets()
        initial = smart_target(points, faces, self.smart_quality.currentText())
        with QSignalBlocker(self.target):
            self.target.setValue(initial)
        self._sync_slider_from_target()
        self.preview_dirty = not self.overview_mode
        self._set_primary_action(False, not self.overview_mode)
        self.toggle_mesh_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.reload_button.setEnabled(False)
        self.showing_original = True
        self._update_estimated_size()
        self._show_poly(poly)
        self.timer.stop()
        self.status.setText(
            f"Overview • {fmt_count(len(faces))} sampled of "
            f"{fmt_count(self.overview_total_triangles)} triangles • editing disabled"
            if self.overview_mode
            else f"Loaded • {fmt_count(len(faces))} triangles"
        )
        if self.verification_screenshot is not None:
            self.target.setValue(getattr(self, "verification_target", 200_000))
            self.timer.stop()
            self.preview()

    def _crop_interaction(self, phase: str, vtk_position) -> bool:
        if phase == "navigation":
            return self._detach_selection_polygon_for_navigation()
        if self.overview_mode:
            if phase == "start":
                self.status.setText("Overview mode is for navigation. Load the full mesh to edit.")
            return False
        if phase == "confirm" and self.crop_candidate is not None:
            self._confirm_crop()
            return True
        if phase == "cancel" and (
            self.crop_candidate is not None
            or self.crop_points
            or self.crop_selection_actor is not None
        ):
            self._cancel_crop("Crop cancelled.")
            return True
        if self.source_poly is None or self.busy or vtk_position is None:
            return False
        x, vtk_y = vtk_position
        qt_y = self.vtk_widget.height() - vtk_y
        point = QPoint(x, qt_y)
        if phase == "start":
            if self.selection_base_quality is None:
                self.timer.stop()
                self.selection_base_quality = self.smart_quality.currentText()
                self.selection_base_algorithm = self.algorithm.currentText()
                self.selection_base_target = self.target.value()
                self.selection_target = None
            self.selection_undo_stack.append(
                self.selected_face_mask.copy() if self.selected_face_mask is not None else None
            )
            self._hide_crop_preview()
            self._hide_loupe()
            self._show_poly(self.source_poly, reset_camera=False)
            self._refresh_persistent_selection()
            self.crop_start = point
            self.crop_points = [point, point, point, point]
            self._update_crop_overlay()
        elif phase == "move" and self.crop_start is not None:
            rect = QRect(self.crop_start, point).normalized()
            self.crop_points = [rect.topLeft(), rect.topRight(), rect.bottomRight(), rect.bottomLeft()]
            self._update_crop_overlay()
        elif phase == "finish" and self.crop_start is not None:
            start = self.crop_start
            self.crop_start = None
            rect = QRect(start, point).normalized()
            if rect.width() < 8 or rect.height() < 8:
                self._cancel_crop("Crop cancelled: drag a larger rectangle.")
                return True
            self.crop_points = [rect.topLeft(), rect.topRight(), rect.bottomRight(), rect.bottomLeft()]
            self._update_crop_overlay()
            self._prepare_polygon_crop()
        elif phase == "left_press" and self.crop_candidate is not None:
            vertex = self._nearest_crop_vertex(point, 12.0)
            if vertex is not None:
                self.crop_drag_index = vertex
                return True
            segment, distance = self._nearest_crop_segment(point)
            if segment is not None and distance <= 10.0:
                insert_at = segment + 1
                self.crop_points.insert(insert_at, point)
                self.crop_drag_index = insert_at
                self._update_crop_overlay()
                return True
            if QPolygonF([QPointF(p) for p in self.crop_points]).containsPoint(
                QPointF(point), Qt.FillRule.OddEvenFill
            ):
                self._confirm_crop()
                return True
            self._detach_selection_polygon_for_navigation()
        elif phase == "edit_move" and self.crop_drag_index is not None:
            self.crop_points[self.crop_drag_index] = point
            self._update_crop_overlay()
            return True
        elif phase == "left_release" and self.crop_drag_index is not None:
            self.crop_points[self.crop_drag_index] = point
            self.crop_drag_index = None
            self._update_crop_overlay()
            self._prepare_polygon_crop()
            return True
        elif phase == "right_press" and self.crop_candidate is not None:
            segment, distance = self._nearest_crop_segment(point)
            if segment is not None and distance <= 12.0 and len(self.crop_points) > 3:
                next_index = (segment + 1) % len(self.crop_points)
                a = self.crop_points[segment]
                b = self.crop_points[next_index]
                remove_index = segment if (point - a).manhattanLength() < (point - b).manhattanLength() else next_index
                self.crop_points.pop(remove_index)
                self._update_crop_overlay()
                self._prepare_polygon_crop()
                return True
        return False

    def _detach_selection_polygon_for_navigation(self) -> bool:
        """Remove stale screen-space geometry while retaining the selected mesh region."""
        if self.crop_candidate is None or not self.crop_points:
            return False
        candidate = self.crop_candidate
        selected_face_mask = candidate[3].copy()
        info_position = self.crop_info_frame.pos() if self.crop_info_frame is not None else None
        self._hide_crop_preview()
        self.crop_candidate = candidate
        self.selected_face_mask = selected_face_mask
        self.delete_selection_button.setEnabled(True)
        self.clear_selection_button.setEnabled(True)
        self._refresh_persistent_selection()
        self._show_selection_primary_action()
        if self.crop_info_label is not None:
            points, faces = candidate[1], candidate[2]
            unit = self.units.currentText()
            size = np.asarray(bounds_size(candidate[0].GetBounds())) / UNIT_MM[unit]
            self.crop_info_label.setText(
                f"SELECTION\n"
                f"Selected: {fmt_count(len(points))} vertices, {fmt_count(len(faces))} triangles\n"
                f"Mesh share: {self._selection_size_summary(len(faces))}\n"
                f"Dimensions: {fmt_size(tuple(size))} {unit}\n"
                "Choose an action • Ctrl+drag adds more"
            )
        if self.crop_info_frame is not None:
            if self.selection_undo_button is not None:
                self.selection_undo_button.setVisible(self._can_step_back_selection())
            self.crop_info_frame.adjustSize()
            self._apply_rounded_mask(self.crop_info_frame, 5)
            if info_position is not None:
                self.crop_info_frame.move(info_position)
            self.crop_info_frame.show()
            self.crop_info_frame.raise_()
        self.status.setText("Selection retained")
        return True

    def _update_crop_overlay(self) -> None:
        for actor in self.crop_overlay_actors:
            self.renderer.RemoveViewProp(actor)
        self.crop_overlay_actors = []
        if len(self.crop_points) < 3:
            self.vtk_widget.GetRenderWindow().Render()
            return
        vtk_points = vtkPoints()
        height = self.vtk_widget.height()
        for point in self.crop_points:
            vtk_points.InsertNextPoint(float(point.x()), float(height - point.y()), 0.0)
        coordinate = vtkCoordinate()
        coordinate.SetCoordinateSystemToDisplay()

        fill_poly = vtkPolyData()
        fill_poly.SetPoints(vtk_points)
        fill_cells = vtkCellArray()
        fill_cells.InsertNextCell(len(self.crop_points))
        for index in range(len(self.crop_points)):
            fill_cells.InsertCellPoint(index)
        fill_poly.SetPolys(fill_cells)
        fill_mapper = vtkPolyDataMapper2D()
        fill_mapper.SetInputData(fill_poly)
        fill_mapper.SetTransformCoordinate(coordinate)
        fill_actor = vtkActor2D()
        fill_actor.SetMapper(fill_mapper)
        fill_actor.GetProperty().SetColor(0.15, 0.62, 1.0)
        fill_actor.GetProperty().SetOpacity(0.10)

        line_poly = vtkPolyData()
        line_poly.SetPoints(vtk_points)
        line_cells = vtkCellArray()
        line_cells.InsertNextCell(len(self.crop_points) + 1)
        for index in range(len(self.crop_points)):
            line_cells.InsertCellPoint(index)
        line_cells.InsertCellPoint(0)
        line_poly.SetLines(line_cells)
        line_mapper = vtkPolyDataMapper2D()
        line_mapper.SetInputData(line_poly)
        line_mapper.SetTransformCoordinate(coordinate)
        line_actor = vtkActor2D()
        line_actor.SetMapper(line_mapper)
        line_actor.GetProperty().SetColor(0.45, 0.88, 1.0)
        line_actor.GetProperty().SetLineWidth(3.0)

        handle_poly = vtkPolyData()
        handle_poly.SetPoints(vtk_points)
        handle_cells = vtkCellArray()
        for index in range(len(self.crop_points)):
            handle_cells.InsertNextCell(1)
            handle_cells.InsertCellPoint(index)
        handle_poly.SetVerts(handle_cells)
        handle_mapper = vtkPolyDataMapper2D()
        handle_mapper.SetInputData(handle_poly)
        handle_mapper.SetTransformCoordinate(coordinate)
        handle_actor = vtkActor2D()
        handle_actor.SetMapper(handle_mapper)
        handle_actor.GetProperty().SetColor(0.65, 0.94, 1.0)
        handle_actor.GetProperty().SetPointSize(11.0)

        self.crop_overlay_actors = [fill_actor, line_actor, handle_actor]
        for actor in self.crop_overlay_actors:
            self.renderer.AddViewProp(actor)
        self.vtk_widget.GetRenderWindow().Render()

    def _world_to_display(self, point: np.ndarray) -> tuple[float, float] | None:
        self.renderer.SetWorldPoint(float(point[0]), float(point[1]), float(point[2]), 1.0)
        self.renderer.WorldToDisplay()
        display = self.renderer.GetDisplayPoint()
        if not all(math.isfinite(value) for value in display):
            return None
        return float(display[0]), float(display[1])

    def _nearest_measure_point(self, position: tuple[int, int], limit: float = 12.0) -> int | None:
        nearest, distance = None, float("inf")
        for index, world in enumerate(self.measure_points):
            display = self._world_to_display(world)
            if display is None:
                continue
            candidate = math.hypot(position[0] - display[0], position[1] - display[1])
            if candidate < distance:
                nearest, distance = index, candidate
        return nearest if distance <= limit else None

    def _pick_measure_point(self, position: tuple[int, int]) -> np.ndarray | None:
        if self.measure_picker is None or self.active_actor is None or self.busy:
            return None
        # Hardware picking follows rendered pixels. Temporarily pick the mesh as a surface so the
        # ruler remains usable in wireframe, vertices, and density displays without a CPU cell walk.
        mesh_property = self.active_actor.GetProperty()
        representation = mesh_property.GetRepresentation()
        mesh_property.SetRepresentationToSurface()
        try:
            picked = self.measure_picker.Pick(position[0], position[1], 0.0, self.renderer)
        finally:
            mesh_property.SetRepresentation(representation)
        if not picked:
            return None
        if self.measure_picker.GetActor() != self.active_actor:
            return None
        point = np.asarray(self.measure_picker.GetPickPosition(), dtype=float)
        return point if point.shape == (3,) and np.all(np.isfinite(point)) else None

    def _measurement_interaction(self, phase: str, position) -> bool:
        if phase == "hide":
            if self.measure_hover_world is not None or self.measure_pending_position is not None:
                self.measure_pending_position = None
                self.measure_pick_timer.stop()
                self.measure_hover_world = None
                self._update_measure_overlay()
            return False
        if phase == "refresh":
            if self.measure_points or self.measure_hover_world is not None:
                self._update_measure_overlay()
            return False
        if self.active_actor is None or self.busy:
            return False
        screen = (int(position[0]), int(position[1]))
        if phase == "move":
            self.measure_pending_position = screen
            if not self.measure_pick_timer.isActive():
                self.measure_pick_timer.start()
            return True
        if phase == "click":
            self.measure_pending_position = None
            self.measure_pick_timer.stop()
            existing = self._nearest_measure_point(screen)
            if existing is not None:
                self.measure_points.pop(existing)
                self.measure_hover_world = None
                self._update_measure_panel()
                self._update_measure_overlay()
                return True
            point = self._pick_measure_point(screen)
            if point is None:
                return False
            self.measure_points.append(point.copy())
            self.measure_hover_world = point
            self._update_measure_panel()
            self._update_measure_overlay()
            return True
        return False

    def _update_measure_hover(self) -> None:
        position = self.measure_pending_position
        self.measure_pending_position = None
        if position is None:
            return
        self.measure_hover_world = self._pick_measure_point(position)
        self._update_measure_overlay()

    def _clear_measurements(self) -> None:
        self.measure_points.clear()
        self.measure_hover_world = None
        self.measure_pending_position = None
        self.measure_pick_timer.stop()
        self._update_measure_panel()
        self._update_measure_overlay()

    def _clear_selection_and_ruler(self) -> None:
        had_selection = bool(self._selected_triangle_count())
        had_ruler = bool(self.measure_points) or self.measure_hover_world is not None
        if had_selection:
            self._clear_selection(message=None)
        if had_ruler:
            self._clear_measurements()
        if had_selection and had_ruler:
            self.status.setText("Selection and ruler cleared")
        elif had_selection:
            self.status.setText("Selection cleared")
        elif had_ruler:
            self.status.setText("Ruler cleared")

    def _ensure_measure_panel(self) -> None:
        if self.measure_info_frame is not None:
            return
        self.measure_info_frame = QFrame(self.vtk_widget)
        self.measure_info_frame.setStyleSheet(
            "QFrame { color: #0B1B34; background: rgba(251, 250, 248, 245); "
            "border: 1px solid #D8DCE5; border-radius: 7px; } "
            "QLabel { color: #0B1B34; border: none; background: transparent; font-size: 12px; } "
            "QComboBox, QPushButton { padding: 5px 8px; background: #FFFFFF; color: #0B1B34; "
            "border: 1px solid #D8DCE5; border-radius: 5px; } "
            "QComboBox:hover, QPushButton:hover { background: #F1F5FF; border-color: #2563FF; }"
        )
        layout = QVBoxLayout(self.measure_info_frame)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)
        self.measure_info_label = QLabel(self.measure_info_frame)
        layout.addWidget(self.measure_info_label)
        controls = QHBoxLayout()
        controls.addWidget(QLabel("Units", self.measure_info_frame))
        self.measure_units = ArrowComboBox(self.measure_info_frame)
        self.measure_units.addItems(list(UNIT_MM))
        preferred = self.units.currentText() if hasattr(self, "units") else "mm"
        self.measure_units.setCurrentText(preferred)
        self.measure_units.currentTextChanged.connect(self._measure_units_changed)
        self.measure_units.setToolTip("Choose the units used for ruler distances.")
        controls.addWidget(self.measure_units)
        clear_button = QPushButton("Clear", self.measure_info_frame)
        clear_button.clicked.connect(self._clear_measurements)
        clear_button.setToolTip(
            f"Remove all ruler points. Shortcut: {self.shortcuts['selection_clear']}."
        )
        controls.addWidget(clear_button)
        layout.addLayout(controls)

    def _measure_units_changed(self, _unit: str) -> None:
        self.measure_units_overridden = True
        self._update_measure_panel()

    def _update_measure_panel(self) -> None:
        if not self.measure_points:
            if self.measure_info_frame is not None:
                self.measure_info_frame.hide()
            return
        self._ensure_measure_panel()
        unit = self.measure_units.currentText() if self.measure_units is not None else "mm"
        segments = [
            float(np.linalg.norm(second - first)) / UNIT_MM[unit]
            for first, second in zip(self.measure_points, self.measure_points[1:])
        ]
        visible = segments[-8:]
        first_index = len(segments) - len(visible) + 1
        rows = ["RULER", f"Points: {len(self.measure_points)}"]
        if first_index > 1:
            rows.append(f"{first_index - 1} earlier segments")
        rows.extend(
            f"{index} to {index + 1}: {length:,.3f} {unit}"
            for index, length in enumerate(visible, start=first_index)
        )
        rows.append(f"Total: {sum(segments):,.3f} {unit}")
        rows.append("Shift+click adds or removes a point.")
        self.measure_info_label.setText("\n".join(rows))
        self.measure_info_frame.adjustSize()
        self.measure_info_frame.show()
        self._position_viewport_overlays()
        self.measure_info_frame.raise_()

    def _update_measure_overlay(self, render: bool = True) -> None:
        if self.measure_overlay_actor is not None:
            self.renderer.RemoveViewProp(self.measure_overlay_actor)
            self.measure_overlay_actor = None
        displays = [self._world_to_display(point) for point in self.measure_points]
        displays = [point for point in displays if point is not None]
        hover = self._world_to_display(self.measure_hover_world) if self.measure_hover_world is not None else None
        if not displays and hover is None:
            if render:
                self.vtk_widget.GetRenderWindow().Render()
            return
        vtk_points = vtkPoints()
        lines = vtkCellArray()

        def add_segment(a: tuple[float, float], b: tuple[float, float]) -> None:
            first = vtk_points.InsertNextPoint(a[0], a[1], 0.0)
            second = vtk_points.InsertNextPoint(b[0], b[1], 0.0)
            lines.InsertNextCell(2)
            lines.InsertCellPoint(first)
            lines.InsertCellPoint(second)

        for first, second in zip(displays, displays[1:]):
            add_segment(first, second)
        for center, radius in [(point, 7.0) for point in displays] + ([(hover, 10.0)] if hover else []):
            ring = [
                (center[0] + radius * math.cos(index * math.tau / 24.0),
                 center[1] + radius * math.sin(index * math.tau / 24.0))
                for index in range(24)
            ]
            for first, second in zip(ring, ring[1:] + ring[:1]):
                add_segment(first, second)
        poly = vtkPolyData()
        poly.SetPoints(vtk_points)
        poly.SetLines(lines)
        coordinate = vtkCoordinate()
        coordinate.SetCoordinateSystemToDisplay()
        mapper = vtkPolyDataMapper2D()
        mapper.SetInputData(poly)
        mapper.SetTransformCoordinate(coordinate)
        actor = vtkActor2D()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(0.20, 0.82, 1.0)
        actor.GetProperty().SetLineWidth(2.5)
        self.measure_overlay_actor = actor
        self.renderer.AddViewProp(actor)
        if render:
            self.vtk_widget.GetRenderWindow().Render()

    def _nearest_crop_vertex(self, point: QPoint, limit: float) -> int | None:
        if not self.crop_points:
            return None
        distances = [math.hypot(point.x() - p.x(), point.y() - p.y()) for p in self.crop_points]
        index = int(np.argmin(distances))
        return index if distances[index] <= limit else None

    def _nearest_crop_segment(self, point: QPoint) -> tuple[int | None, float]:
        best_index, best_distance = None, float("inf")
        p = np.asarray((point.x(), point.y()), dtype=float)
        for index, first in enumerate(self.crop_points):
            second = self.crop_points[(index + 1) % len(self.crop_points)]
            a = np.asarray((first.x(), first.y()), dtype=float)
            b = np.asarray((second.x(), second.y()), dtype=float)
            ab = b - a
            length_squared = float(ab @ ab)
            amount = 0.0 if length_squared == 0 else max(0.0, min(1.0, float((p - a) @ ab) / length_squared))
            distance = float(np.linalg.norm(p - (a + amount * ab)))
            if distance < best_distance:
                best_index, best_distance = index, distance
        return best_index, best_distance

    @staticmethod
    def _points_in_polygon(x: np.ndarray, y: np.ndarray, polygon: list[QPoint]) -> np.ndarray:
        inside = np.zeros(len(x), dtype=bool)
        previous = polygon[-1]
        for current in polygon:
            x1, y1 = previous.x(), previous.y()
            x2, y2 = current.x(), current.y()
            crossing = ((y1 > y) != (y2 > y)) & (
                x < (x2 - x1) * (y - y1) / ((y2 - y1) or 1e-12) + x1
            )
            inside ^= crossing
            previous = current
        return inside

    def _prepare_polygon_crop(self) -> None:
        if self.source_poly is None or self.source_points is None or self.source_faces is None:
            return
        self._mark_geometry_activity("Analyzing selection", 3.0)
        if self.crop_info_frame is not None:
            self.crop_info_frame.hide()
        QApplication.processEvents()
        self.vtk_widget.GetRenderWindow().Render()
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        QApplication.processEvents()
        try:
            width, height = max(1, self.vtk_widget.width()), max(1, self.vtk_widget.height())
            matrix_vtk = self.renderer.GetActiveCamera().GetCompositeProjectionTransformMatrix(
                self.renderer.GetTiledAspectRatio(), -1.0, 1.0
            )
            matrix = np.asarray(
                [[matrix_vtk.GetElement(row, column) for column in range(4)] for row in range(4)],
                dtype=float,
            )
            points_h = np.column_stack((self.source_points, np.ones(len(self.source_points))))
            clip = points_h @ matrix.T
            valid = np.abs(clip[:, 3]) > 1e-12
            screen_x = np.full(len(clip), -1e9)
            screen_y = np.full(len(clip), -1e9)
            screen_x[valid] = (clip[valid, 0] / clip[valid, 3] + 1.0) * width * 0.5
            screen_y[valid] = (1.0 - clip[valid, 1] / clip[valid, 3]) * height * 0.5
            selected_vertices = valid & self._points_in_polygon(screen_x, screen_y, self.crop_points)
            selected_face_mask = np.any(selected_vertices[self.source_faces], axis=1)
            if (
                self.selected_face_mask is not None
                and len(self.selected_face_mask) == len(selected_face_mask)
            ):
                selected_face_mask |= self.selected_face_mask
            selected_faces = self.source_faces[selected_face_mask]
            if len(selected_faces) == 0:
                self._cancel_crop("Selection is empty.")
                return
            used = np.unique(selected_faces)
            remap = np.full(len(self.source_points), -1, dtype=np.int64)
            remap[used] = np.arange(len(used))
            points = np.ascontiguousarray(self.source_points[used])
            faces = np.ascontiguousarray(remap[selected_faces], dtype=np.int32)
            cropped = arrays_polydata(points, faces)
        finally:
            QApplication.restoreOverrideCursor()
        if len(faces) == 0:
            self._cancel_crop("Selection is empty.")
            return
        self.crop_candidate = (cropped, points, faces, selected_face_mask)
        self._show_crop_highlight(cropped)
        suggested_target = smart_target(points, faces, self.smart_quality.currentText())
        maximum = max(4, len(faces) - 1)
        target = min(self.selection_target or suggested_target, maximum)
        self.selection_target = target
        with QSignalBlocker(self.target):
            self.target.setRange(min(1_000, maximum), maximum)
            self.target.setValue(target)
        self._update_dynamic_presets(len(faces))
        self._sync_slider_from_target(len(faces))
        self._update_estimated_size()
        self._show_selection_primary_action()
        unit = self.units.currentText()
        size = np.asarray(bounds_size(cropped.GetBounds())) / UNIT_MM[unit]
        if self.crop_info_frame is None:
            self.crop_info_frame = DraggableOverlayFrame(self.vtk_widget)
            self.crop_info_frame.movedByUser.connect(self._mark_crop_info_positioned)
            self.crop_info_frame.setStyleSheet(
                "QFrame { color: #0B1B34; background: rgba(251, 250, 248, 245); "
                "border: 1px solid #D8DCE5; border-radius: 7px; } "
                "QLabel { color: #0B1B34; border: none; background: transparent; font-size: 12px; } "
                "QPushButton { padding: 5px 8px; background: #FFFFFF; color: #0B1B34; "
                "border: 1px solid #D8DCE5; border-radius: 5px; } "
                "QPushButton:hover { background: #F1F5FF; border-color: #2563FF; }"
            )
            info_layout = QVBoxLayout(self.crop_info_frame)
            info_layout.setContentsMargins(8, 8, 8, 8)
            info_layout.setSpacing(6)
            self.crop_info_label = QLabel(self.crop_info_frame)
            self.crop_info_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
            info_layout.addWidget(self.crop_info_label)
            action_row = QGridLayout()
            action_row.setHorizontalSpacing(6)
            action_row.setVerticalSpacing(6)
            action_specs = (
                ("Crop", "crop", f"Keep only the highlighted triangles. Shortcut: {self.shortcuts['selection_crop']}."),
                ("Add", "add", f"Save this highlight and select more from another view. Shortcut: {self.shortcuts['selection_add']}."),
                ("Optimize", "optimize", f"Optimize only the highlighted triangles. Shortcut: {self.shortcuts['selection_optimize']}."),
                ("Delete", "delete", f"Remove the highlighted triangles. Shortcut: {self.shortcuts['selection_delete']}."),
                ("Step back", "undo", "Remove the most recently added selection region."),
                ("Clear", "clear", f"Clear the current selection without changing the mesh. Shortcut: {self.shortcuts['selection_clear']}."),
            )
            for index, (caption, action, help_text) in enumerate(action_specs):
                button = QPushButton(caption, self.crop_info_frame)
                button.clicked.connect(lambda _=False, a=action: self._apply_selection_action(a))
                button.setToolTip(help_text)
                if action == "undo":
                    self.selection_undo_button = button
                action_row.addWidget(button, index // 3, index % 3)
            info_layout.addLayout(action_row)
        self.crop_info_label.setText(
            f"SELECTION\n"
            f"Selected: {fmt_count(len(points))} vertices, {fmt_count(len(faces))} triangles\n"
            f"Mesh share: {self._selection_size_summary(len(faces))}\n"
            f"Dimensions: {fmt_size(tuple(size))} {unit}\n"
            f"Before: {fmt_count(len(faces))} triangles\n"
            f"Optimization target: {fmt_count(target)} triangles\n"
            f"Drag corners • Left-click line adds • Right-click line removes\n"
            f"Click inside or press Enter adds the selection"
        )
        if self.selection_undo_button is not None:
            self.selection_undo_button.setVisible(self._can_step_back_selection())
        self.crop_info_frame.adjustSize()
        self._apply_rounded_mask(self.crop_info_frame, 5)
        polygon_rect = QPolygonF([QPointF(p) for p in self.crop_points]).boundingRect().toRect()
        label_x = min(polygon_rect.left(), max(8, self.vtk_widget.width() - self.crop_info_frame.width() - 8))
        label_y = min(polygon_rect.bottom() + 8, max(8, self.vtk_widget.height() - self.crop_info_frame.height() - 8))
        if not self.crop_info_user_positioned:
            self.crop_info_frame.move(max(8, label_x), max(8, label_y))
        self.crop_info_frame.show()
        self.crop_info_frame.raise_()
        self.status.setText("Selection active")

    def _mark_crop_info_positioned(self) -> None:
        self.crop_info_user_positioned = True

    def _show_crop_highlight(self, poly: vtkPolyData) -> None:
        if self.crop_selection_actor is not None:
            self.renderer.RemoveActor(self.crop_selection_actor)
        mapper = vtkPolyDataMapper()
        mapper.SetInputData(poly)
        mapper.SetResolveCoincidentTopologyToPolygonOffset()
        mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(-3.0, -3.0)
        actor = vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(0.05, 0.95, 1.0)
        actor.GetProperty().SetOpacity(1.0)
        actor.GetProperty().SetAmbient(0.85)
        actor.GetProperty().SetDiffuse(0.15)
        actor.GetProperty().SetEdgeColor(1.0, 0.55, 0.05)
        actor.GetProperty().EdgeVisibilityOn()
        self.crop_selection_actor = actor
        if self.source_actor is not None:
            self.source_actor.GetProperty().SetOpacity(0.12)
        self.renderer.AddActor(actor)
        self.renderer.ResetCameraClippingRange()
        self.vtk_widget.GetRenderWindow().Render()

    def _confirm_crop(self) -> None:
        self._apply_selection_action("add")

    def _selection_shortcut(self, action: str) -> None:
        if self.busy:
            return
        if self.crop_candidate is not None:
            self._apply_selection_action(action)
            return
        if action == "optimize":
            self._optimize_saved_selection()
        elif action == "delete" and self.selected_face_mask is not None:
            self._delete_selected()

    def _apply_selection_action(self, action: str) -> None:
        if action == "clear":
            self._clear_selection()
            return
        if action == "undo":
            self._undo_selection()
            return
        if self.crop_candidate is None:
            if self.selected_face_mask is None or not self.selected_face_mask.any():
                return
            if action == "optimize":
                self._optimize_saved_selection()
            elif action == "delete":
                self._delete_selected(confirm=False)
            elif action == "crop":
                cropped, points, faces = self._poly_from_face_mask(self.selected_face_mask)
                self._set_working_mesh(cropped, points, faces, "Cropped mesh")
            return
        cropped, points, faces, selected_face_mask = self.crop_candidate
        if action not in {"add", "crop", "optimize", "delete"}:
            return
        self.crop_candidate = None
        self._hide_crop_preview()
        self.selected_face_mask = selected_face_mask.copy()
        self.delete_selection_button.setEnabled(True)
        self.clear_selection_button.setEnabled(True)
        if action == "add":
            self._refresh_persistent_selection()
            self._show_selection_primary_action()
            self._show_selection_action_window()
            self.status.setText(
                f"Selection saved • {fmt_count(int(selected_face_mask.sum()))} triangles • "
                f"{self._selection_size_summary(int(selected_face_mask.sum()))}"
            )
            return
        if action == "delete":
            self._delete_selected(confirm=False)
            return
        if action == "crop":
            self._set_working_mesh(cropped, points, faces, "Cropped mesh")
            return
        self._optimize_selected_region(points, faces, selected_face_mask)

    def _optimize_selected_region(
        self, selected_points: np.ndarray, selected_faces: np.ndarray, selected_face_mask: np.ndarray
    ) -> None:
        if self.source_points is None or self.source_faces is None:
            return
        if len(selected_faces) < 5:
            self.status.setText("Selection is too small to optimize.")
            return
        target = min(
            self.selection_target
            or smart_target(selected_points, selected_faces, self.smart_quality.currentText()),
            len(selected_faces) - 1,
        )
        algorithm = self.algorithm.currentText()
        source_points = self.source_points
        source_faces = self.source_faces
        token = self._begin_mesh_operation(
            "Optimizing selection",
            f"{fmt_count(len(selected_faces))} selected triangles → about {fmt_count(target)}",
        )
        self._set_primary_action(False, False)
        cancel_event = self.operation_cancel_event
        self.status.setText(
            f"Optimizing selected region: {fmt_count(len(selected_faces))} to about "
            f"{fmt_count(target)} triangles…"
        )

        def job():
            try:
                reduced_points, reduced_faces = simplify_arrays(
                    selected_points, selected_faces, target, algorithm
                )
                if cancel_event is not None and cancel_event.is_set():
                    raise OperationCancelled
                untouched_faces = np.ascontiguousarray(source_faces[~selected_face_mask], dtype=np.int32)
                point_offset = len(source_points)
                combined_points = np.ascontiguousarray(
                    np.vstack((source_points, reduced_points)), dtype=np.float64
                )
                combined_faces = np.ascontiguousarray(
                    np.vstack((untouched_faces, reduced_faces + point_offset)), dtype=np.int64
                )
                used = np.unique(combined_faces)
                remap = np.full(len(combined_points), -1, dtype=np.int64)
                remap[used] = np.arange(len(used))
                merged_points = np.ascontiguousarray(combined_points[used])
                merged_faces = np.ascontiguousarray(remap[combined_faces], dtype=np.int32)
                return {
                    "kind": "optimize",
                    "poly": arrays_polydata(merged_points, merged_faces),
                    "points": merged_points,
                    "faces": merged_faces,
                    "removed": len(selected_faces) - len(reduced_faces),
                }
            except OperationCancelled:
                return {"kind": "optimize", "cancelled": True}
            except Exception:
                return {"kind": "optimize", "error": traceback.format_exc()}

        future = self.executor.submit(job)
        self.operation_future = future
        future.add_done_callback(lambda f: self.edit_bridge.done.emit(token, f.result()))

    def _optimize_saved_selection(self) -> None:
        if (
            self.selected_face_mask is None
            or self.source_faces is None
            or len(self.selected_face_mask) != len(self.source_faces)
            or not self.selected_face_mask.any()
        ):
            self.status.setText("No selection")
            return
        mask = self.selected_face_mask.copy()
        _, points, faces = self._poly_from_face_mask(mask)
        self._optimize_selected_region(points, faces, mask)

    def _poly_from_face_mask(self, mask: np.ndarray) -> tuple[vtkPolyData, np.ndarray, np.ndarray]:
        selected_faces = self.source_faces[mask]
        used = np.unique(selected_faces)
        remap = np.full(len(self.source_points), -1, dtype=np.int64)
        remap[used] = np.arange(len(used))
        points = np.ascontiguousarray(self.source_points[used])
        faces = np.ascontiguousarray(remap[selected_faces], dtype=np.int32)
        return arrays_polydata(points, faces), points, faces

    def _selected_triangle_count(self) -> int:
        if self.crop_candidate is not None:
            return len(self.crop_candidate[2])
        if self.selected_face_mask is not None and self.selected_face_mask.any():
            return int(self.selected_face_mask.sum())
        return 0

    def _selection_size_summary(self, selected_triangles: int) -> str:
        total_triangles = len(self.source_faces) if self.source_faces is not None else 0
        if total_triangles <= 0:
            return "0% • 0 B of 0 B"
        selected_triangles = min(max(0, int(selected_triangles)), total_triangles)
        percentage = selected_triangles * 100.0 / total_triangles
        selected_size = binary_stl_size(selected_triangles)
        total_size = binary_stl_size(total_triangles)
        return f"{percentage:.1f}% • {fmt_bytes(selected_size)} of {fmt_bytes(total_size)}"

    def _refresh_persistent_selection(self) -> None:
        if (
            self.selected_face_mask is None
            or self.source_faces is None
            or len(self.selected_face_mask) != len(self.source_faces)
            or not self.selected_face_mask.any()
        ):
            return
        poly, _, _ = self._poly_from_face_mask(self.selected_face_mask)
        self._show_crop_highlight(poly)

    def _show_selection_action_window(self) -> None:
        """Keep selection actions visible whenever geometry remains selected."""
        if (
            self.crop_info_frame is None
            or self.crop_info_label is None
            or self.selected_face_mask is None
            or self.source_faces is None
            or len(self.selected_face_mask) != len(self.source_faces)
            or not self.selected_face_mask.any()
        ):
            return
        poly, points, faces = self._poly_from_face_mask(self.selected_face_mask)
        unit = self.units.currentText()
        size = np.asarray(bounds_size(poly.GetBounds())) / UNIT_MM[unit]
        self.crop_info_label.setText(
            "SELECTION\n"
            f"Selected: {fmt_count(len(points))} vertices, {fmt_count(len(faces))} triangles\n"
            f"Mesh share: {self._selection_size_summary(len(faces))}\n"
            f"Dimensions: {fmt_size(tuple(size))} {unit}\n"
            "Choose an action • Ctrl+drag adds more"
        )
        if self.selection_undo_button is not None:
            self.selection_undo_button.setVisible(self._can_step_back_selection())
        self.crop_info_frame.adjustSize()
        self._apply_rounded_mask(self.crop_info_frame, 5)
        self.crop_info_frame.show()
        self.crop_info_frame.raise_()

    def _can_step_back_selection(self) -> bool:
        if not self.selection_undo_stack:
            return False
        previous = self.selection_undo_stack[-1]
        return previous is not None and bool(previous.any())

    def _undo_selection(self) -> None:
        """Restore the selection that existed before the most recent selection drag."""
        if not self.selection_undo_stack:
            return
        previous = self.selection_undo_stack.pop()
        self.crop_candidate = None
        self._hide_crop_preview()
        self.selected_face_mask = previous.copy() if previous is not None else None
        if self.selected_face_mask is not None and self.selected_face_mask.any():
            self._refresh_persistent_selection()
            self._show_selection_primary_action()
            self._show_selection_action_window()
            self.status.setText("Selection stepped back")
        else:
            self.selected_face_mask = None
            self.delete_selection_button.setEnabled(False)
            self.clear_selection_button.setEnabled(False)
            self.status.setText("Selection cleared")

    def _clear_selection(self, _checked=False, message: str | None = "Selection cleared.") -> None:
        self.selected_face_mask = None
        self.crop_candidate = None
        self.selection_undo_stack.clear()
        self._hide_crop_preview()
        if self.selection_base_quality is not None:
            with QSignalBlocker(self.smart_quality):
                self.smart_quality.setCurrentText(self.selection_base_quality)
            with QSignalBlocker(self.algorithm):
                self.algorithm.setCurrentText(self.selection_base_algorithm or self.algorithm.currentText())
            if self.source_faces is not None:
                with QSignalBlocker(self.target):
                    self.target.setRange(1_000, max(1_000, len(self.source_faces)))
                    self.target.setValue(
                        min(self.selection_base_target or 1_000, max(1_000, len(self.source_faces)))
                    )
            self.selection_base_quality = None
            self.selection_base_algorithm = None
            self.selection_base_target = None
            self.selection_target = None
            self._update_dynamic_presets()
            self._sync_slider_from_target()
            self._update_estimated_size()
        self.delete_selection_button.setEnabled(False)
        self.clear_selection_button.setEnabled(False)
        if self.source_faces is not None and not self.busy:
            unlocked_result = (
                self.preview_poly is not None and self.preview_poly is not self.source_poly
            )
            self._set_primary_action(
                self.pass_ready and unlocked_result,
                unlocked_result or len(self.source_faces) > 1_000,
            )
        if message:
            self.status.setText(message)

    def _delete_selected(self, _checked=False, confirm: bool = True) -> None:
        if (
            self.selected_face_mask is None
            or self.source_faces is None
            or self.source_points is None
            or not self.selected_face_mask.any()
        ):
            return
        selected_count = int(self.selected_face_mask.sum())
        if confirm:
            answer = QMessageBox.question(
                self,
                "Delete selected triangles",
                f"Delete {selected_count:,} highlighted triangles from the current mesh?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Cancel,
            )
            if answer != QMessageBox.StandardButton.Yes:
                return
        mask = self.selected_face_mask.copy()
        source_points = self.source_points
        source_faces = self.source_faces
        kept_faces_source = source_faces[~mask]
        if len(kept_faces_source) == 0:
            QMessageBox.warning(self, APP_NAME, "The selection contains the entire mesh. Use Crop instead.")
            return
        token = self._begin_mesh_operation(
            "Deleting selection", f"Removing {fmt_count(selected_count)} selected triangles"
        )
        self.status.setText(f"Deleting {fmt_count(selected_count)} selected triangles…")

        cancel_event = self.operation_cancel_event

        def job():
            try:
                if cancel_event is not None and cancel_event.is_set():
                    raise OperationCancelled
                used = np.unique(kept_faces_source)
                if cancel_event is not None and cancel_event.is_set():
                    raise OperationCancelled
                remap = np.full(len(source_points), -1, dtype=np.int64)
                remap[used] = np.arange(len(used))
                points = np.ascontiguousarray(source_points[used])
                faces = np.ascontiguousarray(remap[kept_faces_source], dtype=np.int32)
                return {
                    "kind": "delete",
                    "poly": arrays_polydata(points, faces),
                    "points": points,
                    "faces": faces,
                    "removed": selected_count,
                }
            except OperationCancelled:
                return {"kind": "delete", "cancelled": True}
            except Exception:
                return {"kind": "delete", "error": traceback.format_exc()}

        future = self.executor.submit(job)
        self.operation_future = future
        future.add_done_callback(lambda f: self.edit_bridge.done.emit(token, f.result()))

    def _finish_mesh_edit(self, token: int, result: dict) -> None:
        if token != self.edit_generation:
            return
        error = result.get("error")
        if error:
            self._end_mesh_operation()
            QMessageBox.critical(self, APP_NAME, f"Mesh operation failed:\n\n{error}")
            self.status.setText("Mesh operation failed.")
            return
        if result.get("cancelled"):
            self._end_mesh_operation()
            self.status.setText("Mesh operation cancelled")
            return
        kind = result["kind"]
        removed = int(result["removed"])
        if kind == "optimize":
            self._end_mesh_operation()
            self._show_selection_optimization_preview(result, removed)
            return
        else:
            message = f"Deleted {fmt_count(removed)} selected triangles"
        # Restore controls before applying the completed edit. Otherwise the pre-operation button
        # snapshot overwrites the Undo, Previous, Reload Original, and Save states established by
        # the new working mesh.
        self._end_mesh_operation()
        self._set_working_mesh(
            result["poly"],
            result["points"],
            result["faces"],
            message,
            preserve_target=(kind == "optimize"),
            committed_optimization=True if kind == "optimize" else None,
        )

    def _show_selection_optimization_preview(self, result: dict, removed: int) -> None:
        if self.source_poly is None:
            return
        self.preview_poly = result["poly"]
        self.simplified_actor = None
        self.preview_is_selection = True
        self.preview_dirty = False
        preview_points = result["points"]
        preview_faces = result["faces"]
        self.preview_count.setText(fmt_count(len(preview_faces)))
        self.preview_vertices.setText(fmt_count(len(preview_points)))
        self._update_optimization_ratio(len(preview_faces))
        self.estimated_file_size.setText(fmt_bytes(binary_stl_size(len(preview_faces))))
        source_size = np.asarray(bounds_size(self.source_poly.GetBounds()))
        preview_size = np.asarray(bounds_size(self.preview_poly.GetBounds()))
        self.dimension_drift_model_units = np.abs(preview_size - source_size)
        self._update_dimension_labels()
        self._show_poly(self.preview_poly, reset_camera=False)
        self.showing_original = False
        self.toggle_mesh_button.setText("Show original")
        self.toggle_mesh_button.setEnabled(True)
        self._set_primary_action(True, True)
        self.save_button.setEnabled(self.mesh_modified)
        self.status.setText(
            f"Selection optimization ready, removed {fmt_count(removed)} triangles â€¢ "
            "Apply or Cancel"
        )

    def _cancel_crop(self, message: str | None) -> None:
        self.crop_start = None
        self._clear_selection(message=message)

    def _hide_crop_preview(self) -> None:
        for actor in self.crop_overlay_actors:
            self.renderer.RemoveViewProp(actor)
        self.crop_overlay_actors = []
        self.crop_points = []
        self.crop_drag_index = None
        if self.crop_selection_actor is not None:
            self.renderer.RemoveActor(self.crop_selection_actor)
            self.crop_selection_actor = None
        if self.source_actor is not None:
            self.source_actor.GetProperty().SetOpacity(1.0)
        if self.crop_info_frame is not None:
            self.crop_info_frame.hide()
        if hasattr(self, "vtk_widget"):
            QApplication.processEvents()
            self.vtk_widget.GetRenderWindow().Render()

    def _reload_original(self) -> None:
        if self.source_path is None or not self.mesh_modified:
            return
        answer = QMessageBox.question(
            self,
            "Reload original mesh",
            "Discard all crops, orientation changes, and the optimized result, then reload the "
            "untouched source STL?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Cancel,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        self._cancel_crop(None)
        self.load_path(self.source_path)

    def _capture_history_state(self) -> MeshHistoryState:
        return MeshHistoryState(
            self.source_poly,
            self.source_points,
            self.source_faces,
            self.source_actor,
            self.mesh_modified,
            self.preview_poly,
            self.simplified_actor,
            (
                self.dimension_drift_model_units.copy()
                if self.dimension_drift_model_units is not None
                else None
            ),
            self.showing_original,
            self.preview_dirty,
            self.has_committed_optimization,
        )

    def _record_history_state(self) -> None:
        if self.source_poly is None or self.source_points is None or self.source_faces is None:
            return
        state = self._capture_history_state()
        self.undo_stack.append(state)
        self.undo_bytes += state.points.nbytes + state.faces.nbytes
        self.redo_stack.clear()
        self.redo_bytes = 0
        self.undo_button.setEnabled(True)
        self.redo_button.setEnabled(False)
        self.previous_view_poly = None
        self.previous_view_actor = None
        self.previous_mesh_button.setEnabled(True)

    def _set_working_mesh(
        self,
        poly: vtkPolyData,
        points: np.ndarray,
        faces: np.ndarray,
        message: str,
        record_undo: bool = True,
        preserve_target: bool = False,
        cached_actor: vtkActor | None = None,
        modified_state: bool | None = None,
        committed_optimization: bool | None = None,
    ) -> None:
        self._mark_geometry_activity(message, 3.0)
        previous_target = (
            self.selection_base_target
            if preserve_target and self.selection_base_target is not None
            else self.target.value()
        )
        if (
            record_undo
            and self.source_poly is not None
            and self.source_points is not None
            and self.source_faces is not None
        ):
            # Working arrays are replaced, never modified in place, so retaining references makes
            # undo instantaneous even for multi-million-triangle scans.
            self._record_history_state()
        self.timer.stop()
        self._cancel_crop(None)
        self._reset_previous_view()
        self.generation += 1
        self.pending_target = None
        self.source_poly = poly
        self.source_points = points
        self.source_faces = faces
        self.preview_poly = None
        self.preview_is_selection = False
        if committed_optimization is not None:
            self.has_committed_optimization = committed_optimization
        self.mesh_modified = True if modified_state is None else modified_state
        self._update_save_button_label()
        self.reload_button.setEnabled(self.mesh_modified)
        self.source_actor = cached_actor
        self.simplified_actor = None
        self.preview_count.setText("—")
        self.preview_vertices.setText("—")
        self.original_count.setText(fmt_count(len(faces)))
        self.original_vertices.setText(fmt_count(len(points)))
        self._update_optimization_ratio(len(faces) if self.mesh_modified else None)
        with QSignalBlocker(self.target):
            self.target.setMaximum(max(1_000, len(faces)))
        self._update_dynamic_presets()
        target = (
            min(previous_target, max(1_000, len(faces)))
            if preserve_target
            else min(
                smart_target(points, faces, self.smart_quality.currentText()),
                max(1_000, len(faces)),
            )
        )
        with QSignalBlocker(self.target):
            self.target.setValue(target)
        self._sync_slider_from_target()
        self.dimension_drift_model_units = None
        self.preview_dirty = True
        self._set_primary_action(False, len(faces) > 1_000)
        self.toggle_mesh_button.setEnabled(False)
        self.toggle_mesh_button.setText("Show original")
        self.save_button.setEnabled(self.mesh_modified)
        self.showing_original = True
        self._update_dimension_labels()
        self._update_estimated_size()
        self._show_poly(poly)
        self._reset_previous_view()
        self.status.setText(f"{message} • {fmt_count(len(faces))} triangles")

    def _undo_working_mesh(self, _checked=False) -> None:
        if self.busy or not self.undo_stack:
            return
        token = self._begin_mesh_operation("Undo", "Restoring previous mesh state")
        QTimer.singleShot(50, lambda: self._finish_history_navigation("undo", token))

    def _redo_working_mesh(self, _checked=False) -> None:
        if self.busy or not self.redo_stack:
            return
        token = self._begin_mesh_operation("Redo", "Restoring next mesh state")
        QTimer.singleShot(50, lambda: self._finish_history_navigation("redo", token))

    def _finish_history_navigation(self, direction: str, token: int) -> None:
        if token != self.edit_generation:
            return
        if (
            self.source_poly is None
            or self.source_points is None
            or self.source_faces is None
        ):
            self._end_mesh_operation()
            return
        current = self._capture_history_state()
        if direction == "undo":
            self.redo_stack.append(current)
            self.redo_bytes += current.points.nbytes + current.faces.nbytes
            state = self.undo_stack.pop()
            self.undo_bytes -= state.points.nbytes + state.faces.nbytes
            message = "Undo"
        else:
            self.undo_stack.append(current)
            self.undo_bytes += current.points.nbytes + current.faces.nbytes
            state = self.redo_stack.pop()
            self.redo_bytes -= state.points.nbytes + state.faces.nbytes
            message = "Redo"
        self._restore_history_state(state, message)
        self._end_mesh_operation()
        self.undo_button.setEnabled(bool(self.undo_stack))
        self.redo_button.setEnabled(bool(self.redo_stack))
        # Ending the busy state restores the controls that were enabled before navigation.
        # Reapply state-derived availability afterward so undoing back to the loaded mesh does
        # not leave Reload Original enabled from the edited state.
        self.reload_button.setEnabled(self.mesh_modified)
        self._reset_previous_view()

    def _restore_history_state(self, state: MeshHistoryState, message: str) -> None:
        self.timer.stop()
        self._cancel_crop(None)
        self.showing_previous = False
        self.previous_view_poly = None
        self.previous_view_actor = None
        self.previous_mesh_button.setText("Show previous")
        self.generation += 1
        self.pending_target = None
        self.source_poly = state.poly
        self.source_points = state.points
        self.source_faces = state.faces
        self.source_actor = state.actor
        self.mesh_modified = state.modified
        self.preview_poly = state.preview_poly
        self.preview_is_selection = False
        self.simplified_actor = state.preview_actor
        self.dimension_drift_model_units = (
            state.dimension_drift.copy() if state.dimension_drift is not None else None
        )
        self.showing_original = state.showing_original
        self.preview_dirty = state.preview_dirty
        self.has_committed_optimization = state.committed_optimization
        self._update_save_button_label()

        self.original_count.setText(fmt_count(len(state.faces)))
        self.original_vertices.setText(fmt_count(len(state.points)))
        self.reload_button.setEnabled(state.modified)
        with QSignalBlocker(self.target):
            self.target.setMaximum(max(1_000, len(state.faces)))
        self._update_dynamic_presets()
        self._sync_slider_from_target()
        self._update_dimension_labels()
        self._update_estimated_size()

        if state.preview_poly is not None:
            preview_points, preview_faces = polydata_arrays(state.preview_poly)
            self.preview_count.setText(fmt_count(len(preview_faces)))
            self.preview_vertices.setText(fmt_count(len(preview_points)))
            self._update_optimization_ratio(len(preview_faces))
            self.estimated_file_size.setText(fmt_bytes(binary_stl_size(len(preview_faces))))
            self.toggle_mesh_button.setEnabled(state.preview_poly is not state.poly)
            self.toggle_mesh_button.setText(
                "Show optimized" if state.showing_original else "Show original"
            )
            self.save_button.setEnabled(state.modified)
            self._set_primary_action(
                not state.preview_dirty and state.preview_poly is not state.poly,
                (not state.preview_dirty and state.preview_poly is not state.poly)
                or (state.preview_dirty and len(state.faces) > 1_000),
            )
            shown = state.poly if state.showing_original else state.preview_poly
            self._show_poly(shown, reset_camera=False)
        else:
            self.preview_count.setText("—")
            self.preview_vertices.setText("—")
            self._update_optimization_ratio(len(state.faces) if state.modified else None)
            self.toggle_mesh_button.setEnabled(False)
            self.toggle_mesh_button.setText("Show original")
            self.save_button.setEnabled(state.modified)
            self._set_primary_action(False, state.preview_dirty and len(state.faces) > 1_000)
            self._show_poly(state.poly, reset_camera=False)
        self.status.setText(message)

    def _discard_selection_preview_for_retry(self) -> None:
        if not self.preview_is_selection or self.preview_poly is None:
            return
        if self.simplified_actor is not None:
            self.renderer.RemoveActor(self.simplified_actor)
        self.preview_poly = None
        self.simplified_actor = None
        self.preview_is_selection = False
        self.pass_ready = False
        self.showing_original = True
        self.toggle_mesh_button.setText("Show original")
        self.toggle_mesh_button.setEnabled(False)
        self.dimension_drift_model_units = None
        self.drift.setText("â€”")
        self._show_poly(self.source_poly, reset_camera=False)
        self._show_selection_primary_action()

    def _target_changed(self, _value: int) -> None:
        if self.crop_candidate is not None or (
            self.selected_face_mask is not None and self.selected_face_mask.any()
        ):
            self._discard_selection_preview_for_retry()
            self.timer.stop()
            self.selection_target = self.target.value()
            self._sync_slider_from_target(self._selected_triangle_count())
            self._update_estimated_size()
            self.status.setText(f"Selection target • {fmt_count(self.selection_target)} triangles")
            return
        self.preview_dirty = True
        self._set_primary_action(False, not self.busy)
        self.toggle_mesh_button.setEnabled(
            self.preview_poly is not None and self.preview_poly is not self.source_poly
        )
        self._update_estimated_size()
        self._sync_slider_from_target()

    @staticmethod
    def _compact_count(value: int) -> str:
        if value >= 1_000_000:
            return f"{value / 1_000_000:.2g}m"
        if value >= 1_000:
            number = value / 1_000
            return f"{number:.0f}k" if number >= 10 else f"{number:.1f}k"
        return str(value)

    def _update_dynamic_presets(self, selection_total: int | None = None) -> None:
        if self.source_faces is None:
            return
        total = selection_total if selection_total is not None else len(self.source_faces)
        for button, fraction in zip(self.preset_buttons, (0.125, 0.25, 0.5, 1.0)):
            count = total if fraction == 1.0 else max(1, round(total * fraction))
            button.setProperty("preset_value", count)
            button.setText(self._compact_count(count))
            if fraction == 1.0:
                description = f"Target all {total:,} triangles."
            else:
                description = f"Target {count:,} triangles ({fraction * 100:g}%)."
            button.setToolTip(description)
            button.setMouseTracking(True)

    def _apply_smart_target(self, _checked=False) -> None:
        if self.source_points is None or self.source_faces is None:
            return
        if self.crop_candidate is not None or (
            self.selected_face_mask is not None and self.selected_face_mask.any()
        ):
            self._discard_selection_preview_for_retry()
            self.timer.stop()
            if self.crop_candidate is not None:
                _, points, faces, _ = self.crop_candidate
            else:
                _, points, faces = self._poly_from_face_mask(self.selected_face_mask)
            target = min(
                smart_target(points, faces, self.smart_quality.currentText()),
                max(1, len(faces) - 1),
            )
            self.selection_target = target
            with QSignalBlocker(self.target):
                self.target.setValue(target)
            self._sync_slider_from_target(len(faces))
            self._update_estimated_size()
            self.status.setText(f"Selection target • {fmt_count(target)} triangles")
            return
        target = smart_target(
            self.source_points, self.source_faces, self.smart_quality.currentText()
        )
        self.preview_dirty = True
        self._set_primary_action(False, not self.busy)
        self.target.setValue(target)
        self._update_estimated_size()

    def _algorithm_changed(self, _algorithm: str) -> None:
        if self.source_faces is None:
            return
        if self.crop_candidate is not None or (
            self.selected_face_mask is not None and self.selected_face_mask.any()
        ):
            self._discard_selection_preview_for_retry()
            self.timer.stop()
            self._update_estimated_size()
            self.status.setText(f"Selection algorithm • {_algorithm}")
            return
        self.preview_dirty = True
        self._set_primary_action(False, not self.busy)
        self.toggle_mesh_button.setEnabled(
            self.preview_poly is not None and self.preview_poly is not self.source_poly
        )
        self._update_estimated_size()

    def _slider_changed(self, value: int) -> None:
        if self.source_faces is None:
            return
        selection_total = self._selected_triangle_count()
        total = selection_total or len(self.source_faces)
        minimum = min(1_000, max(4, total - 1))
        low = math.log10(minimum)
        high = math.log10(max(minimum + 1, total))
        count = max(minimum, int(round(10 ** (low + (high - low) * value / 1000), -2)))
        with QSignalBlocker(self.target):
            self.target.setValue(count)
        if selection_total:
            self._discard_selection_preview_for_retry()
            self.timer.stop()
            self.selection_target = min(count, max(4, selection_total - 1))
            self._update_estimated_size()
            self.status.setText(f"Selection target • {fmt_count(self.selection_target)} triangles")
            return
        self.preview_dirty = True
        self._set_primary_action(False, not self.busy)
        self.toggle_mesh_button.setEnabled(
            self.preview_poly is not None and self.preview_poly is not self.source_poly
        )
        self._update_estimated_size()

    def _sync_slider_from_target(self, selection_total: int | None = None) -> None:
        if self.source_faces is None:
            return
        total = selection_total or len(self.source_faces)
        minimum = min(1_000, max(4, total - 1))
        low = math.log10(minimum)
        high = math.log10(max(minimum + 1, total))
        pos = round(1000 * (math.log10(max(minimum, self.target.value())) - low) / (high - low))
        with QSignalBlocker(self.slider):
            self.slider.setValue(max(0, min(1000, pos)))

    def preview(self) -> None:
        if self.source_points is None or self.source_faces is None:
            return
        if self._selected_triangle_count():
            self.timer.stop()
            self.status.setText(
                f"Selection active • {self.shortcuts['selection_optimize']} to optimize"
            )
            return
        if not self.preview_dirty:
            return
        target = min(self.target.value(), len(self.source_faces))
        if target < 4:
            return
        if target >= len(self.source_faces):
            self.timer.stop()
            self.preview_poly = self.source_poly
            self.simplified_actor = self.source_actor
            self.preview_count.setText(fmt_count(len(self.source_faces)))
            self.preview_vertices.setText(fmt_count(len(self.source_points)))
            self._update_optimization_ratio(len(self.source_faces))
            self.dimension_drift_model_units = np.zeros(3)
            self._update_dimension_labels()
            self.estimated_file_size.setText(fmt_bytes(binary_stl_size(len(self.source_faces))))
            self.preview_dirty = False
            self._set_primary_action(False, False)
            self.toggle_mesh_button.setEnabled(False)
            self.save_button.setEnabled(self.mesh_modified)
            self.showing_original = True
            self.status.setText(f"No optimization needed • {fmt_count(len(self.source_faces))} triangles")
            return
        if self.busy:
            self.pending_target = target
            self.status.setText(f"Finishing current optimization; queued {fmt_count(target)} triangles…")
            return
        self.pending_target = None
        self.generation += 1
        self.running_target = target
        generation = self.generation
        self._begin_mesh_operation(
            "Optimizing",
            f"Optimizing {fmt_count(len(self.source_faces))} triangles to about {fmt_count(target)}",
        )
        self._set_primary_action(False, False)
        self.save_button.setEnabled(self.mesh_modified)
        self.status.setText(f"Optimizing to about {fmt_count(target)} triangles…")
        points = self.source_points
        faces = self.source_faces
        algorithm = self.algorithm.currentText()
        self.operation_uses_process = True
        future = self.optimization_executor.submit(
            simplify_process_job, points, faces, target, algorithm
        )
        self.operation_future = future

        def completed(result_future) -> None:
            try:
                result = result_future.result()
            except Exception:
                result = (None, None, traceback.format_exc())
            self.bridge.done.emit(generation, *result)

        future.add_done_callback(completed)

    def _finish_simplify(self, generation: int, points, faces, error) -> None:
        if generation != self.generation:
            return
        self._end_mesh_operation()
        target_changed = self.running_target is not None and self.target.value() != self.running_target
        self.preview_dirty = target_changed
        self._set_primary_action(False, self.preview_dirty)
        self.running_target = None
        if error:
            self.status.setText("Optimization failed.")
            self.preview_dirty = True
            self._set_primary_action(False, True)
            QMessageBox.critical(self, APP_NAME, error)
        elif generation == self.generation:
            self.preview_poly = arrays_polydata(points, faces)
            self.preview_is_selection = False
            self.simplified_actor = None
            self.preview_count.setText(fmt_count(len(faces)))
            self.preview_vertices.setText(fmt_count(len(points)))
            self._update_optimization_ratio(len(faces))
            self.estimated_file_size.setText(fmt_bytes(binary_stl_size(len(faces))))
            source_size = np.asarray(bounds_size(self.source_poly.GetBounds()))
            preview_size = np.asarray(bounds_size(self.preview_poly.GetBounds()))
            drift = np.abs(preview_size - source_size)
            self.dimension_drift_model_units = drift
            self._update_dimension_labels()
            self._show_poly(self.preview_poly, reset_camera=False)
            self.showing_original = False
            self.toggle_mesh_button.setText("Show original")
            self.toggle_mesh_button.setEnabled(True)
            self._set_primary_action(True, True)
            self.save_button.setEnabled(self.mesh_modified)
            self.status.setText(f"Optimized result ready • {fmt_count(len(faces))} triangles")
            if self.verification_screenshot is not None:
                capture_path = self.verification_screenshot
                self.verification_screenshot = None
                QTimer.singleShot(750, lambda: self._capture_and_exit(capture_path))
        if self.pending_target is not None:
            self.pending_target = None
            self.preview_dirty = True
            QTimer.singleShot(0, self.preview)

    def _units_changed(self, _unit: str) -> None:
        self._update_dimension_labels()
        self._update_scale_bar()
        if self.measure_units is not None and not self.measure_units_overridden:
            with QSignalBlocker(self.measure_units):
                self.measure_units.setCurrentText(_unit)
            self._update_measure_panel()

    def _update_optimization_ratio(self, optimized_triangles: int | None) -> None:
        if self.loaded_triangle_count <= 0 or not optimized_triangles:
            self.optimization_ratio.setText("—")
            return
        reduction = 100.0 * (1.0 - optimized_triangles / self.loaded_triangle_count)
        self.optimization_ratio.setText(f"{reduction:.1f}%")

    def _update_save_button_label(self) -> None:
        label = "Save current mesh"
        if self.loaded_triangle_count > 0 and self.source_faces is not None:
            reduction = 100.0 * (1.0 - len(self.source_faces) / self.loaded_triangle_count)
            if reduction >= 0.05:
                percentage = f"{reduction:.1f}".rstrip("0").rstrip(".")
                label += f" (-{percentage}%)"
        self.save_button.setText(label + "…")

    def _update_dimension_labels(self) -> None:
        unit = self.units.currentText()
        divisor = UNIT_MM[unit]
        self.dimensions_caption.setText(f"Dimensions ({unit}):")
        if self.source_poly is not None:
            size = np.asarray(bounds_size(self.source_poly.GetBounds())) / divisor
            self.dimensions.setText(fmt_size(tuple(size)))
        if self.dimension_drift_model_units is not None:
            drift = self.dimension_drift_model_units / divisor
            self.drift.setText(" x ".join(f"{v:.4f}" for v in drift) + f" {unit}")
        else:
            self.drift.setText("—")

    def _update_estimated_size(self) -> None:
        if self.source_faces is None or self.source_points is None:
            self.preview_count.setText("—")
            self.preview_vertices.setText("—")
            self.estimated_file_size.setText("—")
            return
        if self.overview_mode:
            self.preview_count.setText("—")
            self.preview_vertices.setText("—")
            self.optimization_ratio.setText("—")
            self.estimated_file_size.setText("—")
            return
        working_triangles = len(self.source_faces)
        selected_triangles = self._selected_triangle_count()
        requested = self.selection_target if selected_triangles else self.target.value()
        target = min(
            max(1, int(requested or self.target.value())),
            selected_triangles or working_triangles,
        )
        estimated_triangles = (
            working_triangles - selected_triangles + target
            if selected_triangles
            else target
        )
        vertex_ratio = len(self.source_points) / max(1, working_triangles)
        estimated_vertices = min(
            len(self.source_points),
            max(4, round(estimated_triangles * vertex_ratio)),
        )
        self.preview_count.setText(f"~{fmt_count(estimated_triangles)}")
        self.preview_vertices.setText(f"~{fmt_count(estimated_vertices)}")
        self._update_optimization_ratio(estimated_triangles)
        self.dimension_drift_model_units = None
        self.drift.setText("—")
        self.estimated_file_size.setText(fmt_bytes(binary_stl_size(estimated_triangles)))

    def _set_primary_action(self, pass_ready: bool, enabled: bool) -> None:
        self.pass_ready = pass_ready
        self.preview_button.setText("Apply" if pass_ready else "Optimize")
        self.preview_button.setToolTip(
            "Apply this optimized result as the mesh for the next pass."
            if pass_ready
            else "Optimize the mesh using the current settings."
        )
        self.preview_button.setEnabled(enabled)
        if hasattr(self, "cancel_preview_button"):
            has_unlocked_result = (
                self.preview_poly is not None
                and self.source_poly is not None
                and self.preview_poly is not self.source_poly
            )
            self.cancel_preview_button.setEnabled(has_unlocked_result and not self.busy)

    def _primary_optimize_action(self, _checked=False) -> None:
        if self.pass_ready:
            self._apply_optimized_pass()
        elif self._selected_triangle_count():
            self._selection_shortcut("optimize")
        else:
            self.preview()

    def _show_selection_primary_action(self) -> None:
        if not hasattr(self, "preview_button") or not self._selected_triangle_count():
            return
        self.preview_button.setText("Optimize selection")
        self.preview_button.setToolTip(
            "Optimize only the highlighted triangles using the current settings."
        )
        self.preview_button.setEnabled(not self.busy)

    def _cancel_optimized_preview(self, _checked=False) -> None:
        if (
            self.busy
            or self.source_poly is None
            or self.preview_poly is None
            or self.preview_poly is self.source_poly
        ):
            return
        was_selection_preview = self.preview_is_selection
        if self.simplified_actor is not None:
            self.renderer.RemoveActor(self.simplified_actor)
        self.preview_poly = None
        self.preview_is_selection = False
        self.simplified_actor = None
        self.pending_target = None
        self.running_target = None
        self.showing_original = True
        self.showing_previous = False
        self.toggle_mesh_button.setText("Show original")
        self.toggle_mesh_button.setEnabled(False)
        self.previous_mesh_button.setText("Show previous")
        self.dimension_drift_model_units = None
        self.drift.setText("â€”")
        self.preview_dirty = True
        self._update_estimated_size()
        self._set_primary_action(
            False, self.source_faces is not None and len(self.source_faces) > 1_000
        )
        self.save_button.setEnabled(self.mesh_modified)
        self._show_poly(self.source_poly, reset_camera=False)
        if was_selection_preview and self._selected_triangle_count():
            self._show_selection_primary_action()
            self._refresh_persistent_selection()
            self.status.setText("Selection optimization cancelled â€¢ selection retained")
        else:
            self.status.setText("Optimization cancelled")

    def _apply_optimized_pass(self, _checked=False) -> None:
        if (
            self.busy
            or self.preview_poly is None
            or self.source_poly is None
            or self.preview_poly is self.source_poly
        ):
            return
        points, faces = polydata_arrays(self.preview_poly)
        applied_poly = self.preview_poly
        applied_actor = self.simplified_actor
        selection_pass = self.preview_is_selection
        if selection_pass:
            self.preview_poly = None
            self.simplified_actor = None
            self.preview_is_selection = False
        self._set_working_mesh(
            applied_poly,
            points,
            faces,
            "Applied optimization",
            preserve_target=selection_pass,
            cached_actor=applied_actor,
            committed_optimization=True,
        )

    def _toggle_mesh(self) -> None:
        if self.source_poly is None or self.preview_poly is None:
            return
        self.showing_previous = False
        self.previous_mesh_button.setText("Show previous")
        if self.showing_original:
            self.toggle_mesh_button.setText("Show original")
            self.showing_original = False
            self._show_poly(self.preview_poly, reset_camera=False)
        else:
            self.toggle_mesh_button.setText("Show optimized")
            self.showing_original = True
            self._show_poly(self.source_poly, reset_camera=False)

    def _reset_previous_view(self) -> None:
        self.showing_previous = False
        self.previous_view_poly = None
        self.previous_view_actor = None
        if hasattr(self, "previous_mesh_button"):
            self.previous_mesh_button.setText("Show previous")
            previous = self.undo_stack[-1].poly if self.undo_stack else None
            current = (
                self.source_poly
                if self.showing_original or self.preview_poly is None
                else self.preview_poly
            )
            self.previous_mesh_button.setEnabled(
                previous is not None and previous is not current and not self.busy
            )

    def _toggle_previous_mesh(self) -> None:
        if self.source_poly is None or not self.undo_stack:
            return
        if self.showing_previous:
            self.showing_previous = False
            self.previous_mesh_button.setText("Show previous")
            current = (
                self.source_poly
                if self.showing_original or self.preview_poly is None
                else self.preview_poly
            )
            self._show_poly(current, reset_camera=False)
            previous = self.undo_stack[-1].poly if self.undo_stack else None
            self.previous_mesh_button.setEnabled(previous is not current and not self.busy)
            return

        previous = self.undo_stack[-1].poly
        if self.previous_view_poly is not previous or self.previous_view_actor is None:
            self.previous_view_poly = previous
            self._show_poly(previous, reset_camera=False)
            self.previous_view_actor = self.active_actor
        else:
            self._set_actor_display_mode(self.previous_view_actor)
            self._show_cached_actor(self.previous_view_actor, reset_camera=False)
        self.showing_previous = True
        self.previous_mesh_button.setText("Show current")
        current = (
            self.source_poly
            if self.showing_original or self.preview_poly is None
            else self.preview_poly
        )
        self.previous_mesh_button.setEnabled(current is not previous and not self.busy)

    def _capture_and_exit(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.vtk_widget.GetRenderWindow().Render()
        capture = vtkWindowToImageFilter()
        capture.SetInput(self.vtk_widget.GetRenderWindow())
        capture.SetInputBufferTypeToRGBA()
        capture.ReadFrontBufferOff()
        capture.Update()
        rendered = capture.GetOutput()
        image_width, image_height, _ = rendered.GetDimensions()
        rgba = vtk_to_numpy(rendered.GetPointData().GetScalars()).reshape(
            image_height, image_width, 4
        )
        rgba = np.ascontiguousarray(np.flipud(rgba))
        viewport_image = QImage(
            rgba.data,
            image_width,
            image_height,
            image_width * 4,
            QImage.Format.Format_RGBA8888,
        ).copy()

        screenshot = self.grab()
        painter = QPainter(screenshot)
        viewport_position = self.vtk_widget.mapTo(self, QPoint(0, 0))
        painter.drawImage(
            QRect(
                viewport_position.x(),
                viewport_position.y(),
                self.vtk_widget.width(),
                self.vtk_widget.height(),
            ),
            viewport_image,
        )
        for overlay in (
            self.view_pad,
            self.orientation_indicator,
            self.scale_bar,
            self.density_legend,
            self.loading_frame,
            self.crop_info_frame,
            self.measure_info_frame,
            self.loupe_frame,
        ):
            if overlay is not None and overlay.isVisible():
                position = overlay.mapTo(self, QPoint(0, 0))
                painter.drawPixmap(position, overlay.grab())
        painter.end()
        if not screenshot.save(os.fspath(path), "PNG"):
            QMessageBox.critical(self, APP_NAME, f"Could not save verification screenshot:\n{path}")
            return
        QApplication.instance().quit()

    def _show_poly(self, poly: vtkPolyData, reset_camera: bool = True) -> None:
        if poly is self.source_poly and self.source_actor is not None:
            actor = self.source_actor
        elif poly is self.preview_poly and self.simplified_actor is not None:
            actor = self.simplified_actor
        else:
            normals = vtkPolyDataNormals()
            normals.SetInputData(poly)
            normals.ComputePointNormalsOn()
            normals.ComputeCellNormalsOff()
            normals.SplittingOff()
            normals.ConsistencyOn()
            normals.Update()
            mapper = vtkPolyDataMapper()
            mapper.SetInputConnection(normals.GetOutputPort())
            actor = vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetColor(0.76, 0.80, 0.84)
            actor.GetProperty().SetInterpolationToPhong()
            actor.GetProperty().SetEdgeColor(0.1, 0.1, 0.12)
            actor.GetProperty().SetEdgeVisibility(False)
            if poly is self.source_poly:
                self.source_actor = actor
            elif poly is self.preview_poly:
                self.simplified_actor = actor
            elif poly is self.previous_view_poly:
                self.previous_view_actor = actor
        if (
            self._display_mode() == "Density"
            and id(poly) not in self.density_cache
        ):
            self.pending_density_poly = poly
            self.density_legend.setVisible(True)
            self.density_legend.raise_()
            self.renderer.RemoveAllViewProps()
            self.preview_actor = None
            self.active_actor = None
            self.vtk_widget.GetRenderWindow().Render()
            QTimer.singleShot(0, lambda requested=poly: self._request_density_analysis(requested))
            return
        self.pending_density_poly = None
        self._set_actor_display_mode(actor)
        self._show_cached_actor(actor, reset_camera)

    def _show_cached_actor(self, actor: vtkActor | None, reset_camera: bool = False) -> None:
        if actor is None:
            return
        self._hide_loupe()
        self.renderer.RemoveAllViewProps()
        self.renderer.AddActor(actor)
        self.preview_actor = actor
        self.active_actor = actor
        if (
            actor is self.source_actor
            and self.crop_selection_actor is not None
            and self.selected_face_mask is not None
        ):
            self.renderer.AddActor(self.crop_selection_actor)
            actor.GetProperty().SetOpacity(0.12)
        if reset_camera:
            self.renderer.ResetCamera()
            self.renderer.GetActiveCamera().Zoom(1.28)
            self.renderer.ResetCameraClippingRange()
        self._update_measure_overlay(render=False)
        self.vtk_widget.GetRenderWindow().Render()
        density_visible = self._display_mode() == "Density"
        self.density_legend.setVisible(density_visible)
        if density_visible:
            self.density_legend.raise_()

    def _show_loupe(self, visible: bool) -> None:
        if not visible:
            self._hide_loupe()
            return
        if self.active_actor is None:
            return
        interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        x, y = interactor.GetEventPosition()
        width, height = self.vtk_widget.GetRenderWindow().GetSize()
        if width <= 0 or height <= 0:
            return
        if self.loupe_frame is None:
            diameter = 360
            self.loupe_frame = QFrame(self.vtk_widget)
            self.loupe_frame.setFixedSize(diameter, diameter)
            self.loupe_frame.setMask(QRegion(0, 0, diameter, diameter, QRegion.RegionType.Ellipse))
            self.loupe_frame.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
            self.loupe_frame.setStyleSheet(
                "QFrame { border: 3px solid #2563FF; border-radius: 180px; background: #080b10; }"
            )
            self.loupe_label = QLabel(self.loupe_frame)
            self.loupe_label.setGeometry(3, 3, diameter - 6, diameter - 6)
            self.loupe_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        self.vtk_widget.GetRenderWindow().Render()
        capture = vtkWindowToImageFilter()
        capture.SetInput(self.vtk_widget.GetRenderWindow())
        capture.SetInputBufferTypeToRGBA()
        capture.ReadFrontBufferOff()
        capture.Update()
        rendered = capture.GetOutput()
        image_width, image_height, _ = rendered.GetDimensions()
        rgba = vtk_to_numpy(rendered.GetPointData().GetScalars()).reshape(image_height, image_width, 4)
        rgba = np.ascontiguousarray(np.flipud(rgba))
        image = QImage(
            rgba.data, image_width, image_height, image_width * 4, QImage.Format.Format_RGBA8888
        ).copy()

        diameter = self.loupe_frame.width()
        inner = diameter - 6
        crop_size = max(20, inner // 4)
        image_y = image_height - y
        crop_left = max(0, min(image_width - crop_size, x - crop_size // 2))
        crop_top = max(0, min(image_height - crop_size, image_y - crop_size // 2))
        crop = image.copy(crop_left, crop_top, crop_size, crop_size)
        pixmap = QPixmap.fromImage(crop).scaled(
            inner,
            inner,
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.loupe_label.setPixmap(pixmap)

        margin = 10
        qt_y = height - y
        left = min(max(margin, x - diameter // 2), max(margin, width - diameter - margin))
        top = min(max(margin, qt_y - diameter // 2), max(margin, height - diameter - margin))
        self.loupe_frame.move(left, top)
        self.loupe_frame.show()
        self.loupe_frame.raise_()

    def _hide_loupe(self) -> None:
        if self.loupe_frame is not None:
            self.loupe_frame.hide()

    def _set_actor_display_mode(self, actor: vtkActor) -> None:
        mode = self._display_mode()
        mapper = actor.GetMapper()
        mapper.ScalarVisibilityOff()
        mapper.SetScalarModeToDefault()
        actor.GetProperty().SetColor(0.76, 0.80, 0.84)
        actor.GetProperty().SetAmbient(0.0)
        actor.GetProperty().SetDiffuse(1.0)
        actor.GetProperty().SetInterpolationToPhong()
        if mode == "Wireframe":
            actor.GetProperty().SetRepresentationToWireframe()
            actor.GetProperty().SetLineWidth(1.0)
            actor.GetProperty().SetPointSize(1.0)
            actor.GetProperty().SetEdgeVisibility(False)
        elif mode == "Vertices":
            actor.GetProperty().SetRepresentationToPoints()
            actor.GetProperty().SetPointSize(2.5)
            actor.GetProperty().SetEdgeVisibility(False)
        elif mode == "Density":
            actor.GetProperty().SetRepresentationToSurface()
            actor.GetProperty().SetEdgeVisibility(False)
            actor.GetProperty().SetAmbient(0.72)
            actor.GetProperty().SetDiffuse(0.28)
            actor.GetProperty().SetInterpolationToFlat()
            if actor is self.source_actor:
                poly = self.source_poly
            elif actor is self.previous_view_actor:
                poly = self.previous_view_poly
            else:
                poly = self.preview_poly
            density_colors = self.density_cache.get(id(poly)) if poly is not None else None
            if density_colors is not None:
                # Accept the former (point, cell) cache shape while restoring older history in
                # development sessions; new entries store only the smaller point-color array.
                colors = density_colors[0] if isinstance(density_colors, tuple) else density_colors
                render_poly = mapper.GetInput()
                if render_poly is None:
                    mapper.Update()
                    render_poly = mapper.GetInput()
                point_data = render_poly.GetPointData()
                if point_data.GetArray("PointDensityColors") is None:
                    vtk_colors = numpy_to_vtk(colors, deep=True)
                    vtk_colors.SetName("PointDensityColors")
                    point_data.AddArray(vtk_colors)
                point_data.SetActiveScalars("PointDensityColors")
                mapper.SetScalarModeToUsePointFieldData()
                mapper.SelectColorArray("PointDensityColors")
                mapper.SetColorModeToDirectScalars()
                mapper.InterpolateScalarsBeforeMappingOff()
                mapper.ScalarVisibilityOn()
                mapper.Modified()
        else:
            actor.GetProperty().SetRepresentationToSurface()
            actor.GetProperty().SetLineWidth(1.0)
            actor.GetProperty().SetPointSize(1.0)
            actor.GetProperty().SetEdgeVisibility(False)

    def _active_density_mesh(self):
        if self.showing_previous and self.previous_view_poly is not None:
            return self.previous_view_poly, *polydata_arrays(self.previous_view_poly)
        if self.active_actor is self.simplified_actor and self.preview_poly is not None:
            return self.preview_poly, *polydata_arrays(self.preview_poly)
        if self.source_poly is not None and self.source_points is not None and self.source_faces is not None:
            return self.source_poly, self.source_points, self.source_faces
        return None, None, None

    def _request_density_analysis(self, requested_poly: vtkPolyData | None = None) -> None:
        if self._display_mode() != "Density":
            return
        if requested_poly is self.source_poly:
            poly, points, faces = self.source_poly, self.source_points, self.source_faces
        elif requested_poly is self.preview_poly and self.preview_poly is not None:
            poly, points, faces = self.preview_poly, *polydata_arrays(self.preview_poly)
        elif requested_poly is self.previous_view_poly and self.previous_view_poly is not None:
            poly, points, faces = self.previous_view_poly, *polydata_arrays(self.previous_view_poly)
        else:
            poly, points, faces = self._active_density_mesh()
        if poly is None or points is None or faces is None:
            return
        if id(poly) in self.density_cache:
            self._show_poly(poly, reset_camera=False)
            return
        if self.busy:
            QTimer.singleShot(250, lambda requested=poly: self._request_density_analysis(requested))
            return
        self.density_generation += 1
        token = self.density_generation
        poly_key = id(poly)
        self._begin_mesh_operation(
            "Analyzing point density",
            f"Mapping {fmt_count(len(points))} vertices across {fmt_count(len(faces))} triangles",
        )
        cancel_event = self.operation_cancel_event

        def job():
            try:
                return point_density_colors(points, faces, cancel_event), None
            except OperationCancelled:
                return None, "cancelled"
            except Exception:
                return None, traceback.format_exc()

        future = self.executor.submit(job)
        self.operation_future = future
        future.add_done_callback(
            lambda f: self.density_bridge.done.emit(token, poly_key, *f.result())
        )

    def _finish_density_analysis(self, token: int, poly_key: int, colors, error) -> None:
        if token != self.density_generation:
            return
        self._end_mesh_operation()
        if error:
            self.status.setText("Point density analysis failed")
            QMessageBox.critical(self, APP_NAME, error)
            return
        self.density_cache[poly_key] = colors
        if self._display_mode() == "Density":
            requested = self.pending_density_poly
            if requested is not None and id(requested) == poly_key:
                self._show_poly(requested, reset_camera=False)
            self.status.setText("Point density ready")

    def _apply_display_mode(self, mode: str) -> None:
        self.settings.setValue("display/type", mode)
        self.density_legend.setVisible(mode == "Density")
        if mode == "Density":
            self.density_legend.raise_()
            poly, _points, _faces = self._active_density_mesh()
            if poly is not None:
                self._show_poly(poly, reset_camera=False)
            return
        self.pending_density_poly = None
        for actor in (self.source_actor, self.simplified_actor, self.previous_view_actor):
            if actor is not None:
                self._set_actor_display_mode(actor)
        shown = (
            self.previous_view_actor
            if self.showing_previous
            else self.source_actor if self.showing_original else self.simplified_actor
        )
        self._show_cached_actor(shown, reset_camera=False)

    def _save_shortcut_activated(self) -> None:
        if self.save_button.isEnabled():
            self.save_file()

    def _show_about(self) -> None:
        QMessageBox.about(
            self,
            f"About {APP_NAME}",
            f"{APP_NAME} {APP_VERSION}\n\n"
            "STL mesh inspection, selection, and optimization.\n\n"
            "GNU General Public License v3.0 or later.",
        )

    def _open_repository(self) -> None:
        if REPOSITORY_URL:
            QDesktopServices.openUrl(QUrl(REPOSITORY_URL))

    def save_file(self) -> None:
        if (
            not self.mesh_modified
            or self.source_poly is None
            or self.source_faces is None
            or self.source_path is None
        ):
            return
        suggested = self.source_path.with_name(
            f"{self.source_path.stem}_{len(self.source_faces) // 1000}k.stl"
        )
        path, _ = QFileDialog.getSaveFileName(
            self, "Save current mesh", os.fspath(suggested), "STL mesh (*.stl)"
        )
        if not path:
            return
        if not path.lower().endswith(".stl"):
            path += ".stl"
        try:
            save_stl(self.source_poly, Path(path))
        except OSError:
            QMessageBox.critical(self, APP_NAME, "VTK could not save the STL.")
            return
        self.status.setText(f"Saved {path}")


def main() -> int:
    cli_name = Path(sys.executable).stem.lower().endswith("cli")
    if "--cli" in sys.argv or cli_name:
        args = [arg for arg in sys.argv[1:] if arg != "--cli"]
        return cli_main(args)
    verify_parser = argparse.ArgumentParser(add_help=False)
    verify_parser.add_argument("--verification-screenshot", type=Path)
    verify_parser.add_argument("--verification-target", type=int, default=200_000)
    verify_parser.add_argument("--diagnostic-log", type=Path)
    verify_args, qt_args = verify_parser.parse_known_args(sys.argv[1:])
    app = QApplication([sys.argv[0], *qt_args])
    app.setApplicationName(APP_NAME)
    app_icon = resource_path("assets/meshmill-mark.svg")
    if app_icon.exists():
        app.setWindowIcon(QIcon(os.fspath(app_icon)))
    window = MainWindow()
    window.diagnostic_log_path = verify_args.diagnostic_log
    if window.diagnostic_log_path is not None:
        window.diagnostic_log_path.unlink(missing_ok=True)
        window._diagnostic("session_start", argv=sys.argv[1:])
    window.verification_screenshot = verify_args.verification_screenshot
    window.verification_target = verify_args.verification_target
    window.showMaximized()
    paths = [arg for arg in qt_args if not arg.startswith("-")]
    if paths:
        def load_initial() -> None:
            window.load_path(Path(paths[0]))
        QTimer.singleShot(0, load_initial)
    return app.exec()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    raise SystemExit(main())
