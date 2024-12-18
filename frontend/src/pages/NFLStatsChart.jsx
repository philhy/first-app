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
  const [selectedTeams, setSelectedTeams] = useState([]);
  const [selectedCategories, setSelectedCategories] = useState([]);
  const [selectedWeek, setSelectedWeek] = useState("");
  const [selectedSeason, setSelectedSeason] = useState("");

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

  const handleTeamChange = (event) => {
    const { selectedOptions } = event.target;

    const selectedValues = Array.from(
      selectedOptions,
      (option) => option.value
    );
    if (selectedValues.includes("All")) {
      setSelectedTeams(["All"]);
    } else {
      setSelectedTeams([...new Set(selectedValues)]);
    }
  };

  const handleCategoryChange = (e) => {
    const { options } = e.target;
    const selected = Array.from(options)
      .filter((option) => option.selected)
      .map((option) => option.value);
    setSelectedCategories(selected);
  };

  const prepareChartData = () => {
    let filteredData;

    if (selectedWeek === "All") {
      filteredData = teamStats
        .filter((item) => (selectedTeams.includes("All") || selectedTeams.includes(item.team)) && Number(item.season) === Number(selectedSeason))
        .reduce((acc, curr) => {
          const teamIndex = acc.findIndex((el) => el.team === curr.team);
          if (teamIndex > -1) {
            selectedCategories.forEach((category) => {
              acc[teamIndex][category] =
                (acc[teamIndex][category] || 0) + Number(curr[category] || 0);
            });
          } else {
            const newEntry = { team: curr.team };
            selectedCategories.forEach((category) => {
              newEntry[category] = Number(curr[category] || 0);
            });
            acc.push(newEntry);
          }
          return acc;
        }, []);
    } else {
      filteredData = teamStats.filter(
        (item) =>
          (selectedTeams.includes("All") ||
            selectedTeams.includes(item.team)) &&
          Number(item.week) === Number(selectedWeek) &&
          Number(item.season) === Number(selectedSeason)
      );
    }

    console.log(filteredData);

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
      hoverBackgroundColor: "rgba(34, 40, 58, 1)",
      hoverBorderColor: "rgba(34, 40, 58, 1)",
    }));

    setChartData({ labels, datasets });
  };

  useEffect(() => {
    if (selectedTeams.length && selectedCategories.length) {
      prepareChartData();
    }
  }, [selectedSeason, selectedWeek, selectedTeams, selectedCategories]);

  const weeks = [...new Set(teamStats.map((item) => item.week))].sort(
    (a, b) => Number(a) - Number(b)
  );
  const seasons = [...new Set(teamStats.map((item) => item.season))];
  const uniqueTeams = [...new Set(teamStats.map((item) => item.team))];

  const excludeKeys = ["team", "id", "season", "week", "record", "game_date"];

  return (
    <div>
      <h2>NFL Team Stats</h2>
      <div>
        <label>Selected Season: </label>
        <br />
        <select
          value={selectedSeason}
          onChange={(e) => setSelectedSeason(e.target.value)}
          style={{ width: "200px", height: "20px" }}
        >
          {seasons.map((season) => (
            <option key={season} value={season}>
              {season}
            </option>
          ))}
        </select>
        <br />
        <label>Selected Week: </label>
        <br />
        <select
          value={selectedWeek}
          onChange={(e) => setSelectedWeek(e.target.value)}
          style={{ width: "200px", height: "20px" }}
        >
          <option value="All">All Weeks</option>
          {weeks.map((week) => (
            <option key={week} value={week}>
              {week}
            </option>
          ))}
        </select>
        <br />
        <label>Selected Team: </label>
        <br />
        <select
          multiple
          value={selectedTeams}
          onChange={handleTeamChange}
          style={{ width: "200px", height: "100px" }}
        >
          <option value="All">All Teams</option>
          {uniqueTeams.map((team) => (
            <option key={team} value={team}>
              {team}
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
        selectedTeams.length === 1 &&
        selectedTeams.includes("All") === false ? (
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
