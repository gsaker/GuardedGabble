# GuardedGabble
**A self hosted encrypted chat messaging app**

## Server Installation
First clone the repository
```bash
git clone https://github.com/gsaker/GuardedGabble
```
Then change directory to the root of the project
```bash
cd GuardedGabble
```
Make sure all dependencies are installed
```
pip install socket threading
```
To start the server refer to the following guide 
```bash
python main.py <Host Address> <Port Number> <Encryption Enabled> <Store Messages>
```
For example
```bash
python src/server/main.py 127.0.0.1 64147 true false
```

## Client Building
To build a client app, first install pyinstaller and pillow
```bash
pip install pyinstaller pillow
```
Then build the app using pyinstaller
```bash
pyinstaller -n GuardedGabble -F --windowed --icon=img/icon.ico src/client/main.py
```