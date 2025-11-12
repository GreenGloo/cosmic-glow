import { Lock, Zap, Shield, TrendingUp, CheckCircle2, ArrowRight } from "lucide-react";
import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-white dark:from-slate-950 dark:to-slate-900">
      {/* Navigation */}
      <nav className="border-b border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                OWN-AI
              </span>
            </div>
            <div className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-100">
                Features
              </a>
              <a href="#pricing" className="text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-100">
                Pricing
              </a>
              <a href="#how-it-works" className="text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-100">
                How It Works
              </a>
              <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium transition-colors">
                Get Started
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-20 pb-32 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center">
            <div className="inline-flex items-center px-4 py-2 bg-blue-50 dark:bg-blue-900/20 rounded-full mb-8">
              <Lock className="w-4 h-4 mr-2 text-blue-600 dark:text-blue-400" />
              <span className="text-sm font-medium text-blue-600 dark:text-blue-400">
                Your Data. Your AI. Your Control.
              </span>
            </div>

            <h1 className="text-5xl md:text-7xl font-bold text-slate-900 dark:text-white mb-6 leading-tight">
              Stop Sending Your<br />
              <span className="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                Proprietary Data
              </span>
              <br />
              to OpenAI
            </h1>

            <p className="text-xl text-slate-600 dark:text-slate-400 mb-10 max-w-3xl mx-auto">
              Fine-tune and deploy private AI models on your own data. Enterprise-grade AI without the ML expertise or data privacy risks.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-lg font-semibold text-lg transition-colors flex items-center justify-center group">
                Start Free Trial
                <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </button>
              <button className="bg-white dark:bg-slate-800 border-2 border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600 text-slate-900 dark:text-white px-8 py-4 rounded-lg font-semibold text-lg transition-colors">
                Schedule Demo
              </button>
            </div>

            <div className="mt-12 flex items-center justify-center gap-8 text-sm text-slate-600 dark:text-slate-400">
              <div className="flex items-center">
                <CheckCircle2 className="w-5 h-5 mr-2 text-green-600" />
                SOC 2 Compliant
              </div>
              <div className="flex items-center">
                <CheckCircle2 className="w-5 h-5 mr-2 text-green-600" />
                HIPAA Ready
              </div>
              <div className="flex items-center">
                <CheckCircle2 className="w-5 h-5 mr-2 text-green-600" />
                On-Premise Available
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Social Proof */}
      <section className="py-12 bg-slate-100 dark:bg-slate-900/50 border-y border-slate-200 dark:border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <p className="text-center text-slate-600 dark:text-slate-400 mb-8">
            Trusted by forward-thinking enterprises
          </p>
          <div className="flex justify-center items-center gap-12 opacity-50">
            {/* Placeholder for company logos */}
            <div className="text-2xl font-bold text-slate-400">ACME Corp</div>
            <div className="text-2xl font-bold text-slate-400">TechStart</div>
            <div className="text-2xl font-bold text-slate-400">DataSec</div>
            <div className="text-2xl font-bold text-slate-400">HealthTech</div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-slate-900 dark:text-white mb-4">
              Everything you need to own your AI
            </h2>
            <p className="text-xl text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
              From data ingestion to production deployment, we handle the entire ML pipeline.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="bg-white dark:bg-slate-800 p-8 rounded-2xl border border-slate-200 dark:border-slate-700 hover:shadow-lg transition-shadow">
              <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center mb-4">
                <Lock className="w-6 h-6 text-blue-600 dark:text-blue-400" />
              </div>
              <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-2">
                Complete Data Privacy
              </h3>
              <p className="text-slate-600 dark:text-slate-400">
                Your proprietary data never leaves your infrastructure. Deploy on-premise or in your VPC.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="bg-white dark:bg-slate-800 p-8 rounded-2xl border border-slate-200 dark:border-slate-700 hover:shadow-lg transition-shadow">
              <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center mb-4">
                <Zap className="w-6 h-6 text-purple-600 dark:text-purple-400" />
              </div>
              <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-2">
                One-Click Fine-Tuning
              </h3>
              <p className="text-slate-600 dark:text-slate-400">
                Upload your data and fine-tune Llama, Mistral, or Qwen models in minutes. No ML expertise required.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="bg-white dark:bg-slate-800 p-8 rounded-2xl border border-slate-200 dark:border-slate-700 hover:shadow-lg transition-shadow">
              <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center mb-4">
                <TrendingUp className="w-6 h-6 text-green-600 dark:text-green-400" />
              </div>
              <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-2">
                Production-Ready API
              </h3>
              <p className="text-slate-600 dark:text-slate-400">
                OpenAI-compatible API endpoints with automatic scaling, monitoring, and failover.
              </p>
            </div>

            {/* Feature 4 */}
            <div className="bg-white dark:bg-slate-800 p-8 rounded-2xl border border-slate-200 dark:border-slate-700 hover:shadow-lg transition-shadow">
              <div className="w-12 h-12 bg-orange-100 dark:bg-orange-900/30 rounded-lg flex items-center justify-center mb-4">
                <Shield className="w-6 h-6 text-orange-600 dark:text-orange-400" />
              </div>
              <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-2">
                Enterprise Security
              </h3>
              <p className="text-slate-600 dark:text-slate-400">
                SOC 2 compliant infrastructure with SSO, audit logs, and role-based access control.
              </p>
            </div>

            {/* Feature 5 */}
            <div className="bg-white dark:bg-slate-800 p-8 rounded-2xl border border-slate-200 dark:border-slate-700 hover:shadow-lg transition-shadow">
              <div className="w-12 h-12 bg-pink-100 dark:bg-pink-900/30 rounded-lg flex items-center justify-center mb-4">
                <CheckCircle2 className="w-6 h-6 text-pink-600 dark:text-pink-400" />
              </div>
              <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-2">
                Automated Data Pipeline
              </h3>
              <p className="text-slate-600 dark:text-slate-400">
                Intelligent data cleaning, formatting, and validation. We handle the messy preprocessing.
              </p>
            </div>

            {/* Feature 6 */}
            <div className="bg-white dark:bg-slate-800 p-8 rounded-2xl border border-slate-200 dark:border-slate-700 hover:shadow-lg transition-shadow">
              <div className="w-12 h-12 bg-indigo-100 dark:bg-indigo-900/30 rounded-lg flex items-center justify-center mb-4">
                <TrendingUp className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
              </div>
              <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-2">
                Performance Analytics
              </h3>
              <p className="text-slate-600 dark:text-slate-400">
                Real-time monitoring, A/B testing, and detailed analytics to measure model performance.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="py-24 px-4 sm:px-6 lg:px-8 bg-slate-50 dark:bg-slate-900/50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-slate-900 dark:text-white mb-4">
              From data to deployment in 3 steps
            </h2>
            <p className="text-xl text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
              We've eliminated the complexity of AI deployment
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="relative">
              <div className="bg-white dark:bg-slate-800 p-8 rounded-2xl border-2 border-blue-200 dark:border-blue-800">
                <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold text-xl mb-4">
                  1
                </div>
                <h3 className="text-2xl font-semibold text-slate-900 dark:text-white mb-3">
                  Upload Your Data
                </h3>
                <p className="text-slate-600 dark:text-slate-400">
                  Drop your documents, codebases, or datasets. We automatically clean, format, and validate everything.
                </p>
              </div>
            </div>

            <div className="relative">
              <div className="bg-white dark:bg-slate-800 p-8 rounded-2xl border-2 border-purple-200 dark:border-purple-800">
                <div className="w-12 h-12 bg-purple-600 rounded-full flex items-center justify-center text-white font-bold text-xl mb-4">
                  2
                </div>
                <h3 className="text-2xl font-semibold text-slate-900 dark:text-white mb-3">
                  One-Click Training
                </h3>
                <p className="text-slate-600 dark:text-slate-400">
                  Select your base model (Llama, Mistral, Qwen) and click train. We handle all the GPU orchestration.
                </p>
              </div>
            </div>

            <div className="relative">
              <div className="bg-white dark:bg-slate-800 p-8 rounded-2xl border-2 border-green-200 dark:border-green-800">
                <div className="w-12 h-12 bg-green-600 rounded-full flex items-center justify-center text-white font-bold text-xl mb-4">
                  3
                </div>
                <h3 className="text-2xl font-semibold text-slate-900 dark:text-white mb-3">
                  Deploy Instantly
                </h3>
                <p className="text-slate-600 dark:text-slate-400">
                  Get an OpenAI-compatible API endpoint. Deploy to our cloud or download for on-premise hosting.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-24 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-slate-900 dark:text-white mb-4">
              Simple, transparent pricing
            </h2>
            <p className="text-xl text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
              10x cheaper than building an in-house ML team
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {/* Startup Tier */}
            <div className="bg-white dark:bg-slate-800 p-8 rounded-2xl border border-slate-200 dark:border-slate-700">
              <h3 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">Startup</h3>
              <div className="mb-6">
                <span className="text-4xl font-bold text-slate-900 dark:text-white">$2,000</span>
                <span className="text-slate-600 dark:text-slate-400">/month</span>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-start">
                  <CheckCircle2 className="w-5 h-5 mr-3 text-green-600 flex-shrink-0 mt-0.5" />
                  <span className="text-slate-600 dark:text-slate-400">1 fine-tuned model</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle2 className="w-5 h-5 mr-3 text-green-600 flex-shrink-0 mt-0.5" />
                  <span className="text-slate-600 dark:text-slate-400">Cloud-hosted inference</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle2 className="w-5 h-5 mr-3 text-green-600 flex-shrink-0 mt-0.5" />
                  <span className="text-slate-600 dark:text-slate-400">1M tokens/month included</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle2 className="w-5 h-5 mr-3 text-green-600 flex-shrink-0 mt-0.5" />
                  <span className="text-slate-600 dark:text-slate-400">Email support</span>
                </li>
              </ul>
              <button className="w-full bg-slate-900 dark:bg-white text-white dark:text-slate-900 py-3 rounded-lg font-semibold hover:bg-slate-800 dark:hover:bg-slate-100 transition-colors">
                Get Started
              </button>
            </div>

            {/* Growth Tier */}
            <div className="bg-gradient-to-b from-blue-600 to-indigo-600 p-8 rounded-2xl border-2 border-blue-400 relative transform scale-105">
              <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                <span className="bg-yellow-400 text-slate-900 px-4 py-1 rounded-full text-sm font-bold">
                  MOST POPULAR
                </span>
              </div>
              <h3 className="text-2xl font-bold text-white mb-2">Growth</h3>
              <div className="mb-6">
                <span className="text-4xl font-bold text-white">$5,000</span>
                <span className="text-blue-100">/month</span>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-start">
                  <CheckCircle2 className="w-5 h-5 mr-3 text-blue-100 flex-shrink-0 mt-0.5" />
                  <span className="text-white">3 fine-tuned models</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle2 className="w-5 h-5 mr-3 text-blue-100 flex-shrink-0 mt-0.5" />
                  <span className="text-white">Cloud or on-prem deployment</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle2 className="w-5 h-5 mr-3 text-blue-100 flex-shrink-0 mt-0.5" />
                  <span className="text-white">10M tokens/month included</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle2 className="w-5 h-5 mr-3 text-blue-100 flex-shrink-0 mt-0.5" />
                  <span className="text-white">Priority support</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle2 className="w-5 h-5 mr-3 text-blue-100 flex-shrink-0 mt-0.5" />
                  <span className="text-white">Custom integrations</span>
                </li>
              </ul>
              <button className="w-full bg-white text-blue-600 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors">
                Get Started
              </button>
            </div>

            {/* Enterprise Tier */}
            <div className="bg-white dark:bg-slate-800 p-8 rounded-2xl border border-slate-200 dark:border-slate-700">
              <h3 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">Enterprise</h3>
              <div className="mb-6">
                <span className="text-4xl font-bold text-slate-900 dark:text-white">Custom</span>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-start">
                  <CheckCircle2 className="w-5 h-5 mr-3 text-green-600 flex-shrink-0 mt-0.5" />
                  <span className="text-slate-600 dark:text-slate-400">Unlimited models</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle2 className="w-5 h-5 mr-3 text-green-600 flex-shrink-0 mt-0.5" />
                  <span className="text-slate-600 dark:text-slate-400">On-premise deployment</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle2 className="w-5 h-5 mr-3 text-green-600 flex-shrink-0 mt-0.5" />
                  <span className="text-slate-600 dark:text-slate-400">Unlimited usage</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle2 className="w-5 h-5 mr-3 text-green-600 flex-shrink-0 mt-0.5" />
                  <span className="text-slate-600 dark:text-slate-400">Dedicated support</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle2 className="w-5 h-5 mr-3 text-green-600 flex-shrink-0 mt-0.5" />
                  <span className="text-slate-600 dark:text-slate-400">SLA guarantees</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle2 className="w-5 h-5 mr-3 text-green-600 flex-shrink-0 mt-0.5" />
                  <span className="text-slate-600 dark:text-slate-400">Custom development</span>
                </li>
              </ul>
              <button className="w-full bg-slate-900 dark:bg-white text-white dark:text-slate-900 py-3 rounded-lg font-semibold hover:bg-slate-800 dark:hover:bg-slate-100 transition-colors">
                Contact Sales
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-blue-600 to-indigo-600">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Ready to own your AI?
          </h2>
          <p className="text-xl text-blue-100 mb-10">
            Join forward-thinking enterprises who've taken control of their AI destiny.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-blue-50 transition-colors">
              Start Free Trial
            </button>
            <button className="bg-transparent border-2 border-white text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-white/10 transition-colors">
              Schedule Demo
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-900 text-slate-400 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <h3 className="text-white font-bold text-xl mb-4">OWN-AI</h3>
              <p className="text-sm">
                Enterprise AI fine-tuning as a service. Own your data, own your AI.
              </p>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white">Features</a></li>
                <li><a href="#" className="hover:text-white">Pricing</a></li>
                <li><a href="#" className="hover:text-white">Documentation</a></li>
                <li><a href="#" className="hover:text-white">API Reference</a></li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white">About</a></li>
                <li><a href="#" className="hover:text-white">Blog</a></li>
                <li><a href="#" className="hover:text-white">Careers</a></li>
                <li><a href="#" className="hover:text-white">Contact</a></li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Legal</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white">Privacy</a></li>
                <li><a href="#" className="hover:text-white">Terms</a></li>
                <li><a href="#" className="hover:text-white">Security</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-slate-800 pt-8 text-center text-sm">
            <p>&copy; 2024 OWN-AI. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
