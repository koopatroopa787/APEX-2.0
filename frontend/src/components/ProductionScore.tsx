import React from 'react';
import { CircularDotMatrix } from './NothingGauges';
import { motion } from 'framer-motion';

const ProductionScore = ({ data }: { data: any }) => {
    if (!data) return null;

    const score = data.readiness_score;
    const isAlert = data.status === "RED";

    return (
        <div className="flex flex-col items-center justify-center py-4 h-full">
            <div className="relative">
                <CircularDotMatrix
                    value={score}
                    size={200}
                    label="SURVIVAL_PROB"
                />

                {/* Decorative scanning line */}
                <div className="absolute inset-0 pointer-events-none rounded-full overflow-hidden">
                    <motion.div
                        className="w-full h-[1px] bg-white opacity-20 shadow-[0_0_15px_white]"
                        animate={{ top: ['0%', '100%'] }}
                        transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
                        style={{ position: 'absolute' }}
                    />
                </div>
            </div>

            <div className="mt-8 grid grid-cols-2 gap-x-8 gap-y-2 w-full max-w-[200px]">
                <div className="flex flex-col">
                    <span className="nothing-text-label text-[8px] opacity-30">STATUS</span>
                    <span className={`text-[10px] font-black tracking-widest ${isAlert ? 'text-[#FF3B30]' : 'text-white'}`}>
                        {data.status}_READY
                    </span>
                </div>
                <div className="flex flex-col text-right">
                    <span className="nothing-text-label text-[8px] opacity-30">NODES</span>
                    <span className="text-[10px] font-black tracking-widest text-white">4_ACTIVE</span>
                </div>
                <div className="col-span-2 pt-2 border-t border-white/5 mt-2">
                    <p className="text-[9px] text-white/30 font-mono italic leading-tight uppercase">
                        Optimization logic: Cox Actuarial Drift. Reliability targeted @ 0.999.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default ProductionScore;
