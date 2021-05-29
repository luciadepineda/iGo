# iGo
iGo is a Telegram Bot implemented with Python. It guides users (in Barcelona) from their current position to their destination by the fastest road by car, using the new concept of "itime", which takes into account the state of traffic in real time in certain sections of the city.

## Installation
In order for iGo to work, it is necessary to install the libraries mentioned in the "requirements.txt" file attached.
- "csv" to read in CSV format
- "pickle" to read and write data in Python from/to files
- "urllib" to download files from the web
- "networkx" to manipulate graphs
- "osmnx" to get site graphs
- "haversine" to calculate distances between coordinates
- "staticmap" for painting maps
- "python-telegram-bot" to interact with Telegram
- "scikit-learn" to use the function 'osmnx.distance.nearest_nodes'

The first three are standard and you do not need to do anything to have them. The other libraries can be installed with "pip3 install" or "sudo pip3 install" commands.
However, osmnx takes some work: you must first do a "sudo apt install libspatialindex-dev" (in Ubuntu) or a "brew install spatialindex gdal" (in Mac).
Moreover, you algo have to install the lastest installers:
1. pip3 install --upgrade pip setuptools wheel
2. pip3 install --upgrade osmnx
3. pip3 install --upgrade staticmap

## Usage
The iGo Telegram Bot is very easy and intuitive to use. There are two options: the first is to use the command /where and send your location for the bot to know where you are, and then type /go destination and it will automatically show you the fastest route by car. The second option is to use the command /pos to fix a position of origin (instead of your actual location) and then use /go to specify the destination. Moreover, the command /help will explain all of this previously mentioned.

## Support
In case you have any questions, do not hesitate to contact us: lucia.de.pineda@estudiantat.upc.edu / judith.devers@estudiantat.upc.edu

## Images
Here are some images showing the different commands available:

![IMG_2176](https://user-images.githubusercontent.com/83398396/120075200-990d0600-c0a0-11eb-991f-bef3082d428b.jpg)

IMG_2177.jpg![image](https://user-images.githubusercontent.com/83398396/120075634-6a902a80-c0a2-11eb-9385-ef1312aa4160.png)

IMG_2178.jpg![image](https://user-images.githubusercontent.com/83398396/120075719-b7740100-c0a2-11eb-8834-f40c34acbab0.png)

IMG_2179.jpg![image](https://user-images.githubusercontent.com/83398396/120075726-be027880-c0a2-11eb-8a30-c0ae8dffa210.png)


