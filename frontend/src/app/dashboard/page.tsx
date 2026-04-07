"use client";

import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import { Plus, TrendingUp, TrendingDown, UserPlus, UserMinus } from "lucide-react";
import Header from "@/components/header";
import AccountCard from "@/components/account-card";
import { getToken } from "@/lib/auth";
import {
  listAccounts,
  createAccount,
  getChangesSummary,
  type Account,
  type ChangeSummary,
} from "@/lib/api";

export default function DashboardPage() {
  const router = useRouter();
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [summary, setSummary] = useState<ChangeSummary | null>(null);
  const [showAdd, setShowAdd] = useState(false);
  const [newUsername, setNewUsername] = useState("");
  const [loading, setLoading] = useState(true);

  const loadData = useCallback(async () => {
    const token = getToken();
    if (!token) {
      router.push("/login");
      return;
    }
    try {
      const [accts, sum] = await Promise.all([
        listAccounts(token),
        getChangesSummary(token),
      ]);
      setAccounts(accts);
      setSummary(sum);
    } catch {
      router.push("/login");
    } finally {
      setLoading(false);
    }
  }, [router]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleAddAccount = async (e: React.FormEvent) => {
    e.preventDefault();
    const token = getToken();
    if (!token || !newUsername.trim()) return;
    await createAccount(token, { instagram_username: newUsername.trim() });
    setNewUsername("");
    setShowAdd(false);
    loadData();
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-pulse text-gray-400">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="max-w-6xl mx-auto px-4 sm:px-6 py-8">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <button
            onClick={() => setShowAdd(!showAdd)}
            className="flex items-center gap-2 px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-hover transition text-sm font-medium"
          >
            <Plus size={16} />
            Add Account
          </button>
        </div>

        {/* Add Account Form */}
        {showAdd && (
          <form
            onSubmit={handleAddAccount}
            className="mb-6 bg-white rounded-xl shadow-sm border border-gray-200 p-5 flex items-end gap-4"
          >
            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Instagram Username
              </label>
              <input
                type="text"
                value={newUsername}
                onChange={(e) => setNewUsername(e.target.value)}
                placeholder="e.g. username"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent outline-none"
                required
              />
            </div>
            <button
              type="submit"
              className="px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary-hover transition text-sm font-medium"
            >
              Track
            </button>
          </form>
        )}

        {/* Summary Cards */}
        {summary && summary.total_changes > 0 && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
            <SummaryCard
              label="New Followers"
              value={summary.new_followers}
              icon={<TrendingUp size={18} />}
              color="text-success"
              bg="bg-green-50"
            />
            <SummaryCard
              label="Lost Followers"
              value={summary.lost_followers}
              icon={<TrendingDown size={18} />}
              color="text-danger"
              bg="bg-red-50"
            />
            <SummaryCard
              label="New Following"
              value={summary.new_following}
              icon={<UserPlus size={18} />}
              color="text-info"
              bg="bg-blue-50"
            />
            <SummaryCard
              label="Unfollowed"
              value={summary.lost_following}
              icon={<UserMinus size={18} />}
              color="text-warning"
              bg="bg-amber-50"
            />
          </div>
        )}

        {/* Accounts Grid */}
        {accounts.length === 0 ? (
          <div className="text-center py-16">
            <p className="text-gray-400 text-lg mb-2">No accounts tracked yet</p>
            <p className="text-gray-400 text-sm">
              Click &quot;Add Account&quot; to start tracking an Instagram profile.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {accounts.map((account) => (
              <AccountCard key={account.id} account={account} />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

function SummaryCard({
  label,
  value,
  icon,
  color,
  bg,
}: {
  label: string;
  value: number;
  icon: React.ReactNode;
  color: string;
  bg: string;
}) {
  return (
    <div className={`${bg} rounded-xl p-4`}>
      <div className={`${color} mb-2`}>{icon}</div>
      <p className="text-2xl font-bold text-gray-900">{value}</p>
      <p className="text-xs text-gray-500">{label}</p>
    </div>
  );
}
