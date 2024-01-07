import { useEffect, useState } from "react";
import axios from "../api/axios";
import "../css/Home.css";
import { Link } from "react-router-dom";

const GET_OPEN_JOBS_URL = "jobs/read-open";

const Home = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(GET_OPEN_JOBS_URL);
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
            <div key={item.id}>
              <Link to={`/job/${item.id}`} style={{ textDecoration: "none" }}>
                <li>
                  <strong>Job Name:</strong> {item.job_name}
                  <br />
                  <strong>Employer:</strong>
                  <Link
                    to={`/user/${item.employer_id}`}
                    style={{ textDecoration: "none" }}
                  >
                    <span className="employer-username">
                      {item.employer.username}
                    </span>
                  </Link>
                  <br />
                  <strong>Pay in Euro:</strong> {item.pay_in_euro}
                  <br />
                  <hr />
                </li>
              </Link>
            </div>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Home;
