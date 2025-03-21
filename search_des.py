import os
import csv
import pandas as pd
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Ensure necessary NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')

# Disable chained assignment warning
pd.options.mode.chained_assignment = None

# Define dynamic paths
BASE_DIR = os.getcwd()
CSV_PATH = os.path.join(BASE_DIR, "results.csv")
TEMPLATE_PATH = os.path.join(BASE_DIR, "templates", "output.html")


def clean_text(text):
    """Remove non-alphanumeric characters and tokenize words."""
    text = re.sub(r'\W+', ' ', text)  # Remove non-word characters
    tokens = word_tokenize(text.lower())  # Tokenize and convert to lowercase
    tokens = [word for word in tokens if word not in stopwords.words("english")]  # Remove stopwords
    return " ".join(tokens)


def similarity_computation(q):
    corpus = []

    # ✅ Tokenize and clean the query
    query_cleaned = clean_text(q)
    if not query_cleaned.strip():
        print("⚠️ Error: Query contains only stopwords or is empty. Skipping similarity check.")
        return

    corpus.append(query_cleaned)
    print(f"Processed query: {query_cleaned}")

    # ✅ Load dataset
    if not os.path.exists(CSV_PATH):
        print(f"⚠️ Error: {CSV_PATH} not found. Run the scraper first.")
        return

    df = pd.read_csv(CSV_PATH)
    if "description" not in df.columns:
        print("⚠️ Error: 'description' column missing in results.csv")
        return

    # ✅ Remove empty descriptions
    df = df.dropna(subset=["description"])
    if df.empty:
        print("⚠️ Error: No valid product descriptions found. Cannot compute similarity.")
        return

    print(f"✅ Number of product descriptions: {len(df['description'])}")

    # ✅ Preprocess product descriptions
    for desc in df["description"]:
        cleaned_desc = clean_text(desc)
        if cleaned_desc.strip():  # Only add if not empty
            corpus.append(cleaned_desc)

    # ✅ Ensure corpus has enough data
    if len(corpus) < 2:
        print("⚠️ Error: Not enough data for similarity comparison.")
        return

    # ✅ Compute TF-IDF and similarity matrix
    try:
        tfidf = TfidfVectorizer()
        result = tfidf.fit_transform(corpus)
        sim_matrix = cosine_similarity(result[0:1], result)

        # ✅ Update similarity scores in the dataset
        df["sim_index"] = sim_matrix[0][1:]
        df.sort_values(by="sim_index", ascending=False, inplace=True)
        df.to_csv(CSV_PATH, index=False)
        print('✅ CSV file updated successfully!')

    except ValueError as e:
        print(f"⚠️ TF-IDF Error: {e}. Likely due to empty vocabulary.")
        return

    # ✅ Generate output HTML table
    with open(CSV_PATH, encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header

        headers = ['Image', 'Name', 'Company', 'Price', 'Link']
        table_html = '<table>'
        table_html += '<tr>' + ''.join([f'<th>{header}</th>' for header in headers]) + '</tr>'

        for row in reader:
            if len(row) < 6:  # Ensure data is valid
                continue

            image_url, company, name, price, rating, link = row[:6]
            row_html = f'''
            <tr>
                <td><img src="{image_url}" class="thumbnail"></td>
                <td>{name}</td>
                <td>{company}</td>
                <td>{price}</td>
                <td><a href="{link}" target="_blank">View</a></td>
            </tr>
            '''
            table_html += row_html

        table_html += '</table>'

    # ✅ Generate HTML file
    html_content = f'''
    <html>
    <head>
    <style>
        table {{
            border-collapse: collapse;
            width: 100%;
        }}
        td, th {{
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }}
        tr:nth-child(even) {{
            background-color: #dddddd;
        }}
        .thumbnail {{
            max-width: 100px;
            max-height: 100px;
        }}
    </style>
    </head>
    <body>
        {table_html}
    </body>
    </html>
    '''

    with open(TEMPLATE_PATH, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("✅ output.html updated successfully!")

