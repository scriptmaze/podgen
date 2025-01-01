import React, { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone"
import { Upload, X, AlertCircle } from 'lucide-react';
import { Alert, AlertTitle, AlertDescription } from '../components/ui/alert';
import API from "../services/api"; // Axios instance for API requests

function FileUpload() {
  const [isDragging, setIsDragging] = useState(false);
  const [file, setFile] = useState(null); // Store the selected file
  const [message, setMessage] = useState(""); // Display success/error messages
  const [podcastPath, setPodcastPath] = useState(null); // Store the generated podcast path
  const [isProcessing, setIsProcessing] = useState(false); // Track whether a file is being processed
  const [alertVisible, setAlertVisible] = useState(false);
  
  // Handle drag events
  const handleDrag = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setIsDragging(true);
    } else if (e.type === "dragleave") {
      setIsDragging(false);
    }
  }, []);

  // Handle file selection
  const onDrop = (acceptedFiles) => {
    if (isProcessing) {
      // Prevent new uploads during processing
      setMessage("Un fichier est déjà en cours de traitement. Veuillez patienter.");
      setAlertVisible(true);
      return;
    }

    setFile(acceptedFiles[0]); // Set the selected file
    setMessage(""); // Clear any previous messages
  };
  
  const { getRootProps, getInputProps } = useDropzone({
    accept: ".pdf",
    onDrop,
    disabled: isProcessing,
  }); 
  
const removeFile = () => {
    setFile(null);
    setMessage(""); // Clear messages
    setAlertVisible(false);
  };

  // Handle file upload
  const handleUpload = async (event) => {
    event.preventDefault();

    if (!file) {
      setMessage("Veuillez sélectionner un fichier avant de l'uploader.");
      setAlertVisible(true);
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
      setAlertVisible(true);
      setPodcastPath(response.data.podcast_path); // Set the podcast path from the backend
    } catch (error) {
      console.error("Error during file upload:", error);
      setMessage("Il y a eu une erreur quand le fichier s'est fait upload :{");
      setAlertVisible(true);
    } finally {
      setIsProcessing(false); // Reset processing state
    }
  };

  

  return (
    <div className="w-full max-w-2xl mx-auto p-4 space-y-4">
      {/* File Upload Zone */}
      <div
        {...getRootProps()}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        className={`
          w-full p-8 border-2 border-dashed rounded-lg
          flex flex-col items-center justify-center gap-4
          transition-colors duration-200
          ${isDragging ? "border-blue-500 bg-blue-50" : "border-gray-300 bg-gray-50 hover:bg-gray-100"}
        `}
      >
        <Upload size={40} className={isDragging ? "text-blue-500" : "text-gray-400"} />
        <div className="text-center">
          <p className="text-lg font-medium mb-1">
            {file ? file.name : "Glissez-déposez votre fichier PDF ici, ou cliquez pour sélectionner."}
          </p>
          <p className="text-sm text-gray-500">Seuls les fichiers PDF sont acceptés</p>
        </div>
        <input {...getInputProps()} />
      </div>

      {/* File Removal Button */}
      {file && (
        <div className="flex justify-end">
          <button onClick={removeFile} className="p-2 hover:bg-gray-200 rounded-full">
            <X size={20} className="text-gray-500" />
          </button>
        </div>
      )}

      {/* Upload Button */}
      <button
        onClick={handleUpload}
        disabled={isProcessing || !file}
        className={`
          w-full py-2 px-4 rounded-lg font-medium
          transition-colors duration-200
          ${isProcessing || !file ? "bg-gray-100 text-gray-400 cursor-not-allowed" : "bg-blue-500 hover:bg-blue-600 text-white"}
        `}
      >
        {isProcessing ? "Traitement en cours..." : "Uploader"}
      </button>

      {/* Success/Error Message */}
      {/* {message && (
        <p className="text-center text-sm mt-2">
          {message}
        </p>
      )} */}

      {/* Podcast Playback */}
      {podcastPath && (
        <div className="mt-4">
          <h3 className="font-medium">Podcast généré :</h3>
          <audio controls>
            <source src={podcastPath} type="audio/mpeg" />
            Votre navigateur ne supporte pas l'élément audio.
          </audio>
        </div>
      )}

      {/* Error Handling */}
      {alertVisible && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{message}</AlertDescription>
        </Alert>
      )}
    </div>

    // <div align="center">
    //   <h2>Uploader un fichier PDF</h2>
    //   <div {...getRootProps()} style={{ border: "2px dashed #ccc", padding: "20px", width: "300px", textAlign: "center" }}>
    //     <input {...getInputProps()} />
    //     {file ? (
    //       <p>{file.name}</p> // Show the file name if a file is selected
    //     ) : (
    //       <p>Glissez-déposez votre fichier PDF ici, ou cliquez pour sélectionner.</p>
    //     )}
    //   </div>

    //   <button onClick={handleUpload} disabled={isProcessing || !file}>
    //     {isProcessing ? "Traitement en cours..." : "Uploader"}
    //   </button>

    //   {message && <p>{message}</p>}
    //   {podcastPath && (
    //     <div>
    //       <h3>Podcast généré :</h3>
    //       <audio controls>
    //         <source src={podcastPath} type="audio/mpeg" />
    //         Votre navigateur ne supporte pas l'élément audio.
    //       </audio>
    //     </div>
    //   )}
    // </div>
  );
}

export default FileUpload;
