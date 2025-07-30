import pandas as pd

# Example DataFrames
list1 = [
    {
        "additional_information": "",
        "description": "",
        "display": "Boiler",
        "id": "bvh0iji3k1k579s45oqg",
        "readable_key": "BOILER"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Burner",
        "id": "bvh0iji3k1k579s45ok0",
        "readable_key": "BURNER"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Chillers",
        "id": "c4jph2fvh5p2kt8gaod0",
        "readable_key": "CHILLERS"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Domestic Refrigeration",
        "id": "c4jph2fvh5p2kt8gaoag",
        "readable_key": "DOMESTIC_REFRIGERATION"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Dryer",
        "id": "bvh0iji3k1k579s45ong",
        "readable_key": "DRYER"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Fixed Fire Suppression Equipment",
        "id": "c4npc0fvh5p7ptpegbbg",
        "readable_key": "FIXED_FIRE_SUPPRESION_EQUIPMENT"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Flare",
        "id": "bvh0iji3k1k579s45opg",
        "readable_key": "FLARE"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Furnace",
        "id": "bvh0iji3k1k579s45olg",
        "readable_key": "FURNACE"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Generator",
        "id": "cn35lm5upt9g72rf6gmg",
        "readable_key": "GENERATOR"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Heater",
        "id": "bvh0iji3k1k579s45ol0",
        "readable_key": "HEATER"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Incinerator",
        "id": "bvh0iji3k1k579s45om0",
        "readable_key": "INCINERATOR"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Industrial Refrigeration including Food Processing and Cold Storage",
        "id": "c4jph2fvh5p2kt8gaocg",
        "readable_key": "INDUSTRIAL_REFRIGERATION_INCLUDING_FOOD_PROCESSING_AND_COLD_STORAGE"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Internal Combustion Engine",
        "id": "bvh0iji3k1k579s45oo0",
        "readable_key": "INTERNAL_COMBUSTION_ENGINE"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Kiln",
        "id": "bvh0iji3k1k579s45omg",
        "readable_key": "KILN"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Medium \u0026 Large Commercial Refrigeration",
        "id": "c4jph2fvh5p2kt8gaobg",
        "readable_key": "MEDIUM_AND_LARGE_COMMERCIAL_REFRIGERATION"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Mobile Air Conditioning",
        "id": "c4jph2fvh5p2kt8gaoe0",
        "readable_key": "MOBILE_AIR_CONDITIONING"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Open Burning",
        "id": "bvh0iji3k1k579s45op0",
        "readable_key": "OPEN_BURNING"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Other",
        "id": "bvh0iji3k1k579s45oq0",
        "readable_key": "OTHER"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Oven",
        "id": "bvh0iji3k1k579s45on0",
        "readable_key": "OVEN"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Portable Fire Suppression Equipment",
        "id": "c4npc0fvh5p7ptpegbb0",
        "readable_key": "PORTABLE_FIRE_SUPPRESION_EQUIPMENT"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Residential and Commercial A/C including Heat Pumps",
        "id": "c4jph2fvh5p2kt8gaodg",
        "readable_key": "RESIDENTIAL_AND_COMMERCIAL_A_OR_C_INCLUDING_HEAT_PUMPS"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Stand-alone Commercial Applications",
        "id": "c4jph2fvh5p2kt8gaob0",
        "readable_key": "STAND_ALONE_COMMERCIAL_APPLICATIONS"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Thermal Oxidizer",
        "id": "bvh0iji3k1k579s45oog",
        "readable_key": "THERMAL_OXIDIZER"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Transport Refrigeration",
        "id": "c4jph2fvh5p2kt8gaoc0",
        "readable_key": "TRANSPORT_REFRIGERATION"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Turbine",
        "id": "bvh0iji3k1k579s45okg",
        "readable_key": "TURBINE"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Fixed Fire Suppression Equipment",
        "id": "c4npc0fvh5p7ptpegbbg",
        "readable_key": "FIXED_FIRE_SUPPRESION_EQUIPMENT"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Other",
        "id": "bvh0iji3k1k579s45oq0",
        "readable_key": "OTHER"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Portable Fire Suppression Equipment",
        "id": "c4npc0fvh5p7ptpegbb0",
        "readable_key": "PORTABLE_FIRE_SUPPRESION_EQUIPMENT"
    },
{
        "additional_information": "",
        "description": "",
        "display": "Chillers",
        "id": "c4jph2fvh5p2kt8gaod0",
        "readable_key": "CHILLERS"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Domestic Refrigeration",
        "id": "c4jph2fvh5p2kt8gaoag",
        "readable_key": "DOMESTIC_REFRIGERATION"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Industrial Refrigeration including Food Processing and Cold Storage",
        "id": "c4jph2fvh5p2kt8gaocg",
        "readable_key": "INDUSTRIAL_REFRIGERATION_INCLUDING_FOOD_PROCESSING_AND_COLD_STORAGE"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Medium \u0026 Large Commercial Refrigeration",
        "id": "c4jph2fvh5p2kt8gaobg",
        "readable_key": "MEDIUM_AND_LARGE_COMMERCIAL_REFRIGERATION"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Mobile Air Conditioning",
        "id": "c4jph2fvh5p2kt8gaoe0",
        "readable_key": "MOBILE_AIR_CONDITIONING"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Other",
        "id": "bvh0iji3k1k579s45oq0",
        "readable_key": "OTHER"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Residential and Commercial A/C including Heat Pumps",
        "id": "c4jph2fvh5p2kt8gaodg",
        "readable_key": "RESIDENTIAL_AND_COMMERCIAL_A_OR_C_INCLUDING_HEAT_PUMPS"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Stand-alone Commercial Applications",
        "id": "c4jph2fvh5p2kt8gaob0",
        "readable_key": "STAND_ALONE_COMMERCIAL_APPLICATIONS"
    },
    {
        "additional_information": "",
        "description": "",
        "display": "Transport Refrigeration",
        "id": "c4jph2fvh5p2kt8gaoc0",
        "readable_key": "TRANSPORT_REFRIGERATION"
    }
]

df_keys = pd.DataFrame.from_dict(list1)
df_data = pd.read_excel("dataSource/Base_Carbone_V23.6-v2.xlsx")

keys = df_keys['readable_key'].dropna().tolist()

# Function to find keys in a row (across all columns)
def find_keys_in_row(row):
    text_combined = ' '.join([str(cell) for cell in row if pd.notnull(cell)]).lower()
    return [key for key in keys if key.lower() in text_combined]

# Apply to all rows
df_data['found_keys'] = df_data.apply(find_keys_in_row, axis=1)
# Summary: Count how many times each key was found
# Initialize summary with all keys from df_keys
summary = {key: 0 for key in df_keys['readable_key']}

# Count how many times each key appears in df_data['keys_found']
for keys in df_data['found_keys']:
    for key in keys:
        summary[key] += 1

print("\n🔍 Summary of keys in df_data:")
for key, count in summary.items():
    print(f"{key}: {count} rows matched")

df_data.to_excel("FoundKeys_BC.xlsx", index=False)
print(df_data.columns)

