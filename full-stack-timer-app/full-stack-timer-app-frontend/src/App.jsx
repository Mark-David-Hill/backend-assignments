import { useState } from "react";
import AddTimerButton from "./components/AddTimerButton";
import TimersList from "./components/TimersList";
import LoginForm from "./components/LoginForm";

function App() {
  const [isUpdatingTimer, setIsUpdatingTimer] = useState(false);

  return (
    <div className="app-container">
      <h1>Timers App</h1>
      <div className="timers-container">
        <LoginForm />
        <TimersList
          isUpdatingTimer={isUpdatingTimer}
          setIsUpdatingTimer={setIsUpdatingTimer}
        />
        <AddTimerButton setIsUpdatingTimer={setIsUpdatingTimer} />
      </div>
    </div>
  );
}

export default App;
