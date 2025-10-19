"use client";

import { useState } from "react";
import LoginModal from "./components/LoginModal.jsx";
import DepositModal from "./components/DepositModal.jsx";
import SpinPanel from "./components/SpinPanel.jsx";
import FallingItems from "./components/FallingItems.jsx";
import { getUserProfile, registerUser } from "../grpc/user_profile_client.js";
import { deposit } from "../grpc/money_transaction_client.js";

export default function Home() {
	const [modal, setModalDialog] = useState({ login: false, deposit: false });
	const [showSpinPanel, setShowSpinPanel] = useState(false);
	const [user, setUser] = useState({
		username: "",
		password: "",
		balance: 0,
		uuid: "",
		isLoggedIn: false,
	});

	const handleAuth = (action, username, password) => {
		const callback = action === "login" ? getUserProfile : registerUser;
		callback(username, password, (err, resp) => {
			if (err) {
				console.error(
					`Ошибка ${
						action === "login" ? "авторизации" : "регистрации"
					}:`,
					err.message
				);
				setUser({
					username: "",
					password: "",
					balance: 0,
					uuid: "",
					isLoggedIn: false,
				});
			} else {
				const userProfile = resp.getUserProfile();
				const uuid = userProfile.getUuid();
				const balance = userProfile.getBalance();

				console.log("Успешная авторизация:", {
					username,
					uuid,
					balance,
				});

				setUser({
					username,
					password,
					balance: Number(balance),
					uuid,
					isLoggedIn: true,
				});
				setModalDialog((prev) => ({ ...prev, login: false }));
			}
		});
	};

	const refreshBalance = () => {
		if (!user.isLoggedIn || !user.username) return;
		getUserProfile(user.username, user.password, (err, resp) => {
			if (err) {
				console.warn(
					"Не удалось обновить профиль:",
					err && err.message
				);
				return;
			}
			try {
				const up = resp.getUserProfile();
				const balance = Number(
					up?.getBalance?.() ?? up?.getBalance ?? 0
				);
				setUser((prev) => ({ ...prev, balance: Number(balance) }));
			} catch (e) {
				const userProfile = resp.getUserProfile
					? resp.getUserProfile()
					: null;
				if (
					userProfile &&
					typeof userProfile.getBalance === "function"
				) {
					setUser((prev) => ({
						...prev,
						balance: Number(userProfile.getBalance()),
					}));
				}
			}
		});
	};

	const handleLogout = () => {
		setShowSpinPanel(false);
		setUser({
			username: "",
			password: "",
			balance: 0,
			uuid: "",
			isLoggedIn: false,
		});
	};

	const handleDeposit = (amount) => {
		deposit(user.username, user.password, amount, (err, resp) => {
			if (err) {
				console.error("Ошибка депозита:", err.message);
				setUser((prev) => ({ ...prev, isLoggedIn: false }));
			} else {
				setUser((prev) => ({
					...prev,
					balance: prev.balance + amount,
				}));
				setModalDialog((prev) => ({ ...prev, deposit: false }));
			}
		});
	};

	return (
		<div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500">
			<FallingItems />

			<div className="fixed top-6 right-6 z-10">
				{user.isLoggedIn ? (
					<div className="flex flex-col items-center">
						<button
							onClick={handleLogout}
							className="px-6 py-2 bg-white text-purple-600 rounded-lg font-semibold shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
						>
							Выйти
						</button>
						<span className="mt-2 text-sm text-white">
							Баланс: {user.balance}₽
						</span>
					</div>
				) : (
					<button
						onClick={() =>
							setModalDialog((prev) => ({ ...prev, login: true }))
						}
						className="px-6 py-2 bg-white text-purple-600 rounded-lg font-semibold shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
					>
						Войти
					</button>
				)}
			</div>

			<div className="flex items-center justify-center min-h-screen px-4">
				<div className="flex flex-col items-center text-center text-white max-w-3xl w-full">
					<h1 className="text-6xl font-bold mb-4 drop-shadow-lg">
						Добро пожаловать в «DADEP Casino»
					</h1>
					<p className="text-2xl mb-6">
						{user.isLoggedIn
							? `Привет, ${user.username}! Как насчёт депа?`
							: "Войдите, чтобы продолжить"}
					</p>

					{user.isLoggedIn && (
						<>
							<div className="flex gap-4 mb-6">
								<button
									onClick={() =>
										setModalDialog((prev) => ({
											...prev,
											deposit: true,
										}))
									}
									className="mt-4 px-8 py-3 bg-white text-purple-600 rounded-lg font-semibold shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
								>
									Депнуть
								</button>
								<button
									onClick={() => setShowSpinPanel((s) => !s)}
									className="mt-4 px-8 py-3 bg-yellow-400 text-purple-600 rounded-lg font-semibold shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
								>
									Крутить
								</button>
							</div>

							{showSpinPanel && user.uuid && (
								<div className="w-full flex justify-center">
									<SpinPanel
										userUuid={user.uuid}
										onClose={() => setShowSpinPanel(false)}
										onFinish={() => {
											refreshBalance();
										}}
									/>
								</div>
							)}
						</>
					)}
				</div>
			</div>

			<LoginModal
				isOpen={modal.login}
				onClose={() =>
					setModalDialog((prev) => ({ ...prev, login: false }))
				}
				onLogin={(u, p) => handleAuth("login", u, p)}
				onRegister={(u, p) => handleAuth("register", u, p)}
			/>

			<DepositModal
				isOpen={modal.deposit}
				onClose={() =>
					setModalDialog((prev) => ({ ...prev, deposit: false }))
				}
				onDeposit={handleDeposit}
			/>
		</div>
	);
}
