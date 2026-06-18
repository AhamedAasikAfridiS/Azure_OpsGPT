export default function LoadingState({ label = "Loading", fullPage = false }) {
  return (
    <div className={fullPage ? "state-page" : "state-box"}>
      <div className="spinner" />
      <span>{label}</span>
    </div>
  );
}
