import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  transpilePackages: ["@thatopen/components", "@thatopen/ui", "three"],
  // Use Turbopack (default in Next.js 16)
  turbopack: {},
};

export default nextConfig;
