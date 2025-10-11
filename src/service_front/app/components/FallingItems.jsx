import { useEffect, useState } from "react";

export default function FallingItems() {
  const [items, setItems] = useState([]);

  // Список картинок для падения
  const images = [
    "dog.webp",
    "dog2.webp",
    "mellstroy.gif",
    "slot.webp",
    "slot2.webp"
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      const id = Math.random().toString(36).substring(7);

      const randomImage = images[Math.floor(Math.random() * images.length)];

      const newItem = {
        id,
        left: Math.random() * window.innerWidth,
        size: 50 + Math.random() * 100,
        duration: 4 + Math.random() * 8,
        src: randomImage,
      };

      setItems(prev => [...prev, newItem]);

      setTimeout(() => {
        setItems(prev => prev.filter(c => c.id !== id));
      }, newItem.duration * 1000);
    }, 400);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="pointer-events-none fixed inset-0 overflow-hidden z-0">
      {items.map(item => (
        <img
          key={item.id}
          src={item.src}
          alt="falling item"
          className="absolute animate-fall"
          style={{
            left: item.left,
            width: item.size,
            height: item.size,
            animationDuration: `${item.duration}s`,
          }}
        />
      ))}
      <style jsx>{`
        @keyframes fall {
          0% {
            transform: translateY(-100px) rotate(0deg);
            opacity: 1;
          }
          100% {
            transform: translateY(110vh) rotate(720deg);
            opacity: 0;
          }
        }

        .animate-fall {
          animation-name: fall;
          animation-timing-function: linear;
        }
      `}</style>
    </div>
  );
}
