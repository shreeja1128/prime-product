import csv
import os
import container

def write_output():
    # Setup paths
    BASE_DIR = os.getcwd()
    CSV_PATH = os.path.join(BASE_DIR, "results.csv")
    TEMPLATE_PATH = os.path.join(BASE_DIR, "templates", "output.html")

    table_html = container.html_code

    # Ensure results.csv exists before proceeding
    if not os.path.exists(CSV_PATH):
        print(f"⚠️ Error: {CSV_PATH} not found. No data to display.")
        return

    # Read CSV data
    with open(CSV_PATH, encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader, None)  # Skip header row

        if not headers:
            print("⚠️ Error: results.csv is empty. No data to display.")
            return

        table_html += '<table>'
        headers_display = ['Image', 'Name', 'Company', 'Price', 'Rating', 'Link']
        header_row = '<tr>' + ''.join([f'<th>{header}</th>' for header in headers_display]) + '</tr>'
        table_html += header_row

        row_count = 0  # Track number of rows added
        amazon_count = 0  # Track Amazon products

        for row in reader:
            if not row or len(row) < 6:  # Ensure valid data
                continue

            image_url = row[0] if row[0] else "https://via.placeholder.com/100"
            company = row[1] if row[1] else "Unknown"
            name = row[2] if row[2] else "No Name"
            price = row[3] if row[3] else "N/A"
            rating = row[4] if row[4] else "No Rating"
            link = row[5] if row[5] else "#"

            # Count Amazon products
            if company.lower() == "amazon":
                amazon_count += 1

            row_html = f'''
            <tr class="{company}">
                <td><img src="{image_url}" class="thumbnail"></td>
                <td>{name}</td>
                <td>{company}</td>
                <td>{price}</td>
                <td>{rating}</td>
                <td><a href="{link}" target="_blank">View Product</a></td>
            </tr>
            '''
            table_html += row_html
            row_count += 1

        table_html += '</table>'
        table_html += '<script src="/static/js/script.js"></script>'

    print(f"✅ Successfully added {row_count} products to output.html")
    print(f"✅ Writing {amazon_count} Amazon products to output.html")  # Debugging statement

    # Full HTML page
    html = f'''
    <html lang="en" dir="ltr">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Product Comparison</title>
        <link rel="stylesheet" href="/static/css/style_display.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css">
        <style>
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            td, th {{
                border: 1px solid #ddd;
                padding: 10px;
                text-align: left;
            }}
            th {{
                background-color: #f4f4f4;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            .thumbnail {{
                max-width: 100px;
                max-height: 100px;
            }}
        </style>
    </head>
    <body>
        <nav>
            <div class="menu">
                <div class="logo">
                    <a href="/home">Prime Product</a>
                </div>
                <ul>
                    <form class="input-box" action="/searching_des" method="post">
                        <input type="text" id="input_des" name="search_des" placeholder="Search keywords here..." />
                        <button class="button">Search</button>
                    </form>
                </ul>
            </div>
        </nav>
        {table_html}
    </body>
    </html>
    '''

    # Save the HTML to file
    with open(TEMPLATE_PATH, 'w', encoding='utf-8') as f:
        f.write(html)

    print("✅ output.html generated successfully!")
