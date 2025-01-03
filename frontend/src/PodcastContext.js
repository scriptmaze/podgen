import React, { createContext, useContext, useState, useEffect } from "react";

const PodcastContext = createContext();

export const PodcastProvider = ({ children }) => {
  const [isProcessing, setIsProcessing] = useState(() => {
    return JSON.parse(localStorage.getItem("isProcessing")) || false;
  });

  const [isGenerated, setIsGenerated] = useState(() => {
    return JSON.parse(localStorage.getItem("isGenerated")) || false;
  });

  const [podcastPath, setPodcastPath] = useState(() => {
    return localStorage.getItem("podcastPath") || null;
  });

  // NEW: State for storing multiple podcasts
  const [podcasts, setPodcasts] = useState([]);

  useEffect(() => {
    localStorage.setItem("isProcessing", JSON.stringify(isProcessing));
    localStorage.setItem("isGenerated", JSON.stringify(isGenerated));
    localStorage.setItem("podcastPath", podcastPath || "");
  }, [isProcessing, isGenerated, podcastPath]);

  const startProcessing = () => {
    setIsProcessing(true);
    setIsGenerated(false);
    setPodcastPath(null);
  };

  const finishProcessing = () => {
    setIsProcessing(false);
    setIsGenerated(true);
  };

  const resetPodcastState = () => {
    setIsProcessing(false);
    setIsGenerated(false);
    setPodcastPath(null);
  };

  return (
    <PodcastContext.Provider
      value={{
        isProcessing,
        isGenerated,
        podcastPath,
        setPodcastPath,
        startProcessing,
        finishProcessing,
        resetPodcastState,
        podcasts, // Expose podcasts
        setPodcasts, // Expose function to update podcasts
      }}
    >
      {children}
    </PodcastContext.Provider>
  );
};

export const usePodcastContext = () => useContext(PodcastContext);
