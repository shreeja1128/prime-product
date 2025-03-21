# 🛒 Prime Product Using Webscraping

A powerful web-based product comparison tool that scrapes product details from multiple e-commerce websites (Amazon, Flipkart, Snapdeal, Paytm Mall, ShopClues, etc.) and presents them side-by-side to help users make informed shopping decisions.



## 📌 Table of Contents

- [About the Project](#about-the-project)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Results](#results)
- [Future Enhancements](#future-enhancements)
- [Contributors](#contributors)
- [License](#license)



## 📖 About the Project

With the explosion of e-commerce, finding the best deals requires navigating across various websites—an often time-consuming process. This project automates that using **web scraping**, **natural language processing (NLP)**, and **cosine similarity**, enabling:

- Aggregated and filtered product data from major e-commerce websites
- Prime product identification (where the product of their prices results in a prime number)
- Easy comparison with a user-friendly interface built using Flask and JavaScript



## ✨ Key Features

- 🔍 **Search any product** using a keyword-based search bar
- 🛍️ **Multi-site comparison**: Compare results across Amazon, Flipkart, Snapdeal, Paytm Mall, ShopClues
- 🧠 **Cosine Similarity + NLP** for better matching and filtering
- ✅ **Filters** to choose which websites to include
- 📊 **Real-time scraping** using BeautifulSoup
- 📁 **Exportable results** via CSV



## ⚙️ Tech Stack

### 📌 Frontend:
- HTML
- CSS
- JavaScript

### 📌 Backend:
- Python
- Flask

### 📌 Libraries Used:
- `BeautifulSoup` – Web scraping
- `NLTK` – Tokenization & text preprocessing
- `scikit-learn` – Cosine similarity (TF-IDF vectorizer)
- `Pandas` – Data processing
- `Requests` – HTTP requests



## 🏗️ System Architecture

```plaintext
User Interface (HTML, CSS, JS)
          |
          v
Flask Server (Backend)
          |
          v
Web Scrapers (Amazon, Flipkart, etc.)
          |
          v
NLP + Cosine Similarity Processing
          |
          v
Display Data & Store in CSV
```



## 🧪 Installation

### Prerequisites
- Python 3.x
- pip

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/prime-product-scraper.git
   cd prime-product-scraper
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Flask App**
   ```bash
   python website.py
   ```

4. **Open in Browser**
   Navigate to `http://127.0.0.1:5000/`



## 🚀 Usage

- Use the search bar to type in product names (e.g., “iPhone 14 Pro Max”).
- Select desired e-commerce sites using checkboxes.
- Click Search to fetch and compare results.
- Filters and product details will be displayed including:
  - Name
  - Image
  - Price
  - Ratings
  - Direct link to buy
- Cosine similarity is used to compare relevant matches.



## 🖼️ Screenshots

| Home Page | Filtered Results |
|-----------|------------------|
| ![Home](screenshots/home.png) | ![Filtered](screenshots/filtered.png) |



## 📈 Results

Example: *Search: “Nike Shoes”*

| Website     | Count |
|-------------|-------|
| Amazon      | 56    |
| Snapdeal    | 19    |
| Paytm Mall  | 32    |
| ShopClues   | 12    |
| Flipkart    | 40    |

- Cosine similarity matrix and IDF values were computed.
- Tokens and keyword relevance were used to refine accuracy.



## 🔮 Future Enhancements

- 📱 Develop a mobile app version
- 📊 Visualize trends with charts (price tracking)
- 🧠 Use machine learning for personalized recommendations
- 🧾 Add user review scraping
- 🔐 User authentication for saved preferences
