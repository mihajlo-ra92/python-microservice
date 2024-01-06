import { useEffect, useState } from "react";
import axios from "../api/axios";
import "../css/Home.css";
import { Link } from "react-router-dom";

const GET_JOBS_URL = "jobs/read-all";

const Home = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(GET_JOBS_URL);
        console.log(JSON.stringify(response.data));
        setData(response.data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching data:", error);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="container">
      {loading ? (
        <p>Loading...</p>
      ) : (
        <ul>
          {data.map((item) => (
            <li key={item.id}>
              <Link to={`/job/${item.id}`} style={{ textDecoration: "none" }}>
                <div className="job-details">
                  <div className="text-content">
                    <strong>Job Name:</strong> {item.job_name}
                    <br />
                    <strong>Employer ID:</strong> {item.employer_id}
                    <br />
                    <strong>Worker ID:</strong>{" "}
                    {item.worker_id ? item.worker_id : "N/A"}
                    <br />
                    <strong>Job Description:</strong> {item.job_desc}
                    <br />
                    <strong>Pay in Euro:</strong> {item.pay_in_euro}
                    <br />
                    <strong>Completed:</strong> {item.completed ? "Yes" : "No"}
                    <br />
                  </div>
                  <div className="job-image">
                    <img
                      src={
                        "https://www.offidocs.com/imageswebp/100x100pxicon.jpg.webp"
                      }
                      alt={`Job ${item.id}`}
                    />
                    <hr />
                  </div>
                </div>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Home;
