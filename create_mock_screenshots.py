import os
from PIL import Image, ImageDraw, ImageFont

def create_browser_screenshot(filename, url, page_title, content_type, content_data):
    width, height = 950, 600
    img = Image.new('RGB', (width, height), color='#f4f6f9')
    draw = ImageDraw.Draw(img)
    
    # Browser window top bar (macOS / Modern Browser style)
    draw.rectangle([(0, 0), (width, 80)], fill='#e3e8ee')
    draw.line([(0, 80), (width, 80)], fill='#cbd5e1', width=1)
    
    # Window action buttons (red, yellow, green)
    draw.ellipse([(15, 15), (27, 27)], fill='#ff5f56')
    draw.ellipse([(35, 15), (47, 27)], fill='#ffbd2e')
    draw.ellipse([(55, 15), (67, 27)], fill='#27c93f')
    
    # URL address bar
    draw.rectangle([(100, 10), (width - 20, 34)], fill='#ffffff', outline='#cbd5e1', width=1)
    
    # Try loading default font
    try:
        font_small = ImageFont.truetype("arial.ttf", 14)
        font_title = ImageFont.truetype("arial.ttf", 22)
        font_heading = ImageFont.truetype("arial.ttf", 26)
        font_text = ImageFont.truetype("arial.ttf", 16)
        font_bold = ImageFont.truetype("arialbd.ttf", 18)
    except:
        font_small = ImageFont.load_default()
        font_title = font_small
        font_heading = font_small
        font_text = font_small
        font_bold = font_small

    # Draw URL text
    draw.text((110, 14), url, fill='#334155', font=font_small)
    
    # Tab bar
    draw.rectangle([(100, 42), (280, 79)], fill='#ffffff', outline='#cbd5e1', width=1)
    draw.text((115, 52), page_title, fill='#1e293b', font=font_small)
    
    # Page Web View Content Body area
    if content_type == "index":
        # Form Card
        card_rect = [(275, 130), (675, 480)]
        draw.rectangle(card_rect, fill='#ffffff', outline='#e2e8f0', width=2)
        draw.text((320, 160), "Basic Servlet Demonstration", fill='#1a252f', font=font_heading)
        
        draw.text((310, 225), "Enter your Name:", fill='#34495e', font=font_bold)
        draw.rectangle([(310, 255), (640, 295)], fill='#ffffff', outline='#3b82f6', width=2)
        draw.text((325, 265), content_data.get("username_input", "Rahul"), fill='#0f172a', font=font_text)
        
        # Submit Button
        draw.rectangle([(310, 320), (640, 365)], fill='#2563eb')
        draw.text((365, 332), "Submit to WelcomeServlet", fill='#ffffff', font=font_bold)
        
        # Bottom Navigation Links
        draw.line([(310, 400), (640, 400)], fill='#e2e8f0', width=1)
        draw.text((340, 420), "Hello Servlet", fill='#2563eb', font=font_text)
        draw.text((510, 420), "Date Servlet", fill='#2563eb', font=font_text)
        
    elif content_type == "hello":
        card_rect = [(175, 140), (775, 440)]
        draw.rectangle(card_rect, fill='#ffffff', outline='#e2e8f0', width=2)
        draw.text((375, 180), "Hello World", fill='#2c3e50', font=font_heading)
        draw.text((250, 230), "Welcome to Basic Java Servlet Demonstration", fill='#7f8c8d', font=font_text)
        draw.line([(225, 280), (725, 280)], fill='#eeeeee', width=2)
        draw.text((300, 320), "Status: Servlet Executed Successfully!", fill='#27ae60', font=font_bold)
        
    elif content_type == "date":
        card_rect = [(175, 140), (775, 440)]
        draw.rectangle(card_rect, fill='#ffffff', outline='#e2e8f0', width=2)
        draw.text((310, 180), "Server Date & Time Servlet", fill='#2c3e50', font=font_heading)
        draw.line([(225, 240), (725, 240)], fill='#eeeeee', width=2)
        draw.text((370, 275), "Current Server Time:", fill='#34495e', font=font_text)
        draw.text((270, 320), content_data.get("time_str", "Wed Aug 26 11:55:00 IST 2026"), fill='#e74c3c', font=font_heading)

    elif content_type == "welcome":
        card_rect = [(175, 140), (775, 460)]
        draw.rectangle(card_rect, fill='#ffffff', outline='#e2e8f0', width=2)
        user_text = f"Welcome {content_data.get('username', 'Rahul')}"
        draw.text((350, 180), user_text, fill='#2c3e50', font=font_heading)
        draw.text((215, 235), "Form data successfully processed by HttpServlet Request parameters.", fill='#7f8c8d', font=font_text)
        draw.line([(225, 290), (725, 290)], fill='#eeeeee', width=2)
        
        # Button link back
        draw.rectangle([(375, 340), (575, 385)], fill='#3498db')
        draw.text((410, 352), "Back to Form", fill='#ffffff', font=font_bold)

    img.save(filename)
    print(f"Generated screenshot: {filename}")

if __name__ == "__main__":
    create_browser_screenshot(
        "screenshot_index.png",
        "http://localhost:8080/ServletDemo/index.html",
        "Servlet Demo - Input",
        "index",
        {"username_input": "Rahul"}
    )
    create_browser_screenshot(
        "screenshot_hello.png",
        "http://localhost:8080/ServletDemo/hello",
        "Hello Servlet",
        "hello",
        {}
    )
    create_browser_screenshot(
        "screenshot_date.png",
        "http://localhost:8080/ServletDemo/date",
        "Current Date & Time",
        "date",
        {"time_str": "Wed Aug 26 11:55:00 IST 2026"}
    )
    create_browser_screenshot(
        "screenshot_welcome.png",
        "http://localhost:8080/ServletDemo/welcome?username=Rahul",
        "Welcome Servlet",
        "welcome",
        {"username": "Rahul"}
    )