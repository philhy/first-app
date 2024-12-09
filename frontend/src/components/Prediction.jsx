import React from "react";
import "../styles/Prediction.css";

function Prediction({ prediction, onDelete, canDelete=true }) {
  const formattedDate = new Date(prediction.created_at).toLocaleDateString(
    "en-US"
  );

  return (
    <div className="prediction-container">
      <p className="prediction-title">{prediction.author_username}</p>
      <p className="prediction-title">{prediction.title}</p>
      <p className="prediction-content">{prediction.content}</p>
      <p className="prediction-date">{formattedDate}</p>
      {canDelete && (
        <button
          className="delete-button"
          onClick={() => onDelete(prediction.id)}
        >
          Delete
        </button>
      )}
    </div>
  );
}

export default Prediction;
