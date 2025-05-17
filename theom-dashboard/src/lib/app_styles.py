def stylesheet():
    return (
        """
        QWidget {
            background-color: #111111;
            color: #b9c7cb;
            font-family: 'Segoe UI', sans-serif;
            font-size: 14px;
        }

        QListWidget {
            background-color: #191a1c;
            border: none;
            padding: 4px;
        }

        QListWidget::item {
            padding: 10px;
            margin: 4px 0;
            border-radius: 6px;
        }

        QListWidget::item:selected {
            background-color: #2a2e32;
            color: #ffffff;
        }

        QLineEdit {
            background-color: #191a1c;
            color: #b9c7cb;
            border: 1px solid #2f3336;
            border-radius: 6px;
            padding: 8px 12px;
        }

        QLineEdit:focus {
            border: 1px solid #3e8ecf;
            outline: none;
        }

        QPushButton {
            background-color: #2a2e32;
            color: #b9c7cb;
            padding: 10px 16px;
            border: 1px solid #2f3336;
            border-radius: 6px;
        }

        QPushButton:hover {
            background-color: #3a4045;
        }

        QPushButton:pressed {
            background-color: #1e2225;
        }

        QPushButton:disabled {
            background-color: #2b2d2f;
            color: #777;
            border: 1px solid #333;
        }

        QLabel {
            font-size: 16px;
            color: #b9c7cb;
        }

        QScrollArea {
            border: none;
        }

        QComboBox {
            background-color: #191a1c;
            color: #b9c7cb;
            border: 1px solid #2f3336;
            border-radius: 6px;
            padding: 6px 12px;
            min-height: 32px;
        }

        QComboBox:hover {
            border: 1px solid #3e8ecf;
        }

        QComboBox::drop-down {
            background-color: #191a1c;
            border-left: none;
        }

        QComboBox QAbstractItemView {
            background-color: #191a1c;
            border: 1px solid #2f3336;
            selection-background-color: #3e8ecf;
            color: #b9c7cb;
            padding: 4px;
            outline: none;
        }

        QComboBox QAbstractItemView::item {
            padding: 8px 12px;
            border-radius: 4px;
        }

        QComboBox QAbstractItemView::item:selected {
            background-color: #3e8ecf;
            color: #ffffff;
        }
        QFrame {
            background-color: #191a1c;
            border-radius: 8px;
        }
        QCalendarWidget {
            background-color: #1f1f1f;
            color: #e0e0e0;
        }
        /* ensure every cell is dark by default */
        QCalendarWidget QAbstractItemView::item {
            background-color: #1f1f1f;
        }
        QCalendarWidget QToolButton {
            background-color: #2a2a2a;
            color: white;
            border: none;
        }
        QCalendarWidget QMenu {
            background-color: #2a2a2a;
            color: white;
        }
        QCalendarWidget QSpinBox {
            background-color: #2a2a2a;
            color: white;
            selection-background-color: #444;
        }
        QCalendarWidget QAbstractItemView {
            selection-background-color: #444;
            selection-color: white;
            gridline-color: #333;
        }
        QCalendarWidget QHeaderView::section {
            background-color: #444444;
            color: #ffffff;
            border: none;
        }
        QCalendarWidget QHeaderView:horizontal::section {
            background-color: #444444;
            color: #ffffff;
            border: none;
        }
        QCalendarWidget QHeaderView:vertical::section {
            background-color: #555555;
            color: #ffcc00;
            border: none;
        }
        """
    )

def stylesheet_light():
    return (
        """
        QWidget {
            background-color: #f4f6f8;
            color: #2e2e2e;
            font-family: 'Segoe UI', sans-serif;
            font-size: 14px;
        }

        QListWidget {
            background-color: #ffffff;
            border: 0px solid #e0e0e0;
            padding: 4px;
        }

        QListWidget::item {
            padding: 10px;
            margin: 4px 0;
            border-radius: 6px;
        }

        QListWidget::item:selected {
            background-color: #cce4ff;
            color: #1a1a1a;
        }

        QLineEdit {
            background-color: #ffffff;
            color: #2e2e2e;
            border: 1px solid #ccc;
            border-radius: 6px;
            padding: 8px 12px;
        }

        QLineEdit:focus {
            border: 1px solid #66aaff;
            outline: none;
        }

        QPushButton {
            background-color: #ffffff;
            color: #2e2e2e;
            padding: 10px 16px;
            border: 1px solid #ccc;
            border-radius: 6px;
        }

        QPushButton:hover {
            background-color: #f0f0f0;
        }

        QPushButton:pressed {
            background-color: #e0e0e0;
        }

        QPushButton:disabled {
            background-color: #f4f4f4;
            color: #999;
            border: 1px solid #ddd;
        }

        QLabel {
            font-size: 16px;
            color: #2e2e2e;
        }

        QScrollArea {
            border: none;
        }

        QComboBox {
            background-color: #ffffff;
            color: #2e2e2e;
            border: 1px solid #ccc;
            border-radius: 6px;
            padding: 6px 12px;
            min-height: 32px;
        }

        QComboBox:hover {
            border: 1px solid #66aaff;
        }

        QComboBox::drop-down {
            background-color: #ffffff;
            border-left: none;
        }

        QComboBox QAbstractItemView {
            background-color: #ffffff;
            border: 1px solid #ccc;
            selection-background-color: #cce4ff;
            color: #2e2e2e;
            padding: 4px;
            outline: none;
        }

        QComboBox QAbstractItemView::item {
            padding: 8px 12px;
            border-radius: 4px;
        }

        QComboBox QAbstractItemView::item:selected {
            background-color: #66aaff;
            color: #ffffff;
        }
        """
    )