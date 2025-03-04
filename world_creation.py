import json
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from config import OPENAI_API_KEY
from helper import save_world
from prompts import *
from typing import Literal


def generate_npcs(
    world_type, world_name, kingdom_name, town_name, town_description, num_npcs=3
):
    """Generate NPCs for a given town based on world type."""
    if num_npcs < 2:
        raise ValueError("Number of NPCs must be at least 2.")

    if world_type == "Fantasy":
        npc_prompt = generate_npc_prompt_fantasy(
            world_name, kingdom_name, town_name, town_description, num_npcs
        )
    elif world_type == "Sci-Fi":
        npc_prompt = generate_npc_prompt_scifi(world_name, town_name, num_npcs)
    elif world_type == "Cyberpunk":
        npc_prompt = generate_npc_prompt_cyberpunk(world_name, town_name, num_npcs)

    llm = ChatOpenAI(model_name="gpt-4-turbo", openai_api_key=OPENAI_API_KEY)

    response = llm.invoke(npc_prompt)
    npcs_output = response.content.strip()
    npcs = {}

    # Parsing NPC responses correctly
    lines = [line.strip() for line in npcs_output.split("\n") if line.strip()]

    current_npc = None
    for line in lines:
        if "Character" in line and "Name:" in line:
            current_npc = line.replace("Character", "").replace("Name:", "").strip()
            npcs[current_npc] = {"name": current_npc, "description": ""}
        elif "Description:" in line and current_npc:
            npcs[current_npc]["description"] = line.replace("Description:", "").strip()
        elif current_npc and npcs[current_npc]["description"] == "":
            npcs[current_npc][
                "description"
            ] = line  # Handle cases where description is on a new line

    # Remove empty NPCs (if any due to parsing issues)
    npcs = {k: v for k, v in npcs.items() if v["description"]}

    return npcs


def generate_world(
    world_type: Literal["Fantasy", "Sci-Fi", "Cyberpunk"] = "Fantasy",
    custom_system_prompt: str = None,
    world_concept: str = None,
    world_name: str = None,
    world_description: str = None,
) -> dict:
    if world_type not in ["Fantasy", "Sci-Fi", "Cyberpunk"]:
        raise ValueError(
            "Invalid world type. Choose from: 'Fantasy', 'Sci-Fi', 'Cyberpunk'."
        )

    """Generates a fantasy world with kingdoms, towns, and NPCs."""
    llm = ChatOpenAI(model_name="gpt-4-turbo", openai_api_key=OPENAI_API_KEY)

    # **Step 1: Generate World Information**
    if world_type == "Fantasy":
        system_prompt = generate_system_prompt_fantasy(custom_system_prompt)
        world_prompt = generate_world_prompt_fantasy(
            world_concept, world_name, world_description
        )
    elif world_type == "Sci-Fi":
        system_prompt = generate_system_prompt_scifi(custom_system_prompt)
        world_prompt = generate_world_prompt_scifi(
            world_concept, world_name, world_description
        )
    elif world_type == "Cyberpunk":
        system_prompt = generate_system_prompt_cyberpunk(custom_system_prompt)
        world_prompt = generate_world_prompt_cyberpunk(
            world_concept, world_name, world_description
        )

    print("🌍 Generating a new world...")

    response = llm.invoke(
        ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(system_prompt),
                HumanMessagePromptTemplate.from_template(world_prompt),
            ]
        ).format()
    )

    world_output = response.content.strip().split("\n", 1)

    if len(world_output) < 2:
        raise ValueError("🚨 AI failed to generate a valid world structure.")

    world = {
        "name": world_output[0].replace("World Name: ", "").strip(),
        "description": world_output[1].replace("World Description:", "").strip(),
        world_structure_types[world_type][0]: {},
    }

    print(f"✅ World created: {world['name']}")

    ### **Step 2: Generate Kingdoms**
    print(f"🏰 Generating {world_structure_types[world_type][0]}...")

    if world_type == "Fantasy":
        structure_prompt = generate_kingdom_prompt_fantasy(
            world["name"], world["description"]
        )
    elif world_type == "Sci-Fi":
        structure_prompt = generate_planet_prompt_scifi(
            world["name"], world["description"]
        )
    elif world_type == "Cyberpunk":
        structure_prompt = generate_city_prompt_cyberpunk(
            world["name"], world["description"]
        )

    response = llm.invoke(structure_prompt)
    structure_output = response.content.strip()
    structures = {}

    for output in structure_output.split("\n\n"):
        lines = output.strip().split("\n")
        if len(lines) < 2:
            print(
                f"⚠️ Skipping malformed {world_structure_types[world_type][0]} data: {output}"
            )
            continue

        structure_name = (
            lines[0]
            .replace(f"{world_structure_types[world_type][0]} Name: ", "")
            .strip()
        )
        structure_description = (
            lines[1]
            .replace(f"{world_structure_types[world_type][0]} Description: ", "")
            .strip()
        )
        structures[structure_name] = {
            "name": structure_name,
            "description": structure_description,
            {world_structure_types[world_type][1]}: {},
        }

    world[{world_structure_types[world_type][0]}] = structures
    print(f"✅ {world_structure_types[world_type][0]} generated.")

    ### **Step 3: Generate Towns**
    print(f"🏙️ Generating {world_structure_types[world_type][1]}...")

    for structure_name, structure_data in world["kingdoms"].items():
        if world_type == "Fantasy":
            smaller_structure_prompt = generate_town_prompt_fantasy(
                structure_name, structure_data["description"]
            )
        elif world_type == "Sci-Fi":
            smaller_structure_prompt = generate_planet_prompt_scifi(
                structure_name, structure_data["description"]
            )
        elif world_type == "Cyberpunk":
            smaller_structure_prompt = generate_city_prompt_cyberpunk(
                structure_name, structure_data["description"]
            )

        response = llm.invoke(smaller_structure_prompt)
        ss_output = response.content.strip()
        ss = {}

        for output in ss_output.split("\n\n"):
            lines = output.strip().split("\n")
            if len(lines) < 2:
                print(
                    f"⚠️ Skipping malformed {world_structure_types[world_type][1]} data: {output}"
                )
                continue

            ss_name = (
                lines[0]
                .replace(f"{world_structure_types[world_type][1]} Name: ", "")
                .strip()
            )
            ss_description = (
                lines[1]
                .replace(f"{world_structure_types[world_type][1]} Description: ", "")
                .strip()
            )
            ss[ss_name] = {"name": ss_name, "description": ss_description, "npcs": {}}

        kingdom_data[world_structure_types[world_type][1]] = ss

    print(f"✅ {world_structure_types[world_type][1]} generated.")

    ### **Step 4: Generate NPCs**
    print(f"👤 Generating {world_structure_types[world_type][2]}...")

    for kingdom_name, kingdom_data in world[
        world_structure_types[world_type][0]
    ].items():
        for town_name, town_data in kingdom_data[
            world_structure_types[world_type][1]
        ].items():
            npcs = generate_npcs(
                world_type,
                world["name"],
                kingdom_name,
                town_name,
                town_data["description"],
            )
            town_data["npcs"] = npcs

    print("✅ NPCs generated.")
    save_world(world)

    return world
