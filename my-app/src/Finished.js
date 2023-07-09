import Box from "@mui/material/Box";
import React from "react";
import {useNavigate} from "react-router-dom";
import {Success, ChoiceButton} from "./FinishedTheme";



function Finished() {
    const navigate = useNavigate();
    const handleClick =() => {
        navigate("/")
    }
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
                    <Box mb={2}>
                        <Success>All files are now registered in database</Success>
                    </Box>

                    <Box>
                      <ChoiceButton variant="contained" color="primary" onClick={handleClick}>
                        Return home
                      </ChoiceButton>
                    </Box>
                </div>
            </Box>
    );
};

export default Finished;