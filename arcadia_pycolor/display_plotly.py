from __future__ import annotations
import json
import os
import re
import subprocess
import tempfile
import webbrowser
from typing import Dict, List


def display_all_colors() -> None:
    """
    Display an interactive dashboard of all colors, palettes, and gradients.

    This function creates an interactive HTML dashboard showing all available
    colors, palettes, and gradients in the arcadia_pycolor system. The dashboard
    includes searchable tabs for colors, palettes, and gradients, and preserves
    the terminal-style formatting used by the library's __repr__ methods.

    Examples:
        >>> import arcadia_pycolor as apc
        >>> apc.display_all_colors()
    """
    # Create a script to output color information
    script_content = """
import arcadia_pycolor as apc
import json
import os
import sys

# Create a temp directory for the output files
output = {
    "colors": [],
    "palettes": [],
    "gradients": [],
    "gradient_palettes": []
}

# Process colors
for name in apc.colors_all:
    color = getattr(apc.colors, name)
    if hasattr(color, 'name') and hasattr(color, 'hex_code'):
        output["colors"].append({
            "name": color.name,
            "repr": repr(color),
            "hex_code": color.hex_code
        })

# Process palettes
for palette in apc.palettes.all_palettes:
    output["palettes"].append({
        "name": palette.name,
        "repr": repr(palette)
    })

# Process gradients
for gradient in apc.gradients.all_gradients:
    output["gradients"].append({
        "name": gradient.name,
        "repr": repr(gradient)
    })

    # Also add the resampled palette
    resampled = gradient.resample_as_palette(steps=7)
    output["gradient_palettes"].append({
        "name": f"{gradient.name} (resampled)",
        "repr": repr(resampled)
    })

# Write the output as JSON
print(json.dumps(output))
"""

    # Write the script to a temporary file
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.py') as f:
        f.write(script_content)
        script_path = f.name

    # Run the script and capture the output
    try:
        result = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)
    except Exception as e:
        print(f"Error collecting color data: {e}")
        return
    finally:
        # Clean up the script file
        os.unlink(script_path)

    # Create HTML content
    html_content = generate_dashboard_html(data)

    # Write the HTML to a temporary file
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
        f.write(html_content)
        temp_filepath = f.name

    # Open the HTML file in the default web browser
    webbrowser.open('file://' + temp_filepath)

    return temp_filepath


def ansi_to_html(ansi_text: str) -> str:
    """
    Convert ANSI color codes to HTML span elements with inline CSS.

    Args:
        ansi_text: Text containing ANSI color escape sequences

    Returns:
        HTML string with color formatting
    """
    # Background color pattern: \033[48;2;R;G;Bm
    bg_pattern = r'\033\[48;2;(\d+);(\d+);(\d+)m'
    # Foreground color pattern: \033[38;2;R;G;Bm
    fg_pattern = r'\033\[38;2;(\d+);(\d+);(\d+)m'
    # Reset pattern: \033[0m
    reset_pattern = r'\033\[0m'

    # Replace background colors
    html_text = re.sub(
        bg_pattern,
        r'<span style="background-color: rgb(\1, \2, \3);">',
        ansi_text
    )

    # Replace foreground colors
    html_text = re.sub(
        fg_pattern,
        r'<span style="color: rgb(\1, \2, \3);">',
        html_text
    )

    # Replace reset codes with closing spans
    html_text = html_text.replace('\033[0m', '</span>')

    return html_text


