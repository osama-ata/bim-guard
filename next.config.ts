import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  transpilePackages: ["@thatopen/components", "@thatopen/ui", "three"],
  // Use Turbopack (default in Next.js 16)
  turbopack: {},
  async rewrites() {
    return [
      {
        source: "/api/python/:path*",
        destination: "http://127.0.0.1:8000/api/v1/:path*", // Proxy to FastAPI
      },
    ];
  },
};

export default nextConfig;
