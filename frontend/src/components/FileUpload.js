import React, { useState } from "react";
import API from "../services/api"; // Axios instance for API requests

function FileUpload() {
  const [file, setFile] = useState(null); // Store the selected file
  const [message, setMessage] = useState(""); // Display success/error messages
  const [podcastPath, setPodcastPath] = useState(null); // Store the generated podcast path
  const [isProcessing, setIsProcessing] = useState(false); // Track whether a file is being processed

  // Handle file selection
  const handleFileChange = (event) => {
    if (isProcessing) {
      // Prevent new uploads during processing
      setMessage(
        "Un fichier est déjà en cours de traitement. Veuillez patienter."
      );
      return;
    }

    setFile(event.target.files[0]); // Set the selected file
    setMessage(""); // Clear any previous messages
  };

  // Handle file upload
  const handleUpload = async (event) => {
    event.preventDefault();

    if (!file) {
      setMessage("Veuillez sélectionner un fichier avant de l'uploader.");
      return;
    }

    // Clear previous podcast and show loading message
    setPodcastPath(null);
    setMessage("Traitement du fichier en cours...");
    setIsProcessing(true); // Set processing state to true

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await API.post("/upload-pdf/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      // On successful upload
      setMessage(response.data.message); // Display success message
      setPodcastPath(response.data.podcast_path); // Set the podcast path from the backend
    } catch (error) {
      console.error("Error during file upload:", error);
      setMessage("Il y a eu une erreur quand le fichier s'est fait upload :{");
    } finally {
      setIsProcessing(false); // Reset processing state
    }
  };

  return (
    <div align="center">
      <h2>Uploader un fichier PDF</h2>
      <form onSubmit={handleUpload}>
        <input
          type="file"
          accept="application/pdf"
          onChange={handleFileChange}
          disabled={isProcessing} // Disable file input during processing
        />
        <button type="submit" disabled={isProcessing}>
          {isProcessing ? "Traitement en cours..." : "Uploader"}
        </button>
      </form>
      {message && <p>{message}</p>}
      {podcastPath && (
        <div>
          <h3>Podcast généré :</h3>
          <audio controls>
            <source src={podcastPath} type="audio/mpeg" />
            Votre navigateur ne supporte pas l'élément audio.
          </audio>
        </div>
      )}
    </div>
  );
}

export default FileUpload;