def generate_dashboard_html(data: Dict) -> str:
    """
    Generate HTML content for the color dashboard.

    Args:
        data: Dictionary containing colors, palettes, and gradients data
    """
    # Process the data
    colors_data = get_colors_html(data["colors"])
    palettes_data = get_palettes_html(data["palettes"])
    gradients_data = get_gradients_html(data["gradients"], data["gradient_palettes"])

    # Create HTML
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Arcadia PyColor Dashboard</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                max-width: 1200px;
                margin: 0 auto;
            }}

            h1, h2 {{
                color: #333;
            }}

            .tab {{
                overflow: hidden;
                border: 1px solid #ccc;
                background-color: #f1f1f1;
                border-radius: 5px 5px 0 0;
            }}

            .tab button {{
                background-color: inherit;
                float: left;
                border: none;
                outline: none;
                cursor: pointer;
                padding: 14px 16px;
                transition: 0.3s;
                font-size: 16px;
            }}

            .tab button:hover {{
                background-color: #ddd;
            }}

            .tab button.active {{
                background-color: #5088C5;
                color: white;
            }}

            .tabcontent {{
                display: none;
                padding: 20px;
                border: 1px solid #ccc;
                border-top: none;
                border-radius: 0 0 5px 5px;
            }}

            .color-list {{
                margin-top: 20px;
                line-height: 1.2;
                white-space: pre;
                font-family: monospace;
                padding: 0;
            }}

            .color-simple-item {{
                display: block;
                margin-bottom: 3px;
                cursor: pointer;
                position: relative;
                transition: background-color 0.2s;
            }}

            .color-simple-item:hover {{
                background-color: #f0f0f0;
            }}

            .color-simple-item.copied {{
                background-color: #e8f4e8;
            }}

            .palette-grid, .gradient-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }}

            .palette-item, .gradient-item {{
                border: 1px solid #eee;
                border-radius: 5px;
                padding: 15px;
            }}

            .search {{
                width: 100%;
                padding: 10px;
                margin-bottom: 20px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 16px;
            }}

            pre {{
                overflow-x: auto;
                background-color: #f9f9f9;
                padding: 8px;
                border-radius: 4px;
                margin: 0;
            }}

            .item-name {{
                font-weight: bold;
                margin-bottom: 10px;
                font-size: 18px;
            }}

            .color-repr, .palette-repr, .gradient-repr {{
                font-family: monospace;
                white-space: pre;
                background-color: #f9f9f9;
                padding: 10px;
                border-radius: 4px;
                font-size: 14px;
                line-height: 1.5;
                overflow-x: auto;
            }}

            .notification {{
                position: fixed;
                bottom: 20px;
                right: 20px;
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border-radius: 4px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
                display: none;
                z-index: 1000;
            }}
        </style>
    </head>
    <body>
        <h1>Arcadia PyColor Dashboard</h1>

        <div class="tab">
            <button class="tablinks active" onclick="openTab(event, 'Colors')">Colors</button>
            <button class="tablinks" onclick="openTab(event, 'Palettes')">Palettes</button>
            <button class="tablinks" onclick="openTab(event, 'Gradients')">Gradients</button>
        </div>

        <div id="Colors" class="tabcontent" style="display: block;">
            <input type="text" id="colorSearch" class="search" placeholder="Search colors...">
            {colors_data}
        </div>

        <div id="Palettes" class="tabcontent">
            <input type="text" id="paletteSearch" class="search" placeholder="Search palettes...">
            <div class="palette-grid">
                {palettes_data}
            </div>
        </div>

        <div id="Gradients" class="tabcontent">
            <input type="text" id="gradientSearch" class="search" placeholder="Search gradients...">
            <div class="gradient-grid">
                {gradients_data}
            </div>
        </div>

        <div id="notification" class="notification"></div>

        <script>
            // Function to copy hex code to clipboard
            function copyHexCode(element) {{
                const hexCode = element.getAttribute('data-hex');
                navigator.clipboard.writeText(hexCode)
                    .then(() => {{
                        // Show notification
                        const notification = document.getElementById('notification');
                        notification.textContent = 'Copied: ' + hexCode;
                        notification.style.display = 'block';

                        // Add highlighting to the clicked element
                        element.classList.add('copied');

                        // Hide notification and remove highlighting after a moment
                        setTimeout(() => {{
                            notification.style.display = 'none';
                            element.classList.remove('copied');
                        }}, 1500);
                    }})
                    .catch(err => {{
                        console.error('Could not copy text: ', err);
                    }});
            }}

            function openTab(evt, tabName) {{
                var i, tabcontent, tablinks;

                tabcontent = document.getElementsByClassName("tabcontent");
                for (i = 0; i < tabcontent.length; i++) {{
                    tabcontent[i].style.display = "none";
                }}

                tablinks = document.getElementsByClassName("tablinks");
                for (i = 0; i < tablinks.length; i++) {{
                    tablinks[i].className = tablinks[i].className.replace(" active", "");
                }}

                document.getElementById(tabName).style.display = "block";
                evt.currentTarget.className += " active";
            }}

            // Search functionality for colors
            document.getElementById('colorSearch').addEventListener('input', function() {{
                filterItems('color-simple-item', this.value);
            }});

            // Search functionality for palettes
            document.getElementById('paletteSearch').addEventListener('input', function() {{
                filterItems('palette-item', this.value);
            }});

            // Search functionality for gradients
            document.getElementById('gradientSearch').addEventListener('input', function() {{
                filterItems('gradient-item', this.value);
            }});

            function filterItems(itemClass, query) {{
                if (itemClass === 'color-simple-item') {{
                    // Special handling for color spans in pre
                    query = query.toLowerCase();
                    const items = document.getElementsByClassName(itemClass);

                    for (let i = 0; i < items.length; i++) {{
                        const item = items[i];
                        const text = item.textContent.toLowerCase();

                        if (text.includes(query)) {{
                            item.style.display = "block";
                        }} else {{
                            item.style.display = "none";
                        }}
                    }}
                }} else {{
                    // Normal handling for other items
                    query = query.toLowerCase();
                    const items = document.getElementsByClassName(itemClass);

                    for (let i = 0; i < items.length; i++) {{
                        const item = items[i];
                        const text = item.textContent.toLowerCase();

                        if (text.includes(query)) {{
                            item.style.display = "";
                        }} else {{
                            item.style.display = "none";
                        }}
                    }}
                }}
            }}
        </script>
    </body>
    </html>
    """

    return html


def get_colors_html(colors_data: List[Dict]) -> str:
    """
    Generate HTML for the colors tab.

    Args:
        colors_data: List of color data dictionaries
    """
    # Create a compact display of colors with no extra newlines
    html = '<pre class="color-list">'

    for color in colors_data:
        # Get the representation with ANSI color codes
        repr_text = color["repr"]
        # Convert ANSI to HTML
        repr_html = ansi_to_html(repr_text)

        # Add the color as a line in the pre element with copy-on-click functionality
        hex_code = color["hex_code"]
        color_name = color["name"]
        html += f'<span class="color-simple-item" data-name="{color_name}" data-hex="{hex_code}" title="Click to copy {hex_code}" onclick="copyHexCode(this)">{repr_html}</span>'

    html += '</pre>'

    return html


def get_palettes_html(palettes_data: List[Dict]) -> str:
    """
    Generate HTML for the palettes tab.

    Args:
        palettes_data: List of palette data dictionaries
    """
    # Generate HTML for each palette
    palette_items = []
    for palette in palettes_data:
        repr_text = palette["repr"]
        # Convert ANSI to HTML
        repr_html = ansi_to_html(repr_text)

        palette_items.append(
            f"""
            <div class="palette-item" data-name="{palette['name']}">
                <div class="item-name">{palette['name']}</div>
                <div class="palette-repr">{repr_html}</div>
            </div>
            """
        )

    return "".join(palette_items)


def get_gradients_html(gradients_data: List[Dict], resampled_data: List[Dict]) -> str:
    """
    Generate HTML for the gradients tab.

    Args:
        gradients_data: List of gradient data dictionaries
        resampled_data: List of resampled gradient palette data
    """
    # Generate HTML for each gradient
    gradient_items = []

    for i, gradient in enumerate(gradients_data):
        # Get the gradient's representation
        repr_text = gradient["repr"]
        # Convert ANSI to HTML
        repr_html = ansi_to_html(repr_text)

        # Get the resampled palette representation
        resampled = resampled_data[i]
        palette_html = ansi_to_html(resampled["repr"])

        gradient_items.append(
            f"""
            <div class="gradient-item" data-name="{gradient['name']}">
                <div class="item-name">{gradient['name']}</div>
                <div class="gradient-repr">{repr_html}</div>
                <div style="margin-top: 15px;">
                    <b>Resampled as palette (7 steps):</b>
                    <div class="palette-repr">{palette_html}</div>
                </div>
            </div>
            """
        )

    return "".join(gradient_items)


# Reference to colors_all - will be populated when imported by __init__.py
colors_all = []
