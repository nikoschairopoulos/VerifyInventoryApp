json_form_behaviour = {
    "building_level": {
        "technologies": [
            {
                "text": 'Electrical Generators',
                "value": "El. Generators",
                "IS_B_COMPONENT":True,
                "types": [
                    {
                        "text": "photovoltaic panel",
                        "value": "pv",
                        "subtypes": None
                    },
                    {
                        "text": "wind turbine",
                        "value": "wind",
                        "subtypes": None
                    }
                ],
            },
            {
                "text": "Thermal Sources",
                "value": "Thermal Sources",
                "IS_B_COMPONENT":True,
                "types": [
                    {
                        "text": "boiler",
                        "value": "boiler",
                        "subtypes": [
                            {
                                "text": "natural gas",
                                "value": "ngas"
                            },
                            {
                                "text": "diesel",
                                "value": "diesel"
                            },
                            {
                                "text": "biomass",
                                "value": "biomass"
                            },
                            {
                                "text": "oil",
                                "value": "oil"
                            }
                        ]
                    },
                    {
                        "text": "heatpump",
                        "value": "heat_pump",
                        "subtypes": None
                    },
                    {
                        "text": "aircondition",
                        "value": "air_conditioning",
                        "subtypes": None
                    },
                    {
                        "text": "solar thermal panel",
                        "value": "solar",
                        "subtypes": None
                    }, {
                        "text": "geo thermal",
                        "value": "geo",
                        "subtypes": None
                    },
                    {
                        "text": "district heating",
                        "value": "district_heating",
                        "subtypes": None
                    },
                    {
                        "text": "fan coil",
                        "value": "fan",
                        "subtypes": None
                    },
                ],
            },
            {
                "text": 'Glazing',
                "value": "Glazing",
                "IS_B_COMPONENT":True,
                "types": [
                    {
                        "text": "frame",
                        "value": "frame",
                        "subtypes": None
                    },
                    {
                        "text": "glass",
                        "value": "glass",
                        "subtypes": None
                    }
                ],
            },
            {
                "text": 'Insulation',
                "value": 'Insulation',
                "IS_B_COMPONENT":True,
                "types": [
                    {
                        "text": "building insulation",
                        "value": "building_insulation",
                        "subtypes": None
                    },
                    {
                        "text": "water tank insulation",
                        "value": "dhw_insulation",
                        "subtypes": None
                    }
                ],
            },
            {
                "text": 'PCM',
                "value": 'PCM',
                "IS_B_COMPONENT":True,
                "types": [
                    {
                        "text": "phase change material standard",
                        "value": "pcm",
                        "subtypes": None
                    },
                ],
            },
            {
                "text": 'Water Storage',
                "value": 'Water Storage',
                "IS_B_COMPONENT":True,
                "types": [
                    {
                        "text": "water storage tank",
                        "value": "hot_water",
                        "subtypes": None
                    },
                ],
            },
            {
                "text": 'Ventilation',
                "value": 'Ventilation',
                "IS_B_COMPONENT":True,
                "types": [
                    {
                        "text": "mixing ventilation",
                        "value": "mixing_ventilation",
                        "subtypes": None
                    },
                    {
                        "text": "displacement ventilation",
                        "value": "displacement_ventilation",
                        "subtypes": None
                    },
                    {
                        "text": "stratum ventilation",
                        "value": "stratum_ventilation ",
                        "subtypes": None
                    },
                    {
                        "text": "natural ventilation",
                        "value": "natural_ventilation",
                        "subtypes": None
                    },
                    {
                        "text": "micro ventilation",
                        "value": "micro_ventilation",
                        "subtypes": None
                    }
                ],
            },
            {
                "text": 'Electrical Storage (ESS)',
                "value": "El. Storage",
                "IS_B_COMPONENT":True,
                "types": [
                    {
                        "text": "flywheel",
                        "value": "flywheel",
                        "subtypes": None
                    },
                ],
            },
            {
                "text": "Batteries (Buildings)",
                "value": "B_Batteries",
                "IS_B_COMPONENT":True,
                "types": [
                    {
                        "text": "battery Li-ion",
                        "value": "battery_li_ion",
                        "subtypes": None
                    },
                    {
                        "text": "battery lead acid",
                        "value": "lead_acid",
                        "subtypes": None
                    },
                    {
                        "text": "battery flow",
                        "value": "flow",
                        "subtypes": None
                    },
                ],
            }
        ]
    },
    "district_level": {
        "technologies": [

            {
                "text": 'Plants',
                "value": 'Plants',
                "IS_B_COMPONENT":False,
                "types": [
                    {
                        "text": 'Power Plant',
                        "value": 'power_plant',
                        "subtypes": None
                    },
                    {
                        "text": 'Geothermal / Hydro Plant',
                        "value": "geothermal_hydro_plant",
                        "subtypes": None
                    },
                    {
                        "text": 'Incineration Plant',
                        "value": 'incineration_plant',
                        "subtypes": None
                    },
                    {
                        "text": "Tidal Plant",
                        "value": "tidal_device_plant",
                        "subtypes": None
                    },
                    {
                        "text": "Fuel Cell Plant",
                        "value": "fuel_cell_plant",
                        "subtypes": None
                    },
                    {
                        "text": "Solar Park",
                        "value": "solar_park",
                        "subtypes": None
                    },
                    {
                        "text": "Wind Park",
                        "value": "wind_park",
                        "subtypes": None
                    }
                ]}
            ,
            {
                "text": "Transport",
                "value": 'Transport',
                "IS_B_COMPONENT":False,
                "types": [
                    {
                        "text": 'Electric Vehicle',
                        "value": "electric_vehicle",
                        "subtypes": None
                    },
                    {
                        "text": 'Conventional Vehicle',
                        "value": "conventional_vehicle",
                        "subtypes": None
                    }
                ],
            },
            {
                "text": 'Public',
                "value": 'Public',
                "IS_B_COMPONENT":False,
                "types": [
                    {
                        "text": 'Charging Station',
                        "value": "charging_station",
                        "subtypes": None
                    },
                    {
                        "text": 'Transformer',
                        "value": "transformer",
                        "subtypes": None
                    },
                    {
                        "text": 'Lighting',
                        "value": "lighting",
                        "subtypes": None
                    },
                    {
                        "text": 'Interconnection',
                        "value": "interconnection",
                        "subtypes": None
                    }
                ],
            },
            {
                "text": "Batteries + ESS",
                "value": "D_Batteries",
                "IS_B_COMPONENT":False,
                "types": [
                    {
                        "text": "battery Li-ion",
                        "value": "battery_li_ion",
                        "subtypes": None
                    },
                    {
                        "text": "battery lead acid",
                        "value": "lead_acid",
                        "subtype": None
                    },
                    {
                        "text": "battery flow",
                        "value": "flow",
                        "subtypes": None
                    },
                    {
                        "text": "flywheel",
                        "value": "flywheel",
                        "subtypes": None
                    }
                ],
            }

        ]}
}


