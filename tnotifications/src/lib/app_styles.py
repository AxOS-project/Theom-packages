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

    QFrame {
        background-color: #282c34;
        border-radius: 8px;
    }

    QFrame#WeatherBox {
        background-color: #282c34;
        border-radius: 8px;
        padding: 10px;
    }

    QFrame#SunBox {
        background-color: #282c34;
        border-radius: 8px;
        padding: 10px;
    }

    QFrame#wbButtonBox {
        background-color: #282c34;
        border-radius: 8px;
        padding: 10px;
    }

    QFrame#MusicBox {
        background-color: #282c34;
        border-radius: 8px;
        padding: 10px;
    }

    QFrame#SystemStatsBox {
        background-color: #282c34;
        border-radius: 8px;
        padding: 10px;
    }

    QCalendarWidget {
        background-color: rgba(20, 20, 20, 0.75);
        color: #b0b4bc;
    }

    QCalendarWidget QAbstractItemView::item {
        background-color: rgba(20, 20, 20, 0.75);
    }

    QCalendarWidget QToolButton {
        background-color: #282c34;
        color: #b0b4bc;
        border: none;
    }

    QCalendarWidget QMenu {
        background-color: #282c34;
        color: #b0b4bc;
    }

    QCalendarWidget QSpinBox {
        background-color: #282c34;
        color: #b0b4bc;
        selection-background-color: #4b5a66;
    }

    QCalendarWidget QAbstractItemView {
        selection-background-color: #d35d6e;
        selection-color: #ffffff;
        gridline-color: #333333;
    }

    QCalendarWidget QHeaderView::section {
        background-color: #4b5a66;
        color: #ffffff;
        border: none;
    }

    QCalendarWidget QHeaderView:horizontal::section {
        background-color: #4b5a66;
        color: #ffffff;
        border: none;
    }

    QCalendarWidget QHeaderView:vertical::section {
        background-color: #4b5a66;
        color: #d35d6e;
        border: none;
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
        background-color: #FFFFFF;
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
        background-color: #E6D3BB;
        color: #4B5A66;
        padding: 10px 16px;
        border: 1px solid #A70B06;
        border-radius: 6px;
    }

    QPushButton:hover {
        background-color: #D3C0A7;
    }

    QPushButton:pressed {
        background-color: #BFA68C;
    }

    QPushButton:disabled {
        background-color: #D8D0C8;
        color: #9E9E9E;
        border: 1px solid #B5B5B5;
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
        background-color: #FFFFFF;
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
        background-color: #FFFFFF;
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

    QFrame {
        background-color: #F5EFE4;
        border-radius: 8px;
    }

    QFrame#WeatherBox {
        background-color: #EAE3D6;
        border-radius: 8px;
        padding: 10px;
    }

    QFrame#SunBox {
        background-color: #EAE3D6;
        border-radius: 8px;
        padding: 10px;
    }

    QFrame#wbButtonBox {
        background-color: #EAE3D6;
        border-radius: 8px;
        padding: 10px;
    }

    QFrame#MusicBox {
        background-color: #EAE3D6;
        border-radius: 8px;
        padding: 10px;
    }

    QFrame#SystemStatsBox {
        background-color: #EAE3D6;
        border-radius: 8px;
        padding: 10px;
    }

    QCalendarWidget {
        background-color: #F0E8DC;
        color: #4B5A66;
    }

    QCalendarWidget QAbstractItemView::item {
        background-color: #F0E8DC;
    }

    QCalendarWidget QToolButton {
        background-color: #E6D3BB;
        color: #4B5A66;
        border: none;
    }

    QCalendarWidget QMenu {
        background-color: #EFE1CA;
        color: #4B5A66;
    }

    QCalendarWidget QSpinBox {
        background-color: #FFFFFF;
        color: #4B5A66;
        selection-background-color: #D3C0A7;
    }

    QCalendarWidget QAbstractItemView {
        selection-background-color: #0986D3;
        selection-color: #FFFFFF;
        gridline-color: #D8D0C8;
    }

    QCalendarWidget QHeaderView::section {
        background-color: #D3C0A7;
        color: #4B5A66;
        border: none;
    }

    QCalendarWidget QHeaderView:horizontal::section {
        background-color: #D3C0A7;
        color: #4B5A66;
        border: none;
    }

    QCalendarWidget QHeaderView:vertical::section {
        background-color: #E6D3BB;
        color: #A70B06;
        border: none;
    }
    """
