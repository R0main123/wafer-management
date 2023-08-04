# wafer-management
Improved Data-Extraction with React

## 1. Installing dependecies
To install all dependecies, please run 
```bash
pip install -r requirements.txt
```

You will also need to install MongoDB. PLease go to the official mogoDB website

## 2. MongoDB Installation
### Windows

1. Download the MongoDB Community Server from the [MongoDB Download Center](https://www.mongodb.com/try/download/community).

2. Select the version of MongoDB to download. It's usually best to choose the current release.

3. Choose `Windows x64` in the platform dropdown menu.

4. Choose the `MSI` package option.

5. Click `Download`.

Once downloaded, follow the install wizard to install MongoDB.

1. Run the installer that you downloaded.

2. Follow the installation wizard. Choose the `Complete` setup type when it's offered.

3. When the wizard finishes, MongoDB will be installed as a Windows service, which means it will start up automatically with your computer.

 

### Configuring MongoDB
Once installed, you can start MongoDB by starting the MongoDB service:

1. Open the Services console: Press `Win + R`, then type `services.msc` and press `Enter`.

2. Look for `MongoDB` in the services list, right click on it and select `Start`.

By default, MongoDB listens on port 27017, and stores its data in `C:\Program Files\MongoDB\Server\4.4\data` (replace `4.4` with the version number you installed).

 

### Connecting to MongoDB
You can connect to MongoDB with the Mongo shell, or with a programming language-specific client library.

 

### Client Libraries
We will use MongoDB with python interface, so you won't need to use Mongo's shell, but if you want to have a look on all datas and how datas are organized, you can open 
ongoDB application.
See the [MongoDB Documentation](https://docs.mongodb.com/manual/applications/drivers/) for a list of MongoDB client libraries for various programming languages.

### Further Reading
For more information about MongoDB, see the [MongoDB Manual](https://docs.mongodb.com/manual/).

### Troubleshooting
If you have any problems installing or configuring MongoDB, please consult the [MongoDB Documentation](https://docs.mongodb.com/manual/installation/).


## 3. Getting started
Please click on the `wafer-Management.bat` file to get started with the application. Then, choose `Register New Measures` and drag and drop the files you want to register. You can drop .txt files, lim files, .tbl files, or .tbl.Z.
#### TXT Files:
They are just uploaded in the folder DataFiles, read and register in the database. They are deleted after being processed.

#### TBL files:
They are uploaded, read, registered in the database and then converted into .txt files. Converted files are available in the folder Converted Files.

#### TBL.Z files:
They are uncompress and then treated as tbl files.

#### LIM files:
First, we check if their twin is present in the uploaded files. If it is, we process them. Else, we ignore it without raising any error.


#

Then, return to the home menu and go to `Open existing wafer`.
Here, you have a view on all wafers you have registered. you can browse the list with a mouse or using the tactile screen. You can also use the trackpad but its usage is more delicate. 
Once on the page of the wafers, you have three buttons on each: `Wafer Map`, `Normal plots` and `Delete wafer`. The first two will ask you to select a value (R, Leak, C, Cmes and/or VBD, depending on what is available in the wafer).

Wafer Map will ask you to choose a session and a structure and will plot the wafer Map of the value inside this structure. 

Normal plots allows you to choose multiples structures and will display the normal distribution of the value.

The application displays only values that are available in the wafer, and once you chose a value, it displays only sessions and structures that contains this value.

The third button allows you to delete the wafer. It will **definitevely** disappear from the database and the application.

By clicking on a card, you will be shown the list of all sessions in the wafer. A click on a session shows you all structures in the session. 
### Filter Menu:
The Filter Menu allows you to choose parameters you want to select: temperature, session, die, filename and type of measurements. Once you have selected one or multiples parameters, choose one or more structure in the sessions. Then, you will be able to plot the data you have selected, register them into a PowerPoint or in an Excel file.

**Don't forget to select structures.** By default, if you don't select a parameter in the filter menu, it will select all the parameters (For example if you don't choose any temperature, it will take all data no matter the temperature of the measurements)


## Change database
If you want to create multiple databases, you can go to `getter.py` file and change the name of default parameter in `get_db_name` (Line 4). From now, each time you will create and connect to a database, it is this one which will be taken. If you want to connect to an older DB, You will have to change this parameter to the name of the wanted database.