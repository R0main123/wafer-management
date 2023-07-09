import React, {useContext, useEffect, useState} from 'react';
import Popper from '@mui/material/Popper';
import MenuItem from '@mui/material/MenuItem';
import ClickAwayListener from '@mui/material/ClickAwayListener';
import MenuList from '@mui/material/MenuList';
import Paper from '@mui/material/Paper';
import {OpenContext} from "./Open";
import {filterProps} from "framer-motion";

export default function SubMenu({ children, items, color, filterType, structures, selectedItems, setSelectedItems }) {
  const [anchorEl, setAnchorEl] = useState(null);
  const [selectedItem, setSelectedItem] = useState(items[0]);
  const open = Boolean(anchorEl);
  const { selectedWafer, setStructures } = useContext(OpenContext);


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
                  break;
              case 'Temperature':
                  url = `filter_by_Temps/${selectedWafer}/${selectedItem}`
                  break;
              case 'NameOfFile':
                  url = `filter_by_Filenames/${selectedWafer}/${selectedItem}`
                  break;
              case 'Coordinates':
                  url = `filter_by_Coords/${selectedWafer}/${selectedItem}`
                  break;
              default:
                  console.log("Unknown filter Type: " + filterType)
                  return;
          }

          fetch(url)
          .then(response => response.json())
          .then(data => {
              const intersection = structures.filter(value => data.includes(value));
              setStructures(intersection)
          });
      }

      if (deselecting) {
        // Refetch all structures
        fetch(`/get_structures/${selectedWafer}`)
          .then(response => response.json())
          .then(data => {
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
                        break;
                      case 'Temperature':
                        url = `filter_by_Temps/${selectedWafer}/${item}`
                        break;
                      case 'NameOfFile':
                        url = `filter_by_Filenames/${selectedWafer}/${item}`
                        break;
                      case 'Coordinates':
                        url = `filter_by_Coords/${selectedWafer}/${item}`
                        break;
                      default:
                        console.log("Unknown filter Type: " + filterType)
                        return;
                  }

                  fetch(url)
                      .then(response => response.json())
                      .then(data => {
                          const intersection = structures.filter(value => data.includes(value));
                          setStructures(intersection)
                      });
              }

              });
            });

            // After all filters have been applied
            setStructures(data);
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