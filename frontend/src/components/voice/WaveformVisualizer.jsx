import React, { useEffect, useRef } from 'react';

export default function WaveformVisualizer() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    let animationId;
    let bars = Array(20).fill(0).map(() => Math.random());

    const animate = () => {
      ctx.clearRect(0, 0, width, height);

      // Update bars
      bars = bars.map((bar) => {
        const newHeight = bar + (Math.random() - 0.5) * 0.3;
        return Math.max(0.1, Math.min(1, newHeight));
      });

      // Draw bars
      const barWidth = width / bars.length;
      bars.forEach((bar, index) => {
        const barHeight = bar * height * 0.8;
        const x = index * barWidth;
        const y = (height - barHeight) / 2;

        // Gradient
        const gradient = ctx.createLinearGradient(0, y, 0, y + barHeight);
        gradient.addColorStop(0, '#3949AB');
        gradient.addColorStop(1, '#1A237E');

        ctx.fillStyle = gradient;
        ctx.fillRect(x + 2, y, barWidth - 4, barHeight);
      });

      animationId = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      if (animationId) {
        cancelAnimationFrame(animationId);
      }
    };
  }, []);

  return (
    <div className="w-80 h-48 bg-nyaya-blue rounded-2xl p-6 shadow-2xl">
      <canvas
        ref={canvasRef}
        width={280}
        height={120}
        className="w-full h-full"
      />
    </div>
  );
}
