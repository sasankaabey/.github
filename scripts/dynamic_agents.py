#!/usr/bin/env python3
"""
Session Router Integration Helper - Uses agent_config_cli to assign tasks

This module integrates session_router with the agent configuration system,
allowing tasks to be assigned to dynamically configured agents.

Import this module in session_router.py to get dynamic agent assignment.
"""

import json
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any
from enum import Enum


class AgentType(Enum):
    """Available agent types (dynamically loaded from config)"""
    CLAUDE_CODE = "claude-code"
    CODEX = "codex"
    CHATGPT = "chatgpt"
    PERPLEXITY = "perplexity"
    GEMINI = "gemini"


class DynamicAgentManager:
    """Load and manage agents from config file"""
    
    CONFIG_FILE = Path.home() / ".config" / "session-router" / "agents.json"
    
    _instance = None
    _agents_cache = None
    
    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super(DynamicAgentManager, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def load_agents(cls) -> Dict[str, Any]:
        """Load agents from config file, with caching"""
        if cls._agents_cache is not None:
            return cls._agents_cache
        
        if not cls.CONFIG_FILE.exists():
            print(f"⚠ Agent config not found at {cls.CONFIG_FILE}")
            print("  Run: python3 ~/.github/scripts/agent_config_cli.py")
            # Fall back to empty dict
            return {}
        
        try:
            data = json.loads(cls.CONFIG_FILE.read_text())
            cls._agents_cache = data
            return data
        except Exception as e:
            print(f"✗ Failed to load agents: {e}", file=sys.stderr)
            return {}
    
    @classmethod
    def get_enabled_agents(cls, specialty: Optional[str] = None) -> List[str]:
        """Get list of enabled agent IDs, optionally filtered by specialty"""
        agents = cls.load_agents()
        enabled = [id for id, agent in agents.items() if agent.get("enabled", True)]
        
        if specialty:
            enabled = [
                id for id in enabled 
                if specialty in agent.get("specialties", [])
                for agent in [agents.get(id)]
            ]
        
        return enabled
    
    @classmethod
    def get_agent_by_specialty(cls, specialty: str) -> Optional[str]:
        """Get best agent for a specialty (first enabled one found)"""
        agents = cls.load_agents()
        for id, agent in agents.items():
            if (agent.get("enabled", True) and 
                specialty in agent.get("specialties", [])):
                return id
        return None
    
    @classmethod
    def get_best_agent_for_task(cls, task_type: str) -> Optional[str]:
        """Get best agent for task type"""
        # Map task types to specialties
        task_specialty_map = {
            "implementation": "debugging",
            "testing": "server-ops",
            "documentation": "documentation",
            "yaml": "yaml",
            "review": "review",
            "deployment": "server-ops",
            "research": "research",
            "analysis": "analysis",
            "architecture": "planning",
        }
        
        specialty = task_specialty_map.get(task_type.lower())
        if specialty:
            return cls.get_agent_by_specialty(specialty)
        
        # Default fallback
        enabled = cls.get_enabled_agents()
        return enabled[0] if enabled else None
    
    @classmethod
    def get_agent_config(cls, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get full config for an agent"""
        agents = cls.load_agents()
        return agents.get(agent_id)
    
    @classmethod
    def print_agent_summary(cls):
        """Print summary of loaded agents"""
        agents = cls.load_agents()
        enabled = len([a for a in agents.values() if a.get("enabled", True)])
        total = len(agents)
        print(f"Agents loaded: {enabled}/{total} enabled")
        
        for id, agent in sorted(agents.items()):
            status = "✓" if agent.get("enabled", True) else "✗"
            cost = agent.get("cost", "unknown")
            print(f"  {status} {id:<20} ({cost})")


def get_agent_for_decomposition(task_type: str) -> str:
    """
    Choose appropriate agent for a decomposition step
    
    Usage in TaskDecomposer:
        agent_id = get_agent_for_decomposition("implementation")
        
    Returns agent ID string, falls back to "claude-code" if unavailable
    """
    manager = DynamicAgentManager()
    agent = manager.get_best_agent_for_task(task_type)
    return agent or "claude-code"  # Fallback


# Example integration in session_router.py TaskDecomposer.decompose_task():
"""
# OLD CODE:
Subtask(
    id=f"{task.id}_implement",
    description=f"Implement: {task.name}",
    agent=AgentType.CODEX,  # Hard-coded
    estimated_minutes=task.estimated_minutes - 30,
)

# NEW CODE:
from dynamic_agents import get_agent_for_decomposition

Subtask(
    id=f"{task.id}_implement",
    description=f"Implement: {task.name}",
    agent=get_agent_for_decomposition("implementation"),  # Dynamic!
    estimated_minutes=task.estimated_minutes - 30,
)
"""
