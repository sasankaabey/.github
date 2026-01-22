#!/usr/bin/env python3
"""
Agent Configuration CLI - Manage available AI agents for task routing

Provides interactive menu and CLI commands to:
- List available agents with specialties and costs
- Add custom agents or services
- Enable/disable agents
- Remove agents  
- Test agent availability
- Export configuration

Usage:
    python agent_config_cli.py                  # Interactive menu
    python agent_config_cli.py list            # List all agents
    python agent_config_cli.py add             # Add new agent (interactive)
    python agent_config_cli.py enable <id>     # Enable agent
    python agent_config_cli.py disable <id>    # Disable agent
    python agent_config_cli.py remove <id>     # Remove agent (interactive)
    python agent_config_cli.py test <id>       # Test agent
    python agent_config_cli.py export          # Export to JSON
    python agent_config_cli.py read-config     # Show current config
    
See AGENTS.md for how session_router uses this configuration.
"""

import json
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import List, Optional, Dict, Any
from enum import Enum


class AgentCost(Enum):
    """Cost categories for agents"""
    FREE = "free"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CUSTOM = "custom"


@dataclass
class Agent:
    """Represents an available AI agent or service"""
    id: str                              # Unique identifier (e.g., "claude-code")
    name: str                            # Display name
    description: str                     # What it does
    enabled: bool = True                 # Currently available?
    cost: str = "free"                   # Cost category
    specialties: List[str] = field(default_factory=list)  # e.g., ["server-ops", "debugging"]
    api_key_required: bool = False       # Does it need credentials?
    endpoint: Optional[str] = None       # API endpoint (if applicable)
    notes: str = ""                      # Additional notes
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Agent":
        """Create from dictionary"""
        return cls(**data)


