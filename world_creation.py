import json
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from config import OPENAI_API_KEY
from utils.helper import save_world

def generate_world():
    """Generates a fantasy world with kingdoms, towns, and NPCs."""
    llm = ChatOpenAI(model_name="gpt-4-turbo", openai_api_key=OPENAI_API_KEY)

    # **Step 1: Generate World Information**
    system_prompt = """
    Your job is to help create interesting fantasy worlds that players would love to play in.
    Instructions:
    - Only generate in plain text without formatting.
    - Use simple clear language without being flowery.
    - You must stay below 3-5 sentences for each description.
    """

    world_prompt = """
    Generate a creative description for a unique fantasy world with an
    interesting concept around cities built on the backs of massive beasts.

    Output content in the form:
    World Name: <WORLD NAME>
    World Description: <WORLD DESCRIPTION>

    World Name:
    """

    print("🌍 Generating a new world...")
    
    response = llm.invoke(ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_prompt),
        HumanMessagePromptTemplate.from_template(world_prompt)
    ]).format())

    world_output = response.content.strip().split("\n", 1)
    
    if len(world_output) < 2:
        raise ValueError("🚨 AI failed to generate a valid world structure.")

    world = {
        "name": world_output[0].replace('World Name: ', '').strip(),
        "description": world_output[1].replace('World Description:', '').strip(),
        "kingdoms": {}
    }

    print(f"✅ World created: {world['name']}")

    ### **Step 2: Generate Kingdoms**
    print("🏰 Generating kingdoms...")
    
    kingdom_prompt = f"""
    Create 3 different kingdoms for a fantasy world.
    For each kingdom, generate a name and a description based on the world it's in.

    Output content in the form:
    Kingdom 1 Name: <KINGDOM NAME>
    Kingdom 1 Description: <KINGDOM DESCRIPTION>
    Kingdom 2 Name: <KINGDOM NAME>
    Kingdom 2 Description: <KINGDOM DESCRIPTION>
    Kingdom 3 Name: <KINGDOM NAME>
    Kingdom 3 Description: <KINGDOM DESCRIPTION>

    World Name: {world['name']}
    World Description: {world['description']}
    
    Kingdom 1 Name:
    """

    response = llm.invoke(kingdom_prompt)
    kingdoms_output = response.content.strip()
    kingdoms = {}

    for output in kingdoms_output.split("\n\n"):
        lines = output.strip().split("\n")
        if len(lines) < 2:
            print(f"⚠️ Skipping malformed kingdom data: {output}")
            continue

        kingdom_name = lines[0].replace("Kingdom Name: ", "").strip()
        kingdom_description = lines[1].replace("Kingdom Description: ", "").strip()
        kingdoms[kingdom_name] = {"name": kingdom_name, "description": kingdom_description, "towns": {}}

    world["kingdoms"] = kingdoms
    print("✅ Kingdoms generated.")

    ### **Step 3: Generate Towns**
    print("🏙️ Generating towns...")

    for kingdom_name, kingdom_data in world["kingdoms"].items():
        town_prompt = f"""
        Create 3 different towns for the kingdom {kingdom_name}.
        Provide a name and description for each.

        Output content in the form:
        Town 1 Name: <TOWN NAME>
        Town 1 Description: <TOWN DESCRIPTION>
        Town 2 Name: <TOWN NAME>
        Town 2 Description: <TOWN DESCRIPTION>
        Town 3 Name: <TOWN NAME>
        Town 3 Description: <TOWN DESCRIPTION>

        World Name: {world['name']}
        Kingdom Name: {kingdom_name}
        Kingdom Description: {kingdom_data['description']}
        
        Town 1 Name:
        """

        response = llm.invoke(town_prompt)
        towns_output = response.content.strip()
        towns = {}

        for output in towns_output.split("\n\n"):
            lines = output.strip().split("\n")
            if len(lines) < 2:
                print(f"⚠️ Skipping malformed town data: {output}")
                continue

            town_name = lines[0].replace("Town Name: ", "").strip()
            town_description = lines[1].replace("Town Description: ", "").strip()
            towns[town_name] = {"name": town_name, "description": town_description, "npcs": {}}

        kingdom_data["towns"] = towns

    print("✅ Towns generated.")

    ### **Step 4: Generate NPCs**
    print("👤 Generating NPCs...")

    for kingdom_name, kingdom_data in world["kingdoms"].items():
        for town_name, town_data in kingdom_data["towns"].items():
            npc_prompt = f"""
            Create 3 unique characters (NPCs) for the town {town_name} in {kingdom_name}.
            Provide a name and description for each.

            Output content in the form:
            Character 1 Name: <CHARACTER NAME>
            Character 1 Description: <CHARACTER DESCRIPTION>
            Character 2 Name: <CHARACTER NAME>
            Character 2 Description: <CHARACTER DESCRIPTION>
            Character 3 Name: <CHARACTER NAME>
            Character 3 Description: <CHARACTER DESCRIPTION>

            World Name: {world['name']}
            Kingdom Name: {kingdom_name}
            Town Name: {town_name}
            
            Character 1 Name:
            """

            response = llm.invoke(npc_prompt)
            npcs_output = response.content.strip()
            npcs = {}

            for output in npcs_output.split("\n\n"):
                lines = output.strip().split("\n")
                
                # Ensure the response contains both a name and a description
                npc_name = None
                npc_description = None

                for line in lines:
                    if "Character Name:" in line:
                        npc_name = line.replace("Character Name: ", "").strip()
                    elif "Character Description:" in line:
                        npc_description = line.replace("Character Description: ", "").strip()

                if npc_name and npc_description:
                    npcs[npc_name] = {"name": npc_name, "description": npc_description}
                else:
                    print(f"⚠️ Skipping incomplete NPC data: {output}")

            town_data["npcs"] = npcs
        
    print("✅ NPCs generated.")
    save_world(world)

    return world
