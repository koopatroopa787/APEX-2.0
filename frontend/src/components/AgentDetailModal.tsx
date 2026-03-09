import React, { useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface Thought {
    time: number;
    text: string;
}

interface Agent {
    id: string;
    name: string;
    status: 'IDLE' | 'EXEC' | 'ERR_NODE';
    task: string;
    uptime: string;
    latency: string;
    thoughts: Thought[];
}

interface AgentDetailModalProps {
    agent: Agent | null;
    onClose: () => void;
}

export const AgentDetailModal: React.FC<AgentDetailModalProps> = ({ agent, onClose }) => {
    const terminalRef = useRef<HTMLDivElement>(null);

    // Auto-scroll the terminal to the bottom as new thoughts arrive
    useEffect(() => {
        if (terminalRef.current) {
            terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
        }
    }, [agent?.thoughts]);

    if (!agent) return null;

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'ERR_NODE': return 'text-[#FF3B30] border-[#FF3B30]';
            case 'EXEC': return 'text-white border-white';
            default: return 'text-slate-500 border-slate-500';
        }
    };

    const getStatusBg = (status: string) => {
        switch (status) {
            case 'ERR_NODE': return 'bg-[#FF3B30]/10';
            case 'EXEC': return 'bg-white/10';
            default: return 'bg-transparent';
        }
    };

    return (
        <AnimatePresence>
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="fixed inset-0 z-[100] flexItems-center justify-center p-4 sm:p-6"
                onClick={onClose}
            >
                {/* Extreme Blur Backdrop */}
                <div className="absolute inset-0 bg-black/60 backdrop-blur-xl" />

                {/* Modal Window */}
                <motion.div
                    initial={{ scale: 0.95, y: 20 }}
                    animate={{ scale: 1, y: 0 }}
                    exit={{ scale: 0.95, y: 20 }}
                    transition={{ type: 'spring', damping: 25, stiffness: 300 }}
                    className="relative w-full max-w-4xl h-[600px] border border-[#2A2A2A] bg-[#0A0A0A]/90 rounded-xl overflow-hidden flex flex-col shadow-2xl"
                    onClick={(e) => e.stopPropagation()} // Prevent closing when clicking inside
                >
                    {/* Header Bar */}
                    <div className="border-b border-[#2A2A2A] px-6 py-4 flex items-center justify-between bg-black/50">
                        <div className="flex items-center gap-4">
                            <div className={`px-2 py-1 border text-[10px] font-mono font-bold tracking-widest ${getStatusColor(agent.status)} ${getStatusBg(agent.status)}`}>
                                {agent.status}
                            </div>
                            <h2 className="text-white text-lg font-mono tracking-widest uppercase">{agent.name}</h2>
                        </div>
                        <button
                            onClick={onClose}
                            className="text-slate-500 hover:text-white transition-colors"
                        >
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <path d="M18 6L6 18M6 6l12 12" />
                            </svg>
                        </button>
                    </div>

                    {/* Content Split */}
                    <div className="flex-1 flex flex-col md:flex-row overflow-hidden">
                        {/* Left Pane: Metrics & Task */}
                        <div className="w-full md:w-1/3 border-r border-[#2A2A2A] p-6 flex flex-col gap-8 bg-[#050505]/50">

                            <div>
                                <p className="text-slate-500 text-[10px] font-mono tracking-wider mb-2 uppercase">Current Assignment</p>
                                <p className={`text-sm font-mono tracking-wide ${agent.status === 'ERR_NODE' ? 'text-[#FF3B30]' : 'text-slate-300'}`}>
                                    &gt; {agent.task}
                                </p>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div className="p-3 border border-[#2A2A2A] rounded bg-black/40">
                                    <p className="text-slate-500 text-[10px] font-mono tracking-wider mb-1 uppercase">Uptime</p>
                                    <p className="text-white text-xs font-mono">{agent.uptime}</p>
                                </div>
                                <div className="p-3 border border-[#2A2A2A] rounded bg-black/40">
                                    <p className="text-slate-500 text-[10px] font-mono tracking-wider mb-1 uppercase">Latency</p>
                                    <p className={`text-xs font-mono ${agent.latency === 'ERR' ? 'text-[#FF3B30]' : 'text-white'}`}>
                                        {agent.latency}
                                    </p>
                                </div>
                            </div>

                            <div className="mt-auto">
                                <p className="text-slate-600 text-[9px] font-mono uppercase tracking-widest">
                                    System Diagnostics Active
                                </p>
                            </div>
                        </div>

                        {/* Right Pane: Thought Stream Terminal */}
                        <div className="w-full md:w-2/3 flex flex-col bg-black">
                            <div className="border-b border-[#2A2A2A] px-4 py-2 bg-[#0A0A0A]">
                                <p className="text-slate-500 text-[10px] font-mono tracking-wider uppercase">Internal Thought Stream -- tail -f var/log/agent</p>
                            </div>
                            <div
                                ref={terminalRef}
                                className="flex-1 overflow-y-auto p-4 flex flex-col gap-1 font-mono text-[11px]"
                            >
                                {/* Render thoughts in reverse so newest is at the bottom, or map normally if we receive them oldest-first. 
                    Given the mock stream pushes to index 0, the first element is the newest. We should reverse it for terminal view. */}
                                {[...agent.thoughts].reverse().map((thought, idx) => {
                                    const date = new Date(thought.time);
                                    const timeString = `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}:${date.getSeconds().toString().padStart(2, '0')}.${date.getMilliseconds().toString().padStart(3, '0')}`;

                                    return (
                                        <motion.div
                                            key={`${thought.time}-${idx}`}
                                            initial={{ opacity: 0, x: -10 }}
                                            animate={{ opacity: 1, x: 0 }}
                                            className="flex gap-4"
                                        >
                                            <span className="text-slate-600 shrink-0">[{timeString}]</span>
                                            <span className={
                                                thought.text.includes('CRITICAL') || thought.text.includes('ERR')
                                                    ? 'text-[#FF3B30]'
                                                    : 'text-slate-300'
                                            }>
                                                {thought.text}
                                            </span>
                                        </motion.div>
                                    )
                                })}
                                {/* Blinking cursor at the end */}
                                <div className="flex gap-4 mt-2">
                                    <span className="text-slate-600">[{new Date().getHours().toString().padStart(2, '0')}:{new Date().getMinutes().toString().padStart(2, '0')}:--.---]</span>
                                    <span className="w-2 h-3 bg-white animate-pulse inline-block"></span>
                                </div>
                            </div>
                        </div>
                    </div>
                </motion.div>
            </motion.div>
        </AnimatePresence>
    );
};
