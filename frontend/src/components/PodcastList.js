import React from "react";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import CardActions from "@mui/material/CardActions";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";

const PodcastList = ({ podcasts, selectedPodcast, setSelectedPodcast }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {podcasts.length > 0 ? (
        podcasts.map((podcast) => (
          <Card
            key={podcast.id}
            className={`cursor-pointer ${
              selectedPodcast?.id === podcast.id ? "border border-blue-500" : ""
            }`}
          >
            <CardContent
              onClick={() => {
                console.log("Selected Podcast:", podcast); // Debugging
                setSelectedPodcast(podcast);
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
                onClick={() => {
                  console.log("Play Button Clicked:", podcast); // Debugging
                  setSelectedPodcast(podcast); // Set the selected podcast
                }}
              >
                Play
              </Button>
            </CardActions>
          </Card>
        ))
      ) : (
        <p>No podcasts generated yet.</p>
      )}
    </div>
  );
};

export default PodcastList;
