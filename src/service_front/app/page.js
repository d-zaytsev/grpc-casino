'use client'

import { useState } from 'react'
import LoginModal from './components/LoginModal.jsx'
import FallingItems from './components/FallingItems.jsx';
import DepositModal from './components/DepositModal.jsx';
import { getUserProfile, registerUser } from '../grpc/client.js';

export default function Home() {
  const [isLoginModalOpen, setIsLogModalOpen] = useState(false)
  const [isDepositModalOpen, setIsDepositModalOpen] = useState(false)
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [username, setUsername] = useState("")
  const [userbalance, setUserBalance] = useState("0")

  const handleLogin = (username, password) => {
    getUserProfile(username, password, (err, resp) => {
      if (err) {
        console.error('Ошибка авторизации:', err.message);
        setIsLoggedIn(false);
      } else {
        setIsLoggedIn(true);
        setUsername(username);
        setUserBalance(resp.u[2][2]);
      }
    });

    setIsLogModalOpen(false);
  }

  const handelRegister = (username, password) => {
    registerUser(username, password, (err, resp) => {
      if (err) {
        console.error('Ошибка регистрации:', err.message);
        setIsLoggedIn(false);
      } else {
            setIsLoggedIn(true);
            setUsername(username);
      }
    });

    setIsLogModalOpen(false);
  }

  const handleLogout = () => {
    setIsLoggedIn(false)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500">
      <FallingItems />  {/* Рофло эффект */}
      {/* Кнопка Выхода/Входа */}
      <div className="fixed top-6 right-6 z-10">
        {isLoggedIn ? (
          <div className="flex flex-col items-center">
          <button
            onClick={handleLogout}
            className="px-6 py-2 bg-white text-purple-600 rounded-lg font-semibold shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
          >
            Выйти
          </button>
          <span className="mt-2 text-sm text-white">
              Баланс: {userbalance}₽
            </span>
          </div>
        ) : (
            <button
              onClick={() => setIsLogModalOpen(true)}
              className="px-6 py-2 bg-white text-purple-600 rounded-lg font-semibold shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
            >
              Войти
            </button>  
        )}
      </div>

      {/* Основной контент домашней страницы */}
      <div className="flex items-center justify-center min-h-screen px-4">
        <div className="flex flex-col items-center text-center text-white max-w-2xl">
          <h1 className="text-6xl font-bold mb-4 drop-shadow-lg">
            Добро пожаловать в «DADEP Casino»
          </h1>
          <p className="text-2xl mb-6">
            {isLoggedIn ? `Привет, ${username}! Как насчёт депа?` : 'Войдите, чтобы продолжить'}
          </p>
          {isLoggedIn && (
            <button
              onClick={() => setIsDepositModalOpen(true)}
              className="mt-4 px-8 py-3 bg-white text-purple-600 rounded-lg font-semibold shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
            >
              Депнуть
            </button>
          )}
        </div>
      </div>


      {/* Модальные окна*/}
      <LoginModal
        isOpen={isLoginModalOpen}
        onClose={() => setIsLogModalOpen(false)}
        onLogin={handleLogin}
        onRegister={handelRegister}
      />
      <DepositModal
        isOpen={isDepositModalOpen}
        onClose={() => setIsDepositModalOpen(false)}
        onDeposit={(amount) => setIsDepositModalOpen(false)}
      />
    </div>
  )
}
