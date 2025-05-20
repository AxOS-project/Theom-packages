def stylesheet():
    return """
    QWidget {
        background-color: #23262d;
        color: #d8dadc;
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
    }

    QListWidget {
        background-color: #2c2f36;
        border: none;
        padding: 4px;
    }

    QListWidget::item {
        padding: 10px;
        margin: 4px 0;
        border-radius: 6px;
    }

    QListWidget::item:selected {
        background-color: #0986d3;
        color: #ffffff;
    }

    QLineEdit {
        background-color: #2c2f36;
        color: #d8dadc;
        border: 1px solid #4b5a66;
        border-radius: 6px;
        padding: 8px 12px;
    }

    QLineEdit:focus {
        border: 1px solid #0986d3;
        outline: none;
    }

    QPushButton {
        background-color: #2a2e32;
        color: #d8dadc;
        padding: 10px 16px;
        border: 1px solid #4b5a66;
        border-radius: 6px;
    }

    QPushButton:hover {
        background-color: #424245;
    }

    QPushButton:pressed {
        background-color: #23262d;
    }

    QPushButton:disabled {
        background-color: #606060;
        color: #9e9e9e;
        border: 1px solid #333333;
    }

    QLabel {
        font-size: 16px;
        color: #d8dadc;
    }

    QScrollArea {
        border: none;
    }

    QComboBox {
        background-color: #2c2f36;
        color: #d8dadc;
        border: 1px solid #4b5a66;
        border-radius: 6px;
        padding: 6px 12px;
        min-height: 32px;
    }

    QComboBox:hover {
        border: 1px solid #0986d3;
    }

    QComboBox::drop-down {
        background-color: #2c2f36;
        border-left: none;
    }

    QComboBox QAbstractItemView {
        background-color: #2c2f36;
        border: 1px solid #4b5a66;
        selection-background-color: #0986d3;
        color: #d8dadc;
        padding: 4px;
        outline: none;
    }

    QComboBox QAbstractItemView::item {
        padding: 8px 12px;
        border-radius: 4px;
    }

    QComboBox QAbstractItemView::item:selected {
        background-color: #0986d3;
        color: #ffffff;
    }
    """


def stylesheet_light():
    return """
    QWidget {
        background-color: #EFE1CA;
        color: #4B5A66;
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
    }

    QListWidget {
        background-color: #F5EFE4;
        border: none;
        padding: 4px;
    }

    QListWidget::item {
        padding: 10px;
        margin: 4px 0;
        border-radius: 6px;
    }

    QListWidget::item:selected {
        background-color: #0986D3;
        color: #FFFFFF;
    }

    QLineEdit {
        background-color: #F5EFE4;
        color: #4B5A66;
        border: 1px solid #A70B06;
        border-radius: 6px;
        padding: 8px 12px;
    }

    QLineEdit:focus {
        border: 1px solid #0986D3;
        outline: none;
    }

    QPushButton {
        background-color: #D8C4AC;
        color: #4B5A66;
        padding: 10px 16px;
        border: 1px solid #A70B06;
        border-radius: 6px;
    }

    QPushButton:hover {
        background-color: #C3B092;
    }

    QPushButton:pressed {
        background-color: #A9987B;
    }

    QPushButton:disabled {
        background-color: #B0A090;
        color: #9E9E9E;
        border: 1px solid #999999;
    }

    QLabel {
        font-size: 16px;
        color: #4B5A66;
    }

    QScrollArea {
        border: none;
        background-color: transparent;
    }

    QComboBox {
        background-color: #F5EFE4;
        color: #4B5A66;
        border: 1px solid #A70B06;
        border-radius: 6px;
        padding: 6px 12px;
        min-height: 32px;
    }

    QComboBox:hover {
        border: 1px solid #0986D3;
    }

    QComboBox::drop-down {
        background-color: #F5EFE4;
        border-left: none;
    }

    QComboBox QAbstractItemView {
        background-color: #F5EFE4;
        border: 1px solid #A70B06;
        selection-background-color: #0986D3;
        color: #4B5A66;
        padding: 4px;
        outline: none;
    }

    QComboBox QAbstractItemView::item {
        padding: 8px 12px;
        border-radius: 4px;
    }

    QComboBox QAbstractItemView::item:selected {
        background-color: #0986D3;
        color: #FFFFFF;
    }
    """