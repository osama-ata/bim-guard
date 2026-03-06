import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight, CheckCircle2, Shield, Zap } from "lucide-react";

export default function LandingPage() {
    return (
        <div className="flex min-h-screen flex-col bg-background text-foreground">
            {/* Navigation */}
            <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
                <div className="container flex h-16 items-center justify-between">
                    <div className="flex items-center gap-2 font-bold text-xl">
                        <div className="h-8 w-8 rounded-lg bg-primary flex items-center justify-center text-primary-foreground">
                            <Shield className="h-5 w-5" />
                        </div>
                        BIMGuard AI
                    </div>
                    <nav className="hidden md:flex items-center gap-6 text-sm font-medium">
                        <Link href="#features" className="hover:text-primary transition-colors">
                            Features
                        </Link>
                        <Link href="#how-it-works" className="hover:text-primary transition-colors">
                            How it Works
                        </Link>
                        <Link href="#pricing" className="hover:text-primary transition-colors">
                            Pricing
                        </Link>
                    </nav>
                    <div className="flex items-center gap-4">
                        <Link href="/dashboard">
                            <Button>
                                Go to Dashboard <ArrowRight className="ml-2 h-4 w-4" />
                            </Button>
                        </Link>
                    </div>
                </div>
            </header>

            <main className="flex-1">
                {/* Hero Section */}
                <section className="relative overflow-hidden py-24 lg:py-32">
                    <div className="absolute inset-0 -z-10 bg-[radial-gradient(45%_40%_at_50%_60%,var(--primary)_0%,transparent_100%)] opacity-10" />
                    <div className="container flex flex-col items-center text-center">
                        <div className="inline-flex items-center rounded-full border px-3 py-1 text-sm font-medium backdrop-blur-sm mb-6">
                            <span className="flex h-2 w-2 rounded-full bg-primary mr-2"></span>
                            New: Automated ISO 19650 Compliance
                        </div>
                        <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl md:text-6xl lg:text-7xl max-w-4xl bg-clip-text text-transparent bg-gradient-to-b from-foreground to-foreground/70">
                            Intelligent BIM Compliance <br /> for Modern Construction
                        </h1>
                        <p className="mt-6 max-w-2xl text-lg text-muted-foreground sm:text-xl leading-relaxed">
                            Automate your building information model validation. Ensure compliance, detect clashes, and generate detailed reports in seconds, not days.
                        </p>
                        <div className="mt-10 flex flex-col sm:flex-row gap-4">
                            <Link href="/dashboard">
                                <Button size="lg" className="h-12 px-8 text-base">
                                    Get Started for Free
                                </Button>
                            </Link>
                            <Button size="lg" variant="outline" className="h-12 px-8 text-base">
                                View Documentation
                            </Button>
                        </div>
                    </div>
                </section>

                {/* Features Section */}
                <section id="features" className="py-24 bg-muted/30">
                    <div className="container">
                        <div className="mx-auto max-w-2xl text-center mb-16">
                            <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
                                Everything you need to validate your models
                            </h2>
                            <p className="mt-4 text-lg text-muted-foreground">
                                Built for BIM managers, architects, and engineers who demand precision and speed.
                            </p>
                        </div>
                        <div className="grid gap-8 md:grid-cols-3">
                            <div className="relative overflow-hidden rounded-2xl border bg-background p-8 transition-shadow hover:shadow-lg">
                                <div className="mb-4 inline-flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 text-primary">
                                    <Zap className="h-6 w-6" />
                                </div>
                                <h3 className="mb-2 text-xl font-bold">Instant Analysis</h3>
                                <p className="text-muted-foreground">
                                    Upload IFC files and get immediate feedback on compliance issues, metadata completeness, and geometry errors.
                                </p>
                            </div>
                            <div className="relative overflow-hidden rounded-2xl border bg-background p-8 transition-shadow hover:shadow-lg">
                                <div className="mb-4 inline-flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 text-primary">
                                    <Shield className="h-6 w-6" />
                                </div>
                                <h3 className="mb-2 text-xl font-bold">Standard Compliance</h3>
                                <p className="text-muted-foreground">
                                    Pre-configured checks for ISO 19650, COBie, and local building regulations. Customizable rule sets for your specific needs.
                                </p>
                            </div>
                            <div className="relative overflow-hidden rounded-2xl border bg-background p-8 transition-shadow hover:shadow-lg">
                                <div className="mb-4 inline-flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 text-primary">
                                    <CheckCircle2 className="h-6 w-6" />
                                </div>
                                <h3 className="mb-2 text-xl font-bold">Automated Reporting</h3>
                                <p className="text-muted-foreground">
                                    Generate comprehensive PDF and spreadsheet reports. Track issue resolution progress over time with historical data.
                                </p>
                            </div>
                        </div>
                    </div>
                </section>

                {/* CTA Section */}
                <section className="py-24">
                    <div className="container">
                        <div className="relative overflow-hidden rounded-3xl bg-primary px-6 py-16 shadow-2xl sm:px-16 md:pt-24 lg:flex lg:gap-x-20 lg:px-24 lg:pt-0">
                            <div className="mx-auto max-w-md text-center lg:mx-0 lg:flex-auto lg:py-24 lg:text-left">
                                <h2 className="text-3xl font-bold tracking-tight text-primary-foreground sm:text-4xl">
                                    Ready to streamline your workflow?
                                    <br />
                                    Start validating today.
                                </h2>
                                <p className="mt-6 text-lg leading-8 text-primary-foreground/80">
                                    Join thousands of construction professionals who trust BIMGuard AI for their model validation needs.
                                </p>
                                <div className="mt-10 flex items-center justify-center gap-x-6 lg:justify-start">
                                    <Link href="/dashboard">
                                        <Button size="lg" variant="secondary" className="text-primary font-bold">
                                            Launch Dashboard
                                        </Button>
                                    </Link>
                                    <Link href="#" className="text-sm font-semibold leading-6 text-primary-foreground">
                                        Learn more <span aria-hidden="true">→</span>
                                    </Link>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </main>

            {/* Footer */}
            <footer className="border-t py-12 md:py-16">
                <div className="container flex flex-col items-center justify-between gap-4 md:flex-row">
                    <p className="text-sm text-muted-foreground">
                        &copy; 2026 BIMGuard AI. All rights reserved.
                    </p>
                    <div className="flex gap-4 text-sm text-muted-foreground">
                        <Link href="#" className="hover:underline">Privacy Policy</Link>
                        <Link href="#" className="hover:underline">Terms of Service</Link>
                    </div>
                </div>
            </footer>
        </div>
    );
}
