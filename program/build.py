import re
import os

def parse_journey(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    html_output = []
    
    img_pattern = re.compile(r'^!\[(.*?)\]\((.*?)\)\s*$')
    map_pattern = re.compile(r'^🗺️\s*\[(.*?)\]\((.*?)\)\s*$')
    
    current_day = None
    current_event = None
    current_image = None
    
    def flush_event():
        nonlocal current_event, current_image
        if current_event:
            # check if it has an image
            if current_image:
                theme_class = " cruise-theme" if "🚢" in current_day or "🌊" in current_day else ""
                html_output.append(f'                <div class="card{theme_class}">\n')
                html_output.append('                    <div class="card-img-wrapper">\n')
                html_output.append(f'                        <img src="{current_image[1]}" alt="{current_image[0]}" class="card-img" loading="lazy">\n')
                html_output.append('                    </div>\n')
                html_output.append('                    <div class="card-content">\n')
            else:
                theme_class = " cruise-theme" if "🚢" in current_day or "🌊" in current_day else ""
                
                if current_day and "啟程準備" in current_day:
                    html_output.append(f'                <div class="card info-card">\n')
                    html_output.append('                    <div class="card-content full-width">\n')
                else:
                    html_output.append(f'                <div class="card text-card{theme_class}">\n')
                    html_output.append('                    <div class="card-content full-width" style="padding: 16px 24px;">\n')
            
            time_str = current_event.get('time', '')
            title_str = current_event.get('title', '')
            if current_image:
                html_output.append(f'                        <div class="time-badge">{time_str}</div>\n')
                html_output.append(f'                        <h2 class="card-title">{title_str}</h2>\n')
            else:
                if current_day and "啟程準備" in current_day:
                    html_output.append(f'                        <h2 class="card-title">{title_str}</h2>\n')
                    html_output.append('                        <ul>\n')
                else:
                    if time_str:
                        html_output.append(f'                        <p class="card-desc"><strong>{time_str} ｜ {title_str}</strong></p>\n')
                    else:
                        html_output.append(f'                        <p class="card-desc">{title_str}</p>\n')
            
            for note in current_event.get('notes', []):
                topic = note[0].strip('：: ')
                content = note[1].strip()
                content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
                
                if current_day and "啟程準備" in current_day and not current_image:
                    if topic:
                        html_output.append(f'                            <li><strong>{topic}：</strong> {content}</li>\n')
                    else:
                        html_output.append(f'                            <li>{content}</li>\n')
                else:
                    if not topic:
                        html_output.append(f'                        <p class="card-desc">{content}</p>\n')
                    else:
                        note_class = "note"
                        if "管家" in topic or "專屬" in topic:
                            note_class = "note calm"
                        html_output.append(f'                        <div class="{note_class}">\n')
                        html_output.append(f'                            <div class="note-header-wrap"><strong>{topic}：</strong></div>\n')
                        html_output.append(f'                            {content}\n')
                        html_output.append('                        </div>\n')
            
            if current_day and "啟程準備" in current_day and not current_image:
                 html_output.append('                        </ul>\n')

            html_output.append('                    </div>\n')
            html_output.append('                </div>\n\n')
            
            current_event = None
            current_image = None

    def flush_day():
        flush_event()
        if current_day:
            html_output.append('            </div>\n')
            html_output.append('        </div>\n\n')
            
    day_id = 0
    for line in lines:
        line_s = line.strip()
        if not line_s:
            continue
            
        m_day = re.match(r'^(?:###|##)\s+(.*?(?:Day|啟程|賦歸).*)$', line)
        if m_day:
            flush_day()
            title = m_day.group(1).replace('**', '').strip()
            day_id_str = f'day{day_id}'
            is_cruise = "🚢" in title or "🌊" in title
            theme_class = " cruise-theme" if is_cruise else (" info-theme" if "啟程準備" in title else "")
            section_class = " cruise-theme" if is_cruise else ""
            
            html_output.append(f'        <!-- Day {day_id} -->\n')
            html_output.append(f'        <div class="day-section{section_class}" id="{day_id_str}">\n')
            html_output.append(f'            <div class="day-header{theme_class}" onclick="toggleSection(\'{day_id_str}-content\', this)">\n')
            html_output.append(f'                {title}\n')
            html_output.append('                <span class="toggle-icon">▲</span>\n')
            html_output.append('            </div>\n')
            html_output.append(f'            <div class="day-content" id="{day_id_str}-content">\n')
            day_id += 1
            current_day = title
            continue
            
        m_img = img_pattern.match(line_s)
        if m_img:
            flush_event()
            url = m_img.group(2)
            if url.startswith('<') and url.endswith('>'):
                url = url[1:-1]
            current_image = (m_img.group(1), url)
            continue
            
        m_event = re.match(r'^-\s*\*\*(.*?)(?:｜|\|)(.*?)\*\*', line_s)
        if m_event:
            flush_event()
            current_event = {
                'time': m_event.group(1).strip(),
                'title': m_event.group(2).strip(),
                'notes': []
            }
            continue
            
        # Exception for "啟程準備" style headers which might just be bold text without time | title format
        m_simple_event = re.match(r'^-\s*\*\*(.*?)\*\*(?:：|:)?$', line_s)
        if m_simple_event and current_day and "啟程準備" in current_day and not m_event:
            flush_event()
            current_event = {
                'time': '',
                'title': m_simple_event.group(1).strip(),
                'notes': []
            }
            continue

        m_note = re.match(r'^(?:\s+-|\s*\*)\s*\*\*(.*?)\*\*[：:\s]*(.*)$', line)
        if m_note and current_event:
            current_event['notes'].append((m_note.group(1).strip(), m_note.group(2).strip()))
            continue
            
        m_map = map_pattern.match(line_s)
        if m_map and current_day:
            flush_event()
            map_title = m_map.group(1)
            map_url = m_map.group(2)
            if map_url.startswith('<') and map_url.endswith('>'):
                map_url = map_url[1:-1]
                
            html_output.append('                <div class="map-link-container">\n')
            html_output.append(f'                    <a href="{map_url}" target="_blank" class="map-btn">\n')
            html_output.append(f'                        <span>📍</span> {map_title}\n')
            html_output.append('                    </a>\n')
            
            iframe_src = map_url
            if "google.com/maps/dir" in map_url:
                parts = map_url.split('/dir/')
                if len(parts) > 1:
                    raw_locations = list(filter(None, parts[1].split('/')))
                    locations = []
                    for loc in raw_locations:
                        if loc.startswith('@') or loc.startswith('data=') or loc.startswith('?'):
                            break
                        locations.append(loc)
                        
                    if len(locations) >= 2:
                        saddr = locations[0]
                        daddr = "+to:".join(locations[1:])
                        iframe_src = f"https://maps.google.com/maps?saddr={saddr}&daddr={daddr}&output=embed"
                    
            html_output.append(f'                    <iframe class="map-iframe" src="{iframe_src}" title="{map_title}" allowfullscreen="" loading="lazy"></iframe>\n')
            html_output.append('                </div>\n')
            continue
            
        m_desc = re.match(r'^(?:\s+-|\s*\*)\s*([^:\*].*)$', line)
        if m_desc and current_event:
             current_event['notes'].append(("", m_desc.group(1).strip()))
             continue

    flush_day()
    return "".join(html_output)

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(root_dir, 'template.html')
    journey_path = os.path.join(root_dir, 'journey.md')
    index_path = os.path.join(root_dir, 'index.html')

    if not os.path.exists(template_path):
        print(f"Error: {template_path} not found.")
        return
        
    html_content = parse_journey(journey_path)
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
        
    final_html = template.replace('<!-- CONTENT_PLACEHOLDER -->', html_content)
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
        
    print("Successfully built index.html from journey.md")

if __name__ == '__main__':
    main()
