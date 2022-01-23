import sys
import jinja2
import os
import markdown
import xml

topic = sys.argv[1]

content_dir = 'content/'

source_topic_dir = f'{content_dir}source/{topic}/'
article_md_dir = source_topic_dir + 'articles/'
footer_file = f'{source_topic_dir}appendices/footer.html'

product_dir = content_dir + 'product/'
product_topic_dir = product_dir + topic + '/'
article_html_dir = product_topic_dir + topic + '/'

articles_filenames = sorted([
    filename.split('.')[0]
    for filename in os.listdir(article_md_dir)
])

with open('html_template.jinja', 'r') as input_file:
    template_str = input_file.read()

template_j2 = jinja2.Template(template_str)

if not os.path.isdir(product_dir):
    os.mkdir(product_dir)

if not os.path.isdir(product_topic_dir):
    os.mkdir(product_topic_dir)

if not os.path.isdir(article_html_dir):
    os.mkdir(article_html_dir)

articles_info = {}

if os.path.isfile(footer_file):
    with open(footer_file, 'r') as input_file:
        footer_html = '\n' + input_file.read()
else:
    footer_html = ''

for name in articles_filenames:

    with open(f'{article_md_dir}{name}.md', 'r', encoding='utf-8') as input_file:
        text = input_file.read()

    body = markdown.markdown(text) + footer_html

    html_raw = template_j2.render(title=name, body=body)

    root = xml.etree.ElementTree.fromstring(html_raw)

    articles_info[name] = root.find('body/h1').text

    html_pretty = template_j2.render(title=articles_info[name], body=body)

    with open(f'{article_html_dir}{name}.html', 'w', encoding='utf-8', errors='xmlcharrefreplace') as output_file:
        output_file.write(html_pretty)

index_body = f'<h1>{topic}</h1>\n<ul>\n' + ''.join(
    [f'<li><a href=\"{topic}/{filename}.html\">{articles_info[filename]}</a></li>\n'
     for filename in articles_info.keys()]
) + '</ul>'

index_html = template_j2.render(title=topic, body=index_body)

with open(f'{product_topic_dir}index.html', 'w', encoding='utf-8') as output_file:
    output_file.write(index_html)
