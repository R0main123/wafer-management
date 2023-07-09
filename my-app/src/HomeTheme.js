import { createTheme } from "@mui/material/styles";
import { styled } from "@mui/system";
import { Button } from '@mui/material';



export const homeTheme = createTheme({
    palette: {
        primary: {
            main: '#3f51b5',
        },
    },
    typography:{
        fontSize: 10,
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

export const ChoiceButton = styled(Button)({
    display: "inline-block",
    backgroundColor: "#3498db",
    color: "#fff",
    padding: "10px 20px",
    margin: "10px",
    borderRadius: "20px",
    justifyContent: "center",
    transition: "background-color 0.3s",
    '&:hover':{
        backgroundColor: "#2980b9",
    },
});







