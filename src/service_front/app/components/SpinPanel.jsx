"use client";

import { useEffect, useRef, useState } from "react";
import { GameServiceClient } from "../../grpc/service_game_grpc_web_pb.js";
import { SpinRequest } from "../../grpc/service_game_pb.js";

const ENVOY_ADDR =
	process.env.NEXT_PUBLIC_ENVOY_ADDR || "http://localhost:8082";

const SYMBOLS = ["🍒", "🍋", "🔔", "💎", "🍇", "🍊", "⭐", "7️⃣", "🍀", "🍔"];

export default function SpinPanel({ userUuid, onClose, onFinish }) {
	const [isSpinning, setIsSpinning] = useState(false);
	const [frames, setFrames] = useState([]);
	const [isFinal, setIsFinal] = useState(false);
	const [error, setError] = useState(null);
	const streamRef = useRef(null);
	const clientRef = useRef(null);

	useEffect(() => {
		clientRef.current = new GameServiceClient(ENVOY_ADDR, null, null);
		return () => {
			if (streamRef.current?.cancel) {
				try {
					streamRef.current.cancel();
				} catch {}
			}
		};
	}, []);

	function handleData(resp) {
		const symbols = resp.getSymbolsList();
		const final = !!resp.getIsFinal();
		setFrames((prev) => [...prev, symbols]);
		setIsFinal(final);
		if (final) {
			setIsSpinning(false);
			onFinish?.(resp);
		}
	}

	function handleError(err) {
		console.error("stream error", err);
		let msg = err?.message || err?.code || String(err);
		setError(msg);
		setIsSpinning(false);
	}

	function handleEnd() {
		setIsSpinning(false);
	}

	function startSpin() {
		setError(null);
		setFrames([]);
		setIsFinal(false);
		if (!userUuid) return setError("No user logged in");

		setIsSpinning(true);
		const client = clientRef.current;
		const req = new SpinRequest();
		req.setUserUuid(userUuid);

		try {
			const stream = client.getResults(req, {});
			streamRef.current = stream;
			stream.on("data", handleData);
			stream.on("error", handleError);
			stream.on("end", handleEnd);
		} catch (err) {
			handleError(err);
		}
	}

	const lastFrame = frames.at(-1) || null;

	return (
		<div className="relative p-6 bg-white/20 rounded-lg shadow-xl w-full max-w-2xl z-50">
			{onClose && (
				<button
					onClick={() => {
						streamRef.current?.cancel?.();
						setIsSpinning(false);
						onClose();
					}}
					aria-label="Close slot panel"
					className="absolute top-3 right-3 w-8 h-8 flex items-center justify-center bg-white/50 hover:bg-white/100 rounded-full text-gray-800 transition"
				>
					✕
				</button>
			)}

			<div className="mb-4">
				<div className="flex items-center justify-center space-x-6">
					{lastFrame ? (
						lastFrame.map((s, i) => {
							const idx = Number.isFinite(+s)
								? +s % SYMBOLS.length
								: 0;
							return (
								<div
									key={i}
									className="w-24 h-40 flex items-center justify-center bg-gray-100 rounded-lg text-5xl"
								>
									{SYMBOLS[idx]}
								</div>
							);
						})
					) : (
						<div className="text-sm text-white-500">
							Нажми Крутить, чтобы начать!
						</div>
					)}
				</div>
			</div>

			<div className="mt-4 flex justify-center">
				<button
					className="px-8 py-4 bg-green-600 hover:bg-green-700 rounded-lg disabled:opacity-50 text-white font-extrabold text-lg shadow-lg transform transition-transform hover:scale-105 duration-150"
					onClick={startSpin}
					disabled={isSpinning}
					aria-live="polite"
				>
					{isSpinning ? "Крутим..." : "Крутить"}
				</button>
			</div>

			{isFinal &&
				lastFrame?.length === 3 &&
				lastFrame[0] === lastFrame[1] &&
				lastFrame[1] === lastFrame[2] && (
					<div className="mt-4 text-yellow-500 font-bold text-center text-xl">
						ПОБЕДА!
					</div>
				)}

			{error && (
				<div className="mt-3 text-red-500 break-words text-sm">
					Error: {String(error)}
				</div>
			)}
		</div>
	);
}
