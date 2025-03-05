
world_structure_types = {
    "Fantasy": ["kingdoms", "towns", "npcs"],
    "Sci-Fi": ["planets", "space stations", "npcs"],
    "Cyberpunk": ["cities", "cybernetics", "npcs"]
}

### Fantasy Prompts ###

def generate_system_prompt_fantasy():
    FANTASY_SYSTEM_PROMPT = """
        Your job is to help create interesting fantasy worlds that players would love to play in.
        Instructions:
        - Only generate in plain text without formatting.
        - Use simple clear language without being flowery.
        - You must stay below 3-5 sentences for each description.
        """
    
    return FANTASY_SYSTEM_PROMPT

def generate_world_prompt_fantasy(world_name: str | None = None, concept: str = None):
    if world_name is None:
        world_name =  "<WORLD NAME>"

    if concept is None:
        concept = "In this world, there are cities built on the backs of massive beasts."

    FANTASY_WORLD_PROMPT = f"""
        Generate a creative description for a unique fantasy world. Take the following into account when imagining this world:
            {concept}

        Output content in the form:
        World Name: {world_name}
        World Description: "<WORLD DESCRIPTION>"
        """
    
    return FANTASY_WORLD_PROMPT

def generate_kingdom_prompt_fantasy(world_name: str, world_description: str, num_kingdoms: int = 3):
    if num_kingdoms < 2:
        raise ValueError("Number of kingdoms must be at least 2.")
    
    FANTASY_KINGDOM_PROMPT = f"""
        Create {num_kingdoms} different kingdoms for a fantasy world named {world_name}.
        The world looks like this: {world_description}.
        For each kingdom, generate a name and a description based on the world it's in.

        Output content in the form:
        Kingdom 1 Name: <KINGDOM NAME>
        Kingdom 1 Description: <KINGDOM DESCRIPTION>
        Kingdom 2 Name: <KINGDOM NAME>
        Kingdom 2 Description: <KINGDOM DESCRIPTION>
        Kingdom 3 Name: <KINGDOM NAME>
        Kingdom 3 Description: <KINGDOM DESCRIPTION>
        """
    
    return FANTASY_KINGDOM_PROMPT

def generate_town_prompt_fantasy(kingdom_name: str, kingdom_description: str, num_towns: int = 3):
    if num_towns < 2:
        raise ValueError("Number of towns must be at least 2.")
    
    FANTASY_TOWN_PROMPT = f"""
        Create {num_towns} different towns for a fantasy kingdom {kingdom_name}.
        The kingdom looks like this: {kingdom_description}.
        For each town, generate a name and a description based on the kingdom it's in.

        Output content in the form:
        Town 1 Name: <TOWN NAME>
        Town 1 Description: <TOWN DESCRIPTION>
        Town 2 Name: <TOWN NAME>
        Town 2 Description: <TOWN DESCRIPTION>
        Town 3 Name: <TOWN NAME>
        Town 3 Description: <TOWN DESCRIPTION>
        """
    
    return FANTASY_TOWN_PROMPT

def generate_npc_prompt_fantasy(world_name: str, kingdom_name: str, town_name: str, town_description: str, num_npcs: int = 3):
    if num_npcs < 2:
        raise ValueError("Number of NPCs must be at least 2.")
    
    FANTASY_NPC_PROMPT = f"""
            Create {num_npcs} unique characters (NPCs) for the town {town_name} in {kingdom_name}, in the fantasy world of {world_name}.
            Provide a name and description for each.

            The town looks like this: {town_description}.

            Output content in the form:
            Character 1 Name: <CHARACTER NAME>
            Character 1 Description: <CHARACTER DESCRIPTION>
            Character 2 Name: <CHARACTER NAME>
            Character 2 Description: <CHARACTER DESCRIPTION>
            Character 3 Name: <CHARACTER NAME>
            Character 3 Description: <CHARACTER DESCRIPTION>
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

def generate_world_prompt_scifi(world_name: str | None = None, concept: str = None):
    if world_name is None:
        world_name =  "<WORLD NAME>"

    if concept is None:
        concept = "In this world, there are planets hosting different interstellar civilizations."

    SCIFI_WORLD_PROMPT = f"""
        Generate a creative description for a unique sci-fi world. Take the following into account when imagining this world:
            {concept}

        Output content in the form:
        World Name: {world_name}
        World Description: "<WORLD DESCRIPTION>"
        """
    
    return SCIFI_WORLD_PROMPT

def generate_planet_prompt_scifi(world_name: str, world_description: str, num_planets: int = 3):
    if num_planets < 2:
        raise ValueError("Number of planets must be at least 2.")
    
    SCIFI_PLANET_PROMPT = f"""
        Create {num_planets} different planets for a sci-fi world named {world_name}.
        The world looks like this: {world_description}.
        For each planet, generate a name and a description based on the world it's in.

        Output content in the form:
        Planet 1 Name: <PLANET NAME>
        Planet 1 Description: <PLANET DESCRIPTION>
        Planet 2 Name: <PLANET NAME>
        Planet 2 Description: <PLANET DESCRIPTION>
        Planet 3 Name: <PLANET NAME>
        Planet 3 Description: <PLANET DESCRIPTION>
        """
    
    return SCIFI_PLANET_PROMPT

def generate_space_station_prompt_scifi(planet_name: str, planet_description: str, num_stations: int = 3):
    if num_stations < 2:
        raise ValueError("Number of space stations must be at least 2.")
    
    SCIFI_STATION_PROMPT = f"""
        Create {num_stations} different space stations for a sci-fi world, orbiting around planet {planet_name}.
        Here is a description of the planet: {planet_description}.
        For each station, generate a name and a description based on the world it's in.

        Output content in the form:
        Station 1 Name: <STATION NAME>
        Station 1 Description: <STATION DESCRIPTION>
        Station 2 Name: <STATION NAME>
        Station 2 Description: <STATION DESCRIPTION>
        Station 3 Name: <STATION NAME>
        Station 3 Description: <STATION DESCRIPTION>
        """
    
    return SCIFI_STATION_PROMPT

def generate_npc_prompt_scifi(world_name: str, planet_name: str, station_name: str, station_description: str, num_npcs: int = 3):
    if num_npcs < 2:
        raise ValueError("Number of NPCs must be at least 2.")
    
    SCIFI_NPC_PROMPT = f"""
            Create {num_npcs} unique characters (NPCs) for the space station {station_name} orbiting around planet {planet_name}, in the sci-fi world of {world_name}.
            Here is a description of the space station: {station_description}.
            Provide a name and description for each.

            Output content in the form:
            Character 1 Name: <CHARACTER NAME>
            Character 1 Description: <CHARACTER DESCRIPTION>
            Character 2 Name: <CHARACTER NAME>
            Character 2 Description: <CHARACTER DESCRIPTION>
            Character 3 Name: <CHARACTER NAME>
            Character 3 Description: <CHARACTER DESCRIPTION>
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

