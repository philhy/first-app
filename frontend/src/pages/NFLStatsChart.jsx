import React, { useState, useEffect } from "react";
import api from "../api";
import { Line, Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const NFLStatsChart = () => {
  const [teamStats, setTeamStats] = useState([]);
  const [chartData, setChartData] = useState({});
  const [selectedTeams, setSelectedTeams] = useState("");
  const [selectedCategories, setSelectedCategories] = useState("");

  useEffect(() => {
    fetchNFLData();
  }, []);

  const fetchNFLData = () => {
    api
      .get("/stats/nfl/team")
      .then((res) => {
        setTeamStats(res.data);
      })
      .catch((err) => {
        console.error(err);
        alert("Failed to fetch NFL data");
      });
  };

  const handleTeamChange = (e) => {
    const { options } = e.target;
    const selected = Array.from(options)
      .filter((option) => option.selected)
      .map((option) => option.value);
    setSelectedTeams(selected);
  };

  const handleCategoryChange = (e) => {
    const { options } = e.target;
    const selected = Array.from(options)
      .filter((option) => option.selected)
      .map((option) => option.value);
    setSelectedCategories(selected);
  };

  const prepareChartData = () => {
    const filteredData = teamStats.filter((item) =>
      selectedTeams.includes(item.team)
    );

    const labels = filteredData.map((item) => item.team);

    const colorPalette = [
        "rgb(75, 192, 192)",
        "rgb(255, 99, 132)",
        "rgb(153, 102, 255)",
        "rgb(255, 159, 64)",
        "rgb(54, 162, 235)",
        "rgb(255, 205, 86)",
      ];

    const datasets = selectedCategories.map((category, index) => ({
      label: category.replace("_", " ").toUpperCase(),
      data: filteredData.map((item) => item[category]),
      borderColor: colorPalette[index % colorPalette.length],
      backgroundColor: colorPalette[index % colorPalette.length],
      borderWidth: 1,
      tension: 0.25,
      fill: selectedCategories.length === 1,
      barThickness: 30,
      hoverBackgroundColor: "rgba(75, 192, 192, 1)",
    }));

    setChartData({ labels, datasets });
  };

  useEffect(() => {
    if (selectedTeams.length && selectedCategories.length) {
      prepareChartData();
    }
  }, [selectedTeams, selectedCategories]);

  const excludeKeys = ["team", "id", "season", "week", "record"]

  return (
    <div>
      <h2>NFL Team Stats</h2>
      <div>
        <label>Selected Team: </label>
        <br />
        <select
          multiple
          value={selectedTeams}
          onChange={handleTeamChange}
          style={{ width: "200px", height: "100px" }}
        >
          {teamStats.map((team) => (
            <option key={team.team} value={team.team}>
              {team.team}
            </option>
          ))}
        </select>
      </div>
      <div>
        <label>Selected Category: </label>
        <br />
        <select
          multiple
          value={selectedCategories}
          onChange={handleCategoryChange}
          style={{ width: "200px", height: "100px" }}
        >
          {teamStats.length > 0 &&
            Object.keys(teamStats[0])
              .filter((key) => !excludeKeys.includes(key))
              .map((category) => (
                <option key={category} value={category}>
                  {category.replace("_", " ").toUpperCase()}
                </option>
              ))}
        </select>
      </div>
      {chartData && chartData.labels && chartData.datasets.length > 0 ? (
        selectedTeams.length === 1 ? (
          <Bar data={chartData} />
        ) : (
          <Line data={chartData} />
        )
      ) : (
        <p>Please select a category to display in the chart.</p>
      )}
    </div>
  );
};

export default NFLStatsChart;
