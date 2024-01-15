import Register from "./components/Register";
import Login from "./components/Login";
import Home from "./components/Home";
import Layout from "./components/Layout";
import Missing from "./components/Missing";
import Unauthorized from "./components/Unauthorized";
import Lounge from "./components/Longue";
import RequireAuth from "./components/RequireAuth";
import { Routes, Route } from "react-router-dom";
import Job from "./components/Job";
import User from "./components/User";
import CreateJob from "./components/CreateJob";
import ApplyJob from "./components/ApplyJob";
import WorkerApplications from "./components/WorkerApplications";

const ROLES = {
  Employer: "EMPLOYER",
  Editor: 1984,
  Admin: 5150,
};

function App() {
  return (
    <>
      {/* <Navbar /> */}
      <Routes>
        <Route path="/" element={<Layout />}>
          {/* public routes */}
          <Route path="login" element={<Login />} />
          <Route path="register" element={<Register />} />
          <Route path="unauthorized" element={<Unauthorized />} />
          <Route path="/" element={<Home />} />
          <Route path="/job/:jobId" element={<Job />} />
          <Route path="/user/:username" element={<User />} />
          {/* we want to protect these routes */}

          <Route element={<RequireAuth allowedRoles={["WORKER"]} />}>
            <Route path="/job/apply/:jobId" element={<ApplyJob />} />
            <Route
              path="/worker/applications/:workerId"
              element={<WorkerApplications />}
            />
          </Route>

          <Route element={<RequireAuth allowedRoles={["EMPLOYER"]} />}>
            <Route path="create-job" element={<CreateJob />} />
            <Route
              path="/employer/applications/:employerId"
              element={<WorkerApplications />}
            />
          </Route>

          <Route
            element={
              <RequireAuth allowedRoles={[ROLES.Employer, ROLES.Admin]} />
            }
          >
            <Route path="lounge" element={<Lounge />} />
          </Route>

          {/* catch all */}
          <Route path="*" element={<Missing />} />
        </Route>
      </Routes>
    </>
  );
}

export default App;
