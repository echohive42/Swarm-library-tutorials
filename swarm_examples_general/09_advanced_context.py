"""
# Advanced Context Management Example - RPG Game System
# This example demonstrates complex context management with multiple state variables
# Shows how to maintain and update complex game state across interactions
# Implements a simple RPG system with inventory, stats, and quest management
"""

import os
import random
from termcolor import colored
from swarm import Swarm, Agent
from swarm.types import Result

# Constants
MODEL = "gpt-4o"
HISTORY = []

# Game constants
ITEMS = {
    "health_potion": {"type": "consumable", "effect": "heal", "value": 30},
    "sword": {"type": "weapon", "damage": 15, "value": 100},
    "shield": {"type": "armor", "defense": 10, "value": 80},
    "magic_scroll": {"type": "consumable", "effect": "magic", "value": 50},
}

ENEMIES = {
    "goblin": {"hp": 30, "damage": 5, "xp": 20},
    "wolf": {"hp": 25, "damage": 8, "xp": 15},
    "bandit": {"hp": 40, "damage": 10, "xp": 30},
}

LOCATIONS = {
    "town": ["shop", "inn", "blacksmith"],
    "forest": ["clearing", "cave", "river"],
    "dungeon": ["entrance", "treasure_room", "boss_room"],
}

def initialize_game_state() -> Result:
    """Initialize a new game state with default values."""
    print(colored("\n🎮 Initializing new game state...", "magenta"))
    initial_state = {
        "player": {
            "name": "",
            "level": 1,
            "xp": 0,
            "hp": 100,
            "max_hp": 100,
            "gold": 100,
            "inventory": ["health_potion"],
            "equipped": {"weapon": None, "armor": None}
        },
        "location": "town",
        "quests": [],
        "discovered_locations": ["town"],
        "enemies_defeated": 0
    }
    
    return Result(
        value="Game state initialized. Ready to start adventure!",
        context_variables=initial_state
    )

def check_status(context_variables: dict) -> str:
    """Check the player's current status."""
    print(colored("\n📊 Checking player status...", "magenta"))
    player = context_variables["player"]
    location = context_variables["location"]
    
    status = f"""
Current Status:
Name: {player['name']}
Level: {player['level']} (XP: {player['xp']})
HP: {player['hp']}/{player['max_hp']}
Gold: {player['gold']}
Location: {location}

Inventory:
{', '.join(player['inventory'])}

Equipped:
Weapon: {player['equipped']['weapon'] or 'None'}
Armor: {player['equipped']['armor'] or 'None'}

Quests: {len(context_variables['quests'])}
Enemies Defeated: {context_variables['enemies_defeated']}
Discovered Locations: {', '.join(context_variables['discovered_locations'])}
"""
    return status

def use_item(context_variables: dict, item_name: str) -> Result:
    """Use an item from the inventory.
    
    Args:
        item_name: Name of the item to use
    """
    print(colored(f"\n🎒 Using item: {item_name}...", "magenta"))
    player = context_variables["player"]
    
    if item_name not in player["inventory"]:
        return Result(value=f"You don't have a {item_name} in your inventory.")
    
    if item_name not in ITEMS:
        return Result(value=f"Unknown item: {item_name}")
    
    item = ITEMS[item_name]
    result_msg = ""
    
    if item["type"] == "consumable":
        player["inventory"].remove(item_name)
        if item["effect"] == "heal":
            heal_amount = item["value"]
            player["hp"] = min(player["hp"] + heal_amount, player["max_hp"])
            result_msg = f"Used {item_name}. Healed for {heal_amount} HP."
        elif item["effect"] == "magic":
            result_msg = f"Used {item_name}. Magical effects applied."
    elif item["type"] in ["weapon", "armor"]:
        old_item = player["equipped"][item["type"]]
        if old_item:
            player["inventory"].append(old_item)
        player["equipped"][item["type"]] = item_name
        player["inventory"].remove(item_name)
        result_msg = f"Equipped {item_name}."
        if old_item:
            result_msg += f" Unequipped {old_item}."
    
    return Result(
        value=result_msg,
        context_variables={"player": player}
    )

def travel_to(context_variables: dict, destination: str) -> Result:
    """Travel to a new location.
    
    Args:
        destination: The location to travel to
    """
    print(colored(f"\n🗺️ Traveling to {destination}...", "magenta"))
    if destination not in LOCATIONS:
        return Result(value=f"Cannot travel to {destination}. Location doesn't exist.")
    
    current_location = context_variables["location"]
    discovered = context_variables["discovered_locations"]
    
    if destination not in discovered:
        discovered.append(destination)
    
    return Result(
        value=f"Traveled from {current_location} to {destination}.\nAreas available: {', '.join(LOCATIONS[destination])}",
        context_variables={
            "location": destination,
            "discovered_locations": discovered
        }
    )

