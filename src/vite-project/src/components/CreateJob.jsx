import { useRef, useState, useEffect } from "react";
import {
  faCheck,
  faTimes,
  faInfoCircle,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import axios from "../api/axios";
import { Link } from "react-router-dom";
import "../css/CreateJob.css";

const NAME_REGEX = /^[a-zA-Z0-9]{3,30}$/;
const DESCRIPTION_REGEX = /^.{5,400}$/;

const CREATE_URL = "/jobs/create";

const CreateJob = () => {
  const jobRef = useRef();
  const errRef = useRef();

  const [name, setName] = useState("");
  const [validName, setValidName] = useState(false);
  const [nameFocus, setNameFocus] = useState(false);

  const [description, setDescription] = useState("");
  const [validDescription, setValidDescription] = useState(false);
  const [descriptionFocus, setDescriptionFocus] = useState(false);

  const [pay, setPay] = useState(0);
  const [validPay, setValidPay] = useState(false);
  const [payFocus, setPayFocus] = useState(false);

  const [errMsg, setErrMsg] = useState("");
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    jobRef.current.focus();
  }, []);

  useEffect(() => {
    setValidName(NAME_REGEX.test(name));
  }, [name]);

  useEffect(() => {
    setValidDescription(DESCRIPTION_REGEX.test(description));
  }, [description]);

  useEffect(() => {
    setValidPay(pay > 0);
  }, [pay]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    // if button enabled with JS hack
    const v1 = NAME_REGEX.test(name);
    const v2 = DESCRIPTION_REGEX.test(description);
    const v3 = pay > 0;
    if (!v1 || !v2 || !v3) {
      setErrMsg("Invalid Entry");
      return;
    }
    try {
      const response = await axios.post(
        CREATE_URL,
        JSON.stringify({
          employer_id: "TODO: Read from localstorage",
          job_name: name,
          job_desc: description,
          pay_in_euro: pay,
        }),
        {
          headers: { "Content-Type": "application/json" },
          withCredentials: true,
        }
      );
      console.log(JSON.stringify(response?.data));
      setSuccess(true);
      setName("");
      setDescription("");
      setPay(0);
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
          <h1>Create Job</h1>
          <form onSubmit={handleSubmit}>
            {/* EMAIL */}

            <label htmlFor="name">
              Name:
              <FontAwesomeIcon
                icon={faCheck}
                className={validName ? "valid" : "hide"}
              />
              <FontAwesomeIcon
                icon={faTimes}
                className={validName || !name ? "hide" : "invalid"}
              />
            </label>

            <input
              type="text"
              id="name"
              ref={jobRef}
              autoComplete="off"
              onChange={(e) => setName(e.target.value)}
              value={name}
              required
              aria-invalid={validName ? "false" : "true"}
              aria-describedby="uidnote"
              onFocus={() => setNameFocus(true)}
              onBlur={() => setNameFocus(false)}
            />

            <p
              id="uidnote"
              className={
                nameFocus && name && !validName ? "instructions" : "offscreen"
              }
            >
              <FontAwesomeIcon icon={faInfoCircle} />
              Must be valid job name
            </p>

            {/* USERNAME */}
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
            <input
              type="text"
              id="description"
              autoComplete="off"
              onChange={(e) => setDescription(e.target.value)}
              value={description}
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

            <label htmlFor="pay">
              Password:
              <FontAwesomeIcon
                icon={faCheck}
                className={validPay ? "valid" : "hide"}
              />
              <FontAwesomeIcon
                icon={faTimes}
                className={validPay || !pay ? "hide" : "invalid"}
              />
            </label>
            <input
              type="number"
              id="pay"
              onChange={(e) => setPay(e.target.value)}
              value={pay}
              required
              aria-invalid={validPay ? "false" : "true"}
              aria-describedby="pwdnote"
              onFocus={() => setPayFocus(true)}
              onBlur={() => setPayFocus(false)}
            />
            <p
              id="pwdnote"
              className={payFocus && !validPay ? "instructions" : "offscreen"}
            >
              <FontAwesomeIcon icon={faInfoCircle} />
              Must be valid pay
            </p>

            <button
              disabled={
                !validName || !validPay || !validDescription ? true : false
              }
            >
              Create
            </button>
          </form>
          {/* <p>
            Already registered?
            <br />
            <span className="line">
              <Link to="/">Sign In</Link>
            </span>
          </p> */}
        </section>
      )}
    </>
  );
};

export default CreateJob;
