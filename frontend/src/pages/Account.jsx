import { useState, useEffect } from "react";
import api from "../api";
import "../styles/Account.css";

function Account() {
    const [user, setUser] = useState("");

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
            <p>{user.first_name} {user.last_name}</p>
            <br />
            <label htmlFor="title">User Name:</label>
            <br />
            <p>{user.username}</p>
            <br />
            <label htmlFor="title">Email:</label>
            <br />
            <p>{user.email}</p>
        </div>
    );
}

export default Account