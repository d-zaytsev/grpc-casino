import './globals.css'

export const metadata = {
  title: 'DADEP Casino',
  description: 'Fake online casino',
}

export default function RootLayout({ children }) {
  return (
    <html lang="ru">
      <body>{children}</body>
    </html>
  )
}