import requests
import base64
import json
import os

# Configuration
WEBUI_URL = "http://localhost:7860"  # Change to cloud server URL if needed
REFERENCE_IMAGE_PATH = "matrix_dvd_original.jpg"  # Path to original DVD cover image
OUTPUT_IMAGE_PATH = "matrix_dvd_variation1.png"  # Output path for generated image

# Prompt and generation parameters
payload = {
    "prompt": "A futuristic cyberpunk DVD cover for The Matrix, featuring Neo in a dynamic pose, glowing green and blue holographic effects, neon-lit cityscape background, sleek metallic title font with glitch effect, Warner Bros. logo in a futuristic style, high detail, cinematic lighting, vibrant colors",
    "negative_prompt": "blurry, low quality, distorted text, extra limbs, unrealistic proportions, watermark, signature",
    "steps": 50,
    "cfg_scale": 7.5,
    "width": 512,
    "height": 768,
    "sampler_name": "Euler a",
    "denoising_strength": 0.6,
    "init_images": [],  # Will be filled with base64-encoded reference image
}

# Function to encode image to base64
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded_string}"

# Encode reference image
if not os.path.exists(REFERENCE_IMAGE_PATH):
    raise FileNotFoundError(f"Reference image {REFERENCE_IMAGE_PATH} not found")
payload["init_images"] = [encode_image_to_base64(REFERENCE_IMAGE_PATH)]

# Send request to Automatic1111 WebUI API (img2img endpoint)
response = requests.post(f"{WEBUI_URL}/sdapi/v1/img2img", json=payload)

# Check response
if response.status_code == 200:
    result = response.json()
    # Save the generated image
    generated_image = base64.b64decode(result["images"][0])
    with open(OUTPUT_IMAGE_PATH, "wb") as f:
        f.write(generated_image)
    print(f"Generated image saved to {OUTPUT_IMAGE_PATH}")
else:
    print(f"Error: {response.status_code} - {response.text}")

# Note: To capture a screenshot of the WebUI configuration, manually take a screenshot
# of the img2img tab in the WebUI with the parameters set, and save it as `webui_screenshot.png`.
