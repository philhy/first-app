import { useState, useEffect } from "react";
import api from "../api";
import Prediction from "../components/Prediction";
import "../styles/Home.css";
import { all } from "axios";
import { useNavigate } from "react-router-dom";

function Home() {
  const [all_predictions, setAllPredictions] = useState([]);
  const [filtered_predictions, setFilteredPredictions] = useState([]);
  const [filterCategory, setFilterCategory] = useState("All");
  const [user, setUser] = useState("");

  const categoryOptions = ["All", "Sports"];
  const navigate = useNavigate();

  useEffect(() => {
    getUserInfo();
    getAllPredictions();
  }, []);

  useEffect(() => {
    filterPredictions();
  }, [filterCategory, all_predictions]);

  const getUserInfo = () => {
    api
      .get("/api/user-info/")
      .then((res) => {
        setUser(res.data);
      })
      .catch((err) => {
        console.error(err);
        alert("Failed to fetch user info.");
      });
  };

  const getAllPredictions = () => {
    api
      .get("/api/predictions/all/")
      .then((res) => res.data)
      .then((data) => {
        setAllPredictions(data);
        console.log(data);
      })
      .catch((err) => alert(err));
  };

  const filterPredictions = () => {
    if (filterCategory === "All") {
      setFilteredPredictions(all_predictions);
    } else {
      setFilteredPredictions(
        all_predictions.filter(
          (prediction) =>
            categoryOptions[parseInt(prediction.category) + 1] ===
            filterCategory
        )
      );
    }
  };

  return (
    <div>
      <div>
        <h2>Welcome, {user.first_name || "Guest"}!</h2>
        <h2>All Predictions</h2>
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
            canDelete={false}
            key={prediction.id}
            category={prediction.category}
          />
        ))}
      </div>
    </div>
  );
}

export default Home;
