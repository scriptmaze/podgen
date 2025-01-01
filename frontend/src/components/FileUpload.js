import React, { useState, useEffect, useCallback } from "react";
import { useDropzone } from "react-dropzone"
import { Upload, X, AlertCircle } from 'lucide-react';
import { Alert, AlertTitle, AlertDescription } from '../components/ui/alert';
import { FaPlayCircle } from 'react-icons/fa';
import API from "../services/api"; // Axios instance for API requests

function FileUpload() {
  const [isDragging, setIsDragging] = useState(false);
  const [file, setFile] = useState(null); // Store the selected file
  const [message, setMessage] = useState(""); // Display success/error messages
  const [podcastPath, setPodcastPath] = useState(null); // Store the generated podcast path
  const [isProcessing, setIsProcessing] = useState(false); // Track whether a file is being processed
  const [alert, setAlert] = useState("");
  const [loadingText, setLoadingText] = useState("Traitement en cours");


  useEffect(() => {
    const interval = setInterval(() => {
      setLoadingText((prevText) => {
        // Add a dot or reset when it reaches 3 dots
        if (prevText.length === 23) {
          return "Traitement en cours"; // Reset to the original text
        }
        return prevText + "."; // Add a dot
      });
    }, 500); // Update every 500ms (change the interval to suit your needs)

    return () => clearInterval(interval); // Clean up the interval when the component unmounts
  }, []);
  
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
      setAlert("Error");
      // setAlertVisible(true);
      return;
    }

    setFile(acceptedFiles[0]); // Set the selected file
    setMessage(""); // Clear any previous messages
    setAlert(null);
  };
  
  const { getRootProps, getInputProps } = useDropzone({
    accept: ".pdf",
    onDrop,
    disabled: isProcessing,
  }); 
  
const removeFile = () => {
    setFile(null);
    setMessage(""); // Clear messages
    setAlert(null);
  };

  // Handle file upload
  const handleUpload = async (event) => {
    event.preventDefault();

    if (!file) {
      setMessage("Veuillez sélectionner un fichier avant de l'uploader.");
      setAlert("Error")
      return;
    }

    // setIsProcessing(true);
    // await setTimeout(() => {
    //   setPodcastPath("http://127.0.0.1:8000/media/podcast_output_folder/GoogleTTS/full_audio_output/podcast.mp3");
    //   setIsProcessing(false);
    //   }, 5000)

    // Clear previous podcast and show loading message
    setPodcastPath(null);
    setIsProcessing(true); // Set processing state to true

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await API.post("/upload-pdf/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      // On successful upload
      setMessage(response.data.message); // Display success message
      setAlert("Success");
      setPodcastPath(response.data.podcast_path); // Set the podcast path from the backend
      console.log(response.data.podcast_path)
    } catch (error) {
      console.error("Error during file upload:", error);
      setMessage("Il y a eu une erreur quand le fichier s'est fait upload :{");
      setAlert("Error");
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
      {/* {file && (
        <div className="flex justify-end">
          <button onClick={removeFile} className="p-2 hover:bg-gray-200 rounded-full">
            <X size={20} className="text-gray-500" />
          </button>
        </div>
      )} */}

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
        {isProcessing ? loadingText : "Upload"}
      </button>

      {/* Success/Error Message */}
      {/* {message && (
        <p className="text-center text-sm mt-2">
          {message}
        </p>
      )} */}

      {/* Podcast Playback */}
      {podcastPath && (
        <div className="mt-4 p-4 bg-white rounded-lg shadow-md">
          <h3 className="font-medium text-lg text-gray-700 mb-2">Podcast generated :</h3>
          <div className="flex items-center space-x-4">
            <audio controls className="w-full">
              <source src={podcastPath} type="audio/mpeg" />
              Votre navigateur ne supporte pas l'élément audio.
            </audio>
          </div>
        </div>
      )}

      {/* Error Handling */}
      {alert && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>{alert}</AlertTitle>
          <AlertDescription>{message}</AlertDescription>
        </Alert>
      )}

    </div>
  );
}

export default FileUpload;
