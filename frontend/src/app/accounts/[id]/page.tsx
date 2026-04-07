"use client";

import { useState, useEffect, useCallback, use } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, Camera, Trash2 } from "lucide-react";
import Header from "@/components/header";
import ChangeFeed from "@/components/change-feed";
import FollowerChart from "@/components/follower-chart";
import { getToken } from "@/lib/auth";
import {
  getAccount,
  listSnapshots,
  listChanges,
  triggerSnapshot,
  deleteAccount,
  type Account,
  type Snapshot,
  type ChangeEvent,
} from "@/lib/api";

export default function AccountDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = use(params);
  const router = useRouter();
  const [account, setAccount] = useState<Account | null>(null);
  const [snapshots, setSnapshots] = useState<Snapshot[]>([]);
  const [changes, setChanges] = useState<ChangeEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [snapshotLoading, setSnapshotLoading] = useState(false);

  const loadData = useCallback(async () => {
    const token = getToken();
    if (!token) {
      router.push("/login");
      return;
    }
    try {
      const [acct, snaps, chgs] = await Promise.all([
        getAccount(token, id),
        listSnapshots(token, id),
        listChanges(token, id),
      ]);
      setAccount(acct);
      setSnapshots(snaps);
      setChanges(chgs);
    } catch {
      router.push("/dashboard");
    } finally {
      setLoading(false);
    }
  }, [id, router]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleSnapshot = async () => {
    const token = getToken();
    if (!token) return;
    setSnapshotLoading(true);
    try {
      await triggerSnapshot(token, id);
      await loadData();
    } finally {
      setSnapshotLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm("Are you sure you want to stop tracking this account?")) return;
    const token = getToken();
    if (!token) return;
    await deleteAccount(token, id);
    router.push("/dashboard");
  };

  if (loading || !account) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-pulse text-gray-400">Loading...</div>
      </div>
    );
  }

  const latestSnapshot = snapshots[0];

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="max-w-6xl mx-auto px-4 sm:px-6 py-8">
        {/* Top Navigation */}
        <div className="flex items-center justify-between mb-6">
          <Link
            href="/dashboard"
            className="flex items-center gap-2 text-gray-500 hover:text-gray-700 transition text-sm"
          >
            <ArrowLeft size={16} />
            Back to Dashboard
          </Link>
          <div className="flex items-center gap-3">
            <button
              onClick={handleSnapshot}
              disabled={snapshotLoading}
              className="flex items-center gap-2 px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-hover transition text-sm font-medium disabled:opacity-50"
            >
              <Camera size={16} />
              {snapshotLoading ? "Taking..." : "Take Snapshot"}
            </button>
            <button
              onClick={handleDelete}
              className="p-2 text-gray-400 hover:text-danger transition"
              title="Delete account"
            >
              <Trash2 size={18} />
            </button>
          </div>
        </div>

        {/* Account Header */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                @{account.instagram_username}
              </h1>
              {account.display_name && (
                <p className="text-gray-500 mt-1">{account.display_name}</p>
              )}
            </div>
            {latestSnapshot && (
              <div className="flex gap-8 text-center">
                <div>
                  <p className="text-3xl font-bold text-primary">
                    {latestSnapshot.follower_count}
                  </p>
                  <p className="text-xs text-gray-500">Followers</p>
                </div>
                <div>
                  <p className="text-3xl font-bold text-info">
                    {latestSnapshot.following_count}
                  </p>
                  <p className="text-xs text-gray-500">Following</p>
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Chart */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">
              Follower/Following Trend
            </h2>
            <FollowerChart snapshots={snapshots} />
          </div>

          {/* Change Feed */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">
              Recent Changes ({changes.length})
            </h2>
            <div className="max-h-[340px] overflow-y-auto">
              <ChangeFeed changes={changes} />
            </div>
          </div>
        </div>

        {/* Snapshot History */}
        <div className="mt-6 bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Snapshot History
          </h2>
          {snapshots.length === 0 ? (
            <p className="text-gray-400 text-sm text-center py-4">
              No snapshots yet. Click &quot;Take Snapshot&quot; to start.
            </p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-gray-500 border-b">
                    <th className="pb-2 font-medium">Time</th>
                    <th className="pb-2 font-medium">Followers</th>
                    <th className="pb-2 font-medium">Following</th>
                    <th className="pb-2 font-medium">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {snapshots.map((snap) => (
                    <tr key={snap.id} className="border-b border-gray-50">
                      <td className="py-2.5 text-gray-700">
                        {new Date(snap.snapshot_at).toLocaleString("ko-KR")}
                      </td>
                      <td className="py-2.5 font-medium">{snap.follower_count}</td>
                      <td className="py-2.5 font-medium">{snap.following_count}</td>
                      <td className="py-2.5">
                        <span
                          className={`px-2 py-0.5 rounded-full text-xs ${
                            snap.status === "success"
                              ? "bg-green-100 text-green-700"
                              : "bg-red-100 text-red-700"
                          }`}
                        >
                          {snap.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
