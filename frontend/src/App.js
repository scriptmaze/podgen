import './App.css';

import React from "react";
import FileUpload from "./FileUpload";
import { Container, AppBar, Typography } from "@mui/material";

function App() {
  return (
    <Container>
      <AppBar
        position="static"
        style={{ marginBottom: "2rem", padding: "1rem" }}
      >
        <Typography variant="h4" align="center">
          PodGen
        </Typography>
      </AppBar>
      <Typography variant="body1" align="center">
        Bienvenu chez PodGen! Générez un podcast à partir de n'importe quelle PDF!
      </Typography>
      <FileUpload />
    </Container>
  );
}

export default App;
