
world_structure_types = {
    "Fantasy": ["kingdoms", "towns", "npcs"],
    "Sci-Fi": ["planets", "space stations", "npcs"],
    "Cyberpunk": ["cities", "cybernetics", "npcs"]
}

### Fantasy Prompts ###

def generate_system_prompt_fantasy(custom_prompt = None):
    if custom_prompt is not None:
        return f"{FANTASY_SYSTEM_PROMPT} {custom_prompt}"
    
    FANTASY_SYSTEM_PROMPT = """
        Your job is to help create interesting fantasy worlds that players would love to play in.
        Instructions:
        - Only generate in plain text without formatting.
        - Use simple clear language without being flowery.
        - You must stay below 3-5 sentences for each description.
        """
    
    return FANTASY_SYSTEM_PROMPT

def generate_world_prompt_fantasy(concept: str = None, world_name: str | None = None, description: str = None):
    if world_name is None:
        world_name =  "<WORLD NAME>"

    if description is None:
        description = "<WORLD DESCRIPTION>"

    if concept is None:
        concept = "cities built on the backs of massive beasts"

    FANTASY_WORLD_PROMPT = f"""
        Generate a creative description for a unique fantasy world with an
        interesting concept around {concept}.

        Output content in the form:
        World Name: {world_name}
        World Description: {description}

        World Name:
        """
    
    return FANTASY_WORLD_PROMPT

def generate_kingdom_prompt_fantasy(world_name: str, world_description: str, num_kingdoms: int = 3):
    if num_kingdoms < 2:
        raise ValueError("Number of kingdoms must be at least 2.")
    
    FANTASY_KINGDOM_PROMPT = f"""
        Create {3} different kingdoms for a fantasy world.
        For each kingdom, generate a name and a description based on the world it's in.

        Output content in the form:
        Kingdom 1 Name: <KINGDOM NAME>
        Kingdom 1 Description: <KINGDOM DESCRIPTION>
        Kingdom 2 Name: <KINGDOM NAME>
        Kingdom 2 Description: <KINGDOM DESCRIPTION>
        Kingdom 3 Name: <KINGDOM NAME>
        Kingdom 3 Description: <KINGDOM DESCRIPTION>

        World Name: {world_name}
        World Description: {world_description}

        Kingdom 1 Name:
        """
    
    return FANTASY_KINGDOM_PROMPT

def generate_town_prompt_fantasy(kingdom_name: str, kingdom_description: str, num_towns: int = 3):
    if num_towns < 2:
        raise ValueError("Number of towns must be at least 2.")
    
    FANTASY_TOWN_PROMPT = f"""
        Create {num_towns} different towns for a fantasy kingdom.
        For each town, generate a name and a description based on the kingdom it's in.

        Output content in the form:
        Town 1 Name: <TOWN NAME>
        Town 1 Description: <TOWN DESCRIPTION>
        Town 2 Name: <TOWN NAME>
        Town 2 Description: <TOWN DESCRIPTION>
        Town 3 Name: <TOWN NAME>
        Town 3 Description: <TOWN DESCRIPTION>

        Kingdom Name: {kingdom_name}
        Kingdom Description: {kingdom_description}

        Town 1 Name:
        """
    
    return FANTASY_TOWN_PROMPT

def generate_npc_prompt_fantasy(world_name: str, kingdom_name: str, town_name: str, town_description: str, num_npcs: int = 3):
    if num_npcs < 2:
        raise ValueError("Number of NPCs must be at least 2.")
    
    FANTASY_NPC_PROMPT = f"""
            Create 3 unique characters (NPCs) for the town {town_name} in {kingdom_name}.
            Provide a name and description for each.

            Output content in the form:
            Character 1 Name: <CHARACTER NAME>
            Character 1 Description: <CHARACTER DESCRIPTION>
            Character 2 Name: <CHARACTER NAME>
            Character 2 Description: <CHARACTER DESCRIPTION>
            Character 3 Name: <CHARACTER NAME>
            Character 3 Description: <CHARACTER DESCRIPTION>

            World Name: {world_name}
            Kingdom Name: {kingdom_name}
            Town Name: {town_name}
            
            Character 1 Name:
            """
    
    return FANTASY_NPC_PROMPT

### Sci-Fi Prompts ###

def generate_system_prompt_scifi():
    SCIFI_SYSTEM_PROMPT = """
        Your job is to help create interesting sci-fi worlds that players would love to play in.
        Instructions:
        - Only generate in plain text without formatting.
        - Use simple clear language without being flowery.
        - You must stay below 3-5 sentences for each description.
        """
    
    return SCIFI_SYSTEM_PROMPT

def generate_world_prompt_scifi(concept: str = None, world_name: str | None = None, description: str = None):
    if world_name is None:
        world_name =  "<WORLD NAME>"

    if description is None:
        description = "<WORLD DESCRIPTION>"

    if concept is None:
        concept = "cities in giant spacecrafts"

    SCIFI_WORLD_PROMPT = f"""
        Generate a creative description for a unique sci-fi world with an
        interesting concept around {concept}.

        Output content in the form:
        World Name: {world_name}
        World Description: {description}

        World Name:
        """
    
    return SCIFI_WORLD_PROMPT

def generate_planet_prompt_scifi(world_name: str, world_description: str, num_planets: int = 3):
    if num_planets < 2:
        raise ValueError("Number of planets must be at least 2.")
    
    SCIFI_PLANET_PROMPT = f"""
        Create {num_planets} different planets for a sci-fi world.
        For each planet, generate a name and a description based on the world it's in.

        Output content in the form:
        Planet 1 Name: <PLANET NAME>
        Planet 1 Description: <PLANET DESCRIPTION>
        Planet 2 Name: <PLANET NAME>
        Planet 2 Description: <PLANET DESCRIPTION>
        Planet 3 Name: <PLANET NAME>
        Planet 3 Description: <PLANET DESCRIPTION>

        World Name: {world_name}
        World Description: {world_description}

        Planet 1 Name:
        """
    
    return SCIFI_PLANET_PROMPT

