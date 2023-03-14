import webbrowser, os, sys

url = "https://www.google.com --start-fullscreen"

chrome_path = '/usr/lib/chromium-browser/chromium-browser'
webbrowser.get(chrome_path).open(url)
