import React from 'react';
import {styled, Card, CardContent, Typography, Button, Dialog} from '@mui/material';


export const WaferCard = styled(Card)(({ theme }) => ({
  minWidth: 275,
  maxWidth: 345,
  background: theme.palette.grey[200],
  margin: theme.spacing(2),
  marginBottom: "50px",

  cursor: 'pointer',
  '&:hover': {
    background: theme.palette.grey[300],
  },
  '&.selected': {
    background: theme.palette.grey[400],
  },
}));

export const CarouselContainer = styled('div')({
  width: '100%',
  height: '100%',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
});

export const ActionButton = styled(Button)(({ theme }) => ({
  margin: theme.spacing(1),
}));

export const WaferMapButton =styled(ActionButton)(({ theme }) => ({
  backgroundColor: "#9943d3",
  '&:hover':{
        backgroundColor: "#470075",
    },
}));

export const ExcelButton =styled(ActionButton)(({ theme }) => ({
  backgroundColor: "#43d343",
  '&:hover':{
        backgroundColor: "#037443",
    },
}));

export const PowerPointButton =styled(ActionButton)(({ theme }) => ({
  backgroundColor: "#ff7f3f",
  '&:hover':{
        backgroundColor: "#c85138",
    },
}));

export const DeleteButton =styled(ActionButton)(({ theme }) => ({
  backgroundColor: "#ff5050",
  '&:hover':{
        backgroundColor: "#c81618",
    },
}));


export const ComplianceButton =styled(ActionButton)(({ theme }) => ({
  backgroundColor: "#5096ff",

  '&:hover':{
        backgroundColor: "#0066ff",
        color: "white"
    },
}));



export const CardFront = ({ waferId, onCreateExcelClick, onCreatePptClick, onDeleteClick, onWaferMapClick, ...props }) => (
  <WaferCard {...props}>
    <CardContent
    marginBottom={"20px"}>
      <Typography variant="h5">{waferId}</Typography>
      <WaferMapButton variant="contained" onClick={(event) => {
        event.stopPropagation();
        onWaferMapClick(waferId);
      }}>Wafer Map</WaferMapButton>
      <DeleteButton variant="contained" onClick={(event) => {
        event.stopPropagation();
        onDeleteClick();
      }}>Delete wafer</DeleteButton>
    </CardContent>
  </WaferCard>
);