def generate_world_prompt_cyberpunk(world_name: str | None = None, concept: str = None):
    if world_name is None:
        world_name =  "<WORLD NAME>"

    if concept is None:
        concept = "a dystopian cityscape of infinite skyscrapers and red neon lights, where crime and corruption run rampant."

    CYBERPUNK_WORLD_PROMPT = f"""
        Generate a creative description for a unique cyberpunk world. Take the following into account when imagining this world:
            {concept}

        Output content in the form:
        World Name: {world_name}
        World Description: "<WORLD DESCRIPTION>"
        """
    
    return CYBERPUNK_WORLD_PROMPT

def generate_city_prompt_cyberpunk(world_name: str, world_description: str, num_cities: int = 3):
    if num_cities < 2:
        raise ValueError("Number of cities must be at least 2.")
    
    CYBERPUNK_CITY_PROMPT = f"""
        Create {num_cities} different cities for a cyberpunk world named {world_name}.
        The world looks like this: {world_description}.
        For each city, generate a name and a description based on the world it's in.

        Output content in the form:
        City 1 Name: <CITY NAME>
        City 1 Description: <CITY DESCRIPTION>
        City 2 Name: <CITY NAME>
        City 2 Description: <CITY DESCRIPTION>
        City 3 Name: <CITY NAME>
        City 3 Description: <CITY DESCRIPTION>
        """
    
    return CYBERPUNK_CITY_PROMPT

def generate_cybernetics_prompt_cyberpunk(city_name: str, city_description: str, num_cybernetics: int = 3):
    if num_cybernetics < 2:
        raise ValueError("Number of cybernetics must be at least 2.")
    
    CYBERPUNK_CYBERNETICS_PROMPT = f"""
            Create {num_cybernetics} unique cybernetic beings (cybernetics) for the city {city_name}.
            Here is a description of the city: {city_description}.
            Provide a name and description for each.

            Output content in the form:
            Cybernetic 1 Name: <CYBERNETIC NAME>
            Cybernetic 1 Description: <CYBERNETIC DESCRIPTION>
            Cybernetic 2 Name: <CYBERNETIC NAME>
            Cybernetic 2 Description: <CYBERNETIC DESCRIPTION>
            Cybernetic 3 Name: <CYBERNETIC NAME>
            Cybernetic 3 Description: <CYBERNETIC DESCRIPTION>
        """
    
    return CYBERPUNK_CYBERNETICS_PROMPT

def generate_npc_prompt_cyberpunk(world_name: str, city_name: str, cybernetics_name: str, cybernetics_description: str, num_npcs: int = 3):
    if num_npcs < 2:
        raise ValueError("Number of NPCs must be at least 2.")
    
    CYBERPUNK_NPC_PROMPT = f"""
            Create {num_npcs} unique characters (NPCs) for the cybernetics {cybernetics_name} of city {city_name}, in the cyberpunk world of {world_name}.
            Here is a description of the cybernetics: {cybernetics_description}.
            Provide a name and description for each.

            Output content in the form:
            Character 1 Name: <CHARACTER NAME>
            Character 1 Description: <CHARACTER DESCRIPTION>
            Character 2 Name: <CHARACTER NAME>
            Character 2 Description: <CHARACTER DESCRIPTION>
            Character 3 Name: <CHARACTER NAME>
            Character 3 Description: <CHARACTER DESCRIPTION>
            """
    
    return CYBERPUNK_NPC_PROMPT