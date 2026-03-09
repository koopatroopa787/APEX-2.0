import React from 'react';
import { motion } from 'framer-motion';

interface Agent {
    id: string;
    name: string;
    status: 'IDLE' | 'EXEC' | 'ERR_NODE';
}

export const AgentRegistry: React.FC<{ agents?: Agent[], onSelect?: (agent: Agent) => void }> = ({ agents = [], onSelect }) => {
    return (
        <div className="flex flex-col">
            {agents.map((agent, i) => (
                <div
                    key={agent.id}
                    onClick={() => onSelect && onSelect(agent)}
                    className={`flex items-center justify-between py-3 px-4 transition-colors cursor-pointer ${agent.status === 'ERR_NODE'
                        ? 'bg-[#FF3B30]/10'
                        : 'hover:bg-white/5'
                        }`}
                >
                    <div className="flex items-center gap-3">
                        {/* Icons */}
                        <div className="w-4 flex justify-center">
                            {agent.status === 'IDLE' && (
                                <div className="w-[6px] h-[6px] rounded-full bg-white"></div>
                            )}
                            {agent.status === 'EXEC' && (
                                <div className="w-[10px] h-[10px] rounded-full border-[1.5px] border-white flex items-center justify-center">
                                    <div className="w-[3px] h-[3px] bg-white rounded-full"></div>
                                </div>
                            )}
                            {agent.status === 'ERR_NODE' && (
                                <div className="w-0 h-0 border-l-[5px] border-l-transparent border-r-[5px] border-r-transparent border-b-[8px] border-b-[#FF3B30]"></div>
                            )}
                        </div>

                        <span className={`text-[11px] font-mono tracking-wider ${agent.status === 'ERR_NODE' ? 'text-[#FF3B30] font-bold' :
                            'text-white font-bold'
                            }`}>
                            {agent.name}
                        </span>
                    </div>

                    <span className={`text-[10px] font-mono tracking-wider uppercase ${agent.status === 'ERR_NODE' ? 'text-[#FF3B30]' :
                        agent.status === 'EXEC' ? 'text-white' : 'text-slate-500'
                        }`}>
                        {agent.status}
                    </span>
                </div>
            ))}
        </div>
    );
};
