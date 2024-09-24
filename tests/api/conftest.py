import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.area import router as area_router
from app.api.character import router as character_router
from app.api.enemy import router as enemy_router
from app.api.item import router as item_router
from app.api.psi import router as psi_router
from app.api.shop import router as shop_router

from app.settings import API_DATA_TABLE, AWS_REGION

app = FastAPI()
app.include_router(area_router)
app.include_router(character_router)
app.include_router(enemy_router)
app.include_router(item_router)
app.include_router(psi_router)
app.include_router(shop_router)

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

class Config:
    TABLE_NAME = API_DATA_TABLE
    REGION = AWS_REGION

    mock_areas = [
        {"pk": "area", "sk": "mock_onett#detail", "name": "Mock Onett", "primary_area": "Eagleland"},
        {"pk": "area", "sk": "mock_twoson#detail", "name": "Mock Twoson", "primary_area": "Eagleland"},
        {"pk": "area", "sk": "mock_ness_house#detail", "name": "Mock Ness's House", "primary_area": "Mock Onett"},
        {"pk": "area", "sk": "mock_giant_step#detail", "name": "Mock Giant Step", "primary_area": "Mock Onett"},
        {"pk": "area", "sk": "mock_peaceful_rest_valley#detail", "name": "Mock Peaceful Rest Valley", "primary_area": "Mock Twoson"},
        {"pk": "area", "sk": "mock_happy_happy_village#detail", "name": "Mock Happy Happy Village", "primary_area": "Eagleland"},
        {"pk": "area", "sk": "mock_happy_happy_village_headquarters#detail", "name": "Mock Happy Happy Village Headquarters", "primary_area": "Happy Happy Village"},
        {"pk": "area", "sk": "mock_lilliput_steps#detail", "name": "Mock Lilliput Steps", "primary_area": "Happy Happy Village"},
        {"pk": "area", "sk": "mock_threed#detail", "name": "Mock Threed", "primary_area": "Eagleland"}
    ]

    mock_pc_characters = [
        {"pk": "character", "sk": "pc#mockness", "name": "Mock Ness", "age": 13, "hometown": "Onett", "bio": "Loves to eat burgers from trash cans."},
        {"pk": "character", "sk": "pc#mockpaula", "name": "Mock Paula", "age": 13, "hometown": "Twoson", "bio": "A powerful psychic with a gentle heart."},
        {"pk": "character", "sk": "pc#mockjeff", "name": "Mock Jeff", "age": 13, "hometown": "Winters", "bio": "Inventive young man who can fix anything."},
        {"pk": "character", "sk": "pc#mockpoo", "name": "Mock Poo", "age": 13, "hometown": "Dalaam", "bio": "Dedicated warrior with powerful PSI abilities."}
    ]

    mock_npc_characters = [
        {"pk": "character", "sk": "npc#mockbuzzbuzz", "name": "Mock Buzz Buzz", "areas": ["Onett"], "role": "Quest Giver"},
        {"pk": "character", "sk": "npc#mockliarxagerate", "name": "Mock Liar X. Agerate", "areas": ["Onett"], "role": "Quest Giver"},
        {"pk": "character", "sk": "npc#mockfrankfly", "name": "Mock Frank Fly", "areas": ["Onett"], "role": "Quest Giver/Boss"},
        {"pk": "character", "sk": "npc#mockmreverdread", "name": "Mock Mr. Everdread", "areas": ["Twoson"], "role": "Quest Giver"},
        {"pk": "character", "sk": "npc#mockapplekid", "name": "Mock Apple Kid", "areas": ["Twoson"], "role": "Quest Giver/Inventor"},
        {"pk": "character", "sk": "npc#mockorangekid", "name": "Mock Orange Kid", "areas": ["Twoson"], "role": "Inventor"},
        {"pk": "character", "sk": "npc#mockrunawayfive", "name": "Mock Runaway Five", "areas": ["Twoson", "Threed", "Fourside"], "role": "Quest Giver/Performer"},
        {"pk": "character", "sk": "npc#mockzexonyteminer", "name": "Mock Zexonyte Miner", "areas": ["Onett"], "role": "Quest Giver"}
    ]

    mock_enemies = [
        {
            "pk": "enemy",
            "sk": "mock_abstract_art#detail",
            "name": "Mock Abstract Art",
            "enemy_type": "normal",
            "data_type": "profile",
            "exp_reward": 4361,
            "money_reward": 255,
            "initial_status": "",
            "is_boss": "FALSE",
            "drop": {"item": "Refreshing Herb", "chance": "4/128"},
            "areas": ["Moonside"],
            "stats": {"hp": 301, "pp": 60, "offense": 67, "defense": 79, "guts": 7, "speed": 0},
            "battle_tip": "Use physical attacks to chip away its form."
        },
        {
            "pk": "enemy",
            "sk": "mock_annoying_old_party_man#detail",
            "name": "Mock Annoying Old Party Man",
            "enemy_type": "normal",
            "data_type": "profile",
            "exp_reward": 130,
            "money_reward": 32,
            "initial_status": "",
            "is_boss": "FALSE",
            "drop": {"item": "Protein Drink", "chance": "2/128"},
            "areas": ["Twoson"],
            "stats": {"hp": 99, "pp": 0, "offense": 20, "defense": 25, "guts": 50, "speed": 0},
            "battle_tip": "His rants can be distracting; keep your focus!"
        },
        {
            "pk": "enemy",
            "sk": "mock_annoying_reveler#detail",
            "name": "Mock Annoying Reveler",
            "enemy_type": "insect",
            "data_type": "profile",
            "exp_reward": 150,
            "money_reward": 40,
            "initial_status": "",
            "is_boss": "TRUE",
            "drop": {"item": "Party Hat", "chance": "1/128"},  # Hypothetical drop
            "areas": ["Threed"],
            "stats": {"hp": 110, "pp": 5, "offense": 22, "defense": 28, "guts": 40, "speed": 5},
            "battle_tip": "His celebrations can confuse; stay sharp!"
        }
    ]

    mock_enemy_abilities = [
        {
            "pk": "enemy",
            "sk": "mock_abstract_art#ability#confuse",
            "data_type": "ability",
            "ability_aoe": "single",
            "ability_effect": "Confuse the target, causing them to attack themselves or allies.",
            "ability_target": "enemy",
            "name": "Confuse"
        },
        {
            "pk": "enemy",
            "sk": "mock_abstract_art#ability#giggle",
            "data_type": "ability",
            "ability_aoe": "single",
            "ability_effect": "Giggle at the target, causing them to blush.",
            "ability_target": "enemy",
            "name": "Giggle"
        },
        {
            "pk": "enemy",
            "sk": "mock_annoying_old_party_man#ability#nostalgia_trip",
            "data_type": "ability",
            "ability_aoe": "all",
            "ability_effect": "Lowers the morale of the party with tales of the 'good old days'.",
            "ability_target": "enemy",
            "name": "Nostalgia Trip"
        },
        {
            "pk": "enemy",
            "sk": "mock_annoying_reveler#ability#party_hard",
            "data_type": "ability",
            "ability_aoe": "none",
            "ability_effect": "The reveler parties so hard it might heal or buff itself.",
            "ability_target": "self",
            "name": "Party Hard"
        }
    ]

    mock_enemy_resistances = [
        {
            "pk": "enemy",
            "sk": "mock_abstract_art#resistance#confusion",
            "name": "Confusion",
            "data_type": "resistance",
            "resistance_type": "success",
            "resistance_value": 90
        },
        {
            "pk": "enemy",
            "sk": "mock_annoying_old_party_man#resistance#boredom",
            "name": "Boredom",
            "data_type": "resistance",
            "resistance_type": "effect",
            "resistance_value": 50
        },
        {
            "pk": "enemy",
            "sk": "mock_annoying_reveler#resistance#joy",
            "name": "Joy",
            "data_type": "resistance",
            "resistance_type": "damage",
            "resistance_value": 20
        }
    ]

    mock_enemy_areas = [
        {
        "pk": "enemy",
        "sk": "area#belchs_factory#foppy",
        "area": "Belch's Factory",
        "name": "Foppy"
        },
        {
        "pk": "enemy",
        "sk": "area#belchs_factory#mostly_bad_fly",
        "area": "Belch's Factory",
        "name": "Mostly Bad Fly"
        },
        {
        "pk": "enemy",
        "sk": "area#belchs_factory#slimy_little_pile",
        "area": "Belch's Factory",
        "name": "Slimy Little Pile"
        },
        {
        "pk": "enemy",
        "sk": "area#cave_of_the_past#bionic_kraken",
        "area": "Cave of the Past",
        "name": "Bionic Kraken"
        },
        {
        "pk": "enemy",
        "sk": "area#cave_of_the_past#final_starman",
        "area": "Cave of the Past",
        "name": "Final Starman"
        },
        {
        "pk": "enemy",
        "sk": "area#cave_of_the_past#ghost_of_starman",
        "area": "Cave of the Past",
        "name": "Ghost of Starman"
        },
        {
        "pk": "enemy",
        "sk": "area#cave_of_the_past#nuclear_reactor_robot",
        "area": "Cave of the Past",
        "name": "Nuclear Reactor Robot"
        },
        {
        "pk": "enemy",
        "sk": "area#cave_of_the_past#squatter_demon",
        "area": "Cave of the Past",
        "name": "Squatter Demon"
        },
        {
        "pk": "enemy",
        "sk": "area#cave_of_the_past#ultimate_octobot",
        "area": "Cave of the Past",
        "name": "Ultimate Octobot"
        },
        {
        "pk": "enemy",
        "sk": "area#cave_of_the_past#wild_n_wooly_shambler",
        "area": "Cave of the Past",
        "name": "Wild 'n Wooly Shambler"
        },
        {
        "pk": "enemy",
        "sk": "area#deep_darkness#big_pile_of_puke",
        "area": "Deep Darkness",
        "name": "Big Pile of Puke"
        },
        {
        "pk": "enemy",
        "sk": "area#deep_darkness#demonic_petunia",
        "area": "Deep Darkness",
        "name": "Demonic Petunia"
        }
    ]

    mock_items = {
        "key_items": [
            {
            "pk": "item",
            "sk": "atm_card",
            "name": "ATM Card",
            "used_for": "Access ATMs.",
            "item_type": "key_item"
            },
            {
            "pk": "item",
            "sk": "backstage_pass",
            "name": "Backstage Pass",
            "used_for": "Allows access to backstage at Chaos Theater.",
            "item_type": "key_item"
            },
            {
            "pk": "item",
            "sk": "bad_key_machine",
            "name": "Bad Key Machine",
            "used_for": "Opens any locked door or locker.",
            "item_type": "key_item"
            },
            {
            "pk": "item",
            "sk": "bicycle",
            "name": "Bicycle",
            "used_for": "Lets you travel faster in Twoson. You can't ride with Paula or a Teddy Bear.",
            "item_type": "key_item"
            },
            {
            "pk": "item",
            "sk": "brain_stone",
            "name": "Brain Stone",
            "used_for": "Prevents \"disrupting your senses\" or being unable to use PSI abilities.",
            "item_type": "key_item"
            }
        ],
        "weapons": [
            {
            "pk": "item",
            "sk": "baddest_beam",
            "name": "Baddest Beam",
            "offense": 98,
            "used_by": "Jeff",
            "effects": "Repair Broken Harmonica",
            "item_type": "weapon"
            },
            {
            "pk": "item",
            "sk": "big_league_bat",
            "name": "Big League Bat",
            "offense": 54,
            "used_by": "Ness",
            "item_type": "weapon"
            },
            {
            "pk": "item",
            "sk": "bionic_slingshot",
            "name": "Bionic Slingshot",
            "offense": 30,
            "used_by": "Any",
            "item_type": "weapon"
            }
        ],
        "battle_items": [
            {
            "pk": "item",
            "sk": "bag_of_dragonite",
            "name": "Bag of Dragonite",
            "buy_price": 1000,
            "sell_price": 500,
            "target": "enemy",
            "item_type": "battle_item"
            },
            {
            "pk": "item",
            "sk": "bazooka",
            "name": "Bazooka",
            "buy_price": 950,
            "sell_price": 475,
            "used_by": "Jeff",
            "target": "enemy",
            "item_type": "battle_item"
            },
            {
            "pk": "item",
            "sk": "big_bottle_rocket",
            "name": "Big Bottle Rocket",
            "buy_price": 139,
            "sell_price": 69,
            "used_by": "Jeff",
            "target": "enemy",
            "item_type": "battle_item"
            },
            {
            "pk": "item",
            "sk": "bomb",
            "name": "Bomb",
            "buy_price": 148,
            "sell_price": 74,
            "target": "enemy",
            "item_type": "battle_item"
            },
            {
            "pk": "item",
            "sk": "bottle_rocket",
            "name": "Bottle Rocket",
            "buy_price": 29,
            "sell_price": 14,
            "used_by": "Jeff",
            "target": "enemy",
            "item_type": "battle_item"
            }
        ],
        "edibles": [
            {
            "pk": "item",
            "sk": "bag_of_fries",
            "name": "Bag of Fries",
            "effect_type": "hp",
            "effects": "24 HP",
            "item_type": "edible"
            },
            {
            "pk": "item",
            "sk": "banana",
            "name": "Banana",
            "effect_type": "hp",
            "effects": "25 HP",
            "item_type": "edible"
            },
            {
            "pk": "item",
            "sk": "bean_croquette",
            "name": "Bean Croquette",
            "effect_type": "hp",
            "effects": "40 HP",
            "item_type": "edible"
            },
            {
            "pk": "item",
            "sk": "beef_jerky",
            "name": "Beef Jerky",
            "effect_type": "hp",
            "effects": "150 HP",
            "item_type": "edible"
            },
            {
            "pk": "item",
            "sk": "boiled_egg",
            "name": "Boiled Egg",
            "effect_type": "hp",
            "effects": "40 HP",
            "item_type": "edible"
            },
            {
            "pk": "item",
            "sk": "bottle_of_dx_water",
            "name": "Bottle of DX Water",
            "effect_type": "pp",
            "effects": "1 PP (Poo: 40 PP)",
            "item_type": "edible"
            },
            {
            "pk": "item",
            "sk": "bottle_of_water",
            "name": "Bottle of Water",
            "effect_type": "pp",
            "effects": "1 PP (Poo: 10 PP)",
            "item_type": "edible"
            },
            {
            "pk": "item",
            "sk": "bowl_of_rice_gruel",
            "name": "Bowl of Rice Gruel",
            "effect_type": "hp",
            "effects": "200 HP",
            "item_type": "edible"
            },
            {
            "pk": "item",
            "sk": "brain_food_lunch",
            "name": "Brain Food Lunch",
            "effect_type": "hp/pp",
            "effects": "300 HP, 50 PP (Poo: x2)",
            "item_type": "edible"
            }
        ],
        "armor": [
            {
            "pk": "item",
            "sk": "baseball_cap",
            "name": "Baseball Cap",
            "defense": 5,
            "equip_slot": "Other",
            "item_type": "armor"
            },
            {
            "pk": "item",
            "sk": "bracer_of_kings",
            "name": "Bracer of Kings",
            "defense": 30,
            "equip_slot": "Arms",
            "used_by": "Poo",
            "protects": ["Hypnosis"],
            "item_type": "armor"
            }
        ]
    }

    mock_psi = [
        {
        "pk": "psi",
        "sk": "brainshock_alpha",
        "name": "Brainshock α",
        "effects": "Feel Strange",
        "target": "enemy",
        "pp_cost": 10,
        "psi_class": "alpha",
        "psi_type": "Defense",
        "used_by": [{"name": "poo", "level": 24}]
        },
        {
        "pk": "psi",
        "sk": "brainshock_omega",
        "name": "Brainshock Ω",
        "effects": "Feel Strange",
        "target": "enemy",
        "pp_cost": 30,
        "psi_class": "omega",
        "psi_type": "Defense",
        "used_by": [{"name": "poo", "level": 44}]
        },
        {
        "pk": "psi",
        "sk": "defense_up_alpha",
        "name": "Defense Up α",
        "effects": "Raise Defense",
        "target": "ally",
        "pp_cost": 6,
        "psi_class": "alpha",
        "psi_type": "Defense",
        "used_by": [{"name": "paula", "level": 29}]
        },
        {
        "pk": "psi",
        "sk": "defense_up_omega",
        "name": "Defense Up Ω",
        "effects": "Raise Defense",
        "target": "ally",
        "pp_cost": 18,
        "psi_class": "omega",
        "psi_type": "Defense",
        "used_by": [{"name": "paula", "level": 54}]
        },
        {
        "pk": "psi",
        "sk": "fire_alpha",
        "name": "PSI Fire α",
        "points": {"start": 60, "end": 100},
        "effects": "Damage",
        "target": "enemy",
        "aoe": "row",
        "pp_cost": 6,
        "psi_class": "alpha",
        "psi_type": "Offense",
        "used_by": [{"name": "paula", "level": 3}]
        },
        {
        "pk": "psi",
        "sk": "fire_beta",
        "name": "PSI Fire β",
        "points": {"start": 120, "end": 200},
        "effects": "Damage",
        "target": "enemy",
        "aoe": "row",
        "pp_cost": 12,
        "psi_class": "beta",
        "psi_type": "Offense",
        "used_by": [{"name": "paula", "level": 19}]
        },
        {
        "pk": "psi",
        "sk": "fire_gamma",
        "name": "PSI Fire γ",
        "points": {"start": 180, "end": 300},
        "effects": "Damage",
        "target": "enemy",
        "aoe": "row",
        "pp_cost": 20,
        "psi_class": "gamma",
        "psi_type": "Offense",
        "used_by": [{"name": "paula", "level": 37}]
        }
    ]

    mock_shop_items = [
        {"pk": "shop", "sk": "burglin_park_bakery#item#bread_roll", "area": "Twoson", "name": "Bread Roll", "price": 12},
        {"pk": "shop", "sk": "burglin_park_bakery#item#can_of_fruit_juice", "area": "Twoson", "name": "Can of Fruit Juice", "price": 4},
        {"pk": "shop", "sk": "burglin_park_bakery#item#cookie", "area": "Twoson", "name": "Cookie", "price": 7},
        {"pk": "shop", "sk": "burglin_park_bakery#item#cup_of_coffee", "area": "Twoson", "name": "Cup of Coffee", "price": 6},
        {"pk": "shop", "sk": "burglin_park_bakery#item#lucky_sandwich", "area": "Twoson", "name": "Lucky Sandwich", "price": 128},
        {"pk": "shop", "sk": "burglin_park_bakery#item#skip_sandwich", "area": "Twoson", "name": "Skip Sandwich", "price": 38},
        {"pk": "shop", "sk": "burglin_park_banana_lady#item#banana", "area": "Twoson", "name": "Banana", "price": 5},
        {"pk": "shop", "sk": "burglin_park_condiments_shop#item#carton_of_cream", "area": "Twoson", "name": "Carton of Cream", "price": 4},
        {"pk": "shop", "sk": "burglin_park_condiments_shop#item#jar_of_hot_sauce", "area": "Twoson", "name": "Jar of Hot Sauce", "price": 3},
        {"pk": "shop", "sk": "burglin_park_condiments_shop#item#ketchup_packet", "area": "Twoson", "name": "Ketchup Packet", "price": 2},
        {"pk": "shop", "sk": "burglin_park_condiments_shop#item#salt_packet", "area": "Twoson", "name": "Salt Packet", "price": 2},
        {"pk": "shop", "sk": "burglin_park_condiments_shop#item#sprig_of_parsley", "area": "Twoson", "name": "Sprig of Parsley", "price": 2},
        {"pk": "shop", "sk": "burglin_park_condiments_shop#item#sugar_packet", "area": "Twoson", "name": "Sugar Packet", "price": 3},
        {"pk": "shop", "sk": "burglin_park_condiments_shop#item#tin_of_cocoa", "area": "Twoson", "name": "Tin of Cocoa", "price": 4},
        {"pk": "shop", "sk": "burglin_park_egg_salesman#item#fresh_egg", "area": "Twoson", "name": "Fresh Egg", "price": 12},
        {"pk": "shop", "sk": "burglin_park_ruler_salesman#item#ruler", "area": "Twoson", "name": "Ruler", "price": 2},
        {"pk": "shop", "sk": "burglin_park_sign_shop#item#for_sale_sign", "area": "Twoson", "name": "For Sale Sign", "price": 98},
        {"pk": "shop", "sk": "burglin_park_tool_shop#item#broken_iron", "area": "Twoson", "name": "Broken Iron", "price": 149},
        {"pk": "shop", "sk": "burglin_park_tool_shop#item#broken_spray_can", "area": "Twoson", "name": "Broken Spray Can", "price": 189},
        {"pk": "shop", "sk": "burglin_park_tool_shop#item#copper_bracelet", "area": "Twoson", "name": "Copper Bracelet", "price": 349},
        {"pk": "shop", "sk": "burglin_park_tool_shop#item#defense_spray", "area": "Twoson", "name": "Defense Spray", "price": 500},
        {"pk": "shop", "sk": "burglin_park_tool_shop#item#rust_promoter", "area": "Twoson", "name": "Rust Promoter", "price": 89},
        {"pk": "shop", "sk": "burglin_park_tool_shop#item#travel_charm", "area": "Twoson", "name": "Travel Charm", "price": 60},
        {"pk": "shop", "sk": "dalaam_restaurant#item#bottle_of_water", "area": "Dalaam", "name": "Bottle of Water", "price": 4},
        {"pk": "shop", "sk": "dalaam_restaurant#item#bowl_of_rice_gruel", "area": "Dalaam", "name": "Bowl of Rice Gruel", "price": 88},
        {"pk": "shop", "sk": "dalaam_restaurant#item#brain_food_lunch", "area": "Dalaam", "name": "Brain Food Lunch", "price": 800},
        {"pk": "shop", "sk": "dalaam_restaurant#item#jar_of_delisauce", "area": "Dalaam", "name": "Jar of Delisauce", "price": 300},
        {"pk": "shop", "sk": "deep_darkness_arms_dealer#item#combat_yoyo", "area": "Deep Darkness", "name": "Combat Yo-Yo", "price": 1148},
        {"pk": "shop", "sk": "deep_darkness_arms_dealer#item#multi_bottle_rocket", "area": "Deep Darkness", "name": "Multi Bottle Rocket", "price": 2139},
        {"pk": "shop", "sk": "deep_darkness_arms_dealer#item#rust_promoter_dx", "area": "Deep Darkness", "name": "Rust Promoter DX", "price": 289},
        {"pk": "shop", "sk": "deep_darkness_arms_dealer#item#super_bomb", "area": "Deep Darkness", "name": "Super Bomb", "price": 399},
        {"pk": "shop", "sk": "deep_darkness_shop#item#beef_jerky", "area": "Deep Darkness", "name": "Beef Jerky", "price": 70},
        {"pk": "shop", "sk": "deep_darkness_shop#item#bottle_of_dxwater", "area": "Deep Darkness", "name": "Bottle of DXwater", "price": 198},
        {"pk": "shop", "sk": "deep_darkness_shop#item#charm_coin", "area": "Deep Darkness", "name": "Charm Coin", "price": 3000},
        {"pk": "shop", "sk": "deep_darkness_shop#item#cup_of_noodles", "area": "Deep Darkness", "name": "Cup of Noodles", "price": 98},
        {"pk": "shop", "sk": "deep_darkness_shop#item#diamond_band_2", "area": "Deep Darkness", "name": "Diamond Band (2)", "price": 5198},
        {"pk": "shop", "sk": "deep_darkness_shop#item#protein_drink", "area": "Deep Darkness", "name": "Protein Drink", "price": 38},
        {"pk": "shop", "sk": "deep_darkness_shop#item#secret_herb", "area": "Deep Darkness", "name": "Secret Herb", "price": 380},
        {"pk": "shop", "sk": "desert_arms_dealer#item#bomb", "area": "Dusty Dunes Desert", "name": "Bomb", "price": 148}
        ]
    
    mock_shops = [
        {"pk": "shop", "sk": "shop#burglin_park_bakery#detail", "area": "Twoson", "name": "Burglin Park Bakery"},
        {"pk": "shop", "sk": "shop#burglin_park_banana_lady#detail", "area": "Twoson", "name": "Burglin Park Banana Lady"},
        {"pk": "shop", "sk": "shop#burglin_park_condiments_shop#detail", "area": "Twoson", "name": "Burglin Park Condiments Shop"},
        {"pk": "shop", "sk": "shop#burglin_park_egg_salesman#detail", "area": "Twoson", "name": "Burglin Park Egg Salesman"},
        {"pk": "shop", "sk": "shop#burglin_park_ruler_salesman#detail", "area": "Twoson", "name": "Burglin Park Ruler Salesman"},
        {"pk": "shop", "sk": "shop#burglin_park_sign_shop#detail", "area": "Twoson", "name": "Burglin Park Sign Shop"},
        {"pk": "shop", "sk": "shop#burglin_park_tool_shop#detail", "area": "Twoson", "name": "Burglin Park Tool Shop"},
        {"pk": "shop", "sk": "shop#dalaam_restaurant#detail", "area": "Dalaam", "name": "Dalaam Restaurant"},
        {"pk": "shop", "sk": "shop#deep_darkness_arms_dealer#detail", "area": "Deep Darkness", "name": "Deep Darkness Arms Dealer"},
        {"pk": "shop", "sk": "shop#deep_darkness_shop#detail", "area": "Deep Darkness", "name": "Deep Darkness Shop"},
        {"pk": "shop", "sk": "shop#desert_arms_dealer#detail", "area": "Dusty Dunes Desert", "name": "Desert Arms Dealer"},
        {"pk": "shop", "sk": "shop#desert_drugstore#detail", "area": "Dusty Dunes Desert", "name": "Desert Drugstore"},
        {"pk": "shop", "sk": "shop#desert_food_cart#detail", "area": "Dusty Dunes Desert", "name": "Desert Food Cart"},
        {"pk": "shop", "sk": "shop#fourside_bakery#detail", "area": "Fourside", "name": "Fourside Bakery"},
        {"pk": "shop", "sk": "shop#fourside_dept_store_arms_dealer#detail", "area": "Fourside", "name": "Fourside Dept. Store Arms Dealer"},
        {"pk": "shop", "sk": "shop#fourside_dept_store_burger_shop#detail", "area": "Fourside", "name": "Fourside Dept. Store Burger Shop"},
        {"pk": "shop", "sk": "shop#fourside_dept_store_condiments_shop#detail", "area": "Fourside", "name": "Fourside Dept. Store Condiments Shop"},
        {"pk": "shop", "sk": "shop#fourside_dept_store_food_shop#detail", "area": "Fourside", "name": "Fourside Dept. Store Food Shop"},
        {"pk": "shop", "sk": "shop#fourside_dept_store_item_shop#detail", "area": "Fourside", "name": "Fourside Dept. Store Item Shop"},
        {"pk": "shop", "sk": "shop#fourside_dept_store_sports_shop#detail", "area": "Fourside", "name": "Fourside Dept. Store Sports Shop"},
        {"pk": "shop", "sk": "shop#fourside_dept_store_ticket_counter#detail", "area": "Fourside", "name": "Fourside Dept. Store Ticket Counter"},
        {"pk": "shop", "sk": "shop#fourside_dept_store_tool_shop#detail", "area": "Fourside", "name": "Fourside Dept. Store Tool Shop"},
        {"pk": "shop", "sk": "shop#fourside_dept_store_toy_shop#detail", "area": "Fourside", "name": "Fourside Dept. Store Toy Shop"},
        {"pk": "shop", "sk": "shop#fourside_junk_shop#detail", "area": "Fourside", "name": "Fourside Junk Shop"},
        {"pk": "shop", "sk": "shop#grapefruit_falls_salesman#detail", "area": "Threed", "name": "Grapefruit Falls Salesman"},
        {"pk": "shop", "sk": "shop#happy_happy_village_drugstore#detail", "area": "Happy Happy Village", "name": "Happy Happy Village Drugstore"},
        {"pk": "shop", "sk": "shop#happy_happy_village_selfserve_stand#detail", "area": "Happy Happy Village", "name": "Happy Happy Village Self-Serve Stand"},
        {"pk": "shop", "sk": "shop#lost_underworld_shop#detail", "area": "Lost Underworld", "name": "Lost Underworld Shop"},
        {"pk": "shop", "sk": "shop#magicant_shop#detail", "area": "Magicant", "name": "Magicant Shop"},
        {"pk": "shop", "sk": "shop#moonside_hotel_shop#detail", "area": "Moonside", "name": "Moonside Hotel Shop"},
        {"pk": "shop", "sk": "shop#onett_bakery#detail", "area": "Onett", "name": "Onett Bakery"},
        {"pk": "shop", "sk": "shop#onett_burger_shop#detail", "area": "Onett", "name": "Onett Burger Shop"},
        {"pk": "shop", "sk": "shop#onett_drugstore#detail", "area": "Onett", "name": "Onett Drugstore"},
        {"pk": "shop", "sk": "shop#saturn_valley_after_magicant#detail", "area": "Saturn Valley", "name": "Saturn Valley (After Magicant)"},
        {"pk": "shop", "sk": "shop#saturn_valley_shop#detail", "area": "Saturn Valley", "name": "Saturn Valley Shop"},
        {"pk": "shop", "sk": "shop#scaraba_arms_dealer#detail", "area": "Scaraba", "name": "Scaraba Arms Dealer"},
        {"pk": "shop", "sk": "shop#scaraba_condiments_shop#detail", "area": "Scaraba", "name": "Scaraba Condiments Shop"},
        {"pk": "shop", "sk": "shop#scaraba_food_shop#detail", "area": "Scaraba", "name": "Scaraba Food Shop"},
        {"pk": "shop", "sk": "shop#scaraba_shop#detail", "area": "Scaraba", "name": "Scaraba Shop"},
        {"pk": "shop", "sk": "shop#scaraba_snake_bag_shop#detail", "area": "Scaraba", "name": "Scaraba Snake Bag Shop"},
        {"pk": "shop", "sk": "shop#scaraba_snake_shop#detail", "area": "Scaraba", "name": "Scaraba Snake Shop"},
        {"pk": "shop", "sk": "shop#scaraba_southern_shop#detail", "area": "Scaraba", "name": "Scaraba Southern Shop"},
        {"pk": "shop", "sk": "shop#scaraba_tool_shop#detail", "area": "Scaraba", "name": "Scaraba Tool Shop"},
        {"pk": "shop", "sk": "shop#scaraba_water_shop#detail", "area": "Scaraba", "name": "Scaraba Water Shop"},
        {"pk": "shop", "sk": "shop#summers_gelato_cart#detail", "area": "Summers", "name": "Summers Gelato Cart"},
        {"pk": "shop", "sk": "shop#summers_magic_tart_cart#detail", "area": "Summers", "name": "Summers Magic Tart Cart"},
        {"pk": "shop", "sk": "shop#summers_restaurant#detail", "area": "Summers", "name": "Summers Restaurant"},
        {"pk": "shop", "sk": "shop#summers_shop#detail", "area": "Summers", "name": "Summers Shop"},
        {"pk": "shop", "sk": "shop#tenda_village_trading_post#detail", "area": "Tenda Village", "name": "Tenda Village Trading Post"},
        {"pk": "shop", "sk": "shop#threed_arms_dealer#detail", "area": "Threed", "name": "Threed Arms Dealer"},
        {"pk": "shop", "sk": "shop#threed_bakery#detail", "area": "Threed", "name": "Threed Bakery"},
        {"pk": "shop", "sk": "shop#threed_drugstore#detail", "area": "Threed", "name": "Threed Drugstore"},
        {"pk": "shop", "sk": "shop#topolla_theater#detail", "area": "Fourside", "name": "Topolla Theater"},
        {"pk": "shop", "sk": "shop#toto_shop#detail", "area": "Summers", "name": "Toto Shop"},
        {"pk": "shop", "sk": "shop#twoson_dept_store_bakery#detail", "area": "Twoson", "name": "Twoson Dept. Store Bakery"},
        {"pk": "shop", "sk": "shop#twoson_dept_store_burger_shop#detail", "area": "Twoson", "name": "Twoson Dept. Store Burger Shop"},
        {"pk": "shop", "sk": "shop#twoson_dept_store_shop#detail", "area": "Twoson", "name": "Twoson Dept. Store Shop"},
        {"pk": "shop", "sk": "shop#winters_drugstore#detail", "area": "Winters", "name": "Winters Drugstore"},
        {"pk": "shop", "sk": "shop#winters_laboratory_cave_boy#detail", "area": "Winters", "name": "Winters Laboratory Cave Boy"},
        {"pk": "shop", "sk": "shop#winters_laboratory_cave_boy_after_stonehenge#detail", "area": "Winters", "name": "Winters Laboratory Cave Boy (After Stonehenge)"}
        ]

@pytest.fixture
def config():
    return Config()