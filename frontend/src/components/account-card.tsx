"use client";

import Link from "next/link";
import { Users, UserPlus, Clock } from "lucide-react";
import { type Account } from "@/lib/api";
import { formatDate } from "@/lib/utils";

export default function AccountCard({ account }: { account: Account }) {
  return (
    <Link
      href={`/accounts/${account.id}`}
      className="block bg-white rounded-xl shadow-sm border border-gray-200 p-5 hover:shadow-md transition"
    >
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-lg font-semibold text-gray-900">
          @{account.instagram_username}
        </h3>
        <span
          className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${
            account.is_active
              ? "bg-green-100 text-green-700"
              : "bg-gray-100 text-gray-500"
          }`}
        >
          {account.is_active ? "Active" : "Paused"}
        </span>
      </div>

      {account.display_name && (
        <p className="text-sm text-gray-500 mb-3">{account.display_name}</p>
      )}

      <div className="flex items-center gap-4 text-sm text-gray-600">
        <span className="flex items-center gap-1">
          <Users size={14} />
          Tracking
        </span>
        <span className="flex items-center gap-1">
          <UserPlus size={14} />
          Every {account.check_interval_minutes}min
        </span>
      </div>

      {account.last_checked_at && (
        <p className="mt-3 text-xs text-gray-400 flex items-center gap-1">
          <Clock size={12} />
          Last checked: {formatDate(account.last_checked_at)}
        </p>
      )}
    </Link>
  );
}
