import React, { useState } from 'react';
import {CircularProgress, FormControlLabel} from '@mui/material';
import {Checkbox, ChoiceButton} from "./ChoiceTheme";
import Box from "@mui/material/Box";
import { Select } from "./ChoiceTheme";
import axios from "axios";
import {useNavigate} from "react-router-dom";


const Choice = () => {
  const [checked, setChecked] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleCheckboxChange = (event) => {
    setChecked(event.target.checked);
  };

  const handleClick = async () => {
      setLoading(true);

        axios.post(`http://localhost:3000/options/${checked}`)
        .then(() => {
            navigate("/finished")
        })
            .catch((err) => console.log(err))
            .finally(() => setLoading(false));
  };

  return (
            <Box
                display='flex'
                flexDirection= "column"
                alignItems= "center"
                justifyContent= 'center'
                height= '100vh'
                textAlign= "center"
            >

                <div>
                    {loading ? (
                    <>
                        <CircularProgress />
                        <Select>
                            Processing...
                        </Select>
                    </>
                    ) : (
                        <>
                    <Box mb={2}>
                        <Select>Please select options</Select>
                    </Box>

                    <Box mb={2}>
                      <FormControlLabel
                        control={
                          <Checkbox
                            checked={checked}
                            onChange={handleCheckboxChange}
                            color="primary"
                          />
                        }
                        label="Register J-V measurements (if you have at least one I-V file)"
                      />
                    </Box>

                    <Box>
                      <ChoiceButton variant="contained" color="primary" onClick={handleClick}>
                        Process files
                      </ChoiceButton>
                    </Box>
                </>
            )}
        </div>
     </Box>
  );
};

export default Choice;