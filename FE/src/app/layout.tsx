import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { APP_CONFIG } from '@/constants'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: APP_CONFIG.NAME,
  description: 'AI-powered chatbot for Shopify Community data',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
