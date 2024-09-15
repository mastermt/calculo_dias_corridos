# Calcula de Data Final em meses a frente




using file environment.yml to creat Coda Python environment
conda env create
conda activate flet-dias

flet run --web
flet run --web --port 8000 app.py


To export:

flet build windows
flet build linux
Flet CLI provides flet build apk and flet build aab commands that allow packaging Flet app into Android APK and Android App Bundle (AAB) respectively.
Flet CLI provides flet build ipa command that allows packaging Flet app into an iOS archive bundle and IPA for distribution.
Flet CLI provides flet build web and flet publish commands that allow publishing Flet app into a standalone static website (SPA) that runs entirely in the browser with Pyodide and does not require any code running on the server side.
