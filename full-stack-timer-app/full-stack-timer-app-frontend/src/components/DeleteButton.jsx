import fetchWrapper from "../lib/apiCall";

const DeleteButton = ({ timerId, setIsUpdatingTimer }) => {
  const handleDelete = () => {
    setIsUpdatingTimer(true);
    fetchWrapper
      .apiCall(`/timer/delete/${timerId}`, "DELETE")
      .then(() => setIsUpdatingTimer(false))
      .catch((error) => console.error("couldn't delete timer", error));
  };

  return <button onClick={handleDelete}>x</button>;
};

export default DeleteButton;
