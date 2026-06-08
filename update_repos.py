import requests

# Diccionario completo con tus tecnologías
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
    # 1. Obtener datos de la API
    url = 'https://api.github.com/users/entreunosyceros/repos?sort=pushed&per_page=5'
    repos = requests.get(url).json()
    
    # 2. Construir la cabecera de la tabla con saltos de línea de seguridad (\n)
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
        
        # Limpieza estricta de saltos de línea para mantener las celdas alineadas
        desc = desc.replace('\n', ' ').replace('\r', '').replace('|', '\\|')
        
        # Asignar emoji dinámico
        lang_formatted = LANG_EMOJIS.get(lang, f'💻 {lang}') if lang else '📦 Otros'
        
        # Añadir fila
        table_lines.append(f'| [**{name}**]({html_url}) | {lang_formatted} | {desc} |')
    
    table_lines.append("")  # Línea en blanco después de la tabla
    content_string = '\n'.join(table_lines)

    # 3. Leer y reemplazar en el README
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
        print("README actualizado con éxito.")
    else:
        print("Error: No se encontraron las etiquetas en el README.md")

except Exception as e:
    print(f"Ocurrió un error durante la ejecución: {e}")
