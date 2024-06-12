# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
from __future__ import annotations

"""
This file contains the exact signatures for all functions in module
PySide6.QtQuickWidgets, except for defaults which are replaced by "...".
"""

# Module `PySide6.QtQuickWidgets`

import PySide6.QtQuickWidgets
import PySide6.QtCore
import PySide6.QtGui
import PySide6.QtWidgets
import PySide6.QtQml
import PySide6.QtQuick

import enum
from typing import Any, ClassVar, List, List, Optional, Union, overload
from PySide6.QtCore import Signal


NoneType: TypeAlias = type[None]


class QIntList(object): ...


class QQuickWidget(PySide6.QtWidgets.QWidget):

    sceneGraphError          : ClassVar[Signal] = ... # sceneGraphError(QQuickWindow::SceneGraphError,QString)
    statusChanged            : ClassVar[Signal] = ... # statusChanged(QQuickWidget::Status)

    class ResizeMode(enum.Enum):

        SizeViewToRootObject     : QQuickWidget.ResizeMode = ... # 0x0
        SizeRootObjectToView     : QQuickWidget.ResizeMode = ... # 0x1

    class Status(enum.Enum):

        Null                     : QQuickWidget.Status = ... # 0x0
        Ready                    : QQuickWidget.Status = ... # 0x1
        Loading                  : QQuickWidget.Status = ... # 0x2
        Error                    : QQuickWidget.Status = ... # 0x3


    @overload
    def __init__(self, engine: PySide6.QtQml.QQmlEngine, parent: PySide6.QtWidgets.QWidget) -> None: ...
    @overload
    def __init__(self, parent: Optional[PySide6.QtWidgets.QWidget] = ...) -> None: ...
    @overload
    def __init__(self, source: Union[PySide6.QtCore.QUrl, str], parent: Optional[PySide6.QtWidgets.QWidget] = ...) -> None: ...

    def dragEnterEvent(self, arg__1: PySide6.QtGui.QDragEnterEvent) -> None: ...
    def dragLeaveEvent(self, arg__1: PySide6.QtGui.QDragLeaveEvent) -> None: ...
    def dragMoveEvent(self, arg__1: PySide6.QtGui.QDragMoveEvent) -> None: ...
    def dropEvent(self, arg__1: PySide6.QtGui.QDropEvent) -> None: ...
    def engine(self) -> PySide6.QtQml.QQmlEngine: ...
    def errors(self) -> List[PySide6.QtQml.QQmlError]: ...
    def event(self, arg__1: PySide6.QtCore.QEvent) -> bool: ...
    def focusInEvent(self, event: PySide6.QtGui.QFocusEvent) -> None: ...
    def focusNextPrevChild(self, next: bool) -> bool: ...
    def focusOutEvent(self, event: PySide6.QtGui.QFocusEvent) -> None: ...
    def format(self) -> PySide6.QtGui.QSurfaceFormat: ...
    def grabFramebuffer(self) -> PySide6.QtGui.QImage: ...
    def hideEvent(self, arg__1: PySide6.QtGui.QHideEvent) -> None: ...
    def initialSize(self) -> PySide6.QtCore.QSize: ...
    def keyPressEvent(self, arg__1: PySide6.QtGui.QKeyEvent) -> None: ...
    def keyReleaseEvent(self, arg__1: PySide6.QtGui.QKeyEvent) -> None: ...
    def mouseDoubleClickEvent(self, arg__1: PySide6.QtGui.QMouseEvent) -> None: ...
    def mouseMoveEvent(self, arg__1: PySide6.QtGui.QMouseEvent) -> None: ...
    def mousePressEvent(self, arg__1: PySide6.QtGui.QMouseEvent) -> None: ...
    def mouseReleaseEvent(self, arg__1: PySide6.QtGui.QMouseEvent) -> None: ...
    def paintEvent(self, event: PySide6.QtGui.QPaintEvent) -> None: ...
    def quickWindow(self) -> PySide6.QtQuick.QQuickWindow: ...
    def resizeEvent(self, arg__1: PySide6.QtGui.QResizeEvent) -> None: ...
    def resizeMode(self) -> PySide6.QtQuickWidgets.QQuickWidget.ResizeMode: ...
    def rootContext(self) -> PySide6.QtQml.QQmlContext: ...
    def rootObject(self) -> PySide6.QtQuick.QQuickItem: ...
    def setClearColor(self, color: Union[PySide6.QtGui.QColor, str, PySide6.QtGui.QRgba64, Any, PySide6.QtCore.Qt.GlobalColor, int]) -> None: ...
    def setContent(self, url: Union[PySide6.QtCore.QUrl, str], component: PySide6.QtQml.QQmlComponent, item: PySide6.QtCore.QObject) -> None: ...
    def setFormat(self, format: Union[PySide6.QtGui.QSurfaceFormat, PySide6.QtGui.QSurfaceFormat.FormatOption]) -> None: ...
    def setResizeMode(self, arg__1: PySide6.QtQuickWidgets.QQuickWidget.ResizeMode) -> None: ...
    def setSource(self, arg__1: Union[PySide6.QtCore.QUrl, str]) -> None: ...
    def showEvent(self, arg__1: PySide6.QtGui.QShowEvent) -> None: ...
    def sizeHint(self) -> PySide6.QtCore.QSize: ...
    def source(self) -> PySide6.QtCore.QUrl: ...
    def status(self) -> PySide6.QtQuickWidgets.QQuickWidget.Status: ...
    def timerEvent(self, arg__1: PySide6.QtCore.QTimerEvent) -> None: ...
    def wheelEvent(self, arg__1: PySide6.QtGui.QWheelEvent) -> None: ...


# eof
