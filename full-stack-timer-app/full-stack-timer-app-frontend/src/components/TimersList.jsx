import { useEffect, useState } from "react";
import fetchWrapper from "../lib/apiCall";
import Timer from "./Timer";

const TimersList = ({ isAddingTimer }) => {
  const [allTimers, setAllTimers] = useState(null);

  useEffect(() => {
    fetchWrapper.apiCall("/timers", "GET").then((data) => {
      setAllTimers(data.results);
    });
  }, [isAddingTimer]);

  return (
    <div>
      <div className="timers-list-wrapper">
        {allTimers &&
          allTimers.map((timerData, timerId) => {
            return <Timer key={timerId} timerData={timerData} />;
          })}
      </div>
    </div>
  );
};

export default TimersList;
