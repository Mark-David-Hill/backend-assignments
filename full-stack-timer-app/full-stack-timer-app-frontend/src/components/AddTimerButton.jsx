import { useState } from "react";
import fetchWrapper from "../lib/apiCall";

const AddTimerButton = ({ setIsAddingTimer }) => {
  const [timerName, setTimerName] = useState("");

  const handleSetTimerName = (event) => {
    setTimerName(event.target.value);
  };

  const handleAddTimer = () => {
    setIsAddingTimer(true);

    const body = {
      name: timerName,
    };

    if (timerName) {
      fetchWrapper
        .apiCall(`/timer`, "POST", body)
        .then(() => setIsAddingTimer(false))
        .catch((error) => console.error("couldn't create timer", error));
    }
  };

  return (
    <div className="add-timer">
      <input
        type="text"
        placeholder="Timer Name"
        onChange={handleSetTimerName}
      />
      <button onClick={handleAddTimer}>Add Timer</button>
    </div>
  );
};

export default AddTimerButton;
