'use client'

import { useState } from 'react'
import LoginModal from './components/LoginModal.jsx'

export default function Home() {
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [username, setUsername] = useState("-")

  const handleLogin = (username, password) => {
    // TODO: логика входа
    setUsername(username)
    setIsLoggedIn(true)
    setIsModalOpen(false)
  }

  const handleLogout = () => {
    setIsLoggedIn(false)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500">
      {/* Кнопка Выхода/Входа */}
      <div className="fixed top-6 right-6 z-10">
        {isLoggedIn ? (
          <button
            onClick={handleLogout}
            className="px-6 py-2 bg-white text-purple-600 rounded-lg font-semibold shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
          >
            Выйти
          </button>
        ) : (
          <button
            onClick={() => setIsModalOpen(true)}
            className="px-6 py-2 bg-white text-purple-600 rounded-lg font-semibold shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
          >
            Войти
          </button>
        )}
      </div>

      {/* Основной контент домашней страницы */}
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center text-white">
          <h1 className="text-6xl font-bold mb-4 drop-shadow-lg">
             Добро пожаловать
          </h1>
          <p className="text-xl opacity-90">
            {isLoggedIn ? `Привет, ${username}!` : 'Войдите, чтобы продолжить'}
          </p>
        </div>
      </div>

      {/* Модальное окно входа */}
      <LoginModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onLogin={handleLogin}
      />
    </div>
  )
}
