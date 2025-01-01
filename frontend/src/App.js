import React from "react";
import "./styling/App.scss";

import Header from "./components/Header";
import FileUpload from "./components/FileUpload";

import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <div className="App">
      <Header />
      <div className="container">
        <div className="wrapper">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/features" element={<Features />} />
            <Route path="/how-it-works" element={<HowItWorks />} />
            <Route path="/contact-us" element={<Contact />} />
            <Route path="/file-upload" element={<FileUploadPage />} />
          </Routes>
        </div>
      </div>
    </div>
  );
}

function Home() {
  return (
    <div className="container">
      <div className="wrapper">
        <h5>
          Welcome to <b>PodGen</b>, a creative platform to generate podcasts
          from any PDF!
        </h5>
        <p>Click below to try our file upload service:</p>
        <a href="/file-upload" className="btn">
          Upload a PDF
        </a>
      </div>
    </div>
  );
}

function Features() {
  return (
    <div className="container">
      <div className="wrapper">
        <h2>Discover PodGen's Powerful Features</h2>
        <ul>
          <li>
            Transform your PDFs into engaging podcasts with just a few clicks.
          </li>
          <li>
            Customize voice settings to suit your preferences: choose tones,
            accents, and languages.
          </li>
          <li>
            Automatically generate chapter-based podcast episodes for better
            content navigation.
          </li>
          <li>
            Enhance your podcast with AI-driven summaries, intros, and
            transitions.
          </li>
          <li>Seamlessly share your podcasts on all major platforms.</li>
        </ul>
      </div>
    </div>
  );
}

function HowItWorks() {
  return (
    <div className="container">
      <div className="wrapper">
        <h2>How PodGen Works</h2>
        <ol>
          <li>
            <b>Upload Your PDF:</b> Upload any PDF file—reports, eBooks, study
            materials, or scripts.
          </li>
          <li>
            <b>AI-Driven Conversion:</b> Our AI processes your document and
            converts it into a podcast, complete with natural-sounding
            narration.
          </li>
          <li>
            <b>Customize Your Podcast:</b> Choose narration style, speed, and
            language to match your target audience.
          </li>
          <li>
            <b>Download and Share:</b> Download your podcast in your preferred
            format and share it with your network.
          </li>
        </ol>
      </div>
    </div>
  );
}

function Contact() {
  return (
    <div className="container">
      <div className="wrapper">
        <h2>Contact Us</h2>
        <p>
          Have questions? Feel free to reach out to us via email or our contact
          form.
        </p>
      </div>
    </div>
  );
}

function FileUploadPage() {
  return (
    <div className="container">
      <div className="wrapper">
        <FileUpload />
      </div>
    </div>
  );
}

export default App;
