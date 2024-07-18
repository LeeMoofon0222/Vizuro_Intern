import json

def round_values(obj):
    for key in obj.keys():
        if isinstance(obj[key], float):
            obj[key] = round(obj[key], 2)
        elif isinstance(obj[key], dict):
            round_values(obj[key])
    return obj

def remove_first_two_keys(json_objects):
    updated_json_objects = []
    for obj in json_objects:
        keys_to_remove = list(obj.keys())[:2]
        for key in keys_to_remove:
            obj.pop(key)
        obj = round_values(obj)
        updated_json_objects.append(obj)
    return updated_json_objects

def main():
    input_file = 'edges 1.json'
    output_file = 'output.json'

    with open(input_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    updated_json_data = remove_first_two_keys(json_data)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(updated_json_data, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    main()
