import React, { useState, useEffect, useRef } from 'react';
import {Backdrop, Chip, CircularProgress, Grid, ListItemText, MenuItem, Typography} from '@mui/material';
import {CardFront, CarouselContainer, ExcelButton, PowerPointButton} from './OpenTheme';
import { animateScroll as scroll } from 'react-scroll';
import Box from '@mui/material/Box';
import { Carousel as OriginalCarousel} from "react-responsive-carousel";
import 'react-responsive-carousel/lib/styles/carousel.min.css';
import {TextField} from "@mui/material";
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import Button from '@mui/material/Button';
import FilterMenu from "./FilterMenu";
import axios from "axios";
import { Trash } from "react-bootstrap-icons";
import {Select} from "./ChoiceTheme";
export const OpenContext = React.createContext();

function Open() {
    const [wafers, setWafers] = useState([]);
    const [selectedWafer, setSelectedWafer] = useState(null);
    const [currentSlide, setCurrentSlide] = useState(0);
    const [searchTerm, setSearchTerm] = useState("");
    const [openDialog, setOpenDialog] = useState(false);
    const [openDialogExcelSelectStructures, setOpenDialogExcelSelectStructures] = useState(false);
    const [openDialogPptSelectStructures, setOpenDialogPptSelectStructures] = useState(false);
    const [structures, setStructures] = useState([]);
    const [allStructures, setAllStructures] = useState([]);
    const [matrices, setMatrices] = useState([]);
    const [selectedStructure, setSelectedStructure] = useState(null);
    const [selectedStructures, setSelectedStructures] = useState([]);
    const [openMatricesDialog, setOpenMatricesDialog] = useState(false);
    const [openMatrixDialog, setOpenMatrixDialog] = useState(false);
    const [openDeleteDialog, setOpenDeleteDialog] = useState(false);
    const [matrixImages, setMatrixImages] = useState([]);
    const [selectedMatrix, setSelectedMatrix] = useState(null);
    const [nameOfExcelFile, setNameOfExcelFile] = useState("");
    const [nameOfPptFile, setNameOfPptFile] = useState("");
    const carouselRef = useRef(null);
    const [openDialogMakeExcel, setOpenDialogMakeExcel] = useState(false);
    const [openDialogMakePpt, setOpenDialogMakePpt] = useState(false);
    const [isLoading, setIsLoading] = useState(false);


    useEffect(() => {
        fetch('/open')
            .then(response => response.json())
            .then(data => {
                setWafers(data);
                setCurrentSlide(0);
            });

    }, []);


    useEffect(() => {
        setCurrentSlide(0)
    }, [wafers]);

    useEffect(() => {
        console.log(isLoading);
    }, [isLoading]);

    useEffect(() => {
        console.log(openDialogExcelSelectStructures);
    }, [openDialogExcelSelectStructures]);

    useEffect(() => {
        console.log(openDialogMakeExcel);
    }, [openDialogMakeExcel]);

    useEffect(() => {
        if(selectedWafer){
            fetch(`/get_structures/${selectedWafer}`)
                .then(response => response.json())
                .then(data => {
                    setStructures(data);
                    setAllStructures(data);
                });
        } else {
            setStructures([]);
        }
    }, [selectedWafer]);

    useEffect(() => {
        if(selectedStructure){
              fetch(`/get_matrices/${selectedWafer}/${selectedStructure}`)
              .then(response => response.json())
              .then(data => {
                  setMatrices(data);
                  setOpenMatricesDialog(true);
              });
        }
    }, [selectedStructure])

    const handleCardClick = (waferId, event) => {
          event.stopPropagation();
          setSelectedWafer(waferId);
          setOpenDialog(true);
          document.body.style.overflow = 'hidden';
          scroll.scrollToTop({
            duration: 800,
            delay: 0,
            smooth: 'easeInOutQuart'
          });
    };

    const handleCloseDialog = () => {
          setSelectedWafer(null);
          setOpenDialog(false);
          document.body.style.overflow = 'auto';
    };

    const handleDocumentClick = () => {
        setSelectedWafer(null);
        setOpenDialog(false);
        document.body.style.overflow = 'auto';
    }

    const handleStructureClick = (structureId) => {
      setSelectedStructure(structureId);
    };

    const handleWheel = (event) => {
        if(event.deltaY < 0 && carouselRef.current && typeof carouselRef.current.decrement === "function") {
            carouselRef.current.decrement();
        } else if(carouselRef.current && typeof carouselRef.current.increment === "function") {
            carouselRef.current.increment();
        }
    };

    const handleSearchChange = (event) => {
        setSearchTerm(event.target.value);
    }

    const handleMatrixClic = (waferId, coordinates) => {
        setSelectedMatrix(coordinates);
        setOpenMatrixDialog(true);
        setIsLoading(true);
        fetch(`/plot_matrix/${waferId}/${coordinates}`)
        .then(response => response.json())
        .then(data => {
            setMatrixImages(data);
            setIsLoading(false);
        });
    }

    const handleExcelSelectStructureClick = (structure) => {
        if(selectedStructures.includes(structure)){
            setSelectedStructures(selectedStructures.filter(item => item !== structure));
            console.log(selectedStructures)
        } else {
            setSelectedStructures([...selectedStructures, structure]);
            console.log(selectedStructures)
        }
    }


    const handlePptSelectStructureClick = (structure) => {
        if(selectedStructures.includes(structure)){
            setSelectedStructures(selectedStructures.filter(item => item !== structure));
            console.log(selectedStructures)
        } else {
            setSelectedStructures([...selectedStructures, structure]);
            console.log(selectedStructures)
        }
    }

    function handleCreateExcelClick() {
        setOpenDialogExcelSelectStructures(true);
    }

    function handleCreatePptClick() {
        setOpenDialogPptSelectStructures(true);
    }

    function handleDeleteClick(){
        setOpenDeleteDialog(true);
        setOpenDialog(false);
    }

    const handleStartExcel = async () =>{
        setIsLoading(true);
        handleCloseDialog();
        setOpenDialogExcelSelectStructures(false);
        try {
          const response = await axios.get(`http://localhost:3000/excel_structure/${selectedWafer}/${selectedStructures}/${nameOfExcelFile}`);
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
    }

        const handleStartPpt = async () =>{
        setIsLoading(true);
        handleCloseDialog();
        setOpenDialogPptSelectStructures(false);
        try {
          const response = await axios.get(`http://localhost:3000/ppt_structure/${selectedWafer}/${selectedStructures}/${nameOfPptFile}`);
          if (response.status === 200) {
            setIsLoading(false);
            setOpenDialogMakePpt(false);
            setSelectedStructures([]);
          }
        } catch(error) {
        console.error("Error uploading files: ", error)
      } finally {
            setIsLoading(false);
        }
    }


    const handleDeleteWaferClick = async (waferId) => {
        try {
          const response = await axios.delete(`http://localhost:3000/delete_wafer/${waferId}`);
          if (response.status === 200) {
              setOpenDeleteDialog(false);
            alert("Wafer deleted successfully");
            setSelectedWafer(null);
            window.location.reload();
          }
        } catch(error) {
        console.error("Error uploading files: ", error)
      }
    }

    const handleSelectAll = () => {
        if(selectedStructures.length === structures.length) {
            setSelectedStructures([]);
        } else {
            setSelectedStructures(structures)
        }
    }

    return (
        <OpenContext.Provider value={{selectedWafer, setStructures}}>
            <TextField
              id="outlined-search"
              label="Search for a wafer"
              type="search"
              variant="outlined"
              value={searchTerm}
              onChange={handleSearchChange}
              sx={{
                width: 200,
                marginBottom: 2,
                position: 'absolute',
                top: 10,
                left: 10
              }}
            />
            <Box onWheel={handleWheel}>
                  <OriginalCarousel
                    onWheel={handleWheel}
                    showArrows={false}
                    autoPlay={false}
                    showStatus={false}
                    showIndicators={true}
                    infiniteLoop={true}
                    selectedItem={currentSlide}
                    onChange={setCurrentSlide}
                    showThumbs={false}
                    width={'100%'}
                    dynamicHeight={true}
                    centerMode={false}
                    ref={carouselRef}
                    transitionTime={250}
                    key={wafers.length}
                  >
                    {wafers
                        .filter(waferId => waferId.includes(searchTerm))
                        .reduce((acc, waferId, index) => {
                        if(index % 3 === 0){
                            acc.push([waferId]);
                        }else{
                            acc[acc.length - 1].push(waferId);
                        }
                        return acc;
                    }, []).map((waferGroup, index) => (
                            <CarouselContainer key={index}>
                                {waferGroup.map(waferId => (
                                    <CardFront
                                    waferId={waferId}
                                    onClick={(event) => handleCardClick(waferId, event)}
                                    onCreateExcelClick={handleCreateExcelClick}
                                    onCreatePptClick={handleCreatePptClick}
                                    onDeleteClick={handleDeleteClick}
                                    className={selectedWafer === waferId ? 'selected' : ''}
                                    />
                                ))}
                            </CarouselContainer>
                    ))}
                  </OriginalCarousel>
                <Backdrop open={selectedWafer !== null}
                          onClick={handleDocumentClick}
                          style={{ zIndex: 1, color: '#fff', backgroundColor: 'rgba(0, 0, 0, 0.7)' }}
                />
            </Box>
            <Dialog
              open={openDialog}
              onClose={handleCloseDialog}
              onBackdropClick={handleCloseDialog}
              aria-labelledby="alert-dialog-title"
              aria-describedby="alert-dialog-description"
            >
              <DialogTitle id="alert-dialog-title">{"Wafer Details"}</DialogTitle>
              <DialogContent>
                <Typography variant="h5">{selectedWafer} ({structures.length} structures)</Typography>
                  <FilterMenu selectedWafer={selectedWafer} setStructures={setStructures} structures={structures} allStructures={allStructures} style={{zIndex: 2}}/>
                  {
                      structures.length === 0 ?
                          <div>No structure found</div> : (
                               <Grid container spacing={2}>
                                  {structures.map((structure, index) => (
                                      <Grid item xs={6} key={index} sx={{display: 'flex', justifyContent: index % 2 === 0 ?
                                              'flex-start': 'flex-end'}}>
                                        <Chip
                                            key={index}
                                            label={structure}
                                            onClick={() => handleStructureClick(structure)}
                                            style={{margin: '5px', backgroundColor: "#4fbdff"}}
                                        />
                                      </Grid>
                                  ))}
                               </Grid>
                          )
                  }

                {/* Add more wafer details here */}
              </DialogContent>
              <DialogActions>
                <Button onClick={handleCloseDialog} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
              </DialogActions>
            </Dialog>

            <Dialog
              open={openDialogExcelSelectStructures}
              onClose={() => {
                  setOpenDialogExcelSelectStructures(false);
                  setSelectedStructures([]);
                  setSelectedWafer(null);
                  setOpenDialog(false);
                  document.body.style.overflow = 'auto';
              }}
              aria-labelledby="alert-dialog-title"
              aria-describedby="alert-dialog-description"
            >
              <DialogTitle id="alert-dialog-title">{"Please select structures"}</DialogTitle>
              <DialogContent>
                <Typography variant="h5">{selectedWafer} ({structures.length} structures)</Typography>
                  <Button style={{backgroundColor: "#4fbdff"}} onClick={handleSelectAll}>Select/Unselect All</Button>
                  <FilterMenu selectedWafer={selectedWafer} setStructures={setStructures} structures={structures} allStructures={allStructures} style={{zIndex: 2}}/>
                  <Grid container spacing={2}>
                  {structures.map((structure, index) => (
                      <Grid item xs={6} key={index} sx={{display: 'flex', justifyContent: index % 2 === 0 ?
                              'flex-start': 'flex-end'}}>
                        <Chip
                            key={`Selected ${index}`}
                            label={`${structure}${selectedStructures.includes(structure) ? " \u2714" : ""}`}
                            onClick={() => handleExcelSelectStructureClick(structure)}
                            style={{margin: '5px', backgroundColor: selectedStructures.includes(structure) ? "#4fbdff" : "#888888"}}
                        />
                      </Grid>
                  ))}
                  </Grid>
                {/* Add more wafer details here */}
              </DialogContent>
              <DialogActions>
                  <ExcelButton onClick={() => setOpenDialogMakeExcel(true)}>Make Excel</ExcelButton>
                <Button onClick={() =>{
                    setOpenDialogExcelSelectStructures(false);
                    setSelectedStructures([]);
                  setSelectedWafer(null);
                  setOpenDialog(false);
                  document.body.style.overflow = 'auto';
                }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
              </DialogActions>
            </Dialog>


            <Dialog
              open={openDialogMakeExcel}
              onClose={() => {
                  setOpenDialogExcelSelectStructures(false);
                  setSelectedStructures([]);
                  setSelectedWafer(null);
                  setOpenDialog(false);
                  document.body.style.overflow = 'auto';
              }}
              aria-labelledby="alert-dialog-title"
              aria-describedby="alert-dialog-description"
            >
              <DialogTitle id="alert-dialog-title">{"An excel File will be created with the following structures:"}</DialogTitle>
              <DialogContent>
                  {isLoading ? (
                      <>
                        <Select>
                            <CircularProgress />
                            Processing...
                        </Select>
                    </>
                  ) : (<Grid container spacing={2}>
                  {selectedStructures.map((structure, index) => (
                      <Grid item xs={6} key={index} sx={{display: 'flex', justifyContent: index % 2 === 0 ?
                              'flex-start': 'flex-end'}}>
                        <Chip
                            key={`Selected ${index}`}
                            label={structure}
                            style={{margin: '5px', backgroundColor: "#4fbdff" }}
                        />
                      </Grid>
                  ))}
                  </Grid>)}
                  <TextField autoFocus margin="dense" label="Name of File" fullWidth variant="standard" onChange={(e) => setNameOfExcelFile(e.target.value)} />
              </DialogContent>
              <DialogActions>
                  <ExcelButton onClick={handleStartExcel}>Start</ExcelButton>
                <Button onClick={() =>{
                    setOpenDialogMakeExcel(false);
                    setSelectedStructures([]);
                    setNameOfExcelFile("")
                  setSelectedWafer(null);
                  setOpenDialog(false);
                  document.body.style.overflow = 'auto';
                }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
              </DialogActions>
            </Dialog>

            <Dialog
              open={openDialogPptSelectStructures}
              onClose={() => {
                  setOpenDialogPptSelectStructures(false);
                  setSelectedStructures([]);
                  setSelectedWafer(null);
                  setOpenDialog(false);
                  document.body.style.overflow = 'auto';
              }}
              aria-labelledby="alert-dialog-title"
              aria-describedby="alert-dialog-description"
            >
              <DialogTitle id="alert-dialog-title">{"Please select structures"}</DialogTitle>
              <DialogContent>
                <Typography variant="h5">{selectedWafer} ({structures.length} structures)</Typography>
                  <Button style={{backgroundColor: "#4fbdff"}} onClick={handleSelectAll}>Select/Unselect All</Button>
                  <FilterMenu selectedWafer={selectedWafer} setStructures={setStructures} structures={structures} allStructures={allStructures} style={{zIndex: 2}}/>
                  <Grid container spacing={2}>
                  {structures.map((structure, index) => (
                      <Grid item xs={6} key={index} sx={{display: 'flex', justifyContent: index % 2 === 0 ?
                              'flex-start': 'flex-end'}}>
                        <Chip
                            key={`Selected ${index}`}
                            label={`${structure}${selectedStructures.includes(structure) ? " \u2714" : ""}`}
                            onClick={() => handlePptSelectStructureClick(structure)}
                            style={{margin: '5px', backgroundColor: selectedStructures.includes(structure) ? "#4fbdff" : "#888888"}}
                        />
                      </Grid>
                  ))}
                  </Grid>
                {/* Add more wafer details here */}
              </DialogContent>
              <DialogActions>
                  <PowerPointButton onClick={() => setOpenDialogMakePpt(true)}>Make PowerPoint</PowerPointButton>
                <Button onClick={() =>{
                    setOpenDialogPptSelectStructures(false);
                    setSelectedStructures([]);
                  setSelectedWafer(null);
                  setOpenDialog(false);
                  document.body.style.overflow = 'auto';
                }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
              </DialogActions>
            </Dialog>


            <Dialog
              open={openDialogMakePpt}
              onClose={() => {
                  setOpenDialogPptSelectStructures(false);
                  setSelectedStructures([]);
                  setSelectedWafer(null);
                  setOpenDialog(false);
                  document.body.style.overflow = 'auto';
              }}
              aria-labelledby="alert-dialog-title"
              aria-describedby="alert-dialog-description"
            >
              <DialogTitle id="alert-dialog-title">{"A PowerPoint File will be created with the following structures:"}</DialogTitle>
              <DialogContent>
                  {isLoading ? (
                      <>
                        <Select>
                            <CircularProgress />
                            Processing...
                        </Select>
                    </>
                  ) : (<Grid container spacing={2}>
                  {selectedStructures.map((structure, index) => (
                      <Grid item xs={6} key={index} sx={{display: 'flex', justifyContent: index % 2 === 0 ?
                              'flex-start': 'flex-end'}}>
                        <Chip
                            key={`Selected ${index}`}
                            label={structure}
                            style={{margin: '5px', backgroundColor: "#4fbdff" }}
                        />
                      </Grid>
                  ))}
                  </Grid>)}
                  <TextField autoFocus margin="dense" label="Name of File" fullWidth variant="standard" onChange={(e) => setNameOfPptFile(e.target.value)} />
                {/* Add more wafer details here */}
              </DialogContent>
              <DialogActions>
                  <PowerPointButton onClick={handleStartPpt}>Start</PowerPointButton>
                <Button onClick={() =>{
                    setOpenDialogMakePpt(false);
                    setSelectedStructures([]);
                    setNameOfPptFile("")
                  setSelectedWafer(null);
                  setOpenDialog(false);
                  document.body.style.overflow = 'auto';
                }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
              </DialogActions>
            </Dialog>



            <Dialog
                open={openMatricesDialog}
                onClose={() => setOpenMatricesDialog(false)}
                aria-labelledby="matrices-dialog-title"
                aria-describedby="matrices-dialog-description"
            >
                <DialogTitle id="matrices-dialog-title">{"Matrices"}</DialogTitle>
                <DialogContent>
                    {matrices.map((matrix, index) => (
                        <Chip key={index}
                              label={matrix}
                              style={{margin:'10px', backgroundColor: index % 2 === 0 ? "#e8eaf6" : "#c5cae9"}}
                              onClick={() => handleMatrixClic(selectedWafer, matrix)}
                        />

                    ))}
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => {
                        setOpenMatricesDialog(false);
                        setSelectedStructure(null);
                    }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
                </DialogActions>
            </Dialog>


            <Dialog
                open={openDeleteDialog}
                onClose={() => setOpenDeleteDialog(false)}
                aria-labelledby="delete-dialog-title"
                aria-describedby="delete-dialog-description"
            >
                <DialogTitle id="delete-dialog-title">{"Are you sure you want to delete this wafer?"}</DialogTitle>
                <DialogContent
                    style={{display: 'flex',
                    flexDirection: 'column',
                    alignItems: "center",
                    justifyContent: "center"
                }}>
                    <Chip key="Delete"
                              label="Delete"
                              style={{backgroundColor: 'red'}}
                              icon={<Trash />}
                              onClick={() => handleDeleteWaferClick(selectedWafer)}
                        />
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => {
                        setOpenDeleteDialog(false);
                        setSelectedWafer(null);
                    }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
                </DialogActions>
            </Dialog>

            <Dialog
                open={openMatrixDialog}
                onClose={() => {
                    setOpenMatrixDialog(false);
                    setMatrixImages([]);
                }}
                maxWidth='md'
                fullWidth={true}
                aria-labelledby="matrices-dialog-title"
                aria-describedby="matrices-dialog-description"
            >
                <DialogTitle id="matrices-dialog-title">{`Plots of ${selectedMatrix} in ${selectedStructure}`}</DialogTitle>
                <DialogContent>
                    {
                        isLoading ? (
                            <>
                                <Select>
                                    <CircularProgress />
                                    Processing...
                                </Select>
                            </>
                        ) : (
                            matrixImages.map((img, index) => (
                                <img
                                    src={`data:image/png;base64,${img}`}
                                    alt={`Matrix ${index + 1}`}
                                    style={{ width:"100%", height: 'auto' }}
                                    key={index}
                                />
                            ))
                        )
                    }
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => {
                        setOpenMatrixDialog(false);
                        setSelectedMatrix(null);
                    }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
                </DialogActions>
            </Dialog>

        </OpenContext.Provider>
    );
}

export default Open;