import React from 'react';
import { motion } from 'framer-motion';

interface DotMatrixGaugeProps {
    value: number;
    label: string;
    sublabel?: string;
    segments?: number;
    color?: string;
}

export const DotMatrixGauge: React.FC<DotMatrixGaugeProps> = ({
    value,
    label,
    sublabel,
    segments = 20,
    color = '#FFFFFF'
}) => {
    const activeSegments = Math.round((value / 100) * segments);

    return (
        <div className="flex flex-col">
            <div className="flex justify-between items-end mb-2">
                <span className="nothing-text-label">{label}</span>
                <span className="text-white font-mono text-xl font-bold">{value}%</span>
            </div>

            <div className="flex gap-[2px] h-4">
                {[...Array(segments)].map((_, i) => (
                    <motion.div
                        key={i}
                        initial={{ opacity: 0.1 }}
                        animate={{
                            backgroundColor: i < activeSegments ? color : 'rgba(255, 255, 255, 0.05)',
                            opacity: i < activeSegments ? 1 : 0.2,
                            boxShadow: i < activeSegments ? `0 0 8px ${color}` : 'none'
                        }}
                        transition={{ delay: i * 0.02, duration: 0.5 }}
                        className="w-full rounded-[1px]"
                    />
                ))}
            </div>

            {sublabel && (
                <span className="text-[10px] text-white/30 tracking-widest mt-2 uppercase font-mono">
                    {sublabel}
                </span>
            )}
        </div>
    );
};

export const CircularDotMatrix: React.FC<{ value: number; size?: number; label: string }> = ({
    value,
    size = 120,
    label
}) => {
    const radius = size / 2 - 10;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (value / 100) * circumference;

    return (
        <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
            <svg width={size} height={size} className="transform -rotate-90">
                <circle
                    cx={size / 2}
                    cy={size / 2}
                    r={radius}
                    stroke="rgba(255, 255, 255, 0.05)"
                    strokeWidth="4"
                    fill="none"
                    strokeDasharray="4 4"
                />
                <motion.circle
                    cx={size / 2}
                    cy={size / 2}
                    r={radius}
                    stroke="white"
                    strokeWidth="4"
                    fill="none"
                    strokeDasharray={circumference}
                    initial={{ strokeDashoffset: circumference }}
                    animate={{ strokeDashoffset: offset }}
                    transition={{ duration: 1.5, ease: "easeOut" }}
                    strokeLinecap="round"
                />
            </svg>
            <div className="absolute flex flex-col items-center">
                <span className="text-2xl font-black font-mono">{value}%</span>
                <span className="nothing-text-label text-[8px] opacity-40">{label}</span>
            </div>
        </div>
    );
};
