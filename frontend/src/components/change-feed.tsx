"use client";

import { UserPlus, UserMinus, UserCheck, UserX } from "lucide-react";
import { type ChangeEvent } from "@/lib/api";
import { timeAgo } from "@/lib/utils";

const CHANGE_CONFIG = {
  new_follower: { icon: UserPlus, color: "text-success", bg: "bg-green-50", label: "New Follower" },
  lost_follower: { icon: UserMinus, color: "text-danger", bg: "bg-red-50", label: "Lost Follower" },
  new_following: { icon: UserCheck, color: "text-info", bg: "bg-blue-50", label: "New Following" },
  lost_following: { icon: UserX, color: "text-warning", bg: "bg-amber-50", label: "Unfollowed" },
};

export default function ChangeFeed({ changes }: { changes: ChangeEvent[] }) {
  if (changes.length === 0) {
    return (
      <div className="text-center py-8 text-gray-400 text-sm">
        No changes detected yet. Take a snapshot to start tracking.
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {changes.map((change) => {
        const config = CHANGE_CONFIG[change.change_type];
        const Icon = config.icon;
        return (
          <div
            key={change.id}
            className={`flex items-center gap-3 p-3 rounded-lg ${config.bg}`}
          >
            <div className={`${config.color}`}>
              <Icon size={18} />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900">
                {change.instagram_username}
              </p>
              <p className="text-xs text-gray-500">{config.label}</p>
            </div>
            <span className="text-xs text-gray-400 shrink-0">
              {timeAgo(change.detected_at)}
            </span>
          </div>
        );
      })}
    </div>
  );
}
