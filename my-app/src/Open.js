import React, { useState, useEffect, useRef } from 'react';
import {Backdrop, Chip, CircularProgress, Grid, ListItemText, MenuItem, Typography, Accordion, AccordionSummary, AccordionDetails} from '@mui/material';
import {
    ActionButton,
    CardFront,
    CarouselContainer,
    ComplianceButton,
    ExcelButton,
    PowerPointButton,
    WaferMapButton
} from './OpenTheme';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
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
import {ChoiceButton} from "./FinishedTheme";
import {useNavigate} from "react-router-dom";
export const OpenContext = React.createContext();

function Open() {
    const navigate = useNavigate();
    const [wafers, setWafers] = useState([]);
    const [openDialogMakeExcel, setOpenDialogMakeExcel] = useState(false);
    const [openDialogMakePpt, setOpenDialogMakePpt] = useState(false);
    const [openDialog, setOpenDialog] = useState(false);
    const [openDialogExcelSelectStructures, setOpenDialogExcelSelectStructures] = useState(false);
    const [openDialogPptSelectStructures, setOpenDialogPptSelectStructures] = useState(false);
    const [openMatricesDialog, setOpenMatricesDialog] = useState(false);
    const [openDeleteDialog, setOpenDeleteDialog] = useState(false);
    const [openSetComplianceDialog, setOpenSetComplianceDialog] = useState(false);
    const [openWaferMapDialog, setOpenWaferMapDialog] = useState(false);
    const [openShowWaferMapDialog, setOpenShowWaferMapDialog] = useState(false);
    const [openPlotDialog, setOpenPlotDialog] = useState(false);
    const [openAccordion, setOpenAccordion] = useState(false);
    const [openVBDExcel, setOpenVBDExcel] = useState(false);
    const [openChooseNormal, setOpenChooseNormal] = useState(false);
    const [openPlotsNormal, setOpenPlotsNormal] = useState(false);
    const [selectedWafer, setSelectedWafer] = useState(null);
    const [selectedStructure, setSelectedStructure] = useState(null);
    const [selectedSession, setSelectedSession] = useState(null);
    const [selectedStructures, setSelectedStructures] = useState([]);
    const [selectedMatrix, setSelectedMatrix] = useState(null);
    const [selectedCompliance, setSelectedCompliance] = useState(null);
    const [selectedMatrixIndex, setSelectedMatrixIndex] = useState(null);
    const [selectedNormalMeasure, setSelectedNormalMeasure] = useState(null);
    const [triplets, setTriplets] = useState([]);
    const [openWhatNormal, setOpenWhatNormal] = useState(false);
    const [currentSlide, setCurrentSlide] = useState(0);
    const [currentWaferMap, setCurrentWaferMap] = useState(null);
    const [currentNormalPlots, setCurrentNormalPlots] = useState([])
    const [searchTerm, setSearchTerm] = useState("");
    const [structures, setStructures] = useState([]);
    const [sessions, setSessions] = useState([]);
    const [mapSessions, setMapSessions] = useState([]);
    const [values, setValues] = useState([])
    const [mapStructures, setMapStructures] = useState([]);
    const [allStructures, setAllStructures] = useState([]);
    const [matrices, setMatrices] = useState([]);
    const [matrixImages, setMatrixImages] = useState([]);
    const [nameOfExcelFile, setNameOfExcelFile] = useState("");
    const [nameOfPptFile, setNameOfPptFile] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [newCompliance, setNewCompliance] = useState(null);
    const [compliances, setCompliances] = useState([]);
    const [filteredMapStructuresDisplay, setFilteredMapStructuresDisplay] = useState([]);
    const carouselRef = useRef(null);
    const [filteredStructures, setFilteredStructures] = useState([]);
    const [filteredStructuresDisplay, setFilteredStructuresDisplay] = useState([]);
    const [filteredSessions, setFilteredSessions] = useState([]);
    const [filteredTypes, setFilteredTypes] = useState([]);
    const [filteredTemps, setFilteredTemps] = useState([]);
    const [filteredFiles, setFilteredFiles] = useState([]);
    const [filteredCoords, setFilteredCoords] = useState([]);
    const [chosenValue, setChosenValue] = useState('');


    useEffect(() => {
        fetch('/open')
            .then(response => response.json())
            .then(data => {
                setWafers(data);
                setCurrentSlide(0);
            });

    }, []);

    useEffect(() => {
        if(selectedWafer){
            fetch(`/get_all_structures/${selectedWafer}`)
            .then(response => response.json())
            .then(data => {
                setFilteredStructures(data);
            });
        }
    }, [selectedWafer]);

    useEffect(() => {
        if(selectedWafer){
            fetch(`/get_all_types/${selectedWafer}`)
            .then(response => response.json())
            .then(data => {
                setFilteredTypes(data);
            });

            fetch(`/get_all_temps/${selectedWafer}`)
            .then(response => response.json())
            .then(data => {
                setFilteredTemps(data);
            });

            fetch(`/get_all_filenames/${selectedWafer}`)
            .then(response => response.json())
            .then(data => {
                setFilteredFiles(data);
            });

            fetch(`/get_all_coords/${selectedWafer}`)
            .then(response => response.json())
            .then(data => {
                setFilteredCoords(data);
            });
        } else {
            setFilteredTypes([]);
            setFilteredCoords([]);
            setFilteredFiles([]);
            setFilteredTemps([]);
        }
    }, [selectedWafer]);


    useEffect(() => {
        setCurrentSlide(0)
    }, [wafers]);

    useEffect(() => {
        console.log(selectedMatrix)
    }, [selectedMatrix]);

    useEffect(() => {
        console.log(filteredSessions)
    }, [filteredSessions]);

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
            setIsLoading(true);
            fetch(`/get_sessions/${selectedWafer}`)
            .then(response => response.json())
            .then(data => {
                setSessions(data);
                setFilteredSessions(data);
                console.log(selectedSession)
        })
        setIsLoading(false)
        } else {
            setSessions([])
            setMapSessions([]);
            setFilteredSessions([]);
            console.log(selectedSession)
        }
    }, [selectedWafer]);

    useEffect(() => {
        if(selectedSession){
            fetch(`/get_structures/${selectedWafer}/${selectedSession}`)
                .then(response => response.json())
                .then(data => {
                    setStructures(data);
                    setAllStructures(data);
                });
        } else {
            setStructures([]);
        }
    }, [selectedSession]);

    useEffect(() => {
        console.log(selectedSession);
    }, [selectedSession]);

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


    useEffect(() => {
        setFilteredStructuresDisplay(structures.filter(structure => filteredStructures.includes(structure)));
    }, [structures, filteredStructures]);

    useEffect(() => {
        setFilteredMapStructuresDisplay(mapStructures.filter(structure => filteredStructures.includes(structure)));
    }, [mapStructures, filteredStructures]);


    useEffect(() => {
        console.log(matrixImages.length);
    }, [matrixImages]);


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

    const handleSessionClick = (session) => {
        setSelectedSession(session);
        fetch(`/get_structures/${selectedWafer}/${session}`)
          .then(response => response.json())
          .then(data => {
            setStructures(data);
          });
    }

    const handleComplianceSessionClick = (session) => {
        setSelectedSession(session);
        fetch(`/get_map_structures/${selectedWafer}/${session}`)
          .then(response => response.json())
          .then(data => {
            setStructures(data);
          });

        fetch(`get_compl/${selectedWafer}/${session}`)
        .then(response => response.json())
        .then(data => setSelectedCompliance(data));
    }

    const handleNormalClick = (waferId) => {
        setSelectedWafer(waferId);
        fetch(`/get_normal_values/${waferId}`)
          .then(response => response.json())
          .then(data => {
            setValues(data);
          });
        setOpenWhatNormal(true);
    }



    const handleCloseDialog = () => {
          setSelectedWafer(null);
          setOpenDialog(false);
          setSessions([]);
          setSelectedSession(null);
          document.body.style.overflow = 'auto';
    };

    const handleDocumentClick = () => {
        setSelectedWafer(null);
        setOpenDialog(false);
        document.body.style.overflow = 'auto';
    }

    const handleWheel = (event) => {
        if(event.deltaY < 0 && carouselRef.current && typeof carouselRef.current.decrement === "function") {
            carouselRef.current.decrement();
        } else if(carouselRef.current && typeof carouselRef.current.increment === "function") {
            carouselRef.current.increment();
        }
    };

    const handleSearchChange = (event) => {
        setSearchTerm(event.target.value.toUpperCase());
    }


    const handleChooseSelectStructureClick = (structure) => {
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

    function handleDeleteClick(waferId){
        setSelectedWafer(waferId);
        setOpenDeleteDialog(true);
        setOpenDialog(false);
    }

    const handleWaferMapClick = (waferId) => {
        setSelectedWafer(waferId);
        fetch(`/get_map_sessions/${waferId}`)
            .then(response => response.json())
            .then(data => {
                setMapSessions(data);
                setFilteredSessions(data);
                console.log(selectedSession)
        })
        setOpenWaferMapDialog(true);
    }

    const handleStartExcel = async () =>{
        setIsLoading(true);
        handleCloseDialog();
        setOpenDialogExcelSelectStructures(false);
        try {
          const response = await axios.get(`http://localhost:3000/excel_structure/${selectedWafer}/${filteredSessions}/${selectedStructures}/${filteredTypes}/${filteredTemps}/${filteredFiles}/${filteredCoords}/${nameOfExcelFile}`);
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
          const response = await axios.get(`http://localhost:3000/ppt_structure/${selectedWafer}/${filteredSessions}/${selectedStructures}/${filteredTypes}/${filteredTemps}/${filteredFiles}/${filteredCoords}/${nameOfPptFile}`);
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
      } finally {
            setSelectedWafer(null);
        }
    }

    const handleSetCompliance = async () =>{
        try {
          const response = await axios.get(`http://localhost:3000/set_compl/${selectedWafer}/${selectedSession}/${newCompliance}`);
          if (response.status === 200) {
            setSelectedCompliance(newCompliance);
            setOpenSetComplianceDialog(false);
          }
        } catch(error) {
        console.error("Error uploading files: ", error)
      } finally {
            setOpenSetComplianceDialog(false);
        }
    }


    const handleSelectAll = () => {
        if(selectedStructures.length === structures.length) {
            setSelectedStructures([]);
        } else {
            setSelectedStructures(structures)
        }
    }

    const handleWaferMapStructure = async (structureId) => {
        setOpenShowWaferMapDialog(true);
        setIsLoading(true);
        fetch(`/create_wafer_map/${selectedWafer}/${selectedSession}/${structureId}`)
        .then(response => response.json())
                .then(data => {
                    setCurrentWaferMap(data);
                });
        setIsLoading(false);

    }

    const handlePlotPersonalized = () => {
        setIsLoading(true)
        setOpenPlotDialog(true);
        console.log("Just before fetch")
        fetch(`/plot_selected_matrices/${selectedWafer}/${filteredSessions}/${selectedStructures}/${filteredTypes}/${filteredTemps}/${filteredFiles}/${filteredCoords}`)
        .then(response => {
           return response.json()
        })
        .then(data => {
            setMatrixImages(data);
            setIsLoading(false);
        });
    }

    const registerExcelVBD = async () => {
        setIsLoading(true);
        try {
            fetch(`/get_map_sessions/${selectedWafer}`)
            .then(response => response.json())
            .then(data => {
                setFilteredSessions(filteredSessions.filter(value => data.includes(value)))
        })
          const response = await axios.get(`http://localhost:3000/register_excel_VBD/${selectedWafer}/${filteredSessions}/${selectedStructures}/${filteredTemps}/${filteredFiles}/${filteredCoords}/${nameOfExcelFile}`);
          if (response.status === 200) {
              setOpenDeleteDialog(setOpenVBDExcel(false));
            alert("Excel created successfully");
            setNameOfExcelFile(null);
            window.location.reload();
          }
        } catch(error) {
        console.error("Error uploading files: ", error)
      } finally {
            setIsLoading(false);
        }
    }

    const handleChooseNormal = (item) => {
        setSelectedNormalMeasure(item);
        setOpenChooseNormal(true);
    }

    const handleNormalPlots = () => {
        setOpenPlotsNormal(true);
        setIsLoading(true);
        const url = `/normal_distrib_${selectedNormalMeasure}/${selectedWafer}/${filteredSessions}/${selectedStructures}/${filteredCoords}`
        fetch(url)
        .then(response => response.json())
        .then(data => {
            setCurrentNormalPlots(data);
        });
        setIsLoading(false);
    }

    return (
        <OpenContext.Provider value={{selectedWafer, setStructures}}>
            <Box style={{ position: 'fixed',
                top: 0,
                left: 10,
                display: 'flex',
                justifyContent: 'space-between',
                width: '100%'
            }}>

                <ChoiceButton variant="contained" color="primary" sx={{
                    width: 120,
                    height: 40,
                  }} onClick={() => {
                    navigate("/");
                }}>
                    Return home
                </ChoiceButton>

                <TextField
                  id="outlined-search"
                  label="Search for a wafer"
                  type="search"
                  variant="outlined"
                  value={searchTerm}
                  onChange={handleSearchChange}
                  sx={{
                    margin: '10px',
                    marginRight: '10px',
                    width: 200,
                    marginBottom: 2,
                  }}
                />

            </Box>
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
                                    onWaferMapClick={handleWaferMapClick}
                                    onNormalClick={handleNormalClick}
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
                  {isLoading ? (
                      <>
                        <Select>
                            <CircularProgress />
                            Processing...
                        </Select>
                    </>
                  ) : (
                      <>
                <Typography variant="h5">{selectedWafer} ({sessions.length} sessions)</Typography>
                <FilterMenu selectedWafer={selectedWafer}
                            setStructures={setStructures}
                            structures={structures}
                            allStructures={allStructures}
                            style={{zIndex: 2}}
                            filteredStructures={filteredStructures}
                            setFilteredStructures={setFilteredStructures}
                            session={selectedSession}
                            filteredSessions={filteredSessions}
                            setFilteredSessions={setFilteredSessions}
                            filteredTypes={filteredTypes}
                            setFilteredTypes={setFilteredTypes}
                            filteredTemps={filteredTemps}
                            setFilteredTemps={setFilteredTemps}
                            filteredFiles={filteredFiles}
                            setFilteredFiles={setFilteredFiles}
                            filteredCoords={filteredCoords}
                            setFilteredCoords={setFilteredCoords}
                            setIsloading={setIsLoading}

                />

                <Grid container spacing={2}>
                  {sessions.map((session, index) => (
                  <Grid item xs={12} key={index}>
                    <Accordion expanded={openAccordion === `panel${index}`}>
                      <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls={`panel${index}-content`}
                        id={`panel${index}-header`}
                        onClick={() => {
                          handleSessionClick(session);
                          setOpenAccordion(openAccordion === `panel${index}` ? false : `panel${index}`);
                        }}
                      >
                        <Typography>{session}</Typography>
                      </AccordionSummary>
                      <AccordionDetails>
                        <Button style={{backgroundColor: "#4fbdff"}} onClick={handleSelectAll}>Select/Unselect All</Button>
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
                </>
                )}

              </DialogContent>
              <DialogActions>
                  <ExcelButton onClick={() => setOpenDialogMakeExcel(true)}>Make Excel</ExcelButton>
                  <PowerPointButton onClick={() => setOpenDialogMakePpt(true)}>Make PowerPoint</PowerPointButton>
                  <Button onClick={handlePlotPersonalized} sx={{backgroundColor:'#47a3ff', color: 'white', '&:hover':{backgroundColor: 'blue'}}}>Plot</Button>
                <Button onClick={handleCloseDialog} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
              </DialogActions>
            </Dialog>

            <Dialog
                open={openPlotDialog}
                onClose={() => {
                    setOpenPlotDialog(false);
                    setSelectedStructures([]);
                    setOpenAccordion(false);
                    setMatrixImages([]);
                }}
                maxWidth='md'
                fullWidth={true}
                aria-labelledby="matrices-dialog-title"
                aria-describedby="matrices-dialog-description"
            >
                <DialogTitle id="matrices-dialog-title">{`Plots of your selection`}</DialogTitle>
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
                        setOpenPlotDialog(false);
                        setOpenAccordion(false);
                        setSelectedStructures([])
                        setMatrixImages([]);
                    }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
                </DialogActions>
            </Dialog>


            <Dialog
              open={openDialogMakeExcel}
              onClose={() => {
                  setSelectedStructures([]);
                  setOpenDialogMakeExcel(false);
                  setNameOfExcelFile("");
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
                  document.body.style.overflow = 'auto';
                }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
              </DialogActions>
            </Dialog>

            <Dialog
              open={openDialogMakePpt}
              onClose={() => {
                  setSelectedStructures([]);
                  setOpenDialogMakePpt(false);
                  setNameOfPptFile("");
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

              </DialogContent>
              <DialogActions>
                  <PowerPointButton onClick={handleStartPpt}>Start</PowerPointButton>
                <Button onClick={() =>{
                    setOpenDialogMakePpt(false);
                    setSelectedStructures([]);
                    setNameOfPptFile("")
                  document.body.style.overflow = 'auto';
                }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
              </DialogActions>
            </Dialog>

            <Dialog
              open={openWaferMapDialog}
              onClose={() => {
                  setOpenWaferMapDialog(false);
                  handleCloseDialog();
              }}
              onBackdropClick={() => {
                  setOpenWaferMapDialog(false);
              }}
              aria-labelledby="alert-dialog-title"
              aria-describedby="alert-dialog-description"
            >
              <DialogTitle id="alert-dialog-title">{"Please select a structure in a wafer"}</DialogTitle>
              <DialogContent>
                <Typography variant="h5">{selectedWafer} ({mapSessions.length} sessions)</Typography>
                <FilterMenu selectedWafer={selectedWafer}
                            setStructures={setStructures}
                            structures={structures}
                            allStructures={allStructures}
                            style={{zIndex: 2}}
                            filteredStructures={filteredStructures}
                            setFilteredStructures={setFilteredStructures}
                            session={selectedSession}
                            filteredSessions={filteredSessions}
                            setFilteredSessions={setFilteredSessions}
                            filteredTypes={filteredTypes}
                            setFilteredTypes={setFilteredTypes}
                            filteredTemps={filteredTemps}
                            setFilteredTemps={setFilteredTemps}
                            filteredFiles={filteredFiles}
                            setFilteredFiles={setFilteredFiles}
                            filteredCoords={filteredCoords}
                            setFilteredCoords={setFilteredCoords}
                            setIsloading={setIsLoading}

                />
                {
                mapSessions.length === 0 ?
                <div>Found no sessions with I-V measures</div> : (
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
                          <Typography> Compliance: {selectedCompliance} A</Typography>
                          <ActionButton onClick={() => setOpenSetComplianceDialog(true)}>Set compliance</ActionButton>
                        <Grid container spacing={2}>
                          {filteredStructuresDisplay.map((structure, index) => (
                              <Grid item xs={6} key={index} sx={{display: 'flex', justifyContent: index % 2 === 0 ?
                          'flex-start': 'flex-end'}}>
                            <Chip
                                key={`Selected ${index}`}
                                label={`${structure}${selectedStructures.includes(structure) ? " \u2714" : ""}`}
                                onClick={() => {
                                    handleWaferMapStructure(structure);
                                }}
                                style={{margin: '5px', backgroundColor:  "#4fbdff" }}
                            />
                          </Grid>
                          ))}
                        </Grid>
                      </AccordionDetails>
                    </Accordion>
                  </Grid>
                  ))}
                </Grid>
                )
                }

              </DialogContent>
              <DialogActions>
                  <ExcelButton onClick={() => setOpenVBDExcel(true)}>Make Excel</ExcelButton>
                <Button onClick={() => {
                  setOpenWaferMapDialog(false);
                  handleCloseDialog();
              }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
              </DialogActions>
            </Dialog>


            <Dialog
              open={openSetComplianceDialog}
              onClose={() => {
                  setOpenSetComplianceDialog(false);
                  document.body.style.overflow = 'auto';
              }}
              aria-labelledby="alert-dialog-title"
              aria-describedby="alert-dialog-description"
            >
              <DialogTitle id="alert-dialog-title">{"Please enter a new value:"}</DialogTitle>
              <DialogContent>
                  <TextField autoFocus margin="dense" label="New Compliance value" fullWidth variant="standard" onChange={(e) => setNewCompliance(e.target.value)} />
              </DialogContent>
              <DialogActions>
                  <ComplianceButton onClick={handleSetCompliance}>Set</ComplianceButton>
                <Button onClick={() =>{
                    setOpenSetComplianceDialog(false);
                  document.body.style.overflow = 'auto';
                }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
              </DialogActions>
            </Dialog>


            <Dialog
                open={openShowWaferMapDialog}
                onClose={() => {
                    setOpenShowWaferMapDialog(false);
                    setCurrentWaferMap(null);
                    setSelectedSession(null);
                }}
                maxWidth='md'
                fullWidth={true}
                aria-labelledby="matrices-dialog-title"
                aria-describedby="matrices-dialog-description"
            >
                <DialogTitle id="matrices-dialog-title">{`Plots of ${selectedMatrix} in ${selectedStructure}`}</DialogTitle>
                <DialogContent>
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

                </DialogContent>
                <DialogActions>
                    <Button onClick={() => {
                        setOpenShowWaferMapDialog(false);
                        setCompliances([]);
                        setCurrentWaferMap(null);
                        setSelectedMatrixIndex(null);
                        setSelectedCompliance(null);
                        setSelectedSession(null);
                        setTriplets([]);
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
              open={openVBDExcel}
              onClose={() => {
                  setOpenVBDExcel(false);
              }}
              onBackdropClick={() => {
                  setOpenWaferMapDialog(false);
              }}
              aria-labelledby="alert-dialog-title"
              aria-describedby="alert-dialog-description"
            >
              <DialogTitle id="alert-dialog-title">{"Please select a structure in a wafer"}</DialogTitle>
              <DialogContent>
                <Typography variant="h5">{selectedWafer} ({mapSessions.length} sessions)</Typography>
                <FilterMenu selectedWafer={selectedWafer}
                            setStructures={setStructures}
                            structures={structures}
                            allStructures={allStructures}
                            style={{zIndex: 2}}
                            filteredStructures={filteredStructures}
                            setFilteredStructures={setFilteredStructures}
                            session={selectedSession}
                            filteredSessions={filteredSessions}
                            setFilteredSessions={setFilteredSessions}
                            filteredTypes={filteredTypes}
                            setFilteredTypes={setFilteredTypes}
                            filteredTemps={filteredTemps}
                            setFilteredTemps={setFilteredTemps}
                            filteredFiles={filteredFiles}
                            setFilteredFiles={setFilteredFiles}
                            filteredCoords={filteredCoords}
                            setFilteredCoords={setFilteredCoords}
                            setIsloading={setIsLoading}

                />
                {
                mapSessions.length === 0 ?
                <div>Found no sessions with I-V measures</div> : (
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
                    <TextField autoFocus margin="dense" label="Name of File" fullWidth variant="standard" onChange={(e) => setNameOfExcelFile(e.target.value)} />
                </Grid>
                )
                }

              </DialogContent>
              <DialogActions>
                  <ExcelButton onClick={registerExcelVBD}>Make Excel</ExcelButton>
                <Button onClick={() => {
                  setOpenVBDExcel(false)
              }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
              </DialogActions>
            </Dialog>


            <Dialog
              open={openWhatNormal}
              onClose={() => {
                  setOpenWhatNormal(false);
                  handleCloseDialog();
              }}
              onBackdropClick={() => {
                  setOpenWhatNormal(false);
              }}
              aria-labelledby="alert-dialog-title"
              aria-describedby="alert-dialog-description"
            >
              <DialogTitle id="alert-dialog-title">{"Please select a Value"}</DialogTitle>
              <DialogContent>

                  {values.length === 0 ? (
                      <Typography>No values available in this wafer</Typography>
                  ) : (
                      values.map((item, index) => (
                              <Button
                                  key={index}
                                  variant='contained'
                                  color="primary"
                                  onClick={() => {
                                      handleChooseNormal(item)
                                  }}
                              >{item}</Button>

                      ))
                  )}

              </DialogContent>
              <DialogActions>
                <Button onClick={() => {
                  setOpenWhatNormal(false);
                  handleCloseDialog();
              }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
              </DialogActions>
            </Dialog>


            <Dialog
              open={openChooseNormal}
              onClose={() => {setOpenChooseNormal(false)}}
              onBackdropClick={handleCloseDialog}
              aria-labelledby="alert-dialog-title"
              aria-describedby="alert-dialog-description"
            >
              <DialogTitle id="alert-dialog-title">{"Please select your parameters"}</DialogTitle>
              <DialogContent>
                  {isLoading ? (
                      <>
                        <Select>
                            <CircularProgress />
                            Processing...
                        </Select>
                    </>
                  ) : (
                      <>
                <Typography variant="h5">{selectedWafer} ({sessions.length} sessions)</Typography>
                <FilterMenu selectedWafer={selectedWafer}
                            setStructures={setStructures}
                            structures={structures}
                            allStructures={allStructures}
                            style={{zIndex: 2}}
                            filteredStructures={filteredStructures}
                            setFilteredStructures={setFilteredStructures}
                            session={selectedSession}
                            filteredSessions={filteredSessions}
                            setFilteredSessions={setFilteredSessions}
                            filteredTypes={filteredTypes}
                            setFilteredTypes={setFilteredTypes}
                            filteredTemps={filteredTemps}
                            setFilteredTemps={setFilteredTemps}
                            filteredFiles={filteredFiles}
                            setFilteredFiles={setFilteredFiles}
                            filteredCoords={filteredCoords}
                            setFilteredCoords={setFilteredCoords}
                            setIsloading={setIsLoading}

                />

                <Grid container spacing={2}>
                  {sessions.map((session, index) => (
                  <Grid item xs={12} key={index}>
                    <Accordion expanded={openAccordion === `panel${index}`}>
                      <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls={`panel${index}-content`}
                        id={`panel${index}-header`}
                        onClick={() => {
                          handleSessionClick(session);
                          setOpenAccordion(openAccordion === `panel${index}` ? false : `panel${index}`);
                        }}
                      >
                        <Typography>{session}</Typography>
                      </AccordionSummary>
                      <AccordionDetails>
                        <Button style={{backgroundColor: "#4fbdff"}} onClick={handleSelectAll}>Select/Unselect All</Button>
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
                </>
                )}

              </DialogContent>
              <DialogActions>
                  <Button onClick={handleNormalPlots} sx={{backgroundColor:'#47a3ff', color: 'white', '&:hover':{backgroundColor: 'blue'}}}>Plot</Button>
                <Button onClick={() => {setOpenChooseNormal(false)}} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
              </DialogActions>
            </Dialog>


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
                <DialogTitle id="matrices-dialog-title">{`Plots of your selection`}</DialogTitle>
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
                            currentNormalPlots.map((img, index) => (
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
                        setOpenPlotsNormal(false);
                        setSelectedStructures([]);
                        setOpenAccordion(false);
                        setCurrentNormalPlots([]);
                    }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
                </DialogActions>
            </Dialog>


            {/*
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
                open={openMatricesDialog}
                onClose={() => {
                    setOpenMatricesDialog(false);
                    setSelectedStructure(null);
                    setSelectedCompliance(null);
                }}
                aria-labelledby="matrices-dialog-title"
                aria-describedby="matrices-dialog-description"
            >
                <DialogTitle id="matrices-dialog-title">{"Matrices"}</DialogTitle>
                <DialogContent>
                    {matrices.map((matrix, index) => (
                        <Chip key={index}
                              label={matrix}
                              style={{margin:'10px', backgroundColor: index % 2 === 0 ? "#e8eaf6" : "#c5cae9"}}
                              onClick={() => {
                                  handleMatrixClic(selectedWafer, matrix);
                              }}
                        />

                    ))}
                </DialogContent>
                <DialogTitle id="matrices-dialog-title">{"Registered Compliance"}</DialogTitle>
                <DialogContent>
                    <div>
                        {selectedCompliance}
                        <ComplianceButton onClick={() => setOpenSetComplianceDialog(true)}>Set Compliance</ComplianceButton>
                    </div>
                </DialogContent>
                <DialogActions>
                    <ComplianceButton onClick={handleSelectWaferMap}>Show WaferMap</ComplianceButton>
                    <Button onClick={() => {
                        setNewCompliance(null);
                        setOpenMatricesDialog(false);
                    }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
                </DialogActions>
            </Dialog>


            <div>
                {matrices.map((matrix, index) => (

                    <Dialog
                        open={openWaferMapDialog && selectedMatrixIndex === index}
                        onClose={() => {
                            setOpenWaferMapDialog(false);
                        }}
                        aria-labelledby="matrix-dialog-title"
                        aria-describedby="matrix-dialog-description"
                        key={`dialog-${index}`}
                    >
                        <DialogTitle id="matrix-dialog-title">
                            Please select the compliance you want for matrix {matrix}
                        </DialogTitle>
                        <DialogContent>
                            {currentCompliances.map((item, idx) => (
                                <div key={idx}>
                                    <input
                                        type="radio"
                                        id={`compliance-${index}-${idx}`}
                                        name={`compliance-${index}`}
                                        value={idx}
                                        onChange={e => setSelectedCompliance(item.VBD)}
                                    />
                                    <label htmlFor={`compliance-${index}-${idx}`}>Compliance: {item.Compliance} A (VBD: {item.VBD} V)</label>
                                </div>
                            ))}
                        </DialogContent>
                        <DialogActions>
                            <Button onClick={() => {
                                const matrix = matrices[selectedMatrixIndex];
                                const x = matrix.split(',')[0].slice(1);
                                const y = matrix.split(',')[1].slice(0, -1);
                                setTriplets(triplets.concat([[x, y, selectedCompliance]]));
                                console.log(triplets)
                                if (selectedMatrixIndex < matrices.length - 1) {
                                    setSelectedMatrixIndex(selectedMatrixIndex + 1);
                                } else {
                                    setOpenWaferMapDialog(false);
                                    handleWaferMap();
                                }
                            }}>Next</Button>
                        </DialogActions>
                    </Dialog>
                ))}
            </div>


            <Dialog
              open={openSetComplianceDialog}
              onClose={() => {
                  setOpenSetComplianceDialog(false);
                  document.body.style.overflow = 'auto';
              }}
              aria-labelledby="alert-dialog-title"
              aria-describedby="alert-dialog-description"
            >
              <DialogTitle id="alert-dialog-title">{"Please enter a new value:"}</DialogTitle>
              <DialogContent>
                  <TextField autoFocus margin="dense" label="New Compliance value" fullWidth variant="standard" onChange={(e) => setNewCompliance(e.target.value)} />
              </DialogContent>
              <DialogActions>
                  <ComplianceButton onClick={handleSetCompliance}>Set</ComplianceButton>
                <Button onClick={() =>{
                    setOpenSetComplianceDialog(false);
                  document.body.style.overflow = 'auto';
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

                <DialogTitle id="matrices-dialog-title">{`Registered compliances for ${selectedMatrix}`}</DialogTitle>
                <DialogContent>
                    <div>
                        {
                            compliances.map((item, index) => (
                                <div key={index}>
                                    <p>Compliance: {item.Compliance}A VBD: {item.VBD}V</p>
                                </div>
                            ))
                        }
                    </div>
                    <ComplianceButton onClick={() => setOpenTryComplianceDialog(true)}>Try another compliance</ComplianceButton>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => {
                        setOpenMatrixDialog(false);
                        setSelectedMatrix(null);
                    }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
                </DialogActions>
            </Dialog>

            <Dialog
              open={openTryComplianceDialog}
              onClose={() => {
                  setOpenTryComplianceDialog(false);
                  document.body.style.overflow = 'auto';
              }}
              aria-labelledby="alert-dialog-title"
              aria-describedby="alert-dialog-description"
            >
              <DialogTitle id="alert-dialog-title">{"Please enter a new value:"}</DialogTitle>
              <DialogContent>
                  <TextField autoFocus margin="dense" label="New Compliance value" fullWidth variant="standard" onChange={(e) => setNewCompliance(e.target.value)} />
              </DialogContent>
              <DialogActions>
                  <ComplianceButton onClick={handleTryCompliance}>Try</ComplianceButton>
                <Button onClick={() =>{
                    setOpenTryComplianceDialog(false);
                  document.body.style.overflow = 'auto';
                }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
              </DialogActions>
            </Dialog>


            <Dialog
                open={openShowWaferMapDialog}
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
                    <img
                        src={`data:image/png;base64,${currentWaferMap}`}
                        alt={`Wafer Map of ${selectedStructure}`}
                        style={{ width:"100%", height: 'auto' }}
                    />

                </DialogContent>
                <DialogActions>
                    <Button onClick={() => {
                        setOpenShowWaferMapDialog(false);
                        setCompliances([]);
                        setCurrentWaferMap(null);
                        setSelectedMatrixIndex(null);
                        setSelectedCompliance(null);
                        setTriplets([]);
                    }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
                </DialogActions>
            </Dialog>*/}
        </OpenContext.Provider>
    );
}

export default Open;