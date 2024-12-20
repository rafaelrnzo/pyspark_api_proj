"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import PanoramaFishEyeRoundedIcon from '@mui/icons-material/PanoramaFishEyeRounded';
import DashboardRoundedIcon from '@mui/icons-material/DashboardRounded';

const Sidebar: React.FC = () => {
  const pathname = usePathname(); // Get the current path

  return (
    <div className="flex h-screen">
      <div className="w-full bg-neutral-900 text-white flex flex-col p-6 space-y-6">
        <div className="text-xl font-semibold gap-y-4 flex flex-col">
          <div className="flex gap-x-2">
            <PanoramaFishEyeRoundedIcon />
            <h1>Stream Dashboard</h1>
          </div>
          <div className="w-full h-0.5 bg-white/15"></div>
        </div>
        <ul className="space-y-2">
          {[
            { href: "/", label: "Home" },
            { href: "/about", label: "About" },
            { href: "/services", label: "Services" },
            { href: "/contact", label: "Contact" },
          ].map((link) => (
            <li key={link.href} className="flex">
              <Link
                href={link.href}
                className={`py-3 px-4 w-full rounded-xl ${
                  pathname === link.href
                    ? "bg-blue-600 w-full"
                    : "hover:bg-gray-700"
                }`}
              >
                {link.label}
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Sidebar;
