def stylesheet():
    return """
    QWidget {
        background-color: rgba(30, 30, 30, 0.85);
        color: #b0b4bc;
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
    }

    QListWidget {
        background-color: #282c34;
        border: none;
        padding: 4px;
    }

    QListWidget::item {
        padding: 10px;
        margin: 4px 0;
        border-radius: 6px;
    }

    QListWidget::item:selected {
        background-color: #d35d6e;
        color: #ffffff;
    }

    QLineEdit {
        background-color: #282c34;
        color: #b0b4bc;
        border: 1px solid #4b5a66;
        border-radius: 6px;
        padding: 8px 12px;
    }

    QLineEdit:focus {
        border: 1px solid #d35d6e;
        outline: none;
    }

    QPushButton {
        background-color: #282c34;
        color: #b0b4bc;
        padding: 10px 16px;
        border: 1px solid #4b5a66;
        border-radius: 6px;
    }

    QPushButton:hover {
        background-color: #3a3f4a;
    }

    QPushButton:pressed {
        background-color: rgba(30, 30, 30, 0.85);
    }

    QPushButton:disabled {
        background-color: #606060;
        color: #9e9e9e;
        border: 1px solid #333333;
    }

    QLabel {
        font-size: 16px;
        color: #b0b4bc;
    }

    QScrollArea {
        border: none;
    }

    QComboBox {
        background-color: #282c34;
        color: #b0b4bc;
        border: 1px solid #4b5a66;
        border-radius: 6px;
        padding: 6px 12px;
        min-height: 32px;
    }

    QComboBox:hover {
        border: 1px solid #d35d6e;
    }

    QComboBox::drop-down {
        background-color: #282c34;
        border-left: none;
    }

    QComboBox QAbstractItemView {
        background-color: #282c34;
        border: 1px solid #4b5a66;
        selection-background-color: #d35d6e;
        color: #b0b4bc;
        padding: 4px;
        outline: none;
    }

    QComboBox QAbstractItemView::item {
        padding: 8px 12px;
        border-radius: 4px;
    }

    QComboBox QAbstractItemView::item:selected {
        background-color: #d35d6e;
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