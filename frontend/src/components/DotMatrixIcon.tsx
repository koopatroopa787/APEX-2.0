import React, { useEffect, useRef } from 'react';

interface DotMatrixIconProps {
    type: 'clear' | 'cloudy' | 'rain' | 'snow' | 'storm' | 'alert';
    size?: number;
    color?: string;
    animate?: boolean;
}

const DotMatrixIcon: React.FC<DotMatrixIconProps> = ({
    type,
    size = 64,
    color = '#FFFFFF',
    animate = true
}) => {
    const canvasRef = useRef<HTMLCanvasElement>(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        const gridSize = 16;
        const cellSize = size / gridSize;
        const padding = cellSize * 0.2;
        const dotRadius = (cellSize - padding * 2) / 2;

        let frame = 0;

        const draw = () => {
            ctx.clearRect(0, 0, size, size);

            for (let y = 0; y < gridSize; y++) {
                for (let x = 0; x < gridSize; x++) {
                    let active = false;
                    let alpha = 0.1;

                    // Pattern logic
                    if (type === 'clear') {
                        const dx = x - 7.5;
                        const dy = y - 7.5;
                        const dist = Math.sqrt(dx * dx + dy * dy);
                        active = dist < 5 && dist > 3;
                        if (active && animate) alpha = 0.5 + Math.sin(frame * 0.1 + dist) * 0.4;
                    } else if (type === 'alert') {
                        // Triangle
                        active = (y > 4 && y < 12) && (x > 8 - (y - 4) && x < 8 + (y - 4));
                        if (active) alpha = 1.0;
                    } else {
                        // Default random atmospheric dots
                        if (Math.random() > 0.95) {
                            active = true;
                            alpha = 0.3;
                        }
                    }

                    ctx.beginPath();
                    ctx.arc(
                        x * cellSize + cellSize / 2,
                        y * cellSize + cellSize / 2,
                        dotRadius,
                        0,
                        Math.PI * 2
                    );
                    ctx.fillStyle = active ? color : `rgba(255, 255, 255, ${alpha})`;
                    ctx.globalAlpha = active ? alpha : alpha;
                    ctx.fill();
                }
            }

            if (animate) {
                frame++;
                requestAnimationFrame(draw);
            }
        };

        draw();
    }, [type, size, color, animate]);

    return (
        <canvas
            ref={canvasRef}
            width={size}
            height={size}
            className="rounded-lg"
        />
    );
};

export default DotMatrixIcon;
