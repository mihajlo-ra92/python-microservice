import { useEffect, useState } from "react";
import axios from "../api/axios";
import "../css/Applications.css";
import { Link, useParams } from "react-router-dom";

const GET_APPLICATIONS_URL = "/applications/read-by-worker-id";

const WorkerApplications = () => {
  const [applicationsData, setApplicationsData] = useState([]);
  const [loading, setLoading] = useState(true);
  const { workerId } = useParams();
  console.log("worker");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const responseApplications = await axios.get(
          `${GET_APPLICATIONS_URL}/${workerId}`
        );
        console.log(JSON.stringify(responseApplications.data));
        setApplicationsData(responseApplications.data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching data:", error);
        setLoading(false);
      }
    };

    fetchData();
  }, [workerId]);

  return (
    <>
      <div className="applications-container">
        {loading ? (
          <p>Loading...</p>
        ) : (
          <ul>
            {applicationsData.map((item) => (
              <div key={item.id}>
                <Link
                  to={`/job/${item.job_id}`}
                  style={{ textDecoration: "none" }}
                >
                  <li>
                    <strong>Application Status:</strong>
                    {item.status}
                    <br />
                    <strong>Description:</strong>
                    {item.description}
                    <br />
                    <strong>Job:</strong> {item.job.job_name}
                    <br />
                    <strong>Employer:</strong>
                    <Link
                      to={`/user/${item.job.employer.username}`}
                      style={{ textDecoration: "none" }}
                    >
                      <span className="employer-username">
                        {item.job.employer.username}
                      </span>
                    </Link>
                    <br />
                    <strong>Pay in Euro:</strong> {item.job.pay_in_euro}
                    <br />
                    <strong>Completed: </strong>
                    {item.job.completed ? "Yes" : "No"}
                    <br />
                    <hr />
                  </li>
                </Link>
              </div>
            ))}
          </ul>
        )}
      </div>
    </>
  );
};

export default WorkerApplications;