def generate_space_station_prompt_scifi(world_name: str, num_stations: int = 3):
    if num_stations < 2:
        raise ValueError("Number of space stations must be at least 2.")
    
    SCIFI_STATION_PROMPT = f"""
        Create {num_stations} different space stations for a sci-fi world.
        For each station, generate a name and a description based on the world it's in.

        Output content in the form:
        Station 1 Name: <STATION NAME>
        Station 1 Description: <STATION DESCRIPTION>
        Station 2 Name: <STATION NAME>
        Station 2 Description: <STATION DESCRIPTION>
        Station 3 Name: <STATION NAME>
        Station 3 Description: <STATION DESCRIPTION>

        World Name: {world_name}

        Station 1 Name:
        """
    
    return SCIFI_STATION_PROMPT

def generate_npc_prompt_scifi(world_name: str, station_name: str, num_npcs: int = 3):
    if num_npcs < 2:
        raise ValueError("Number of NPCs must be at least 2.")
    
    SCIFI_NPC_PROMPT = f"""
            Create 3 unique characters (NPCs) for the space station {station_name}.
            Provide a name and description for each.

            Output content in the form:
            Character 1 Name: <CHARACTER NAME>
            Character 1 Description: <CHARACTER DESCRIPTION>
            Character 2 Name: <CHARACTER NAME>
            Character 2 Description: <CHARACTER DESCRIPTION>
            Character 3 Name: <CHARACTER NAME>
            Character 3 Description: <CHARACTER DESCRIPTION>

            World Name: {world_name}
            Station Name: {station_name}

            Character 1 Name:
            """
    
    return SCIFI_NPC_PROMPT

### Cyberpunk Prompts ###

def generate_system_prompt_cyberpunk():
    CYBERPUNK_SYSTEM_PROMPT = """
        Your job is to help create interesting cyberpunk worlds that players would love to play in.
        Instructions:
        - Only generate in plain text without formatting.
        - Use simple clear language without being flowery.
        - You must stay below 3-5 sentences for each description.
        """
    
    return CYBERPUNK_SYSTEM_PROMPT

def generate_world_prompt_cyberpunk(concept: str = None, world_name: str | None = None, description: str = None):
    if world_name is None:
        world_name =  "<WORLD NAME>"

    if description is None:
        description = "<WORLD DESCRIPTION>"

    if concept is None:
        concept = "a dystopian cityscape"

    CYBERPUNK_WORLD_PROMPT = f"""
        Generate a creative description for a unique cyberpunk world with an
        interesting concept around {concept}.

        Output content in the form:
        World Name: {world_name}
        World Description: {description}

        World Name:
        """
    
    return CYBERPUNK_WORLD_PROMPT

def generate_city_prompt_cyberpunk(world_name: str, world_description: str, num_cities: int = 3):
    if num_cities < 2:
        raise ValueError("Number of cities must be at least 2.")
    
    CYBERPUNK_CITY_PROMPT = f"""
        Create {num_cities} different cities for a cyberpunk world.
        For each city, generate a name and a description based on the world it's in.

        Output content in the form:
        City 1 Name: <CITY NAME>
        City 1 Description: <CITY DESCRIPTION>
        City 2 Name: <CITY NAME>
        City 2 Description: <CITY DESCRIPTION>
        City 3 Name: <CITY NAME>
        City 3 Description: <CITY DESCRIPTION>

        World Name: {world_name}
        World Description: {world_description}

        City 1 Name:
        """
    
    return CYBERPUNK_CITY_PROMPT

def generate_cybernetics_prompt_cyberpunk(world_name: str, city_name: str, num_cybernetics: int = 3):
    if num_cybernetics < 2:
        raise ValueError("Number of cybernetics must be at least 2.")
    
    CYBERPUNK_CYBERNETICS_PROMPT = f"""
            Create 3 unique cybernetic beings (cybernetics) for the city {city_name}.
            Provide a name and description for each.

            Output content in the form:
            Cybernetic 1 Name: <CYBERNETIC NAME>
            Cybernetic 1 Description: <CYBERNETIC DESCRIPTION>
            Cybernetic 2 Name: <CYBERNETIC NAME>
            Cybernetic 2 Description: <CYBERNETIC DESCRIPTION>
            Cybernetic 3 Name: <CYBERNETIC NAME>
            Cybernetic 3 Description: <CYBERNETIC DESCRIPTION>

            World Name: {world_name}
            City Name: {city_name}
        """
    
    return CYBERPUNK_CYBERNETICS_PROMPT

def generate_npc_prompt_cyberpunk(world_name: str, city_name: str, num_npcs: int = 3):
    if num_npcs < 2:
        raise ValueError("Number of NPCs must be at least 2.")
    
    CYBERPUNK_NPC_PROMPT = f"""
            Create 3 unique characters (NPCs) for the space station {city_name}.
            Provide a name and description for each.

            Output content in the form:
            Character 1 Name: <CHARACTER NAME>
            Character 1 Description: <CHARACTER DESCRIPTION>
            Character 2 Name: <CHARACTER NAME>
            Character 2 Description: <CHARACTER DESCRIPTION>
            Character 3 Name: <CHARACTER NAME>
            Character 3 Description: <CHARACTER DESCRIPTION>

            World Name: {world_name}
            Station Name: {city_name}

            Character 1 Name:
            """
    
    return CYBERPUNK_NPC_PROMPT