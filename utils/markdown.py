import pandas as pd

def create_markdown():
    df = pd.read_csv('data/csv/sso.csv')

    md_content = ''

    for _, row in df.iterrows():
        title = f'## {row['title']}\n'
        detail = f'{row["detail"]}\n\n'
        md_content += title + detail

    md_file = 'sso.md'
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f'File "{md_file}" has been created.')