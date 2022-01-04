import sys
import jinja2
import os
import markdown

topic = sys.argv[1]

content_dir = f'content/{topic}/'
article_md_dir = content_dir + 'articles/markdown/'
article_html_dir = content_dir + 'articles/html/'

articles_filenames = sorted([
    filename.split('.')[0]
    for filename in os.listdir(article_md_dir)
])

index_body = f'<h1>{topic}</h1>\n<ul>\n' + ''.join(
    [f'<li><a href=\"{topic}/{name}.html\">{name}</a></li>\n' for name in articles_filenames]
) + '</ul>'

with open('html_template.jinja', 'r') as input_file:
    template_str = input_file.read()

template_j2 = jinja2.Template(template_str)

index_html = template_j2.render(title=topic, body=index_body)

with open(f'{content_dir}index.html', 'w', encoding='utf-8') as output_file:
    output_file.write(index_html)

if not os.path.isdir(article_html_dir):
    os.mkdir(article_html_dir)

for name in articles_filenames:

    with open(f'{article_md_dir}{name}.md', 'r', encoding='utf-8') as input_file:
        text = input_file.read()

    body = markdown.markdown(text)

    html = template_j2.render(title=name, body=body)

    with open(f'{article_html_dir}{name}.html', 'w', encoding='utf-8', errors='xmlcharrefreplace') as output_file:
        output_file.write(html)
