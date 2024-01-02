import { useNavigate, useLocation } from "react-router-dom";
import useAxiosPrivate from "../hooks/useAxiosPrivate";
import { useEffect, useState } from "react";

const Users = () => {
  const [users, setUsers] = useState();
  const axiosPrivate = useAxiosPrivate();
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    let isMounted = true;
    const controller = new AbortController();

    const getUsers = async () => {
      try {
        // NOTE: For some reason allways aborts request
        // const response = await axiosPrivate.get("/users/read-logged-in", {
        //   signal: controller.signal,
        // });
        const response = await axiosPrivate.get("/users/read-logged-in");
        console.log("res");
        console.log(response.data);
        isMounted && setUsers(response.data);
      } catch (err) {
        console.error(err);
        navigate("/login", { state: { from: location }, replace: true });
      }
    };

    getUsers();

    return () => {
      isMounted = false;
      controller.abort();
    };
  }, [axiosPrivate, location, navigate]);

  return (
    <>
      <p>Works well.</p>
      <article>
        <h2>Users List</h2>
        {users ? (
          <ul>
            <li key={1}>{users?.username}</li>
          </ul>
        ) : (
          <p>No users to display</p>
        )}
      </article>
    </>
  );
};

export default Users;
