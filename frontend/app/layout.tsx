import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "OWN-AI | Enterprise AI Fine-Tuning as a Service",
  description: "Stop sending your proprietary data to OpenAI. Fine-tune and deploy private AI models on your own data. Enterprise-grade AI without the ML expertise.",
  keywords: "AI, machine learning, fine-tuning, private AI, enterprise AI, LLM, custom models",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
