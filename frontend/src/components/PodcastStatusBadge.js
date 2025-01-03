// components/PodcastStatusBadge.js
import React from "react";
import { usePodcastContext } from "../PodcastContext";

const PodcastStatusBadge = () => {
  const { isProcessing, isGenerated } = usePodcastContext();

  return (
    <div className="fixed bottom-4 right-4">
      {isProcessing && (
        <div className="bg-yellow-400 text-black py-2 px-4 rounded-full shadow-md">
          Podcast is being generated...
        </div>
      )}
      {!isProcessing && isGenerated && (
        <div className="bg-green-500 text-white py-2 px-4 rounded-full shadow-md">
          Podcast generated successfully!
        </div>
      )}
    </div>
  );
};

export default PodcastStatusBadge;
