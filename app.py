from flask import Flask, request, render_template
from model import SpellCheckerModule

app = Flask(__name__)
spell_checker_module = SpellCheckerModule()

# routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/spell', methods=['POST', 'GET'])
def spell():
    if request.method == 'POST':
        text = request.form.get('text', '')  # Safely get the text
        if text:  # Check if text is provided
            corrected_text = spell_checker_module.correct_spell(text)
            corrected_grammar, _ = spell_checker_module.correct_grammar(text)
            return render_template('index.html', corrected_text=corrected_text, corrected_grammar=corrected_grammar)
        else:
            return render_template('index.html', error="No text provided for spell checking.")
    return render_template('index.html')

@app.route('/grammar', methods=['POST', 'GET'])
def grammar():
    if request.method == 'POST':
        file = request.files.get('file')  # Safely get the file
        if file:
            try:
                readable_file = file.read().decode('utf-8', errors='ignore')
                corrected_file_text = spell_checker_module.correct_spell(readable_file)
                corrected_file_grammar, _ = spell_checker_module.correct_grammar(readable_file)
                return render_template('index.html', corrected_file_text=corrected_file_text, corrected_file_grammar=corrected_file_grammar)
            except Exception as e:
                return render_template('index.html', error=f"Error processing file: {e}")
        else:
            return render_template('index.html', error="No file uploaded.")
    return render_template('index.html')

# python main
if __name__ == "__main__":
    app.run()