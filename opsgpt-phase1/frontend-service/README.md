# OpsGPT Frontend Service

The frontend uses React, Vite, React Router, Axios, lucide-react icons, clsx, and Tailwind CSS configuration alongside the app's plain CSS component styles.

## Theme

The UI uses the locked OpsGPT palette:

- Primary teal: `#0F766E`
- Teal hover: `#115E59`
- Teal blue accent: `#0891B2`
- Dark slate: `#0F172A`
- Muted text: `#64748B`
- Background: `#F8FAFC`
- Surface/card: `#FFFFFF`
- Border: `#E2E8F0`
- Success: `#059669`
- Warning: `#D97706`
- Danger: `#DC2626`

## UI Notes

- The layout includes a responsive, collapsible sidebar, accessible header, selected project control, breadcrumbs, and skip-to-content link.
- Tables are wrapped in horizontal scroll containers for smaller screens.
- The generated webhook URL is copied with `navigator.clipboard.writeText` and a fallback copy method.
- The Alertmanager receiver example remains documentation-only and is not rendered in the application UI.
- Member assignment search debounces Core API user search while typing and renders results dynamically.
