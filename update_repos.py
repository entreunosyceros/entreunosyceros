import requests
import os

LANG_EMOJIS = {
    'Python': '🐍 Python',
    'Java': '☕ Java',
    'C': '⚙️ C',
    'C++': '🧪 C++',
    'PHP': '🐘 PHP',
    'Go': '🐹 Go',
    'Shell': '🐚 Bash/Shell',
    'JavaScript': '🌐 JavaScript',
    'TypeScript': '📘 TypeScript',
    'HTML': '📄 HTML5',
    'CSS': '🎨 CSS3',
    'JSON': '🗂️ JSON',
    'Markdown': '📝 Markdown',
    'SQL': '🛢️ MySQL/SQL'
}

try:
    # 1. Comprobar que el README existe
    if not os.path.exists('README.md'):
        print("❌ ERROR: No se encuentra el archivo README.md en la raíz.")
        exit(1)

    # 2. Obtener datos de la API
    url = 'https://api.github.com/users/entreunosyceros/repos?sort=pushed&per_page=5'
    repos = requests.get(url).json()
    
    # Si la API da error de rate limit o similar
    if isinstance(repos, dict) and "message" in repos:
        print(f"❌ ERROR API GitHub: {repos['message']}")
        exit(1)

    # 3. Construir la tabla
    table_lines = [
        "",
        "| Proyecto | Tecnología | Descripción |",
        "| :--- | :---: | :--- |"
    ]
    
    for repo in repos:
        name = repo['name']
        html_url = repo['html_url']
        lang = repo.get('language')
        desc = repo['description'] if repo['description'] else 'Sin descripción.'
        desc = desc.replace('\n', ' ').replace('\r', '').replace('|', '\\|')
        
        lang_formatted = LANG_EMOJIS.get(lang, f'💻 {lang}') if lang else '📦 Otros'
        table_lines.append(f'| [**{name}**]({html_url}) | {lang_formatted} | {desc} |')
    
    table_lines.append("")
    content_string = '\n'.join(table_lines)

    # 4. Leer y reemplazar
    with open('README.md', 'r', encoding='utf-8') as f:
        readme = f.read()
    
    start_tag = ''
    end_tag = ''
    
    if start_tag in readme and end_tag in readme:
        before_part = readme.split(start_tag)[0]
        after_part = readme.split(end_tag)[1]
        
        new_readme = f'{before_part}{start_tag}{content_string}{end_tag}{after_part}'
        
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(new_readme)
        print("✅ ÉXITO: README.md modificado correctamente.")
    else:
        print("❌ ERROR: Las etiquetas ocultas no coinciden.")
        print(f"¿Existe '{start_tag}' en el archivo?: {start_tag in readme}")
        print(f"¿Existe '{end_tag}' en el archivo?: {end_tag in readme}")

except Exception as e:
    print(f"❌ Ocurrió una excepción: {e}")
