import { useRef, useState, useEffect } from "react";
import {
  faCheck,
  faTimes,
  faInfoCircle,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import axios from "../api/axios";
import { Link, useNavigate, useParams } from "react-router-dom";
import "../css/CreateJob.css";
import { jwtDecode } from "jwt-decode";

const DESCRIPTION_REGEX = /^.{5,400}$/;

const APPLY_URL = "/applications/create";

const ApplyJob = () => {
  const navigate = useNavigate();
  const jobRef = useRef();
  const errRef = useRef();

  const [description, setDescription] = useState("");
  const [validDescription, setValidDescription] = useState(false);
  const [descriptionFocus, setDescriptionFocus] = useState(false);

  const [errMsg, setErrMsg] = useState("");
  const [success, setSuccess] = useState(false);

  const token = localStorage.getItem("token");
  const decodedToken = token ? jwtDecode(token) : null;

  const { jobId } = useParams();

  useEffect(() => {
    jobRef.current.focus();
  }, []);

  useEffect(() => {
    setValidDescription(DESCRIPTION_REGEX.test(description));
  }, [description]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!DESCRIPTION_REGEX.test(description)) {
      setErrMsg("Invalid Entry");
      return;
    }
    try {
      const response = await axios.post(
        APPLY_URL,
        JSON.stringify({
          job_id: jobId,
          worker_id: decodedToken.user_id,
          description: description,
        }),
        {
          headers: { "Content-Type": "application/json" },
          withCredentials: true,
        }
      );
      console.log(response);
      setSuccess(true);
      setDescription("");
      navigate("/");
    } catch (err) {
      console.log(err.response.data.message);
      if (err.response.data.message) {
        console.log(
          err.response.data.message.split(",").slice(1).join("").slice(2, -2)
        );
        setErrMsg(
          err.response.data.message.split(",").slice(1).join("").slice(2, -2)
        );
      } else {
        setErrMsg("No Server Response");
      }
      errRef.current.focus();
    }
  };

  return (
    <>
      {success ? (
        <section>
          <h1>Success!</h1>
          <p>
            <a href="#">Sign In</a>
          </p>
        </section>
      ) : (
        <section>
          <p
            ref={errRef}
            className={errMsg ? "errmsg" : "offscreen"}
            aria-live="assertive"
          >
            {errMsg}
          </p>
          <h1>Apply to Job</h1>
          <form onSubmit={handleSubmit}>
            {/* DESCRIPTION */}
            <label htmlFor="description">
              Description:
              <FontAwesomeIcon
                icon={faCheck}
                className={validDescription ? "valid" : "hide"}
              />
              <FontAwesomeIcon
                icon={faTimes}
                className={
                  validDescription || !description ? "hide" : "invalid"
                }
              />
            </label>
            <textarea
              id="description"
              ref={jobRef}
              autoComplete="off"
              onChange={(e) => setDescription(e.target.value)}
              value={description}
              rows={10}
              required
              aria-invalid={validDescription ? "false" : "true"}
              aria-describedby="uidnote"
              onFocus={() => setDescriptionFocus(true)}
              onBlur={() => setDescriptionFocus(false)}
            />
            <p
              id="uidnote"
              className={
                descriptionFocus && description && !validDescription
                  ? "instructions"
                  : "offscreen"
              }
            >
              <FontAwesomeIcon icon={faInfoCircle} />
              Must be valid description
            </p>

            <button disabled={!validDescription ? true : false}>Apply</button>
          </form>
        </section>
      )}
    </>
  );
};

export default ApplyJob;
