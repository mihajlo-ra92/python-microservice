import Register from "./components/Register";
import Login from "./components/Login";
import Home from "./components/Home";
import Layout from "./components/Layout";
import Editor from "./components/Editor";
import Admin from "./components/Admin";
import Missing from "./components/Missing";
import Unauthorized from "./components/Unauthorized";
import Lounge from "./components/Longue";
import LinkPage from "./components/LinkPage";
import RequireAuth from "./components/RequireAuth";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Job from "./components/Job";
import User from "./components/User";
import CreateJob from "./components/CreateJob";

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
          <Route path="linkpage" element={<LinkPage />} />
          <Route path="unauthorized" element={<Unauthorized />} />
          <Route path="/" element={<Home />} />
          <Route path="/job/:jobId" element={<Job />} />
          <Route path="/user/:username" element={<User />} />
          <Route path="create-job" element={<CreateJob />} />
          {/* we want to protect these routes */}

          <Route element={<RequireAuth allowedRoles={[ROLES.Employer]} />}>
            <Route path="editor" element={<Editor />} />
          </Route>

          <Route element={<RequireAuth allowedRoles={[ROLES.Employer]} />}>
            <Route path="admin" element={<Admin />} />
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
