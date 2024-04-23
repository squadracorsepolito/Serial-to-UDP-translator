# Serial-to-JSON-UDP-translator
Real time **Serial CSV** to **UDP JSON** stream translator

<!-- ## General schema
![General schema](img/general-schema.png) -->

## How to use
### Install dependencies
```bash
pip install -r requirements.txt
```

...

### Build executable
```bash
pyinstaller --name SerialToUdpTranslator  main.py --onefile --windowed
```

## Tech stack
- Python 3.12.2
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
