POST_VALIDATIONS = {
    "Emojis": (
        lambda emojis: emojis not in ["No", "Low", "Medium", "High"],
        'The value for Emojis must be between ["No", "Low", "Medium", "High"]',
    ),
    "Type": (
        lambda post_type: post_type not in ["Product", "Service", "Event", "Others"],
        'The value for Emojis must be between ["Product", "Service", "Event", "Others"]',
    ),
    "Language": (
        lambda language: language not in ["English", "Potuguese", "Spanish"],
        'The value for Emojis must be between ["English", "Potuguese", "Spanish"]',
    ),
    "Size": (
        lambda size: 100 > size > 5000,
        "The generated post size must be between 100 and 5000",
    ),
    "Content": (
        lambda post_content: len(post_content) <= 30,
        "Post content/improvements must be 30 characters or more",
    ),
}

IMAGE_VALIDATIONS = {
    "Prompt": (
        lambda prompt: len(prompt) < 10,
        "Prompt text must contain at least 10 characters",
    ),
    "Size": (
        lambda size: size
        not in ("256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"),
        'The size must be between the listed values: ["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"], '
        "if a value is not provided the generated image will be of the proportions 1024x1024",
    ),
    "Quality": (
        lambda quality: quality not in ("standard", "hd"),
        'The quality must be between the listed values: ["standard", "hd"], if a value is not provided the generated '
        "image will be of the quality standard"
    )
}

