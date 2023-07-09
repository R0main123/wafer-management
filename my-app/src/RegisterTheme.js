import React from "react";
import {Dialog, DialogActions, DialogContent, DialogTitle, LinearProgress, styled, TextField, Button} from '@mui/material';
import { Box } from '@mui/material';
import {createTheme} from "@mui/material/styles";


export const registertheme = createTheme({
    palette: {
        primary: {
            main: '#2c2c2c',
        },
    },
    typography:{
        fontSize: 15,
        fontFamily: "system-ui" ,

    },
    components: {
        MuiCssBaseline: {
            styleOverrides: {
                body: {
                    background: "linear-gradient(to top, white, dodgerblue)",
                    backgroundRepeat: "no-repeat",
                    color: "#424242",
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "center",
                    alignItems: "center",
                    minHeight: "100vh",
                    margin: 0,
                    gap: "20px",
                },
            },
        },
    },
});


export const StyledDropzone = styled(Box) (({theme}) => ({
        border: '2px dashed #999',
        padding: theme.spacing(2),
        width: "200px",
        height: "200px",
        textAlign: "center",
}));

export const Infos = styled('p')({
    justifyContent: "center",
    alignContent: "center",
    fontSize: "20px",
})

export const FormatInfos = styled('p')({
    justifyContent: "center",
    alignContent: "center",
    fontSize: "15px",
    marginLeft: "20%",
})

export const StyledDialog = styled(Dialog)`
  .MuiDialogActions-root {
    .MuiButton-root {
      color: whitesmoke;
      background-color: #4949ff;

      &:hover {
        background-color: #2525fd;
      }
    }

  }
`;

export const StyledDialogButton =  styled(Button)`
      color: whitesmoke;
      background-color: #4949ff; 
      border-radius: 20px;
`;

