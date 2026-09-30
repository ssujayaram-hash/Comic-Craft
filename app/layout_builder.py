def build_comic_layout(outline, story, image_paths):
    layout = []

    outline_panels = outline.get("panels", [])
    story_panels = story.get("panels", [])

    for index in range(5):
        outline_panel = outline_panels[index]
        story_panel = story_panels[index]

        layout.append({
            "panel_number": outline_panel["panel_number"],
            "title": outline_panel["title"],
            "scene_description": outline_panel["scene_description"],
            "image_prompt": outline_panel["image_prompt"],
            "image_path": image_paths[index],
            "narration": story_panel["narration"],
            "dialogue": story_panel["dialogue"]
        })

    return layout