import UiEmptyState from "../ui/EmptyState.jsx";

export default function EmptyState({ action, title, detail }) {
  return <UiEmptyState action={action} detail={detail} title={title} />;
}