class AgentConfig:
    """Manages agent configuration file"""
    
    CONFIG_DIR = Path.home() / ".config" / "session-router"
    CONFIG_FILE = CONFIG_DIR / "agents.json"
    
    # Default agents pre-configured
    DEFAULT_AGENTS = {
        "claude-code": Agent(
            id="claude-code",
            name="Claude (Code Interpreter)",
            description="Server operations, SSH, debugging, entity registry edits",
            enabled=True,
            cost="high",
            specialties=["server-ops", "debugging", "ssh", "ha-deployment"],
            api_key_required=False,
            notes="Expert-level capability, use for critical operations"
        ),
        "codex": Agent(
            id="codex",
            name="Codex",
            description="Documentation, YAML drafting, linting, refactoring",
            enabled=True,
            cost="low",
            specialties=["documentation", "yaml", "formatting", "review"],
            api_key_required=False,
            notes="Cost-optimized for drafting and documentation"
        ),
        "chatgpt": Agent(
            id="chatgpt",
            name="ChatGPT",
            description="Planning, architecture review, general questions",
            enabled=True,
            cost="medium",
            specialties=["planning", "architecture", "review", "brainstorm"],
            api_key_required=True,
            notes="General-purpose, good for cross-cutting concerns"
        ),
        "perplexity": Agent(
            id="perplexity",
            name="Perplexity",
            description="Research, finding documentation and solutions",
            enabled=True,
            cost="medium",
            specialties=["research", "docs", "external-knowledge"],
            api_key_required=True,
            notes="Specialized for research and citations"
        ),
        "gemini": Agent(
            id="gemini",
            name="Gemini",
            description="Large document analysis, summarization",
            enabled=True,
            cost="medium",
            specialties=["analysis", "summarization", "large-docs"],
            api_key_required=True,
            notes="Good for analyzing large files and reports"
        ),
    }
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.load_or_create()
    
    def load_or_create(self) -> None:
        """Load existing config or create with defaults"""
        if self.CONFIG_FILE.exists():
            self.load()
        else:
            self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            self.agents = {id: agent for id, agent in self.DEFAULT_AGENTS.items()}
            self.save()
            print(f"✓ Created default config at {self.CONFIG_FILE}")
    
    def load(self) -> None:
        """Load agents from config file"""
        try:
            data = json.loads(self.CONFIG_FILE.read_text())
            self.agents = {
                id: Agent.from_dict(agent_data)
                for id, agent_data in data.items()
            }
            print(f"✓ Loaded {len(self.agents)} agents from config")
        except Exception as e:
            print(f"✗ Failed to load config: {e}")
            self.agents = {id: agent for id, agent in self.DEFAULT_AGENTS.items()}
    
    def save(self) -> None:
        """Save agents to config file"""
        self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        data = {id: agent.to_dict() for id, agent in self.agents.items()}
        self.CONFIG_FILE.write_text(json.dumps(data, indent=2))
        print(f"✓ Saved {len(self.agents)} agents to config")
    
    def list_agents(self, show_all: bool = False) -> None:
        """Display all agents in formatted table"""
        if not self.agents:
            print("No agents configured")
            return
        
        print("\n" + "=" * 100)
        print(f"{'ID':<20} {'Name':<25} {'Cost':<10} {'Status':<10} {'Specialties':<30}")
        print("=" * 100)
        
        for id, agent in sorted(self.agents.items()):
            if not show_all and not agent.enabled:
                continue
            
            status = "✓ Enabled" if agent.enabled else "✗ Disabled"
            specs = ", ".join(agent.specialties[:2]) if agent.specialties else "—"
            
            print(f"{id:<20} {agent.name:<25} {agent.cost:<10} {status:<10} {specs:<30}")
        
        print("=" * 100 + "\n")
    
    def add_agent_interactive(self) -> None:
        """Interactive prompt to add new agent"""
        print("\n--- Add New Agent ---")
        
        agent_id = input("Agent ID (e.g., 'my-llm'): ").strip().lower()
        if agent_id in self.agents:
            print(f"✗ Agent '{agent_id}' already exists")
            return
        
        name = input("Display name: ").strip()
        description = input("Description: ").strip()
        cost = input(f"Cost [{'/'.join([c.value for c in AgentCost])}]: ").strip().lower()
        if cost not in [c.value for c in AgentCost]:
            cost = "medium"
        
        specialties_str = input("Specialties (comma-separated, e.g., 'docs,yaml,review'): ").strip()
        specialties = [s.strip() for s in specialties_str.split(",") if s.strip()]
        
        api_key = input("Requires API key? (y/n) [n]: ").strip().lower() == 'y'
        notes = input("Notes (optional): ").strip()
        
        agent = Agent(
            id=agent_id,
            name=name,
            description=description,
            enabled=True,
            cost=cost,
            specialties=specialties,
            api_key_required=api_key,
            notes=notes
        )
        
        self.agents[agent_id] = agent
        self.save()
        print(f"✓ Added agent '{agent_id}'")
    
    def remove_agent(self, agent_id: str) -> None:
        """Remove an agent"""
        if agent_id not in self.agents:
            print(f"✗ Agent '{agent_id}' not found")
            return
        
        agent = self.agents[agent_id]
        confirm = input(f"Remove agent '{agent.name}'? (y/n): ").strip().lower()
        if confirm == 'y':
            del self.agents[agent_id]
            self.save()
            print(f"✓ Removed agent '{agent_id}'")
    
    def enable_agent(self, agent_id: str) -> None:
        """Enable an agent"""
        if agent_id not in self.agents:
            print(f"✗ Agent '{agent_id}' not found")
            return
        
        self.agents[agent_id].enabled = True
        self.save()
        print(f"✓ Enabled agent '{agent_id}'")
    
    def disable_agent(self, agent_id: str) -> None:
        """Disable an agent"""
        if agent_id not in self.agents:
            print(f"✗ Agent '{agent_id}' not found")
            return
        
        self.agents[agent_id].enabled = False
        self.save()
        print(f"✓ Disabled agent '{agent_id}'")
    
    def get_enabled_agents(self, specialty: Optional[str] = None) -> List[Agent]:
        """Get list of enabled agents, optionally filtered by specialty"""
        agents = [a for a in self.agents.values() if a.enabled]
        
        if specialty:
            agents = [a for a in agents if specialty in a.specialties]
        
        return agents
    
    def test_agent(self, agent_id: str) -> None:
        """Test agent availability"""
        if agent_id not in self.agents:
            print(f"✗ Agent '{agent_id}' not found")
            return
        
        agent = self.agents[agent_id]
        
        if not agent.enabled:
            print(f"✗ Agent '{agent.name}' is disabled")
            return
        
        if agent.api_key_required:
            # Check for environment variable or config
            env_var = f"{agent_id.upper()}_API_KEY"
            from os import getenv
            if not getenv(env_var):
                print(f"⚠ Agent '{agent.name}' requires API key in {env_var}")
                return
        
        print(f"✓ Agent '{agent.name}' is available")
    
    def export_config(self) -> str:
        """Export config as JSON string"""
        data = {id: agent.to_dict() for id, agent in self.agents.items()}
        return json.dumps(data, indent=2)
    
    def show_menu(self) -> None:
        """Interactive menu"""
        while True:
            print("\n" + "=" * 60)
            print("Agent Configuration Manager")
            print("=" * 60)
            print("1. List agents")
            print("2. Add agent")
            print("3. Enable agent")
            print("4. Disable agent")
            print("5. Remove agent")
            print("6. Test agent")
            print("7. Export config")
            print("8. Reset to defaults")
            print("0. Exit")
            print("=" * 60)
            
            choice = input("Select option: ").strip()
            
            if choice == "1":
                self.list_agents(show_all=True)
            
            elif choice == "2":
                self.add_agent_interactive()
            
            elif choice == "3":
                agent_id = input("Agent ID to enable: ").strip()
                self.enable_agent(agent_id)
            
            elif choice == "4":
                agent_id = input("Agent ID to disable: ").strip()
                self.disable_agent(agent_id)
            
            elif choice == "5":
                self.remove_agent(input("Agent ID to remove: ").strip())
            
            elif choice == "6":
                agent_id = input("Agent ID to test: ").strip()
                self.test_agent(agent_id)
            
            elif choice == "7":
                print("\n" + self.export_config() + "\n")
            
            elif choice == "8":
                confirm = input("Reset to default agents? (y/n): ").strip().lower()
                if confirm == 'y':
                    self.agents = {id: agent for id, agent in self.DEFAULT_AGENTS.items()}
                    self.save()
                    print("✓ Reset to defaults")
            
            elif choice == "0":
                print("Goodbye!")
                break
            
            else:
                print("✗ Invalid option")


