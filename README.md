# wafer-management
Improved Data-Extraction with React

<span style="color:red; font-size:2em;">**WARNING:** Be sure to download this project and your python and Mongodb locally on your computer, **NOT ON ONE-DRIVE**</span>
## 1. Installing dependecies
### Python installation
If you don't already have Python on your computer, install it using [this link](https://python.org). When downloading, please ensure you checked "Add to path". Then, go to custom installation and ensure that the **pip** checkbox is checked. 
Follow all the steps of installation and then go to windows settings and search for "Environment variable". Go to "Edit environment variable" > "Advanced" > "Environment Variables..." and then in PATH in the upper window or Path in the lower one. 
Check if you have these two Path: 
```
C:\Users\<Your username>\AppData\Local\Programs\Python\Python311\Scripts\
```
and 
```
C:\Users\<Your username>\AppData\Local\Programs\Python\Python311\
```

If not, add them.
### Pip installation
Then, run 
``` bash
py -m ensurepip --upgrade
```
in a Command Line Interface to install pip.

### Installation of all dependencies
To install all dependencies, please run 
```bash
pip install -r requirements.txt
```

You will also need to install MongoDB. PLease go to the official MongoDB website.

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

By default, MongoDB listens on port 27017, and stores its data in `C:\Program Files\MongoDB\Server\6.0\data` (replace `6.0` with the version number you installed).

 

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


# Update the User interface
If you want to add functionalities, after writing the python code you will have to link it with the interface. If it is your first time dealing with Javascript and React, it may seem difficult, but don't worry, we will face this step together.

## First, Installing the dependecies
The first is to install a good setup on your computer. Run
```bash
node -v
```

and 
```bash
npm -v
```
in a command line (if you can do it in the Terminal of PyCharm it is better). If you see a version number for both it is ok. If these softwares are not already installed, follow the next step.

