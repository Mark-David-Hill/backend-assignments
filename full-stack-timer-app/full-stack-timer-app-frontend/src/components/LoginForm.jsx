import { useState } from "react";
import fetchWrapper from "../lib/apiCall";

const LoginForm = ({ setIsUpdatingTimer }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSetEmail = (event) => {
    setEmail(event.target.value);
  };

  const handleSetPassword = (event) => {
    setPassword(event.target.value);
  };

  const handleLogin = () => {
    setIsUpdatingTimer(true);

    const body = {
      email: email,
      password: password,
    };

    // if (email && password) {
    //   fetchWrapper
    //     .apiCall(`/timer`, "POST", body)
    //     .then(() => setIsUpdatingTimer(false))
    //     .catch((error) => console.error("couldn't login", error));
    // }
  };

  return (
    <div className="login">
      <input type="text" placeholder="Email" onChange={handleSetEmail} />
      <input type="text" placeholder="Password" onChange={handleSetPassword} />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
};

export default LoginForm;
