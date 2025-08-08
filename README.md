# netpi
Network speed web viewer and monitor

## 🚀 Quick Installation 

# NetPi - Installation and Uninstallation Guide  

Below are the necessary commands to completely install and uninstall the **NetPi** project.

---

## Quick Installation

```bash
curl -sSL https://raw.githubusercontent.com/trederndor/netpi/refs/heads/main/fastinstall.sh | bash
```
## Manual Installation

```bash
git clone https://github.com/trederndor/netpi.git ~/netpi
cd ~/netpi
chmod +x ./install.sh
sudo ./install.sh
speedtest
python3 speed.py
```


After that, you can launch the app by running the speed.py script from inside ~/netpi with python.


<img width="1895" height="864" alt="image" src="https://github.com/user-attachments/assets/a248402c-5f60-4e68-97be-8898e426c4ab" />

## Uninstallation
```bash
rm -rf ~/netpi
sudo apt remove speedtest
```

## License

MIT License

This project is distributed under the Creative Commons BY-NC 4.0 license for non-commercial use.

➡️ Commercial use is prohibited without authorization or a paid license.
