import React, { useState, useEffect, useRef } from "react";
import { useDropzone } from "react-dropzone";
import { Upload, AlertCircle } from "lucide-react";
import { Alert, AlertTitle, AlertDescription } from "./ui/alert";
import { usePodcastContext } from "../PodcastContext"; // Import the context
import API from "../services/api";

import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import CardActions from "@mui/material/CardActions";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";

function FileUpload() {
  const [isDragging] = useState(false);
  const [file, setFile] = useState(null); // Store the selected file
  const [message, setMessage] = useState(""); // Display success/error messages
  const [alert, setAlert] = useState("");
  const [loadingText, setLoadingText] = useState("Processing...");
  const [podcasts, setPodcasts] = useState([]); // List of podcasts
  const [selectedPodcast, setSelectedPodcast] = useState(null); // Currently selected podcast

  const {
    setPodcastPath,
    isProcessing,
    startProcessing,
    finishProcessing,
    resetPodcastState,
  } = usePodcastContext(); // Access shared podcast state and processing functions

  const audioRef = useRef(null); // Ref for the audio player

  useEffect(() => {
    const fetchPodcasts = async () => {
      try {
        const response = await API.get("/api/podcasts/");
        console.log("Fetched Podcasts:", response.data.podcasts); // Debugging API response
        setPodcasts(response.data.podcasts);

        // Set the first podcast as the default if no podcast is already selected
        if (response.data.podcasts.length > 0 && !selectedPodcast) {
          setSelectedPodcast(response.data.podcasts[0]);
        }
      } catch (error) {
        console.error("Error fetching podcasts:", error);
      }
    };

    fetchPodcasts();
  }, []); // Fetch podcasts once when the component mounts

  // Animated "Processing..." text
  useEffect(() => {
    const interval = setInterval(() => {
      setLoadingText((prevText) => {
        // Add a dot or reset when it reaches 3 dots
        if (prevText.length === 13) {
          return "Processing"; // Reset to the original text
        }
        return prevText + "."; // Add a dot
      });
    }, 500); // Update every 500ms (change the interval to suit your needs)

    return () => clearInterval(interval); // Clean up the interval when the component unmounts
  }, []);
  
  // Handle file selection
  const onDrop = (acceptedFiles) => {
    if (isProcessing) {
      // Prevent new uploads during processing
      setMessage("A file is currently being processed. Please wait.");
      setAlert("Error");
      return;
    }

    // Reset file state and error message
    setFile(null);
    setMessage("");
    setAlert(null);

    // Filter out invalid files
    const validFiles = acceptedFiles.filter((file) => {
      const isPDF =
        file.type === "application/pdf" || file.name.endsWith(".pdf");
      if (!isPDF) {
        console.warn(`Skipped "${file.name}" because it is not a valid PDF.`);
      }
      return isPDF;
    });

    if (validFiles.length === 0) {
      setMessage("Please upload a valid PDF file.");
      setAlert("Error");
      return;
    }

    setFile(validFiles[0]); // Use the first valid file
  };

  // const removeFile = () => {
  //   setFile(null);
  //   setMessage("");
  //   setAlert(null);
  // };
  
  const { getRootProps, getInputProps } = useDropzone({
    accept: ".pdf",
    onDrop: (acceptedFiles) => setFile(acceptedFiles[0]),
    disabled: isProcessing,
  });

  const fetchPodcasts = async () => {
    try {
      const response = await API.get("/api/podcasts/"); // Fetch podcasts
      setPodcasts(response.data.podcasts);
      if (response.data.podcasts.length > 0 && !selectedPodcast) {
        setSelectedPodcast(response.data.podcasts[0]);
      }
    } catch (error) {
      console.error("Error fetching podcasts:", error);
      setPodcasts([]); // Clear podcasts on failure
    }
  };

  const handlePlayPodcast = (podcast) => {
    setSelectedPodcast(podcast); // Set the selected podcast
    if (audioRef.current) {
      audioRef.current.load(); // Reload the audio element
      audioRef.current.play(); // Programmatically play the audio
    }
  };

  const handleUpload = async (event) => {
    event.preventDefault();

    if (!file) {
      setMessage("Please select a file before uploading.");
      setAlert("Error");
      return;
    }

    resetPodcastState(); // Reset previous state
    startProcessing(); // Begin processing

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await API.post("/upload-pdf/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      if (response.data.podcast_path) {
        setMessage(response.data.message);
        setPodcastPath(response.data.podcast_path);
        finishProcessing();
        fetchPodcasts(); // Re-fetch podcasts after upload
      } else {
        throw new Error("Podcast path not found in the response.");
      }
    } catch (error) {
      console.error("Error during file upload:", error);
      setMessage("An error occurred during the file upload.");
      setAlert("Error");
    } finally {
      resetPodcastState(); // Always reset the state in the end
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-4 space-y-4">
      {/* File Upload Zone */}
      <div
        {...getRootProps()}
        className={`w-full p-8 border-2 border-dashed rounded-lg flex flex-col items-center justify-center gap-4 transition-colors duration-200 ${
          isProcessing
            ? "cursor-not-allowed bg-gray-200"
            : "hover:bg-gray-100 border-gray-300 bg-gray-50"
        }`}
      >
        <Upload size={40} className={isDragging ? "text-blue-500" : "text-gray-400"} />
        <div className="text-center">
          <p className="text-lg font-medium mb-1">
            {file ? file.name : "Drag and drop your PDF file here, or click to select."}
          </p>
          <p className="text-sm text-gray-500">Only PDF files are accepted.</p>
        </div>
        <input {...getInputProps()} />
      </div>

      {/* Upload Button */}
      <button
        onClick={handleUpload}
        disabled={isProcessing || !file}
        className={`w-full py-2 px-4 rounded-lg font-medium transition-colors duration-200 ${isProcessing || !file ? "bg-gray-100 text-gray-400 cursor-not-allowed" : "bg-blue-500 hover:bg-blue-600 text-white"}`}
      >
        {isProcessing ? loadingText : "Upload"}
      </button>

      {/* Error Handling */}
      {alert && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>{alert}</AlertTitle>
          <AlertDescription>{message}</AlertDescription>
        </Alert>
      )}

      {/* Selected Podcast Player */}
      {selectedPodcast && (
        <div className="mt-6 p-4 bg-white rounded-lg shadow-md">
          <h3 className="font-bold text-lg mb-2">
            {selectedPodcast.file_name}
          </h3>
          <audio ref={audioRef} controls className="w-full">
            <source
              src={`${selectedPodcast.podcast_path}`}
              type="audio/mpeg"
            />
            Your browser does not support the audio element.
          </audio>
        </div>
      )}

      {/* Podcast List */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
        {podcasts.map((podcast) => (
          <Card key={podcast.id} className="cursor-pointer">
            <CardContent
              onClick={() => {
                console.log("Selected Podcast:", podcast); // Debugging
                handlePlayPodcast(podcast);
              }}
            >
              <Typography variant="h6" component="div">
                {podcast.file_name}
              </Typography>
              <Typography color="textSecondary">
                {new Date(podcast.created_at).toLocaleDateString()}
              </Typography>
            </CardContent>
            <CardActions>
              <Button
                size="small"
                color="primary"
                onClick={() => handlePlayPodcast(podcast)}
              >
                Play
              </Button>
            </CardActions>
          </Card>
        ))}
      </div>
    </div>
  );
}

export default FileUpload;
