import React, { useCallback, useState, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import {StyledDropzone, registertheme, Infos, FormatInfos, StyledDialog, StyledDialogButton} from "./RegisterTheme";
import CssBaseline from "@mui/material/CssBaseline";
import {ThemeProvider} from "@mui/material/styles";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import axios from 'axios';
import {DialogActions, DialogContent, DialogTitle} from "@mui/material";
import { useNavigate } from "react-router-dom";

function RegisterNewMeasures() {
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const [temp, setTemp] = useState("");
  const [lotId, setLotId] = useState("");
  const [waferId, setWaferId] = useState("");
  const [currentFile, setCurrentFile] = useState(null);
  const [files, setFiles] = useState([]);
  const [fileQueue, setFileQueue] = useState([]);

  const onDrop = useCallback(async (acceptedFiles) => {
    setFileQueue(acceptedFiles);
  }, []);

  useEffect(() => {
    if (fileQueue.length > 0) {
      setCurrentFile(fileQueue[0]);
      setOpen(true);
    }
  }, [fileQueue]);


  useEffect(() => {
    if(fileQueue.length===0 && files.length > 0){
      handleSend();
    }
  }, [files]);


  const handleClose = () => {
    if (!currentFile?.name.startsWith('AL') && (!lotId || !waferId)){
      alert("Please fill out all fields");
      return;
    }

    let newName = "";

    let finalTemp = temp === "" ? 25 : temp;

    if(currentFile.name.startsWith('AL')) {
      newName = currentFile.name.split('.').slice(0, -1).join('.') + '_' + finalTemp + '.' + currentFile.name.split('.').pop();
    } else {
      newName = currentFile.name.split('.').slice(0, -1).join('.') + '@@@' + lotId + '_' + waferId + '_' + finalTemp + '.' + currentFile.name.split('.').pop();
    }

    let newFile = new File([currentFile], newName, {type: currentFile.type, lastModified: new Date() });

    setFiles(oldFileList => [...oldFileList, newFile]);

    setCurrentFile(null);
    setOpen(false);
    setFileQueue(oldFileQueue => oldFileQueue.slice(1));

    setTemp("");
    setLotId("");
    setWaferId("");
  }

  const handleSend = async () => {
    const formData = new FormData();

    files.forEach((file, index) => {
      console.log(file.name)
      formData.append("file", file);
    });

    try {
      const response = await axios.post("http://localhost:3000/upload", formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      if (response.status === 200) {
        console.log("Files uploaded successfully");
        setFiles([]);
        navigate("/Choice");
      }
    } catch(error) {
        console.error("Error uploading files: ", error)
      }
    };

  const {getRootProps, getInputProps, isDragActive} = useDropzone({ onDrop });

  return (
    <ThemeProvider theme={registertheme}>
      <CssBaseline />
      <Box display="flex" alignItems="center" justifyContent="center" flexDirection="column" className="app">
        <div>
          <Infos>Please drag and drop data files below:</Infos>
          <FormatInfos>(Format .txt, .tbl, .tbl.Z or .lim)</FormatInfos>
          <Box display="flex" alignItems="center" justifyContent="center" flexDirection="column" mt={5}>
            <StyledDropzone {...getRootProps()}>
              <input {...getInputProps()} />
              {
                isDragActive ?
                  <p>Please Drop your files here</p> :
                  <p>Drag and Drop your files here, or click to select them</p>
              }
            </StyledDropzone>
          </Box>

          <StyledDialog open={open} onClose={handleClose} onKeyDown={(e) => e.key === 'Enter' && handleClose()}>
            <DialogTitle>{`Please enter the necessary data for ${currentFile?.name}:`}</DialogTitle>
            <DialogContent>
              {
                currentFile?.name.startsWith('AL') ?
                  <TextField autoFocus margin="dense" label="Temperature (defaut: 25)" fullWidth type="number" variant="standard" value={temp} onChange={(e) => setTemp(e.target.value)} />
                : (
                  <>
                    <TextField autoFocus margin="dense" label="Temperature (defaut: 25)" fullWidth type="number" variant="standard" value={temp} onChange={(e) => setTemp(e.target.value)} />
                    <TextField autoFocus margin="dense" label="Lot ID" fullWidth variant="standard" onChange={(e) => setLotId(e.target.value)} />
                    <TextField autoFocus margin="dense" label="Wafer ID" fullWidth variant="standard" onChange={(e) => setWaferId(e.target.value)} />

                  </>
                )
              }
            </DialogContent>
            <DialogActions>
              <StyledDialogButton onClick={handleClose}>
                Confirm
              </StyledDialogButton>
            </DialogActions>
          </StyledDialog>

        </div>
      </Box>
    </ThemeProvider>
  )
}

export default RegisterNewMeasures;