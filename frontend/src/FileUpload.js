import React, { useState } from "react"; 
import API from "./services/api"; // import d'une instance axios qui gére requêtes

function FileUpload() {
  const [file, setFile] = useState(null); // État pour stocker le fichier sélectionné
  const [message, setMessage] = useState(""); // État pour afficher un message (succès ou erreur)

  // Gère sélection d'un fichier par l'utilisateur
  const handleFileChange = (event) => {
    setFile(event.target.files[0]); // Stocke le fichier sélectionné dans l'état
  };

  // Gère envoi du fichier au backend
  const handleUpload = async (event) => {
    event.preventDefault(); // Empêche rechargement de la page pendant upload

    if (!file) {
      setMessage("Veuillez sélectionner un fichier avant de l'uploader."); // Message d'erreur si aucun fichier
      return;
    }

    const formData = new FormData(); // créer objet form pour accepté fichier
    formData.append("file", file); 

    try {
      const response = await API.post("/upload-pdf/", formData, {
        headers: { "Content-Type": "multipart/form-data" }, 
      });
      setMessage(response.data.message); // affiche message de succès retourné par le backend
    } catch (error) {
      console.error("Erreur lors de l'upload   :[   :", error); 
      setMessage("Il y a eu une erreur quand le fichier s'est fait upload :{"); 
    }
  };

  return (
    <div>
      <h1>Uploader un fichier PDF</h1>
      <form onSubmit={handleUpload}>
        <input
          type="file"
          accept="application/pdf" // prend slm des pdf de l'utilisateur 
          onChange={handleFileChange} // utilise handlefilechange quand utilisateur a selectionné fichier
        />
        <button type="submit">Uploader</button>
      </form>
      {message && <p>{message}</p>} {/* Affiche un message si présent */}
    </div>
  );
}

export default FileUpload;
