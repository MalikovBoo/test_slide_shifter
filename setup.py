from setuptools import setup

APP = ['slide_shifter.py']
APP_NAME = 'Slide Shifter'
DATA_FILES = []
OPTIONS = {
    'iconfile': 'img/logo.icns',
    'argv_emulation': True,
    'packages': ['cv2', 'mediapipe', 'pyautogui', 'PySide6', 'shiboken6', 'numpy', 'matplotlib'],
    'includes': ['sys', 'time', 'traceback', 'math', 'requests'],
    'excludes': [
        'tkinter', 'unittest', 'xmlrpc',
        'distutils', 'setuptools', 'PyInstaller', 'rubicon', 'rubicon.objc'
    ],
    'plist': {
        'CFBundleName': 'SlideShifter',
        'CFBundleDisplayName': APP_NAME,
        'CFBundleExecutable': APP_NAME,
        'CFBundleGetInfoString': 'Slide Shifter',
        'CFBundleVersion': '1.0.0, First Edition',
        'CFBundleShortVersionString': '1.0.0',
        'NSCameraUsageDescription': 'Приложению необходим доступ к камере, чтобы отслеживать движения рук и переключать слайды.',
    },
}

setup(
    app=APP,
    name=APP_NAME,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)