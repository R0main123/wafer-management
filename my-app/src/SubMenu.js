import React, {useContext, useEffect, useState} from 'react';
import Popper from '@mui/material/Popper';
import MenuItem from '@mui/material/MenuItem';
import ClickAwayListener from '@mui/material/ClickAwayListener';
import MenuList from '@mui/material/MenuList';
import Paper from '@mui/material/Paper';
import {OpenContext} from "./Open";
import {filterProps} from "framer-motion";

export default function SubMenu({ children, items, color, filterType, structures, selectedItems, setSelectedItems, filteredStructures, setFilteredStructures, session,
                                filteredSessions, setFilteredSessions, filteredTypes, setFilteredTypes, filteredTemps, setFilteredTemps,
                                   filteredFiles, setFilteredFiles, filteredCoords, setFilteredCoords}) {
  const [anchorEl, setAnchorEl] = useState(null);
  const [selectedItem, setSelectedItem] = useState(items[0]);
  const open = Boolean(anchorEl);
  const { selectedWafer } = useContext(OpenContext);


  const handleFilterChange = (selectedItem) => {
      let newSelectedItems = [...selectedItems[filterType]];
      let deselecting = false;

      if(newSelectedItems.includes(selectedItem)){
          newSelectedItems = newSelectedItems.filter(item => item !== selectedItem);
          deselecting = true;
          console.log("New Selected Items: "+newSelectedItems)
      } else {
          newSelectedItems.push(selectedItem);
      }

      setSelectedItems({
          ...selectedItems,
          [filterType]: newSelectedItems
      });


      if(selectedWafer && selectedItem && !deselecting){
          let url;

          switch(filterType){
              case 'TypeOfMeasurements':
                  url = `filter_by_Meas/${selectedWafer}/${selectedItem}`
                  setFilteredTypes(newSelectedItems)
                  break;
              case 'Temperature':
                  url = `filter_by_Temps/${selectedWafer}/${selectedItem}`
                  setFilteredTemps(newSelectedItems)
                  break;
              case 'NameOfFile':
                  url = `filter_by_Filenames/${selectedWafer}/${selectedItem}`
                  setFilteredFiles(newSelectedItems)
                  break;
              case 'Coordinates':
                  url = `filter_by_Coords/${selectedWafer}/${selectedItem}`
                  setFilteredCoords(newSelectedItems)
                  break;
              case 'Session':
                  url = `filter_by_Session/${selectedWafer}/${selectedItem}`
                  setFilteredSessions(selectedItem)
                  break;
              default:
                  console.log("Unknown filter Type: " + filterType)
                  return;
          }

          fetch(url)
          .then(response => response.json())
          .then(data => {
              const intersection = filteredStructures.filter(value => data.includes(value));
              setFilteredStructures(intersection)
          });
      }

      if (deselecting) {
        // Refetch all structures
        fetch(`/get_all_structures/${selectedWafer}`)
          .then(response => response.json())
          .then(data => {
              if(selectedItem.length===0){
                  setFilteredStructures(data);
              }
            // Apply all still selected filters to the data
            Object.keys(selectedItems).forEach(filterType => {
              selectedItems[filterType].forEach(item => {
              if(item !== selectedItem){
                  console.log("Item: "+item)
                  console.log("Selected Item: " + selectedItem)
                  let url;

                  switch(filterType){
                      case 'TypeOfMeasurements':
                        url = `filter_by_Meas/${selectedWafer}/${item}`
                          setFilteredTypes(newSelectedItems)
                        break;
                      case 'Temperature':
                        url = `filter_by_Temps/${selectedWafer}/${item}`
                          setFilteredTemps(newSelectedItems)
                        break;
                      case 'NameOfFile':
                        url = `filter_by_Filenames/${selectedWafer}/${item}`
                          setFilteredFiles(newSelectedItems)
                        break;
                      case 'Coordinates':
                        url = `filter_by_Coords/${selectedWafer}/${item}`
                          setFilteredCoords(newSelectedItems)
                        break;
                      case 'Session':
                          url = `filter_by_Session/${selectedWafer}/${item}`
                          setFilteredSessions(newSelectedItems)
                          break;
                      default:
                        console.log("Unknown filter Type: " + filterType)
                        return;
                  }

                  fetch(url)
                      .then(response => response.json())
                      .then(data => {
                          const intersection = filteredStructures.filter(value => data.includes(value));
                          setFilteredStructures(intersection)
                      });
              }

              });
            });
          setFilteredStructures(data)
          });
      }


  }


  const handleMouseEnter = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMouseLeave = () => {
    setAnchorEl(null);
  };

  return (
    <div
        style={{ display:'flex',
          justifyContent:'center',
          alignItems:'center',
          width: '150px',
          height: '40px',
          backgroundColor: color,
          borderRadius: "10px",
          }}
        onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}
    >
      {children}
      <Popper id="mouse-over-submenu" open={open} anchorEl={anchorEl} placement="right-start" disablePortal>
        <Paper>
          <ClickAwayListener onClickAway={handleMouseLeave}>
            <MenuList>
              {items.map((item, index) => (
                <MenuItem sx key={index} onClick={() => handleFilterChange(item)} style={{marginLeft: 20}}>{item} {selectedItems[filterType].includes(item) && " \u2714"}</MenuItem>
              ))}
            </MenuList>
          </ClickAwayListener>
        </Paper>
      </Popper>
    </div>
  );
}