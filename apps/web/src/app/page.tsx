export default function Home() {
  return (
    <main className="flex min-h-screen items-center justify-center px-6 py-24">
      <div className="w-full max-w-3xl rounded-3xl border border-black/10 bg-white/80 p-10 shadow-[0_24px_80px_rgba(15,23,42,0.08)] backdrop-blur">
        <p className="text-sm font-medium uppercase tracking-[0.3em] text-slate-500">
          Project Setup
        </p>
        <h1 className="mt-4 text-4xl font-semibold tracking-tight text-slate-950">
          Q1 web app scaffold
        </h1>
        <p className="mt-4 max-w-2xl text-base leading-7 text-slate-600">
          Bootstrap cleanup and project tooling configuration will be added on top of this minimal
          entry page.
        </p>
      </div>
    </main>
  );
}
