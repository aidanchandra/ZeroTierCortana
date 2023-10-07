# ZeroTierCortana
A macOS toolbar application to monitor devices attached to a ZeroTier virtual network

**Features:**
* Click to copy virtual IP address
* Secure credential storage in MacOS Keychain
* Force refresh
* Last seen
* Details of device IP in sub-menu

**Installation:**
*You need to generate an API key from Zerotier*
* Go to releases and download most recent
* Drag-and-drop into applications
* Double-click to launch (also searchable in spotlight)
* Enter login password needed for keychain access to securely store/recall your API Key/Network ID (*If you don't like this, feel free to examine the source code and build the application yourself*)

**Building:**
* Clone this repo
* Ensure you have py2app installed
* Run the following command `sudo python3 setup.py py2app`
* 'ZeroTier Cortana' is now build in `dist/`


![image1](images/Screenshot%202023-10-07%20at%204.43.47%20PM.png)