#!/usr/bin/env python3
import json
import sys
from pathlib import Path

def create_html_from_json(json_file_path, output_html_path="kanzenshuu_wj_toriyama.html"):
    """
    Convert JSON data from Kanzenshuu spider to an HTML page
    displaying all wj_toriyama_html content
    """
    
    # Read the JSON file
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File {json_file_path} not found")
        return False
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON file - {e}")
        return False
    
    # Filter out entries that have wj_toriyama_html content
    entries_with_content = []
    for entry in data:
        if entry.get('wj_toriyama_html') and entry.get('status') == 'found':
            entries_with_content.append(entry)
    
    print(f"Found {len(entries_with_content)} entries with wj_toriyama content out of {len(data)} total entries")
    
    # Create HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kanzenshuu Dragon Ball Manga - Toriyama Comments</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
            line-height: 1.6;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            color: #333;
            margin-bottom: 10px;
        }}
        
        .stats {{
            color: #666;
            font-size: 0.9em;
        }}
        
        .chapter-entry {{
            background-color: #fff;
            margin-bottom: 20px;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 4px solid #ff6b35;
        }}
        
        .chapter-header {{
            background-color: #f8f9fa;
            padding: 10px 15px;
            margin: -20px -20px 15px -20px;
            border-radius: 10px 10px 0 0;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .chapter-title {{
            font-size: 1.2em;
            font-weight: bold;
            color: #2c3e50;
            margin: 0;
        }}
        
        .chapter-url {{
            font-size: 0.9em;
            color: #6c757d;
            margin: 5px 0 0 0;
        }}
        
        .chapter-url a {{
            color: #007bff;
            text-decoration: none;
        }}
        
        .chapter-url a:hover {{
            text-decoration: underline;
        }}
        
        .wj-toriyama-content {{
            margin-top: 15px;
        }}
        
        /* Style the wj_toriyama divs */
        .wj_toriyama {{
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 15px;
            margin: 10px 0;
            font-style: italic;
        }}
        
        .back-to-top {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #ff6b35;
            color: white;
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            font-size: 18px;
            cursor: pointer;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        }}
        
        .back-to-top:hover {{
            background-color: #e55a2b;
            transform: translateY(-2px);
        }}
        
        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}
            
            .chapter-entry {{
                padding: 15px;
            }}
            
            .chapter-header {{
                margin: -15px -15px 15px -15px;
                padding: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🐉 Kanzenshuu Dragon Ball Manga</h1>
        <h2>Toriyama's Weekly Jump Comments</h2>
        <div class="stats">
            <p>Found <strong>{len(entries_with_content)}</strong> chapters with Toriyama comments</p>
            <p>Generated from: {Path(json_file_path).name}</p>
        </div>
    </div>
    
    <div class="content">
"""
    
    # Add each entry to the HTML
    for i, entry in enumerate(entries_with_content, 1):
        chapter_id = entry.get('chapter_id', 'Unknown')
        chapter_date = entry.get('chapter_date', 'Unknown')
        url = entry.get('url', '#')
        wj_toriyama_html = entry.get('wj_toriyama_html', '')
        
        html_content += f"""
        <div class="chapter-entry" id="chapter-{i}">
            <div class="chapter-header">
                <h3 class="chapter-title">Chapter {chapter_id.replace('chp-', '').lstrip('0')}</h3>
                <p class="chapter-url">
                    <strong>Date:</strong> {chapter_date} | 
                    <strong>Source:</strong> <a href="{url}" target="_blank">{url}</a>
                </p>
            </div>
            
            <div class="wj-toriyama-content">
                {wj_toriyama_html}
            </div>
        </div>
"""
    
    # Close the HTML
    html_content += """
    </div>
    
    <button class="back-to-top" onclick="window.scrollTo({top: 0, behavior: 'smooth'})" title="Back to top">
        ↑
    </button>
    
    <script>
        // Show/hide back to top button
        window.addEventListener('scroll', function() {
            const backToTop = document.querySelector('.back-to-top');
            if (window.pageYOffset > 300) {
                backToTop.style.display = 'block';
            } else {
                backToTop.style.display = 'none';
            }
        });
        
        // Initially hide the button
        document.querySelector('.back-to-top').style.display = 'none';
    </script>
</body>
</html>"""
    
    # Write the HTML file
    try:
        with open(output_html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ Successfully created HTML file: {output_html_path}")
        print(f"📊 Included {len(entries_with_content)} chapters with Toriyama comments")
        return True
    except Exception as e:
        print(f"Error writing HTML file: {e}")
        return False

def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) < 2:
        print("Usage: python json_to_html.py <json_file> [output_html_file]")
        print("Example: python json_to_html.py results.json kanzenshuu_page.html")
        sys.exit(1)
    
    json_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "kanzenshuu_wj_toriyama.html"
    
    success = create_html_from_json(json_file, output_file)
    if success:
        print(f"\n🌐 Open {output_file} in your browser to view the results!")

if __name__ == "__main__":
    main()