def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Manage AI agents for task routing"
    )
    parser.add_argument("command", nargs="?", default="menu",
                       help="Command: menu, list, add, enable, disable, remove, test, export, read-config")
    parser.add_argument("agent_id", nargs="?",
                       help="Agent ID for enable/disable/remove/test")
    
    args = parser.parse_args()
    config = AgentConfig()
    
    if args.command == "menu":
        config.show_menu()
    elif args.command == "list":
        config.list_agents(show_all=True)
    elif args.command == "add":
        config.add_agent_interactive()
    elif args.command == "enable":
        if not args.agent_id:
            print("✗ Specify agent ID")
            sys.exit(1)
        config.enable_agent(args.agent_id)
    elif args.command == "disable":
        if not args.agent_id:
            print("✗ Specify agent ID")
            sys.exit(1)
        config.disable_agent(args.agent_id)
    elif args.command == "remove":
        if not args.agent_id:
            config.remove_agent(input("Agent ID to remove: ").strip())
        else:
            config.remove_agent(args.agent_id)
    elif args.command == "test":
        if not args.agent_id:
            print("✗ Specify agent ID")
            sys.exit(1)
        config.test_agent(args.agent_id)
    elif args.command == "export":
        print(config.export_config())
    elif args.command == "read-config":
        print(f"Config file: {config.CONFIG_FILE}")
        print(f"Enabled agents: {len(config.get_enabled_agents())}/{len(config.agents)}")
        config.list_agents(show_all=True)
    else:
        print(f"✗ Unknown command: {args.command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
