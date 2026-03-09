import React from 'react';
import { useWebSocket } from '../hooks/useWebSocket';

const DashboardOverview = () => {
    const { data } = useWebSocket("ws://localhost:8000/ws");

    if (!data) return (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 animate-pulse">
            {[...Array(3)].map((_, i) => (
                <div key={i} className="glass-panel rounded-xl p-6 min-h-[160px] bg-white/5" />
            ))}
        </div>
    );

    const activeAgentsPercent = Math.round((data.current_metrics.active_agents / 5) * 100);

    return (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Active Agents */}
            <div className="glass-panel rounded-xl p-6 flex flex-col justify-between min-h-[160px]">
                <p className="text-slate-400 text-[10px] font-mono tracking-wider mb-4 uppercase">ACTIVE_AGENTS</p>
                <div className="flex items-center justify-between mt-auto">
                    <div className="-rotate-90">
                        <svg width="64" height="64" viewBox="0 0 64 64" className="overflow-visible">
                            <circle cx="32" cy="32" r="28" fill="none" stroke="#2A2A2A" strokeWidth="4" />
                            <circle cx="32" cy="32" r="28" fill="none" stroke="#FFFFFF" strokeWidth="4" strokeDasharray="6 4" strokeDashoffset="0" />
                        </svg>
                        <div className="absolute inset-0 flex items-center justify-center rotate-90">
                            <span className="material-symbols-outlined text-white text-[20px]">memory</span>
                        </div>
                    </div>
                    <p className="text-white text-5xl font-sans font-bold tracking-tight">{activeAgentsPercent}%</p>
                </div>
            </div>

            {/* Database Load */}
            <div className="glass-panel rounded-xl p-6 flex flex-col justify-between min-h-[160px]">
                <p className="text-slate-400 text-[10px] font-mono tracking-wider mb-4 uppercase">DATABASE_LOAD</p>
                <div className="mt-auto w-full">
                    <div className="flex justify-between text-[10px] font-mono text-slate-400 mb-3 uppercase">
                        <span>OPT-ROUTING</span>
                        <span>ACTIVE</span>
                    </div>
                    <div className="flex gap-1 h-3 w-full">
                        {[...Array(6)].map((_, i) => {
                            const isActive = i < Math.ceil((data.current_metrics.db_load / 100) * 6);
                            return (
                                <div
                                    key={i}
                                    className={`h-full flex-1 rounded-sm transition-colors duration-500 ${isActive ? 'bg-white' : 'bg-slate-800'}`}
                                />
                            );
                        })}
                    </div>
                </div>
            </div>

            {/* Cost Savings */}
            <div className="glass-panel rounded-xl p-6 flex flex-col justify-between min-h-[160px]">
                <p className="text-slate-400 text-[10px] font-mono tracking-wider mb-4 uppercase">COST_SAVINGS</p>
                <div className="mt-auto">
                    <div className="flex items-center gap-1 text-green-400 mb-1">
                        <span className="material-symbols-outlined text-[14px]">trending_up</span>
                        <span className="text-[12px] font-mono font-bold">+12.4%</span>
                    </div>
                    <p className="text-white text-4xl font-sans font-bold tracking-tight">
                        +${(data.current_metrics.cost_savings_usd / 1000).toFixed(1)}k
                    </p>
                </div>
            </div>
        </div>
    );
};

export default DashboardOverview;
