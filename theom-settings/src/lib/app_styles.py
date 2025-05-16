def stylesheet():
    return (
    """
        QWidget {
            background-color: #2e2e2e;
            color: #ffffff;
        }
        QListWidget {
            background-color: #3b3b3b;
            border: none;
        }
        QListWidget::item {
            padding: 10px;
            margin: 2px 0;
        }
        QListWidget::item:selected {
            background-color: #005c8a;
        }
        QLineEdit {
            background-color: #4c4c4c;
            border: 1px solid #666;
            border-radius: 4px;
            padding: 8px;
        }
        QPushButton {
            background-color: #0078d7;
            padding: 10px;
            border-radius: 5px;
        }
        QPushButton:disabled {
            background-color: #555;
            color: #999;
        }
        QPushButton:hover {
            background-color: #0066bb;
        }
        QLabel {
            font-size: 18px;
        }
        QScrollArea {
            border: none;
        }
        QComboBox {
            background-color: #3b3b3b;
            color: #ffffff;
            border: 1px solid #666;
            border-radius: 5px;
            padding: 6px 10px;
            min-height: 30px;
            selection-background-color: #005c8a;
        }
        QComboBox:hover {
            border: 1px solid #0078d7;
        }
        QComboBox::drop-down {
            background-color: #3b3b3b;
        }
        QComboBox QAbstractItemView {
            background-color: #3b3b3b;
            border: 1px solid #666;
            selection-background-color: #005c8a;
            color: #ffffff;
            padding: 5px;
            outline: none;
        }
        QComboBox QAbstractItemView::item {
            padding: 8px 10px;
        }
        QComboBox QAbstractItemView::item:selected {
            background-color: #0078d7;
            color: #ffffff;
        }
    """
    )