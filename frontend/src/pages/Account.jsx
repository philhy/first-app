import { useState, useEffect } from "react";
import api from "../api";
import Prediction from "../components/Prediction";
import "../styles/Home.css";
import { all } from "axios";
import { useNavigate } from "react-router-dom";

function Account() {
    const [user, setUser] = useState("");
    const [name, setName] = useState("");

    useEffect(() => {
        getUserInfo();
    }, []);

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

    return (
        <div>
            <h2>Account Info</h2>
            <label htmlFor="title">Name:</label>
            <br />
            <input
            type="text"
            id="name"
            name="name"
            onChange={(e) => setName(e.target.value)}
            value={name}
            />
        </div>
    );
}

export default Account