def combat_simulation(context_variables: dict, enemy_type: str) -> Result:
    """Simulate combat with an enemy.
    
    Args:
        enemy_type: Type of enemy to fight
    """
    print(colored(f"\n⚔️ Starting combat with {enemy_type}...", "magenta"))
    if enemy_type not in ENEMIES:
        return Result(value=f"Enemy type '{enemy_type}' not found.")
    
    if "player" not in context_variables:
        return Result(value="Error: No player found. Please initialize game first.")
    
    player = context_variables["player"].copy()  # Create a copy to avoid modifying the original
    enemy = ENEMIES[enemy_type].copy()
    combat_log = [f"Combat started with {enemy_type}!"]
    
    # Calculate player damage
    weapon = player["equipped"]["weapon"]
    base_damage = ITEMS[weapon]["damage"] if weapon else 5
    
    # Calculate player defense
    armor = player["equipped"]["armor"]
    defense = ITEMS[armor]["defense"] if armor else 0
    
    while enemy["hp"] > 0 and player["hp"] > 0:
        # Player turn
        damage_dealt = base_damage
        enemy["hp"] -= damage_dealt
        combat_log.append(f"You deal {damage_dealt} damage to {enemy_type}")
        
        if enemy["hp"] <= 0:
            break
        
        # Enemy turn
        damage_taken = max(0, enemy["damage"] - defense)
        player["hp"] -= damage_taken
        combat_log.append(f"{enemy_type} deals {damage_taken} damage to you")
    
    # Combat results
    if player["hp"] > 0:
        player["xp"] += enemy["xp"]
        enemies_defeated = context_variables.get("enemies_defeated", 0) + 1
        combat_log.append(f"\nVictory! Gained {enemy['xp']} XP")
        
        # Level up check
        if player["xp"] >= player["level"] * 100:
            player["level"] += 1
            player["max_hp"] += 20
            player["hp"] = player["max_hp"]
            combat_log.append(f"Level Up! Now level {player['level']}")
    else:
        combat_log.append("\nDefeat! You have been defeated...")
        player["hp"] = 1  # Prevent actual death for demo
    
    # Update context with new player state and enemies defeated
    updated_context = {
        "player": player,
        "enemies_defeated": enemies_defeated
    }
    
    return Result(
        value="\n".join(combat_log),
        context_variables=updated_context
    )

# Initialize Swarm client
print(colored("Initializing Swarm client...", "cyan"))
client = Swarm()

# Create game master agent
game_master = Agent(
    name="Game Master",
    model=MODEL,
    instructions="""You are a Game Master for an RPG adventure.
    Guide the player through their adventure, maintaining game state and rules.
    
    Available commands:
    1. Initialize new game
    2. Check status
    3. Use items
    4. Travel between locations
    5. Engage in combat
    
    Keep track of player's progress and provide appropriate challenges.
    Be descriptive in your narration but keep it concise.
    Always inform players of their options after each action.""",
    functions=[
        initialize_game_state,
        check_status,
        use_item,
        travel_to,
        combat_simulation
    ]
)

def chat_loop():
    global HISTORY
    context = None  # Will be initialized when game starts
    
    print(colored("\nRPG Adventure System started! Type 'exit' to end.", "green"))
    print(colored("Type 'start' to begin a new game", "cyan"))
    print(colored("Available commands:\n- check status\n- use [item]\n- travel to [location]\n- fight [enemy]", "cyan"))
    
    while True:
        # Get user input
        user_input = input(colored("\nYou: ", "yellow"))
        
        if user_input.lower() == 'exit':
            print(colored("\nEnding game...", "red"))
            break

        # Add user message to history
        HISTORY.append({"role": "user", "content": user_input})

        try:
            # Get response from game master
            print(colored("\nGame Master is responding...", "cyan"))
            response = client.run(
                agent=game_master,
                messages=HISTORY,
                context_variables=context if context is not None else {}
            )

            # Update context with any changes
            if response.context_variables:
                if context is None:
                    context = {}
                context.update(response.context_variables)
            
            # Update history with agent's response
            HISTORY.extend(response.messages)
            
            # Print game master's response
            print(colored(f"\nGame Master: {response.messages[-1]['content']}", "green"))

        except Exception as e:
            print(colored(f"\nError: {str(e)}", "red"))

if __name__ == "__main__":
    try:
        chat_loop()
    except KeyboardInterrupt:
        print(colored("\nGame ended by user.", "yellow"))
    except Exception as e:
        print(colored(f"\nUnexpected error: {str(e)}", "red")) 