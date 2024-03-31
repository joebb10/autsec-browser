import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLineEdit, QPushButton,
                             QToolBar, QTabWidget, QVBoxLayout, QWidget, QLabel, QFileDialog)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtGui import QPixmap

class WebPage(QWebEnginePage):
    def __init__(self):
        super().__init__()

    def acceptNavigationRequest(self, url, _type, isMainFrame):
        ad_domains = [
            'doubleclick.net',
            'google-analytics.com',
            'googleadservices.com',
            'facebook.net',
            'scorecardresearch.com',
            'googletagmanager.com'
            
        ]
        for domain in ad_domains:
            if domain in url.host():
                print(f"Blocked ad: {url.toString()}")
                return False
        return True

class Autsec(QMainWindow):
    def __init__(self):
        super(Autsec, self).__init__()
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)
        self.add_new_tab('https://www.google.com', 'Homepage')
        self.showMaximized()

        self.init_ui()

    def init_ui(self):
        navbar = QToolBar("Navigation")
        navbar.setStyleSheet("background-color: #333;")
        self.addToolBar(navbar)

        new_tab_btn = QPushButton('New Tab', self)
        new_tab_btn.clicked.connect(lambda: self.add_new_tab())
        navbar.addWidget(new_tab_btn)

        self.url_bar = QLineEdit(self)
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        back_btn = QPushButton('Back', self)
        back_btn.clicked.connect(lambda: self.current_tab().back())
        navbar.addWidget(back_btn)

        forward_btn = QPushButton('Forward', self)
        forward_btn.clicked.connect(lambda: self.current_tab().forward())
        navbar.addWidget(forward_btn)

        reload_btn = QPushButton('Reload', self)
        reload_btn.clicked.connect(lambda: self.current_tab().reload())
        navbar.addWidget(reload_btn)

        screenshot_btn = QPushButton('Screenshot', self)
        screenshot_btn.clicked.connect(self.take_screenshot)
        navbar.addWidget(screenshot_btn)

    def add_new_tab(self, url='about:blank', label="Blank"):
        browser = QWebEngineView()
        page = WebPage()
        browser.setPage(page)
        browser.setUrl(QUrl(url))
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))

    def current_tab(self):
        return self.tabs.currentWidget()

    def close_tab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)

    def update_urlbar(self, q, browser=None):
        if browser != self.current_tab():
            return
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

    def navigate_to_url(self):
        q = QUrl(self.url_bar.text())
        if q.scheme() == "":
          q.setScheme("https")
        elif q.scheme() == "http":
           q.setScheme("https")  # Enforce HTTPS
        self.current_tab().setUrl(q)

    def take_screenshot(self):
        browser = self.current_tab()
        pixmap = QPixmap(browser.size())
        browser.render(pixmap)

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Screenshot", "", "PNG Files (*.png);;All Files (*)")
        if file_path:
            pixmap.save(file_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setApplicationName('Autsec Browser')
    window = Autsec()
    app.exec_()
