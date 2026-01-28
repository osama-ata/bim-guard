"use client";

import Image from "next/image";
import dynamic from "next/dynamic";
import { IFCUploadButton } from "@/components/IFCUploadButton";

const HomepageViewer = dynamic(() => import("@/components/HomepageViewer"), {
  ssr: false,
});

export default function Home() {
  return (
    <div className="relative flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black overflow-hidden">
      <HomepageViewer />
      <main className="relative z-10 flex min-h-screen w-full max-w-3xl flex-col items-center justify-center py-32 px-16 bg-white/10 dark:bg-black/10 backdrop-blur-sm sm:items-start text-center sm:text-left transition-all duration-700 ease-in-out">
        <div className="flex flex-col gap-8 w-full items-center sm:items-start animate-in fade-in slide-in-from-bottom-4 duration-1000">
          <Image
            className="dark:invert mb-4"
            src="/next.svg"
            alt="Next.js logo"
            width={100}
            height={20}
            priority
          />
          <div className="flex flex-col gap-4">
            <h1 className="text-5xl font-extrabold tracking-tight text-black dark:text-zinc-50 sm:text-6xl">
              BIM Guard <span className="text-zinc-400">Viewer</span>
            </h1>
            <p className="max-w-md text-xl leading-relaxed text-zinc-500 dark:text-zinc-400">
              The professional way to view and validate your IFC models directly in the browser.
            </p>
          </div>

          <div className="flex flex-col gap-4 w-full sm:flex-row mt-4">
            <IFCUploadButton />
            <a
              className="flex h-12 items-center justify-center rounded-full border border-solid border-black/[.08] px-10 text-base font-semibold transition-all hover:border-black hover:bg-black hover:text-white dark:border-white/[.145] dark:hover:bg-[#1a1a1a] dark:hover:border-white"
              href="/viewer"
            >
              Explore Sample
            </a>
          </div>
        </div>
      </main>
    </div>
  );
}
