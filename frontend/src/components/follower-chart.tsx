"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { type Snapshot } from "@/lib/api";

export default function FollowerChart({ snapshots }: { snapshots: Snapshot[] }) {
  if (snapshots.length === 0) {
    return (
      <div className="text-center py-8 text-gray-400 text-sm">
        No snapshot data yet.
      </div>
    );
  }

  const data = [...snapshots]
    .reverse()
    .map((s) => ({
      time: new Date(s.snapshot_at).toLocaleString("ko-KR", {
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      }),
      followers: s.follower_count,
      following: s.following_count,
    }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
        <XAxis dataKey="time" fontSize={12} tick={{ fill: "#9ca3af" }} />
        <YAxis fontSize={12} tick={{ fill: "#9ca3af" }} />
        <Tooltip
          contentStyle={{
            borderRadius: "8px",
            border: "1px solid #e5e7eb",
            fontSize: "13px",
          }}
        />
        <Legend />
        <Line
          type="monotone"
          dataKey="followers"
          stroke="#6366f1"
          strokeWidth={2}
          dot={{ r: 4 }}
          name="Followers"
        />
        <Line
          type="monotone"
          dataKey="following"
          stroke="#3b82f6"
          strokeWidth={2}
          dot={{ r: 4 }}
          name="Following"
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
