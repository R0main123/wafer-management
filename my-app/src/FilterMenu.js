import React, {useEffect, useState} from 'react';
import Popper from '@mui/material/Popper';
import MenuItem from '@mui/material/MenuItem';
import Button from '@mui/material/Button';
import ClickAwayListener from '@mui/material/ClickAwayListener';
import MenuList from '@mui/material/MenuList';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import SubMenu from "./SubMenu";

export default function FilterMenu({ selectedWafer, setStructures, structures }) {
  const [anchorEl, setAnchorEl] = useState(null);
  const [types, setTypes] = useState([]);
  const [temps, setTemps] = useState([]);
  const [files, setFiles] = useState([]);
  const [coords, setCoords] = useState([]);
  const [selectedItems, setSelectedItems] = useState({
      "TypeOfMeasurements":[],
      "Temperature":[],
      "NameOfFile":[],
      "Coordinates":[]
  });

  const open = Boolean(anchorEl);

  useEffect(() =>{
    if(selectedWafer){
      fetch(`/get_all_types/${selectedWafer}`)
          .then(response => response.json())
          .then(data => {
              setTypes(data);
          });

      fetch(`/get_all_temps/${selectedWafer}`)
          .then(response => response.json())
          .then(data => {
              setTemps(data);
          });

      fetch(`/get_all_filenames/${selectedWafer}`)
          .then(response => response.json())
          .then(data => {
              setFiles(data);
          });

      fetch(`/get_all_coords/${selectedWafer}`)
          .then(response => response.json())
          .then(data => {
              setCoords(data);
          });

    }
  }, [selectedWafer]);


  const handleMouseEnter = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMouseLeave = () => {
    setAnchorEl(null);
  };

  const handleResetFilter =() => {
      fetch(`/get_structures/${selectedWafer}`)
        .then(response => response.json())
        .then(data => setStructures(data));

      setSelectedItems({
          "TypeOfMeasurements":[],
          "Temperature":[],
          "NameOfFile":[],
          "Coordinates":[]
      });
  }

  return (
      <Box display="inline-flex" justifyContent="space-between" width="100%">
        <Box display="inline-flex" onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave} style={{ marginBottom: open ? 200 : 0 }}>
          <Button
            aria-owns={open ? 'mouse-over-popover' : undefined}
            aria-haspopup="true"
          >
            Filter by
          </Button>
          <Popper id="mouse-over-popover" open={open} anchorEl={anchorEl} placement="bottom-start" disablePortal>
            <Paper>
                <MenuList sx={{padding: '0', '& li': {padding: '5'}}}>
                    <SubMenu filterType="TypeOfMeasurements" children="Type of Measurements" items ={types} color="#FF886E" structures={structures} selectedItems={selectedItems} setSelectedItems={setSelectedItems}/>
                    <SubMenu filterType="Temperature" children="Temperature" items ={temps} color="#6EE9FF" structures={structures} selectedItems={selectedItems} setSelectedItems={setSelectedItems}/>
                    <SubMenu filterType="NameOfFile" children="Name of File" items ={files} color="#AAAAAA" structures={structures} selectedItems={selectedItems} setSelectedItems={setSelectedItems}/>
                    <SubMenu filterType="Coordinates" children="Coordinates" items ={coords} color="#FAFF5B" structures={structures} selectedItems={selectedItems} setSelectedItems={setSelectedItems}/>
                </MenuList>
            </Paper>
          </Popper>
        </Box>
        <Button color="primary" onClick={handleResetFilter}>
            Reset filters
        </Button>
      </Box>
  );
}