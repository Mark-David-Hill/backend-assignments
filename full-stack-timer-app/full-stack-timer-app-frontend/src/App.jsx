import { useState } from "react";
import AddTimerButton from "./components/AddTimerButton";
import TimersList from "./components/TimersList";

function App() {
  const [isAddingTimer, setIsAddingTimer] = useState(false);

  return (
    <div className="app-container">
      <div className="timers-container">
        <TimersList isAddingTimer={isAddingTimer} />
        <AddTimerButton setIsAddingTimer={setIsAddingTimer} />
      </div>
    </div>
  );
}

export default App;
