import {styled} from "@mui/system";
import {Button} from "@mui/material";



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

export const Success = styled("h1")({
    display: 'flex',
    flexDirection: "column",
    alignItems: "center",
    justifyContent: 'center',
})