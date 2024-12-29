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
          My Modern Website
        </Typography>
      </AppBar>
      <Typography variant="body1">
        Welcome to my modern React-Django website!
      </Typography>
      <FileUpload />
    </Container>
  );
}

export default App;
