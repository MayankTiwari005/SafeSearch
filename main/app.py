from flask import Flask, render_template, request
from scraper import get_webpage_text
from safety_analyzer import analyze_text_safety as analyze_text
import matplotlib
matplotlib.use('Agg')  # non-GUI backend for Flask
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form.get('url', '').strip()
    if not url:
        return render_template('result.html', error="Please enter a valid URL.")

    text = get_webpage_text(url)
    if not text:
        return render_template('result.html', error="Could not fetch text from this website. Try another one.")

    res = analyze_text(text)
    if res is None:
        return render_template('result.html', error="No readable content found on this page.")

    # Create charts only if we have data
    categories = list(res['category_counts'].keys())
    counts = [res['category_counts'][c] for c in categories]

    # Bar chart
    plt.figure(figsize=(10, 5))
    plt.bar(categories, counts)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    bar_path = os.path.join(STATIC_DIR, 'chart_bar.png')
    plt.savefig(bar_path)
    plt.close()

    # Pie chart
    safe_count = max(0, res['total_words'] - res['unsafe_hits'])
    unsafe_count = res['unsafe_hits']
    plt.figure(figsize=(5, 5))
    plt.pie([safe_count, unsafe_count], labels=['Safe', 'Unsafe'], autopct='%1.1f%%')
    pie_path = os.path.join(STATIC_DIR, 'chart_pie.png')
    plt.savefig(pie_path)
    plt.close()

    return render_template(
        'result.html',
        result=res,
        bar_img='chart_bar.png',
        pie_img='chart_pie.png',
        url=url
    )

if __name__ == '__main__':
    app.run(debug=True)
