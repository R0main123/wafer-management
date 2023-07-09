import React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from "@mui/material/CssBaseline";
import { homeTheme, ChoiceButton} from './HomeTheme';
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import RegisterNewMeasures from "./RegisterNewMeasures";
import Choice from "./Choice";
import Finished from "./Finished";
import Open from "./Open";
import './global.css';



class App extends React.Component {
  render() {
    return (
      <Router>
        <ThemeProvider theme={homeTheme}>
          <CssBaseline />
          <Routes>
            <Route path="/" element={
              <Box display="flex" alignItems="center" justifyContent="center" flexDirection="column" className="app">
                <Typography variant="h2" gutterBottom className="title">
                  Welcome to the Wafer Management App
                </Typography>
                <Box display="flex" alignItems="center" justifyContent="center" flexDirection="column" mt={5}>
                  <ChoiceButton component={Link} to="/register">
                    Register New Measures
                  </ChoiceButton>
                  <ChoiceButton component={Link} to ="/wafers">
                    Open Existing Wafers
                  </ChoiceButton>
                </Box>
              </Box>
            } />
            <Route path="/" element={<App/>} />
            <Route path="/register" element={ <RegisterNewMeasures /> } />
            <Route path="/choice" element={<Choice />} />
            <Route path="/finished" element={<Finished />} />
            <Route path="/wafers" element={<Open />} />
          </Routes>
        </ThemeProvider>

      </Router>
    );
  }
}

export default App;