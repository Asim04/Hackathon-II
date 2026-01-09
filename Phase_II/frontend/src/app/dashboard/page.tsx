import DashboardClient from './DashboardClient';

// Force dynamic rendering for authenticated routes
export const dynamic = 'force-dynamic';

export default function DashboardPage() {
  return <DashboardClient />;
}