## Install npm and/or node.js
First go to the [Node.js website](https://nodejs.org/en) and download the version for current users. Then run the installer and follow the steps.
You should now see the version number when running 
```bash
node -v
```

and 
```bash
npm -v
```

## Getting started with the code
If you want to add a functionality to the data analysis, you must open [Open.js](./my-app/src/Open.js) (in my-app/src/Open.js).
This file contains all elements useful for data analysis, such as Wafer Maps, plotting data, Normal plots...

### Introduction to React
Let's have a look to useful elements of React:
#### useState
This element allows you to use differents states for a variable. For example, let's see this line:
```javascript
const [openWaferMapDialog, setOpenWaferMapDialog] = useState(false);
```
This line contains 2 elements: `openWaferMapDialog` and `setOpenWaferMapDialog`. It determines when the window of the wafer maps have to be open or not. By default, `openWaferMapDialog` is false (`useState(false)`), but we can use `setOpenWaferMapDialog(true)` to change his state and open the window. Then, if we want to close it, we just switch to `setOpenWaferMapDialog(false)`.

We can also store information in a **useState**: for example, this **useState** save all the sessions to be displayed when we open a wafer:
`const [sessions, setSessions] = useState([]);`. We initialize it with an empty array and then fill it when we open a wafer, and we don't forget to empty it when we close the wafer. Don't worry, we will see how to do this later.

It is also possible to register a single element. This line is used to save the structure we wnt to plot the wafer map:
`const [selectedStructure, setSelectedStructure] = useState(null);`.

#### useEffect
Other useful tools in React are **useEffect**. These are a tool used when you want to automatically update an element. Let's have a look:
```javascript
useEffect(() => {
        setFilteredStructuresDisplay(structures.filter(structure => filteredStructures.includes(structure)));
    }, [structures, filteredStructures]);
```
Let's understand this code: the line 
```javascript
setFilteredStructuresDisplay(structures.filter(structure => filteredStructures.includes(structure)));
```

updates the array FilteredStructuresDisplay, by adding only elements present in the array structures (that contains all the structures in the selected session) **AND** in filteredStructures.
The last line, 
```javascript
    }, [structures, filteredStructures]);
```
means that this code will run each time **structures** and/or **filteredStructures** are modified.
So to summarize, this code means that each time we select (or deselect) a filter, the list of structures to be displayed is updated.

Note that when you set a new state for a use State, for example when you add a structure in filteredStructures, it is not always updated instantly, so to be sure we don't have problems, 
we use 

```javascript
useEffect(() => {
        console.log(structures)
    }, [structures]);
```
so we are sure that the list structures is updated each time we select a Session.

#### Dialogs
##### Tags
Now that you are familiar with **useState** and **useEffect**, 
let's have a look to **Dialogs**. These elements open a new window, which allows you to do a lot of things. Let's dissect a Dialog element to see how it is built.

First, How do we initiate a dialog? It is simple. in the section 
```javascript
return (
```
at the end of the code, add these tags: 
```javascript
<Dialog>

</Dialog>
```
and your Dialog is created! Empty, certainly, but created.

You can add it anywhere after the **Box** element (line 779 when I write this tutorial). Just put it outside another Dialog. If it easier for you, you can add it at the very end of the code, just before
```javascript
</OpenContext.Provider>
```

but it is a good practice to group all dialogs depending on their aim (all dialogs related to Wafer maps between them, all those related to normal plots between them...)

##### Headers
Now, let's see how to build a dialog. First, the header. In the opening tag,
```javascript
<Dialog>
```
you have to add some information.
Here is how to do it:
```javascript
<Dialog
    open={openPlotsNormal}
    onClose={() => {
        setOpenPlotsNormal(false);
        setSelectedStructures([]);
        setOpenAccordion(false);
        setCurrentNormalPlots([]);
    }}
    maxWidth='md'
    fullWidth={true}
    aria-labelledby="matrices-dialog-title"
    aria-describedby="matrices-dialog-description"
>
```
 The line `open={openPlotsNormal}` means that the dialog will be open when the state **openPlotsNormal** is set as **true**. That is why it is useful to use useState.

Then, 
```javascript
onClose={() => {
        setOpenPlotsNormal(false);
        setSelectedStructures([]);
        setOpenAccordion(false);
        setCurrentNormalPlots([]);
    }}
```
The `onclose={}` determines what happens when the dialog is closed. For example, here when change the state of openPlotNormal to **false**, we empty both selectedStructures and currentNormalPlots arrays, (respectively the structures were we took the data and the array containing the png of the plots)
and finally we close all the sessions (setOpenAccordion(false)).

Finally, all the lines 
```javascript
maxWidth='md'
    fullWidth={true}
    aria-labelledby="matrices-dialog-title"
    aria-describedby="matrices-dialog-description"
```
are for the style of the dialog.

##### Title and content
The Title of the dialog has to be placed in `<DialogTitle>` tags as follows:
```javascript
<DialogTitle>Plots of the wafer map of {selectedStructure} in {selectedwafer}</DialogTitle>
```

The most important part is the content of the dialog:
###### Display one or multiple pictures
```javascript
<img
    src={`data:image/png;base64,${currentWaferMap}`}
    alt={`Wafer Map of ${selectedStructure}`}
    style={{ width:"100%", height: 'auto' }}
/>
```
(change `${currentWaferMap}` to the variable where is located your picture)
`alt={}` is a text That will appear instead of the picture if there is a problem with your image.

Displaying multiples pictures is exactly the same: sore your pictures in a list and then 
````javascript
matrixImages.map((img, index) => (
<img
    src={`data:image/png;base64,${img}`}
    alt={`Matrix ${index + 1}`}
    style={{ width:"100%", height: 'auto' }}
    key={index}
    />
))
````

###### Conditional display
You can also change your display depending on the conditions. For example, let's study this code:
````javascript
{isLoading ? (
<>
        <Select>
            <CircularProgress />
            Processing...
        </Select>
    </>
  ) : (
      <img
        src={`data:image/png;base64,${currentWaferMap}`}
        alt={`Wafer Map of ${selectedStructure}`}
        style={{ width:"100%", height: 'auto' }}
    />
)}
````
In this code, if the State isLoading is **true**, we will display a loading circle. Else, (i.e at the end of the loading) we display the picture.
Here is how to build this type of code:
````javascript
{ condition ? (
    what to display if the condition is true
) : (
    what to display if the condition is false
    )}
````

###### Create an Excel, a Powerpoint...
If you want to create an Excel, the first step is to know from where you have to start.
For example, if you want to create an Excel with all the VBD values of a structure, you can start from the already existing dialog
````javascript
<Dialog
  open={openWaferMapDialog}
  onClose={() => {
      setOpenAccordion(false);
      setOpenWaferMapDialog(false);
      handleCloseDialog();
  }}
  onBackdropClick={() => {
      setOpenWaferMapDialog(false);
      setOpenAccordion(false);
  }}
  aria-labelledby="alert-dialog-title"
  aria-describedby="alert-dialog-description"
>
````
(line 1010)
and add a button in the `<DialogActions> </DialogActions>` tag.

Here is an example of a button:
````javascript
<ExcelButton onClick={() => setOpenVBDExcel(true)}>Make Excel</ExcelButton>
````
The tags `<ExcelButton></ExcelButton>` is only for style (color, shape...). onClick={} describes the actions to be realized when we click on the button. Here, it set the state `OpenVBDExcel` at true, what opens the corresponding Dialog. 


Then, create a dialog where you can select strcutures. The structure of the dialog depends on how you built your function: does it accept only one or multiple structures? Does it accept filters? Do the user choose the name of the excel or is it created automatically?
All these questions leads to differents dialog but here is a structure for each of them:

###### The function accepts only 1 structure:
````javascript
<Grid container spacing={2}>
  {mapSessions.map((session, index) => (
  <Grid item xs={12} key={index}>
    <Accordion expanded={openAccordion === `panel${index}`}>
      <AccordionSummary
        expandIcon={<ExpandMoreIcon />}
        aria-controls={`panel${index}-content`}
        id={`panel${index}-header`}
        onClick={() => {
          handleComplianceSessionClick(session);
          setOpenAccordion(openAccordion === `panel${index}` ? false : `panel${index}`);
        }}
      >
        <Typography>{session}</Typography>
      </AccordionSummary>
      <AccordionDetails>
        <Button style={{backgroundColor: "#4fbdff"}} onClick={handleSelectAll}>Select/Unselect All</Button>
        <Grid container spacing={2}>
          {structures.map((structure, index) => (
              <Grid item xs={6} key={index} sx={{display: 'flex', justifyContent: index % 2 === 0 ?
          'flex-start': 'flex-end'}}>
            <Chip
                key={`Selected ${index}`}
                label={`${structure}${selectedStructures.includes(structure) ? " \u2714" : ""}`}
                onClick={() => yourFunction(parameters)}
                style={{margin: '5px', backgroundColor: selectedStructures.includes(structure) ? "#4fbdff" : "#888888"}}
            />
          </Grid>
          ))}
        </Grid>
      </AccordionDetails>
    </Accordion>
  </Grid>
  ))}
</Grid>
````

Here, we first map all sessions that contains I-V measurements (for wafer maps of VBD, but we can also map sessions that contains Leakage, C, Cmes, R, ...)
Then, inside each session, we map structures that contains I-V measures. 
Finally, we give each structure a click event, so when we click on a structure it activates the function. We will see later how to build a function.

###### The function accepts multiples strcutures
````javascript
 <Grid container spacing={2}>
  {mapSessions.map((session, index) => (
  <Grid item xs={12} key={index}>
    <Accordion expanded={openAccordion === `panel${index}`}>
      <AccordionSummary
        expandIcon={<ExpandMoreIcon />}
        aria-controls={`panel${index}-content`}
        id={`panel${index}-header`}
        onClick={() => {
          handleComplianceSessionClick(session);
          setOpenAccordion(openAccordion === `panel${index}` ? false : `panel${index}`);
        }}
      >
        <Typography>{session}</Typography>
      </AccordionSummary>
      <AccordionDetails>
          <Button style={{backgroundColor: "#4fbdff"}} onClick={handleSelectAll}>Select/Unselect All</Button>
          <Typography> Compliance: {selectedCompliance} A</Typography>
          <ActionButton onClick={() => setOpenSetComplianceDialog(true)}>Set compliance</ActionButton>
        <Grid container spacing={2}>
          {filteredStructuresDisplay.map((structure, index) => (
              <Grid item xs={6} key={index} sx={{display: 'flex', justifyContent: index % 2 === 0 ?
          'flex-start': 'flex-end'}}>
            <Chip
                key={`Selected ${index}`}
                label={`${structure}${selectedStructures.includes(structure) ? " \u2714" : ""}`}
                onClick={() => handleChooseSelectStructureClick(structure)}
                style={{margin: '5px', backgroundColor: selectedStructures.includes(structure) ? "#4fbdff" : "#888888"}}
            />
          </Grid>
          ))}
        </Grid>
      </AccordionDetails>
    </Accordion>
  </Grid>
  ))}
</Grid>
````
Here, the user can select multiples structures, but you have to add a button to activate the creation of the Excel.


###### Choosing the name of the file
To choose the name of the file, simply add this line to your code:
````javascript
<TextField autoFocus margin="dense" label="Name of File" fullWidth variant="standard" onChange={(e) => setNameOfExcelFile(e.target.value)} />
````
Inside the `<Grid></Grid>` but outside the 
```javascript
{mapSessions.map((session, index) => (
    ...
)}
```
Each time you will write in the TextField, the state nameOfExcelFile will change to store the name you are writing.


## The functions
Finally, here we are. You have built your dialog, you know which strcuture you want to process, but you have now to send these information to you python code. Here is how to do it.
First, create a function.

````javascript
const myFunction = async () =>{
        
    }
````
Then, call your python route:
````javascript
try {
  const response = await axios.get(`http://localhost:3000/name_of_my_route/${selectedWafer}/${filteredSessions}/${selectedStructures}/${filteredTypes}/${filteredTemps}/${filteredFiles}/${filteredCoords}/${nameOfExcelFile}`);
  if (response.status === 200) {
    setIsLoading(false);
    setOpenDialogMakeExcel(false);
    setSelectedStructures([]);
  }
} catch(error) {
console.error("Error uploading files: ", error)
} finally {
    setIsLoading(false);
}
````
Here, the method axios.get calls your corresponding python route. We will see just after what is a route, but just remember that this launch your python code from Javascript.
Then, once your function is finished, we close all dialogs and end the loading.


## Python routes
Finally, the last step, is to build your python route. In the file [app.py](./app.py) write a new route:
````python
@app.route('/my_python_route/<waferId>/<sessions>/<structures>/<types>/<temps>/<files>/<coords>/<file_name>', methods=['GET'])
def my_function_route(waferId, sessions, structures, types, temps, files, coords, file_name):
    """
   Description of the function
    """
    sessions = sessions.split(',') #We parse all the information so it suit the python format
    structures = structures.split(',')
    types = types.split(',')
    temps = temps.split(',')
    files = files.split(',')
    coords = coords.replace("),(", ") (")
    coords = coords.split(" ")
    my_excel_function(waferId, sessions, structures, types, temps, files, coords, file_name)
    return jsonify({'result': 'success'})
````
Rename the function you use in the code. You can give the name you want to your function `my_function_route` but try to give it a name that allows anyone to understand what does your function do.

Same applies for your route ``/my_python_route/...``. The first name is the name of your route, that you also use in your javascript code, and all names between tags are the parameters you received (That you send usind `/${selectedWafer}/...` in JavaScript).

That's all folks! You are now ready to update de User Interface! Congratulations!



