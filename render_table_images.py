import os
from PIL import Image, ImageDraw, ImageFont

def get_font(name, size):
    fonts_dir = "C:/Windows/Fonts"
    font_paths = {
        "segoe": os.path.join(fonts_dir, "segoeui.ttf"),
        "segoe_bold": os.path.join(fonts_dir, "segoeuib.ttf"),
        "segoe_semi": os.path.join(fonts_dir, "seguisb.ttf"),
        "arial": os.path.join(fonts_dir, "arial.ttf"),
        "arial_bold": os.path.join(fonts_dir, "arialbd.ttf"),
        "consolas": os.path.join(fonts_dir, "consola.ttf"),
        "consolas_bold": os.path.join(fonts_dir, "consolab.ttf"),
    }
    path = font_paths.get(name)
    if path and os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def wrap_text(draw, text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def render_table(
    title,
    subtitle,
    headers,
    col_widths,
    rows,
    output_path=None,
    is_tracing=False
):
    pad_h = 24
    pad_v = 14
    margin = 36
    
    total_table_width = sum(col_widths)
    img_width = total_table_width + margin * 2
    
    # Fonts
    title_font = get_font("segoe_bold", 26)
    subtitle_font = get_font("segoe", 17)
    header_font = get_font("segoe_bold", 19)
    body_font = get_font("segoe", 17)
    code_font = get_font("consolas_bold", 17)
    pass_font = get_font("segoe_bold", 17)
    
    # Neutral Gray Palette (No Green Headers)
    header_bg = (55, 65, 81)       # #374151 - Clean Neutral Slate/Gray
    header_text_color = (255, 255, 255)
    row_bg_even = (255, 255, 255)
    row_bg_odd = (248, 250, 252)    # #F8FAFC
    border_color = (209, 213, 219)  # #D1D5DB
    text_color = (31, 41, 55)       # Charcoal text
    title_color = (31, 41, 55)
    subtitle_color = (100, 116, 139)
    code_color = (185, 28, 28)      # Burgundy/Red code identifier
    pass_color = (31, 41, 55)       # Neutral dark charcoal for clean default Pass text

    dummy_img = Image.new("RGB", (100, 100))
    draw = ImageDraw.Draw(dummy_img)

    row_heights = []
    wrapped_rows = []
    line_height = 25
    header_height = 50

    for row_data in rows:
        max_lines_in_row = 1
        wrapped_cells = []
        for col_idx, cell_text in enumerate(row_data):
            c_width = col_widths[col_idx] - pad_h * 2
            f = code_font if (is_tracing and col_idx == 1) else body_font
            lines = wrap_text(draw, cell_text, f, c_width)
            wrapped_cells.append(lines)
            if len(lines) > max_lines_in_row:
                max_lines_in_row = len(lines)
        wrapped_rows.append(wrapped_cells)
        r_height = max(46, pad_v * 2 + max_lines_in_row * line_height)
        row_heights.append(r_height)

    title_area_height = 90
    table_total_height = header_height + sum(row_heights)
    img_height = margin + title_area_height + table_total_height + margin

    img = Image.new("RGB", (img_width, img_height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Title & Subtitle
    draw.text((margin, margin + 2), title, fill=title_color, font=title_font)
    draw.text((margin, margin + 40), subtitle, fill=subtitle_color, font=subtitle_font)

    start_x = margin
    start_y = margin + title_area_height

    # 1. Header row
    curr_x = start_x
    for col_idx, h_text in enumerate(headers):
        c_w = col_widths[col_idx]
        draw.rectangle([curr_x, start_y, curr_x + c_w, start_y + header_height], fill=header_bg)
        draw.rectangle([curr_x, start_y, curr_x + c_w, start_y + header_height], outline=border_color, width=1)
        
        bbox = draw.textbbox((0, 0), h_text, font=header_font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        
        # Center align No. column and Pass/Fail column
        if (col_idx == 0 and len(headers) == 4) or (col_idx == len(headers) - 1 and not is_tracing):
            tx = curr_x + (c_w - tw) // 2
        else:
            tx = curr_x + pad_h
        ty = start_y + (header_height - th) // 2 - 2
        draw.text((tx, ty), h_text, fill=header_text_color, font=header_font)
        curr_x += c_w

    # 2. Body rows
    curr_y = start_y + header_height
    for row_idx, wrapped_cells in enumerate(wrapped_rows):
        r_h = row_heights[row_idx]
        bg_col = row_bg_odd if row_idx % 2 == 1 else row_bg_even
        curr_x = start_x

        for col_idx, lines in enumerate(wrapped_cells):
            c_w = col_widths[col_idx]
            draw.rectangle([curr_x, curr_y, curr_x + c_w, curr_y + r_h], fill=bg_col)
            draw.rectangle([curr_x, curr_y, curr_x + c_w, curr_y + r_h], outline=border_color, width=1)

            # Center alignment for No. column and Pass/Fail
            if col_idx == 0 and len(headers) == 4:
                f = body_font
                c = text_color
                for l_idx, line in enumerate(lines):
                    bbox = draw.textbbox((0, 0), line, font=f)
                    tw = bbox[2] - bbox[0]
                    tx = curr_x + (c_w - tw) // 2
                    ty = curr_y + (r_h - len(lines) * line_height) // 2 + l_idx * line_height
                    draw.text((tx, ty), line, fill=c, font=f)
            elif col_idx == len(headers) - 1 and not is_tracing:
                f = pass_font
                c = pass_color
                for l_idx, line in enumerate(lines):
                    bbox = draw.textbbox((0, 0), line, font=f)
                    tw = bbox[2] - bbox[0]
                    tx = curr_x + (c_w - tw) // 2
                    ty = curr_y + (r_h - len(lines) * line_height) // 2 + l_idx * line_height
                    draw.text((tx, ty), line, fill=c, font=f)
            else:
                if is_tracing and col_idx == 1:
                    f = code_font
                    c = code_color
                else:
                    f = body_font
                    c = text_color
                
                content_h = len(lines) * line_height
                ty = curr_y + (r_h - content_h) // 2
                for l_idx, line in enumerate(lines):
                    draw.text((curr_x + pad_h, ty + l_idx * line_height), line, fill=c, font=f)

            curr_x += c_w
        curr_y += r_h

    draw.rectangle([start_x, start_y, start_x + total_table_width, curr_y], outline=border_color, width=2)

    if output_path:
        img.save(output_path, "PNG", quality=95)
        print(f"Saved: {output_path}")

    return img

def main():
    # Step 11: 14 Testing Cases
    testing_headers = ["No.", "Test", "Expected Result", "Pass/Fail"]
    testing_widths = [70, 480, 580, 150]
    testing_rows = [
        ["1", "Open the application.", "Login appears first.", "Pass"],
        ["2", "Submit empty login fields.", "Validation messages appear.", "Pass"],
        ["3", "Enter incorrect credentials.", "Login is rejected.", "Pass"],
        ["4", "Enter admin / admin123.", "Dashboard opens.", "Pass"],
        ["5", "Read the dashboard greeting.", "Displays Welcome, admin!", "Pass"],
        ["6", "Open Calculator and calculate 10 + 5.", "Displays 15.0.", "Pass"],
        ["7", "Switch tabs and return to Calculator.", "Inputs and result remain.", "Pass"],
        ["8", "Create a social post.", "Post displays the logged-in username.", "Pass"],
        ["9", "Like a post and add a comment.", "Both interactions update correctly.", "Pass"],
        ["10", "Switch tabs and return to Social.", "Posts, likes, and comments remain.", "Pass"],
        ["11", "Open Profile.", "Student information and username appear.", "Pass"],
        ["12", "Tap Logout.", "Login appears; Back does not reopen MainScreen.", "Pass"],
        ["13", "Register a valid account and log in.", "Dashboard displays the registered username.", "Pass"],
        ["14", "Create a post using the registered account.", "Post displays the registered username.", "Pass"],
    ]

    # Guide Questions
    guide_headers = ["No.", "Guide Question", "Technical Explanation / Answer"]
    guide_widths = [70, 430, 780]
    guide_rows = [
        [
            "1",
            "How does DemoAuth connect Login to Dashboard, Social, and Profile?",
            "DemoAuth manages an in-memory session by storing currentUsername when login() succeeds. This recorded username is read in MainScreen.initState() and supplied directly to DashboardPage, SocialMediaPage, and ProfilePage to display personalized greetings, author new posts, and present profile account details."
        ],
        [
            "2",
            "Why must the order of pages match the bottom navigation destinations?",
            "In MainScreen, NavigationBar passes its selected destination index (0 to 3) to IndexedStack. Because IndexedStack displays the child widget exactly matching index, the order of widgets in the pages list must mirror the navigation bar items (Dashboard, Calculator, Social, Profile) so tapping an item opens its intended screen."
        ],
        [
            "3",
            "Why is IndexedStack useful for the Calculator and Social pages?",
            "IndexedStack keeps all child widgets mounted and active in the widget tree rather than disposing and rebuilding them on navigation changes. This preserves controller values, calculation inputs/results, social feed posts, like states, and comments while users navigate between tabs."
        ],
        [
            "4",
            "Why should Logout clear the current username and remove previous routes?",
            "Calling DemoAuth.logout() sets currentUsername to null to terminate the user session. Using Navigator.pushAndRemoveUntil() clears the navigation route history so pressing the Android/system Back button cannot reopen MainScreen without re-authenticating."
        ],
        [
            "5",
            "Which information is lost when this demo application restarts?",
            "Because DemoAuth, the social feed list, and calculator controllers store data exclusively in volatile RAM, all registered accounts, newly created posts, likes, comments, and calculator history are completely reset to initial default values upon an application restart."
        ]
    ]

    img_testing = render_table(
        title="Step 11: Application Testing Table",
        subtitle="Verification results for all 14 integration test scenarios",
        headers=testing_headers,
        col_widths=testing_widths,
        rows=testing_rows,
        output_path="application_testing_table.png",
        is_tracing=False
    )
    img_testing.save("screenshots/application_testing_table.png", "PNG", quality=95)

    img_guide = render_table(
        title="Application Guide Questions & Answers",
        subtitle="Concise technical explanations for architecture and state management",
        headers=guide_headers,
        col_widths=guide_widths,
        rows=guide_rows,
        output_path="guide_questions_table.png",
        is_tracing=False
    )
    img_guide.save("screenshots/guide_questions_table.png", "PNG", quality=95)

    # Combined stacked image
    gap = 40
    comb_w = max(img_testing.width, img_guide.width)
    comb_h = img_testing.height + img_guide.height + gap
    comb_img = Image.new("RGB", (comb_w, comb_h), (255, 255, 255))
    comb_img.paste(img_testing, (0, 0))
    comb_img.paste(img_guide, (0, img_testing.height + gap))
    
    comb_img.save("testing_and_guide_questions_tables.png", "PNG", quality=95)
    comb_img.save("screenshots/testing_and_guide_questions_tables.png", "PNG", quality=95)
    print("Saved combined tables to testing_and_guide_questions_tables.png")

if __name__ == "__main__":
    main()
