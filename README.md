# Serial-to-JSON-UDP-translator
Real time **Serial CSV** to **UDP JSON** stream translator.

The executables can be found in the **Releases** section.

## App
![App](img/app.png)

## General logical schema
![General schema](img/general-schema.png)

## How to use
### Install dependencies
```bash
pip install -r requirements.txt
```

### CONFIG file
To configure the parameters of the program you have to create a 'CONFIG.txt' file with the following parameters:
```txt
VALUES=PARAM1 PARAM2 NULL PARAM3
NEWLINE=;
SEPARATOR=,
BAUDRATE=9600
UDP_PORT=5000
SERIAL_PORT=/dev/ttyUSB0
```
The 'VALUES' params separated by a space indicate the order of the values in the CSV string. The 'NULL' value indicates that the value is not going to be sent, but discarded when the CSV comes into the program. The 'NEWLINE' param indicates the character that separates the CSV strings, the usage of '\n' is not currently supported. The 'SEPARATOR' param indicates the character that separates the values in the CSV string. The 'BAUDRATE' param indicates the baudrate of the serial port. The 'UDP_PORT' param indicates the port of the UDP server. The 'SERIAL_PORT' param indicates the serial port to use.

With the configuration shown above you can send the following JSON (assuming CSV data is: 1,2,3,4\n):
```json
{
    "PARAM1": 1,
    "PARAM2": 2,
    "PARAM3": 4
}
```

## Build executable
```bash
pyinstaller --name SerialToUdpTranslator  main.py --onefile --windowed
```

## Publish new release
Replace 1.0 with your version.
```bash
git add .         
git commit -m "v1.0"  
git tag -a v1.0 -m "Version 1.0"      
git push origin master --tags   
```   
For a complete guide on how it works and how to publish a new release, check [this repo](https://github.com/Paolo-Beci/pyinstaller-all-os-gh-action).

## Tech stack
- Python 3.12.2
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
