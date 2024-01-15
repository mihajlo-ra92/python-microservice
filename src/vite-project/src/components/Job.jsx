import { useEffect, useState } from "react";
import axios from "../api/axios";
import "../css/Job.css";
import { Link, useParams } from "react-router-dom";
import { jwtDecode } from "jwt-decode";

const GET_JOB_URL = "jobs/read-by-id";

const Job = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userType, setUserType] = useState("");
  const { jobId } = useParams();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`${GET_JOB_URL}/${jobId}`);
        console.log(JSON.stringify(response.data));
        setData(response.data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching data:", error);
        setLoading(false);
      }
    };

    fetchData();
    const token = localStorage.getItem("token");
    if (token) {
      setIsAuthenticated(true);
      const decodedToken = jwtDecode(token);
      setUserType(decodedToken.user_type);
    }
  }, [jobId]);

  return (
    <div className="job_container">
      {loading ? (
        <p>Loading...</p>
      ) : (
        <div>
          <h1>{data.job_name}</h1>
          <Link
            to={`/user/${data.employer.username}`}
            style={{ textDecoration: "none" }}
          >
            <p>
              Employer:{" "}
              <span className="employer-username">
                {data.employer.username}
              </span>
            </p>
          </Link>
          <p>
            Job Description:<br></br> {data.job_desc}
          </p>
          <p>Pay in Euro: {data.pay_in_euro}</p>
          <p>Completed: {data.completed ? "Yes" : "No"}</p>
          <Link to={`/job/apply/${jobId}`}>
            <button
              className="apply-button"
              disabled={!isAuthenticated || userType !== "WORKER"}
            >
              Apply to Job
              {isAuthenticated && ["EMPLOYER", "ADMIN"].includes(userType) && (
                <span className="tooltip-text">
                  Only workers can apply to jobs
                </span>
              )}
              {!isAuthenticated && (
                <span className="tooltip-text">Log in to apply</span>
              )}
            </button>
          </Link>
        </div>
      )}
    </div>
  );
};

export default Job;
