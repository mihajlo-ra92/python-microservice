import { useNavigate, useLocation } from "react-router-dom";
import useAxiosPrivate from "../hooks/useAxiosPrivate";
import useAuth from "../hooks/useAuth";
import { useEffect, useState } from "react";

const Users = () => {
  const [users, setUsers] = useState();
  const axiosPrivate = useAxiosPrivate();
  const navigate = useNavigate();
  const location = useLocation();
  const auth = useAuth();
  console.log(auth);

  useEffect(() => {
    let isMounted = true;
    const controller = new AbortController();
    console.log("users2");

    const getUsers = async () => {
      try {
        console.log("before");
        // const response = await axiosPrivate.get("/users/read-logged-in", {
        //   signal: controller.signal,
        // });
        const response = await axiosPrivate.get("/users/read-logged-in");
        console.log("after");
        console.log(response.data);
        isMounted && setUsers(response.data);
        console.log("users");
        console.log(users);
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
  }, []);

  return (
    <>
      <p>Works well.</p>
      <article>
        <h2>Users List</h2>
        {users?.length ? (
          <ul>
            {users.map((user, i) => (
              <li key={i}>{user?.username}</li>
            ))}
          </ul>
        ) : (
          <p>No users to display</p>
        )}
      </article>
    </>
  );
};

export default Users;
