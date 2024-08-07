import { useEffect, useState } from "react";
import fetchWrapper from "../lib/apiCall";
import Timer from "./Timer";

const TimersList = ({ isUpdatingTimer, setIsUpdatingTimer }) => {
  const [allTimers, setAllTimers] = useState(null);

  useEffect(() => {
    try {
      fetchWrapper.apiCall("/timers", "GET").then((data) => {
        console.log(data);
        if (data.results.length > 0) {
          setAllTimers(data.results);
        } else {
          setAllTimers(null);
        }
      });
    } catch (error) {
      console.log("could not get timers", error);
    }
  }, [isUpdatingTimer]);

  return (
    <div>
      <div className="timers-list-wrapper">
        {allTimers &&
          allTimers.map((timerData, timerId) => {
            return (
              <Timer
                key={timerId}
                timerData={timerData}
                setIsUpdatingTimer={setIsUpdatingTimer}
              />
            );
          })}
      </div>
    </div>
  );
};

export default TimersList;
