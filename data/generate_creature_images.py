import json
import dotenv
import requests
import os
import time
import base64

dotenv.load_dotenv()

api_key = os.getenv("STABILITY_API_KEY")

with open('creature_data.json', 'r') as f:
    creature_data = json.load(f)

def generate_creature_image(creature_data: dict):
    prompt = f"""
    An anime-style drawing of a Pokemon artstation creature that is {creature_data['description']}. The art style is 2D, semi-watercolor in a Pokemon-style theme, detailed and energetic on a plain white background."
    """

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    json_data = {
        'text_prompts': [
            {
                'text': prompt
            }
        ],
        'cfg_scale': 7,
        'height': 832,
        'width': 1216,
        'samples': 1,
        'steps': 40
    }

    engine_id = 'stable-diffusion-xl-1024-v1-0'

    url = f'https://api.stability.ai/v1/generation/{engine_id}/text-to-image'

    response = requests.post(url=url, headers=headers, json=json_data)

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    image = data["artifacts"][0]

    with open(f"creature_images/{creature_data['ticker']}.png", "wb") as f:
        f.write(base64.b64decode(image["base64"]))

def main():
    request_count = 0
    start_time = time.time()

    # Just one creature for testing
    # generate_creature_image(creature_data[0])

    for creature in creature_data:
        if os.path.exists(f'creature_images/{creature["ticker"]}.png'):
            print(f"Image for {creature['ticker']} already exists.")
            continue

        print(f"Generating image for {creature['ticker']}")
        generate_creature_image(creature)

        request_count += 1
        if request_count >= 150:
            elapsed_time = time.time() - start_time
            if elapsed_time < 10:
                time.sleep(10 - elapsed_time)
            start_time = time.time()
            request_count = 0

if __name__ == '__main__':
    main()
