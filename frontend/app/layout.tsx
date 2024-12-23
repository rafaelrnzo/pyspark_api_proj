import type { Metadata } from "next";
import { Geist, Geist_Mono, Poppins } from "next/font/google"; // Import Poppins
import "./globals.css";
import Sidebar from "./components/sidebar"; // Import the Sidebar component

// Define Google Fonts
const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const poppins = Poppins({
  variable: "--font-poppins",
  subsets: ["latin"],
  weight: ["400", "600", "700"], // Include desired font weights
});

export const metadata: Metadata = {
  title: "Create Next App",
  description: "Generated by create next app",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${poppins.variable} antialiased w-full h-screen bg-neutral-950`}
      >
        <div className="flex">
          <div className="md:w-1/6 xl:block hidden">
            <Sidebar />
          </div>
          <div className="xl:w-5/6">{children}</div>
        </div>
      </body>
    </html>
  );
}
