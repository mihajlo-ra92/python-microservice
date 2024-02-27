import { useEffect, useState } from "react";
import axios from "../api/axios";
import "../css/Applications.css";
import { Link, useParams } from "react-router-dom";

const GET_APPLICATIONS_URL = "/applications/read-by-employer-id";
const DECIDE_APPLICATION_URL = "/applications/decide";

const EmployerApplications = () => {
  const [applicationsData, setApplicationsData] = useState([]);
  const [loading, setLoading] = useState(true);
  const { employerId } = useParams();

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log(`${GET_APPLICATIONS_URL}/${employerId}`);
        const responseApplications = await axios.get(
          `${GET_APPLICATIONS_URL}/${employerId}`
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
  }, [employerId]);

  const handleDecide = async (applicationId, decision) => {
    try {
      const response = await axios.post(
        `${DECIDE_APPLICATION_URL}/${applicationId}`,
        JSON.stringify({
          decision,
        }),
        {
          headers: { "Content-Type": "application/json" },
          withCredentials: true,
        }
      );
      console.log(response);
      const updatedResponseApplications = await axios.get(
        `${GET_APPLICATIONS_URL}/${employerId}`
      );
      setApplicationsData(updatedResponseApplications.data);
    } catch (error) {
      console.error("Error accepting application:", error);
    }
  };

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
                    <strong>Pay in Euro:</strong> {item.job.pay_in_euro}
                    <br />
                    {item.status === "PENDING" && (
                      <Link>
                        <button
                          onClick={() => handleDecide(item.id, "APPROVED")}
                        >
                          Accept
                        </button>
                        <button
                          onClick={() => handleDecide(item.id, "REJECTED")}
                        >
                          Reject
                        </button>
                      </Link>
                    )}
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

export default EmployerApplications;
