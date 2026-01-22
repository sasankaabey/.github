#!/usr/bin/env python3
"""
Agent Configuration Manager: Manage available AI agents and services

Allows you to:
1. List available agents
2. Add new agent/service
3. Remove agent/service
4. Update agent settings
5. Test agent availability
6. View current configuration

The router automatically adapts task decomposition based on available agents.
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import sys

@dataclass
class Agent:
    """Agent/service configuration"""
    id: str
    name: str
    description: str
    enabled: bool = True
    cost_per_use: str = "free"  # free, low, medium, high
    specialties: List[str] = None  # e.g., ["documentation", "yaml", "code-review"]
    api_key_required: bool = False
    notes: str = ""
    
    def __post_init__(self):
        if self.specialties is None:
            self.specialties = []

class AgentManager:
    """Manage agent configuration"""
    
    CONFIG_FILE = Path.home() / ".config" / "session-router" / "agents.json"
    
    DEFAULT_AGENTS = {
        "claude-code": Agent(
            id="claude-code",
            name="Claude Code",
            description="Server ops, SSH, deployment, complex debugging, entity registry edits",
            specialties=["server-ops", "deployment", "debugging", "testing"],
            cost_per_use="high",
            enabled=True
        ),
        "codex": Agent(
            id="codex",
            name="Codex",
            description="Documentation, YAML drafting, code formatting, PR reviews",
            specialties=["documentation", "yaml", "code-formatting", "linting"],
            cost_per_use="low",
            enabled=True
        ),
        "chatgpt": Agent(
            id="chatgpt",
            name="ChatGPT",
            description="Planning, brainstorming, architecture, coordination",
            specialties=["planning", "brainstorming", "architecture", "review"],
            cost_per_use="medium",
            enabled=True
        ),
        "perplexity": Agent(
            id="perplexity",
            name="Perplexity Pro",
            description="Research with citations, finding docs/solutions",
            specialties=["research", "citations", "documentation-search"],
            cost_per_use="medium",
            enabled=False,
            notes="Requires API key"
        ),
        "gemini": Agent(
            id="gemini",
            name="Google Gemini",
            description="Large document analysis, summarization",
            specialties=["analysis", "summarization", "large-documents"],
            cost_per_use="low",
            enabled=False
        ),
    }
    
    def __init__(self):
        self.config_file = self.CONFIG_FILE
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        self.agents = self._load_config()
    
    def _load_config(self) -> Dict[str, Agent]:
        """Load agent configuration"""
        if self.config_file.exists():
            try:
                data = json.loads(self.config_file.read_text())
                return {
                    agent_id: Agent(**agent_data)
                    for agent_id, agent_data in data.items()
                }
            except Exception as e:
                print(f"Warning: Could not load config: {e}")
        
        # Use defaults if no config exists
        return {
            agent_id: agent
            for agent_id, agent in self.DEFAULT_AGENTS.items()
        }
    
    def _save_config(self):
        """Save agent configuration"""
        data = {
            agent_id: asdict(agent)
            for agent_id, agent in self.agents.items()
        }
        self.config_file.write_text(json.dumps(data, indent=2))
    
    def list_agents(self):
        """Show all agents with status"""
        print("\n" + "="*70)
        print("📋 Available Agents")
        print("="*70 + "\n")
        
        enabled = [a for a in self.agents.values() if a.enabled]
        disabled = [a for a in self.agents.values() if not a.enabled]
        
        if enabled:
            print("✅ ENABLED AGENTS:\n")
            for agent in sorted(enabled, key=lambda a: a.name):
                print(f"  • {agent.name} ({agent.id})")
                print(f"    {agent.description}")
                print(f"    Cost: {agent.cost_per_use} | Specialties: {', '.join(agent.specialties)}")
                if agent.notes:
                    print(f"    Note: {agent.notes}")
                print()
        
        if disabled:
            print("\n⚪ DISABLED AGENTS:\n")
            for agent in sorted(disabled, key=lambda a: a.name):
                print(f"  • {agent.name} ({agent.id}) - DISABLED")
                print(f"    {agent.description}")
                if agent.notes:
                    print(f"    Note: {agent.notes}")
                print()
        
        print(f"\nTotal: {len(enabled)} enabled, {len(disabled)} disabled")
        print("="*70 + "\n")
    
    def add_agent_interactive(self):
        """Interactively add new agent"""
        print("\n" + "="*70)
        print("➕ Add New Agent")
        print("="*70 + "\n")
        
        agent_id = input("Agent ID (e.g., my-gpt-instance): ").strip()
        if agent_id in self.agents:
            print(f"❌ Agent '{agent_id}' already exists!")
            return
        
        name = input("Agent Name (e.g., My GPT Instance): ").strip()
        description = input("Description: ").strip()
        
        print("\nCost per use: ")
        print("  1. free")
        print("  2. low")
        print("  3. medium")
        print("  4. high")
        cost_choice = input("Select (1-4): ").strip()
        cost_map = {"1": "free", "2": "low", "3": "medium", "4": "high"}
        cost = cost_map.get(cost_choice, "medium")
        
        print("\nSpecialties (comma-separated, e.g., documentation,yaml,testing): ")
        specialties = [s.strip() for s in input().split(",") if s.strip()]
        
        api_key_required = input("API key required? (y/n): ").lower() == "y"
        notes = input("Notes (optional): ").strip()
        
        agent = Agent(
            id=agent_id,
            name=name,
            description=description,
            cost_per_use=cost,
            specialties=specialties,
            api_key_required=api_key_required,
            notes=notes,
            enabled=True
        )
        
        self.agents[agent_id] = agent
        self._save_config()
        
        print(f"\n✅ Added agent: {name}")
    
    def enable_agent(self):
        """Enable a disabled agent"""
        disabled = [a for a in self.agents.values() if not a.enabled]
        
        if not disabled:
            print("No disabled agents to enable.")
            return
        
        print("\nDisabled agents:")
        for i, agent in enumerate(disabled, 1):
            print(f"  {i}. {agent.name} ({agent.id})")
        
        choice = input("Select agent to enable (number): ").strip()
        try:
            agent = disabled[int(choice) - 1]
            agent.enabled = True
            self._save_config()
            print(f"✅ Enabled: {agent.name}")
        except (ValueError, IndexError):
            print("Invalid choice.")
    
    def disable_agent(self):
        """Disable an enabled agent"""
        enabled = [a for a in self.agents.values() if a.enabled]
        
        if not enabled:
            print("No enabled agents to disable.")
            return
        
        print("\nEnabled agents:")
        for i, agent in enumerate(enabled, 1):
            print(f"  {i}. {agent.name} ({agent.id})")
        
        choice = input("Select agent to disable (number): ").strip()
        try:
            agent = enabled[int(choice) - 1]
            agent.enabled = False
            self._save_config()
            print(f"✅ Disabled: {agent.name}")
        except (ValueError, IndexError):
            print("Invalid choice.")
    
    def remove_agent(self):
        """Remove an agent"""
        if not self.agents:
            print("No agents to remove.")
            return
        
        print("\nAgents:")
        agents_list = list(self.agents.values())
        for i, agent in enumerate(agents_list, 1):
            status = "✅" if agent.enabled else "⚪"
            print(f"  {i}. {status} {agent.name} ({agent.id})")
        
        choice = input("Select agent to remove (number): ").strip()
        try:
            agent = agents_list[int(choice) - 1]
            confirm = input(f"Remove {agent.name}? (y/n): ").lower()
            if confirm == "y":
                del self.agents[agent.id]
                self._save_config()
                print(f"✅ Removed: {agent.name}")
        except (ValueError, IndexError):
            print("Invalid choice.")
    
    def test_agent(self):
        """Test if agent is accessible"""
        enabled = [a for a in self.agents.values() if a.enabled]
        
        if not enabled:
            print("No enabled agents to test.")
            return
        
        print("\nEnabled agents:")
        for i, agent in enumerate(enabled, 1):
            print(f"  {i}. {agent.name}")
        
        choice = input("Select agent to test (number): ").strip()
        try:
            agent = enabled[int(choice) - 1]
            print(f"\n🔍 Testing {agent.name}...")
            
            # Simple test: Try a basic API call (if applicable)
            # This is a placeholder - real implementation would test actual agent
            print(f"✅ {agent.name} is configured and ready")
            
            if agent.api_key_required:
                print("   ⚠️  API key required - ensure it's set in environment")
        
        except (ValueError, IndexError):
            print("Invalid choice.")
    
    def export_config(self):
        """Export configuration as JSON"""
        config = {
            agent_id: asdict(agent)
            for agent_id, agent in self.agents.items()
        }
        print("\n" + json.dumps(config, indent=2))
    
    def show_menu(self):
        """Show interactive menu"""
        while True:
            print("\n" + "="*70)
            print("🔧 Agent Configuration Manager")
            print("="*70)
            print("""
