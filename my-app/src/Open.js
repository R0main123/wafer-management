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
    const [openNormalExcel, setOpenNormalExcel] = useState(false);
    const [openChooseNormal, setOpenChooseNormal] = useState(false);
    const [openChooseWM, setOpenChooseWM] = useState(false);
    const [openChooseLeak, setOpenChooseLeak] = useState(false);
    const [openChooseR, setOpenChooseR] = useState(false);
    const [openChooseC, setOpenChooseC] = useState(false);
    const [openChooseCmes, setOpenChooseCmes] = useState(false);
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
    const [openWhatWM, setOpenWhatWM] = useState(false);
    const [currentSlide, setCurrentSlide] = useState(0);
    const [currentWaferMap, setCurrentWaferMap] = useState(null);
    const [currentNormalPlots, setCurrentNormalPlots] = useState([])
    const [searchTerm, setSearchTerm] = useState("");
    const [structures, setStructures] = useState([]);
    const [sessions, setSessions] = useState([]);
    const [mapSessions, setMapSessions] = useState([]);
    const [leakSessions, setLeakSessions] = useState([]);
    const [RSessions, setRSessions] = useState([]);
    const [CSessions, setCSessions] = useState([]);
    const [CmesSessions, setCmesSessions] = useState([]);
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
            fetch(`/get_plot_sessions/${selectedWafer}`)
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
            fetch(`/get_plot_structures/${selectedWafer}/${selectedSession}`)
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

    useEffect(() => {
        console.log(leakSessions)
    }, [leakSessions])

    useEffect(() => {
        console.log(CSessions)
    }, [CSessions])

    useEffect(() => {
        console.log(CmesSessions)
    }, [CmesSessions])

    useEffect(() => {
        console.log(RSessions)
    }, [RSessions])

    useEffect(() => {
        console.log(structures)
    }, [structures])


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

    const handleNormalSessionClick = (session) => {
        setSelectedSession(session);
        fetch(`/get_${selectedNormalMeasure}_structures/${selectedWafer}/${session}`)
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
          setOpenAccordion(false);
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

    const handleChoosewhatMap = (waferId) => {
        setIsLoading(true);
        setOpenWhatWM(true);
        setSelectedWafer(waferId);
        fetch(`/get_normal_values/${waferId}`)
          .then(response => response.json())
          .then(data => {
            setValues(data);
          });
        setIsLoading(false);

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
              setOpenVBDExcel(false);
            alert("Excel created successfully");
            setNameOfExcelFile(null);
          }
        } catch(error) {
        console.error("Error uploading files: ", error)
      } finally {
            setIsLoading(false);
        }
    }

    const registerNormalVBD = async () => {
        setIsLoading(true);
        console.log(selectedNormalMeasure);
        try{
            const response = await axios.get(`http://localhost:3000/excel_normal_${selectedNormalMeasure}/${selectedWafer}/${sessions}/${selectedStructures}/${filteredCoords}/${nameOfExcelFile}`);
          if (response.status === 200) {
              setOpenNormalExcel(false);
            alert("Excel created successfully");
            setNameOfExcelFile(null);
          }
        } catch {
            console.error("Error creating excel");
        } finally {
            setIsLoading(false)
        }
    }

    const handleChooseNormal = (item) => {
        setSelectedNormalMeasure(item);
        fetch(`/get_${item}_sessions/${selectedWafer}`)
            .then(response => response.json())
            .then(data => {
                setSessions(data);
                setFilteredSessions(data);
                console.log(selectedSession)
        })
        setOpenChooseNormal(true);
    }

    const handleLeakSessionClick = (waferId) => {
        setSelectedWafer(waferId);
        fetch(`/get_Leak_sessions/${waferId}`)
            .then(response => response.json())
            .then(data => {
                setLeakSessions(data);
                setFilteredSessions(data);
                console.log(selectedSession)
        })
        setOpenChooseLeak(true);
    }

    const handleRSessionClick = (waferId) => {
        setSelectedWafer(waferId);
        fetch(`/get_R_sessions/${waferId}`)
            .then(response => response.json())
            .then(data => {
                setRSessions(data);
                setFilteredSessions(data);
                console.log(selectedSession)
        })
        setOpenChooseR(true);
    }

    const handleCSessionClick = (waferId) => {
        setSelectedWafer(waferId);
        fetch(`/get_C_sessions/${waferId}`)
            .then(response => response.json())
            .then(data => {
                setCSessions(data);
                setFilteredSessions(data);
                console.log(selectedSession)
        })
        setOpenChooseC(true);
    }

    const handleCmesSessionClick = (waferId) => {
        setSelectedWafer(waferId);
        fetch(`/get_Cmes_sessions/${waferId}`)
            .then(response => response.json())
            .then(data => {
                setCmesSessions(data);
                setFilteredSessions(data);
                console.log(selectedSession)
        })
        setOpenChooseCmes(true);
    }

    const manageLeakSessionClick = (session) => {
        setSelectedSession(session);
        fetch(`/get_Leak_structures/${selectedWafer}/${session}`)
          .then(response => response.json())
          .then(data => {
            setStructures(data);
          });
    }

    const manageRSessionClick = (session) => {
        setSelectedSession(session);
        fetch(`/get_R_structures/${selectedWafer}/${session}`)
          .then(response => response.json())
          .then(data => {
            setStructures(data);
          });
    }

    const manageCSessionClick = (session) => {
        setSelectedSession(session);
        fetch(`/get_C_structures/${selectedWafer}/${session}`)
          .then(response => response.json())
          .then(data => {
            setStructures(data);
          });
    }

    const manageCmesSessionClick = (session) => {
        setSelectedSession(session);
        fetch(`/get_Cmes_structures/${selectedWafer}/${session}`)
          .then(response => response.json())
          .then(data => {
            setStructures(data);
          });
    }

    const handleWaferMapLeakStructure = async (structureId) => {
        setOpenShowWaferMapDialog(true);
        setIsLoading(true);
        fetch(`/Leak_wafer_map/${selectedWafer}/${selectedSession}/${structureId}`)
        .then(response => response.json())
                .then(data => {
                    setCurrentWaferMap(data);
                });
        setIsLoading(false);
    }

    const handleWaferMapRStructure = async (structureId) => {
        setOpenShowWaferMapDialog(true);
        setIsLoading(true);
        fetch(`/R_wafer_map/${selectedWafer}/${selectedSession}/${structureId}`)
        .then(response => response.json())
                .then(data => {
                    setCurrentWaferMap(data);
                });
        setIsLoading(false);
    }

    const handleWaferMapCStructure = async (structureId) => {
        setOpenShowWaferMapDialog(true);
        setIsLoading(true);
        fetch(`/C_wafer_map/${selectedWafer}/${selectedSession}/${structureId}`)
        .then(response => response.json())
                .then(data => {
                    setCurrentWaferMap(data);
                });
        setIsLoading(false);
    }

    const handleWaferMapCmesStructure = async (structureId) => {
        setOpenShowWaferMapDialog(true);
        setIsLoading(true);
        fetch(`/Cmes_wafer_map/${selectedWafer}/${selectedSession}/${structureId}`)
        .then(response => response.json())
                .then(data => {
                    setCurrentWaferMap(data);
                });
        setIsLoading(false);
    }

    const handleChooseWM = (item) => {
        setSelectedNormalMeasure(item);
        if(item == "VBD"){
            handleWaferMapClick(selectedWafer);
        } else if(item == "Leak"){
            handleLeakSessionClick(selectedWafer);
        } else if(item == "R"){
            handleRSessionClick(selectedWafer);
        } else if(item == "C"){
            handleCSessionClick(selectedWafer);
        } else if(item == "Cmes"){
            handleCmesSessionClick(selectedWafer);
        }
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
                                    onWaferMapClick={handleChoosewhatMap}
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
                  setOpenAccordion(false);
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
                    setOpenAccordion(false);
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
                  setOpenAccordion(false);
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
                    setOpenAccordion(false);
                    setNameOfPptFile("")
                  document.body.style.overflow = 'auto';
                }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
              </DialogActions>
            </Dialog>

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
                <div>Found no sessions with I-V measurements</div> : (
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
                  setOpenAccordion(false);
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
                    setOpenAccordion(false);
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
                    setOpenAccordion(false);
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
                        setOpenAccordion(false);
                        setSelectedSession(null);
                        setTriplets([]);
                    }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
                </DialogActions>
            </Dialog>

            <Dialog
                open={openDeleteDialog}
                onClose={() => {
                    setOpenDeleteDialog(false);
                    setOpenAccordion(false);
                }}
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
                        setOpenAccordion(false);
                        setSelectedWafer(null);
                    }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
                </DialogActions>
            </Dialog>


            <Dialog
              open={openVBDExcel}
              onClose={() => {
                  setOpenVBDExcel(false);
                  setOpenAccordion(false);
              }}
              onBackdropClick={() => {
                  setOpenWaferMapDialog(false);
                  setOpenAccordion(false);
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
                <div>Found no sessions with I-V measurements</div> : (
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
                  setOpenVBDExcel(false);
                  setOpenAccordion(false);
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
                  setOpenAccordion(false);
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
              open={openWhatWM}
              onClose={() => {
                  setOpenWhatWM(false);
                  setValues([]);
                  handleCloseDialog();
              }}
              onBackdropClick={() => {
                  setValues([]);
                  setOpenAccordion(false);
                  setOpenWhatWM(false);
              }}
              aria-labelledby="alert-dialog-title"
              aria-describedby="alert-dialog-description"
            >
              <DialogTitle id="alert-dialog-title">{"Please select a Value"}</DialogTitle>
              <DialogContent>
                {isLoading ? (
                      <>
                        <Select>
                            <CircularProgress />
                            Processing...
                        </Select>
                    </>
                  ) : (
                  values.length === 0 ? (
                      <Typography>No values available in this wafer</Typography>
                  ) : (
                      values.map((item, index) => (
                              <Button
                                  key={index}
                                  variant='contained'
                                  color="primary"
                                  onClick={() => {
                                      handleChooseWM(item)
                                  }}
                              >{item}</Button>

                      ))
                  ))}

              </DialogContent>
              <DialogActions>
                <Button onClick={() => {
                  setOpenWhatWM(false);
                  setValues([]);
                  handleCloseDialog();
              }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
              </DialogActions>
            </Dialog>


            <Dialog
              open={openChooseNormal}
              onClose={() => {
                  setOpenChooseNormal(false);
                  setOpenAccordion(false);
              }}
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
                          handleNormalSessionClick(session);
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
                <Button onClick={() => {
                    setOpenChooseNormal(false);
                    setOpenAccordion(false);
                }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
              </DialogActions>
            </Dialog>


            <Dialog
              open={openChooseLeak}
              onClose={() => {
                  setOpenChooseLeak(false);
                  setOpenAccordion(false);
              }}
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
                  {leakSessions.map((session, index) => (
                  <Grid item xs={12} key={index}>
                    <Accordion expanded={openAccordion === `panel${index}`}>
                      <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls={`panel${index}-content`}
                        id={`panel${index}-header`}
                        onClick={() => {
                          manageLeakSessionClick(session);
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
                                onClick={() => handleWaferMapLeakStructure(structure)}
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
                <Button onClick={() => {
                    setOpenChooseLeak(false);
                    setOpenAccordion(false);
                }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
              </DialogActions>
            </Dialog>


            <Dialog
              open={openChooseR}
              onClose={() => {
                  setOpenChooseR(false);
                  setOpenAccordion(false);
              }}
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
                  {RSessions.map((session, index) => (
                  <Grid item xs={12} key={index}>
                    <Accordion expanded={openAccordion === `panel${index}`}>
                      <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls={`panel${index}-content`}
                        id={`panel${index}-header`}
                        onClick={() => {
                          manageRSessionClick(session);
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
                                onClick={() => handleWaferMapRStructure(structure)}
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
                <Button onClick={() => {
                    setOpenChooseR(false);
                    setOpenAccordion(false);
                }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
              </DialogActions>
            </Dialog>

            <Dialog
              open={openChooseC}
              onClose={() => {
                  setOpenChooseC(false);
                  setOpenAccordion(false);
              }}
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
                  {CSessions.map((session, index) => (
                  <Grid item xs={12} key={index}>
                    <Accordion expanded={openAccordion === `panel${index}`}>
                      <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls={`panel${index}-content`}
                        id={`panel${index}-header`}
                        onClick={() => {
                          manageCSessionClick(session);
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
                                onClick={() => handleWaferMapCStructure(structure)}
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
                <Button onClick={() => {
                    setOpenChooseC(false);
                    setOpenAccordion(false);
                }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
              </DialogActions>
            </Dialog>

            <Dialog
              open={openChooseCmes}
              onClose={() => {
                  setOpenChooseCmes(false);
                  setOpenAccordion(false);
              }}
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
                  {CmesSessions.map((session, index) => (
                  <Grid item xs={12} key={index}>
                    <Accordion expanded={openAccordion === `panel${index}`}>
                      <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls={`panel${index}-content`}
                        id={`panel${index}-header`}
                        onClick={() => {
                          manageCmesSessionClick(session);
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
                                onClick={() => handleWaferMapCmesStructure(structure)}
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
                <Button onClick={() => {
                    setOpenChooseCmes(false);
                    setOpenAccordion(false);
                }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
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
                    <ExcelButton onClick={() => setOpenNormalExcel(true)}>Make Excel</ExcelButton>
                    <Button onClick={() => {
                        setOpenPlotsNormal(false);
                        setSelectedStructures([]);
                        setOpenAccordion(false);
                        setCurrentNormalPlots([]);
                    }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
                </DialogActions>
            </Dialog>

            <Dialog
              open={openNormalExcel}
              onClose={() => {
                  setOpenNormalExcel(false);
                  setOpenAccordion(false);
              }}
              onBackdropClick={() => {
                  setOpenNormalExcel(false);
                  setOpenAccordion(false);
              }}
              aria-labelledby="alert-dialog-title"
              aria-describedby="alert-dialog-description"
            >
              <DialogTitle id="alert-dialog-title">{"Please select a structure in a wafer"}</DialogTitle>
              <DialogContent>
                <Typography variant="h5">{selectedWafer}</Typography>

                    <TextField autoFocus margin="dense" label="Name of File" fullWidth variant="standard" onChange={(e) => setNameOfExcelFile(e.target.value)} />


              </DialogContent>
              <DialogActions>
                  <ExcelButton onClick={registerNormalVBD}>Make Excel</ExcelButton>
                <Button onClick={() => {
                  setOpenNormalExcel(false);
                  setOpenAccordion(false);
              }} sx={{backgroundColor:'#ff4747', color: 'white', '&:hover':{backgroundColor: 'red'}}}>Close</Button>
              </DialogActions>
            </Dialog>

        </OpenContext.Provider>
    );
}

export default Open;