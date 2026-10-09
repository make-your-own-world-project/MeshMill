from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import meshmill as mm


def test_toolbox_content_stays_inside_scroll_viewport():
    app = QApplication.instance() or QApplication([])
    window = mm.MainWindow()
    window.resize(1920, 1040)
    window.show()
    app.processEvents()

    viewport_width = window.controls_widget.viewport().width()
    assert window.controls_content.minimumWidth() == 0
    assert window.controls_content.width() <= viewport_width

    # These are the widest repeated rows and previously pushed their final
    # controls behind the right edge of the toolbox.
    window.cancel_preview_button.setEnabled(True)
    window.previous_mesh_button.setEnabled(True)
    window._update_action_row_visibility()
    app.processEvents()
    for widget in (
        window.target_display,
        window.smart_quality,
        window.redo_button,
        window.previous_mesh_button,
        window.repository_button,
    ):
        right_edge = widget.mapTo(window.controls_content, widget.rect().topRight()).x()
        assert right_edge <= viewport_width, (widget.text(), right_edge, viewport_width)

    window.source_poly = object()
    window.mesh_modified = True
    window._sync_modified_mesh_actions()
    assert window.save_button.isEnabled() and window.save_button.isVisible()
    assert window.reload_button.isEnabled() and window.reload_button.isVisible()

    window.mesh_modified = False
    window._sync_modified_mesh_actions()
    assert not window.save_button.isEnabled() and not window.save_button.isVisible()
    assert not window.reload_button.isEnabled() and not window.reload_button.isVisible()

    window.close()