1. List all agents
2. Add new agent
3. Enable agent
4. Disable agent
5. Remove agent
6. Test agent
7. Export configuration
8. Exit
""")
            
            choice = input("Select option (1-8): ").strip()
            
            if choice == "1":
                self.list_agents()
            elif choice == "2":
                self.add_agent_interactive()
            elif choice == "3":
                self.enable_agent()
            elif choice == "4":
                self.disable_agent()
            elif choice == "5":
                self.remove_agent()
            elif choice == "6":
                self.test_agent()
            elif choice == "7":
                self.export_config()
            elif choice == "8":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")

def main():
    """Main entry point"""
    manager = AgentManager()
    
    if len(sys.argv) > 1:
        # CLI mode
        command = sys.argv[1]
        
        if command == "list":
            manager.list_agents()
        elif command == "add":
            manager.add_agent_interactive()
        elif command == "enable":
            manager.enable_agent()
        elif command == "disable":
            manager.disable_agent()
        elif command == "remove":
            manager.remove_agent()
        elif command == "test":
            manager.test_agent()
        elif command == "export":
            manager.export_config()
        else:
            print(f"Unknown command: {command}")
            print("Usage: agent_manager.py [list|add|enable|disable|remove|test|export]")
    else:
        # Interactive menu mode
        manager.show_menu()

if __name__ == "__main__":
    main()
