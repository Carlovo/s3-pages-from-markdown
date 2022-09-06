import sys
import jinja2
import os
import shutil
import markdown
import xml.etree.ElementTree as ET

topic = sys.argv[1]
bucket = sys.argv[2]

content_dir = 'content'

source_topic_dir = f'{content_dir}/source/{topic}'
footer_file = source_topic_dir + '/appendices/footer.html'
js_app_file = source_topic_dir + '/appendices/main.js'

product_dir = content_dir + '/product'
product_topic_dir = f'{product_dir}/{topic}-{bucket}'
article_html_dir = product_topic_dir + '/' + topic

md = markdown.Markdown(extensions=['toc', 'tables'])

with open('html_template.jinja', 'r') as input_file:
    template_str = input_file.read()

template_j2 = jinja2.Template(template_str)

if not os.path.isdir(product_dir):
    os.mkdir(product_dir)

if os.path.isdir(product_topic_dir):
    shutil.rmtree(product_topic_dir)

os.mkdir(product_topic_dir)

if os.path.isfile(footer_file):
    with open(footer_file, 'r') as input_file:
        footer_html = '\n' + input_file.read()
else:
    footer_html = ''

if os.path.isfile(js_app_file):
    js_ref = f'<script type="module" src="./main.js"></script>'
else:
    js_ref = ''


def convert_snake_case_to_title_case(text: str) -> str:
    return ' '.join(
        [substring.capitalize() for substring in text.split('_')]
    )


def create_html_link(path: str, text: str) -> str:
    return f'<a href=\"{path}\">{text}</a>'


def create_html_link_list_item(path: str, text: str) -> str:
    return f'<li>{create_html_link(path, text)}</li>'


def create_html_link_list_from_dict(files_to_titles: dict) -> str:
    return '<ul>\n' + '\n'.join(
        [create_html_link_list_item(
            file_to_title,
            files_to_titles[file_to_title]
        )
            for file_to_title in files_to_titles.keys()]
    ) + '\n</ul>\n'


def create_html_breadcrumb_div(content: str) -> str:
    return '<div>\n<p>' + content + '</p>\n</div>\n'


def try_extract_index_title_else_create(dirpath: str) -> str:
    maybe_index_path = os.path.join(dirpath, 'index.md')
    if os.path.exists(maybe_index_path):
        with open(maybe_index_path, 'r', encoding='utf-8') as input_file:
            text = input_file.read()

        body = md.convert(text)
        index_raw = template_j2.render(body=body)
        root = ET.fromstring(index_raw)

        return root.find('body/h1').text
    else:
        return convert_snake_case_to_title_case(dirpath.split('/')[-1])


def sort_dict_by_value(this_dict: dict) -> dict:
    return {
        k: v for k, v in
        sorted(this_dict.items(), key=lambda item: item[1])
    }


breadcrumbs_info = {}

for dirpath, dirnames, filenames in os.walk(source_topic_dir + '/articles'):
    articles_info = {}

    online_subdirs = dirpath.split('/')[4:]
    article_html_subdir = os.path.join(article_html_dir, *online_subdirs)

    online_dirs = [topic] + online_subdirs
    online_path = os.path.join('/', *online_dirs)

    index_title = try_extract_index_title_else_create(dirpath)

    breadcrumbs_info[online_path] = index_title

    breadcrumb_dir_links = [
        create_html_link(os.path.join('/', *online_dirs[:_i + 1]) + '.html',
                         breadcrumbs_info[os.path.join('/', *online_dirs[:_i + 1])])
        for _i, _ in enumerate(online_dirs)
    ]

    breadcrumb_article_primer = ' > '.join(breadcrumb_dir_links) + ' > '
    breadcrumb_index_primer = ' > '.join(breadcrumb_dir_links[:-1])

    if breadcrumb_index_primer:
        breadcrumb_index_primer += ' > '

    os.mkdir(article_html_subdir)

    for filename in filenames:
        if filename == 'index.md':
            continue

        with open(os.path.join(dirpath, filename), 'r', encoding='utf-8') as input_file:
            text = input_file.read()

        name = filename.split('.')[0]

        body = md.convert(text) + footer_html
        html_raw = template_j2.render(body=body)
        root = ET.fromstring(html_raw)

        article_title = root.find('body/h1').text

        body = create_html_breadcrumb_div(
            breadcrumb_article_primer + article_title
        ) + body

        html_pretty = template_j2.render(
            title=article_title,
            body=body,
            script=js_ref
        )

        html_filename = name + '.html'

        with open(os.path.join(article_html_subdir, html_filename), 'x', encoding='utf-8', errors='xmlcharrefreplace') as output_file:
            output_file.write(html_pretty)

        articles_info[
            os.path.join(online_path, html_filename)
        ] = article_title

    index_body = create_html_breadcrumb_div(
        breadcrumb_index_primer + index_title)

    index_body += f'<h1>{index_title}</h1>\n'

    if dirnames:
        dirnames_info = {
            os.path.join(online_path, dirname + '.html'):
            try_extract_index_title_else_create(os.path.join(dirpath, dirname))
            for dirname in dirnames
        }

        dirnames_info_sorted = sort_dict_by_value(dirnames_info)

        index_body += '<h2>Topics</h2>\n' + \
            create_html_link_list_from_dict(dirnames_info_sorted)

    if filenames:
        articles_info_sorted = sort_dict_by_value(articles_info)

        index_body += '<h2>Articles</h2>\n' + \
            create_html_link_list_from_dict(articles_info_sorted)

    if os.path.exists(os.path.join(dirpath, 'index.md')):
        with open(os.path.join(dirpath, 'index.md'), 'r', encoding='utf-8') as input_file:
            text = input_file.read()

        body = md.convert(text)
        index_raw = template_j2.render(body=body)
        root = ET.fromstring(index_raw)

        xml_body = root.find('body')
        xml_h1 = xml_body.find('h1')
        xml_body.remove(xml_h1)

        for child in xml_body:
            index_body += ET.tostring(
                child, encoding='unicode', method='xml')

    index_html = template_j2.render(
        title=index_title,
        body=index_body
    )

    with open(os.path.join(article_html_subdir, '..', online_dirs[-1] + '.html'), 'x', encoding='utf-8') as output_file:
        output_file.write(index_html)

if os.path.isfile(js_app_file):
    shutil.copyfile(js_app_file, article_html_dir + '/main.js')
