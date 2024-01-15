import { useEffect, useState } from "react";
import axios from "../api/axios";
import "../css/User.css";
import { Link, useParams } from "react-router-dom";

const GET_USER_URL = "users/read-by-username";
const GET_JOBS_URL = "jobs/read-by-employer-id";

const EmployerApplications = () => {
  const [userData, setUserData] = useState([]);
  const [jobsData, setJobsData] = useState([]);
  const [loading, setLoading] = useState(true);
  const { username } = useParams();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const responseUser = await axios.get(`${GET_USER_URL}/${username}`);
        console.log(JSON.stringify(responseUser.data));
        setUserData(responseUser.data);

        const responseJobs = await axios.get(
          `${GET_JOBS_URL}/${responseUser.data.id}`
        );
        console.log(JSON.stringify(responseJobs.data));
        setJobsData(responseJobs.data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching data:", error);
        setLoading(false);
      }
    };

    fetchData();
  }, [username]);

  return (
    <>
      <h1>{`${
        userData && userData.user_type
          ? userData?.user_type?.charAt(0).toUpperCase() +
            userData?.user_type?.slice(1).toLowerCase() +
            " Details"
          : ""
      } `}</h1>

      <div className="user-container">
        {loading ? (
          <p>Loading...</p>
        ) : (
          <div>
            <p>
              <strong>Username:</strong> {userData.username}
            </p>
            <p>
              <strong>Email:</strong> {userData.email}
            </p>
            {/* <p>
              <strong>User Type:</strong> {userData.user_type}
            </p> */}
          </div>
        )}
      </div>

      {userData.user_type === "EMPLOYER" ? (
        <div className="jobs-container">
          <ul>
            <h1>Jobs</h1>
            {jobsData.map((item) => (
              <div key={item.id}>
                <Link to={`/job/${item.id}`} style={{ textDecoration: "none" }}>
                  <li>
                    <strong>Job Name:</strong> {item.job_name}
                    <br />
                    {/* <strong>Employer:</strong>
                    <Link
                      to={`/user/${item.employer.username}`}
                      style={{ textDecoration: "none" }}
                    >
                      <span className="employer-username">
                        {item.employer.username}
                      </span>
                    </Link>
                    <br /> */}
                    <strong>Pay in Euro:</strong> {item.pay_in_euro}
                    <br />
                    <strong>Completed: </strong>
                    {item.completed ? "Yes" : "No"}
                    <br />
                    <hr />
                  </li>
                </Link>
              </div>
            ))}
          </ul>
        </div>
      ) : userData.user_type === "WORKER" ? (
        <div className="finished-jobs-container">
          <ul>
            <h1>Finished Jobs</h1>
            {jobsData.map((item) => (
              <div key={item.id}>
                <Link to={`/job/${item.id}`} style={{ textDecoration: "none" }}>
                  <li>
                    <strong>Job Name:</strong> {item.job_name}
                    <br />
                    <strong>Employer:</strong>
                    <Link
                      to={`/user/${item.employer.username}`}
                      style={{ textDecoration: "none" }}
                    >
                      <span className="employer-username">
                        {item.employer.username}
                      </span>
                    </Link>
                    <br />
                    <strong>Pay in Euro:</strong> {item.pay_in_euro}
                    <br />
                    <strong>Completed: </strong>
                    {item.completed ? "Yes" : "No"}
                    <br />
                    <hr />
                  </li>
                </Link>
              </div>
            ))}
          </ul>
        </div>
      ) : (
        <h2>Admin data is private</h2>
      )}
    </>
  );
};

export default EmployerApplications;
