import { useState, useEffect } from "react";
import api from "../api";
import Prediction from "../components/Prediction";
import "../styles/Home.css";
import { all } from "axios";
import { useNavigate } from "react-router-dom";


function UserPredictions() {
  const [predictions, setPredictions] = useState([]);
  const [filtered_predictions, setFilteredPredictions] = useState([]);
  const [content, setContent] = useState("");
  const [title, setTitle] = useState("");
  const [category, setCategory] = useState("Sports");
  const [filterCategory, setFilterCategory] = useState("All");

  const categoryOptions = ["All", "Sports"];
  const categoryMap = {
    Sports: 0,
  };

  const navigate = useNavigate();

  useEffect(() => {
    getPredictions();
  }, []);

  useEffect(() => {
    filterPredictions();
  }, [filterCategory, predictions]);

  const getPredictions = () => {
    api
      .get("/api/predictions/user/")
      .then((res) => res.data)
      .then((data) => {
        setPredictions(data);
        console.log(data);
      })
      .catch((err) => alert(err));
  };

  const deletePrediction = (id) => {
    api
      .delete(`/api/predictions/delete/${id}/`)
      .then((res) => {
        if (res.status === 204) alert("Prediction deleted!");
        else alert("Failed to delete prediction.");
        getPredictions();
      })
      .catch((error) => alert(error));
  };

  const createPrediction = (e) => {
    e.preventDefault();
    const categoryValue = categoryMap[category];

    console.log({ content, title, category });
    api
      .post("/api/predictions/user/", {
        content,
        title,
        category: categoryValue,
      })
      .then((res) => {
        if (res.status === 201) alert("Prediction created!");
        else alert("Failed to create prediction.");
        getPredictions();
      })
      .catch((err) => alert(err));
  };

  const filterPredictions = () => {
    if (filterCategory === "All") {
      setFilteredPredictions(predictions);
    } else {
      setFilteredPredictions(
        predictions.filter(
          (prediction) =>
            categoryOptions[parseInt(prediction.category) + 1] ===
            filterCategory
        )
      );
    }
  };

  return (
    <div>
      <h2>My Predictions</h2>
      <select
        className="category-select"
        onChange={(e) => setFilterCategory(e.target.value)}
        value={filterCategory}
      >
        {categoryOptions.map((option, index) => (
          <option key={index} value={option}>
            {option}
          </option>
        ))}
      </select>
      {filtered_predictions.map((prediction) => (
        <Prediction
          prediction={prediction}
          onDelete={deletePrediction}
          key={prediction.id}
        />
      ))}
      <h2>Create a Prediction</h2>
      <form onSubmit={createPrediction}>
        <label htmlFor="title">Title:</label>
        <br />
        <input
          type="text"
          id="title"
          name="title"
          required
          onChange={(e) => setTitle(e.target.value)}
          value={title}
        />
        <label htmlFor="title">Category:</label>
        <br />
        <select
          className="category-select"
          name="category"
          id="category"
          required
          onChange={(e) => setCategory(e.target.value)}
          value={category}
        >
          {categoryOptions.slice(1).map((option, index) => (
            <option key={index} value={option}>
              {option}
            </option>
          ))}
        </select>
        <br />
        <label htmlFor="title">Content:</label>
        <br />
        <textarea
          name="content"
          id="content"
          required
          value={content}
          onChange={(e) => setContent(e.target.value)}
        ></textarea>
        <br />
        <input type="submit" value="Submit"></input>
      </form>
    </div>
  );
}

export default UserPredictions;
