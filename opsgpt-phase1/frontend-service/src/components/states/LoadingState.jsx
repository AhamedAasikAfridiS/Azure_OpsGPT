import LoadingSpinner from "../ui/LoadingSpinner.jsx";

export default function LoadingState({ label = "Loading", fullPage = false }) {
  return <LoadingSpinner fullPage={fullPage} label={label} />;
}
