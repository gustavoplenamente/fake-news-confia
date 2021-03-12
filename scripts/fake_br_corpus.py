import csv
import os
import re
from typing import List

METADATA_PATH = '../../Fake.br-Corpus-master/full_texts'
FAKE_METADATA = 'fake-meta-information'
NOT_FAKE_METADATA = 'true-meta-information'

TEXTS_PATH = '../../Fake.br-Corpus-master/size_normalized_texts'
FAKE_NEWS = 'fake'
NOT_FAKE_NEWS = 'true'

NEWS_AMOUNT = 3602

NEWS_AUTHOR_FILE = 'fake-br-corpus-news-user.csv'
NEWS_FILE = 'fake-br-corpus-news.csv'
AUTHORS_FILE = 'fake-br-corpus-users.csv'

FAKE_AUTHORS_FILE = 'fake-br-corpus-fake-users.csv'
NOT_FAKE_AUTHORS_FILE = 'fake-br-corpus-not-fake-users.csv'

MISSING = [697, 1468, 4299, 5070]

AUTHORS_IDS = {
    'sao-paulo.estadao.com.br': 1,
    'ceticismopolitico.com': 2,
    'www.territorioeldorado.limao.com.br': 3,
    'emais.estadao.com.br': 4,
    'saude.estadao.com.br': 5,
    'esportes.estadao.com.br': 6,
    'brasil.estadao.com.br': 7,
    'www1.folha.uol.com.br': 8,
    'afolhabrasil.com.br': 9,
    'www.topfivetv.com': 10,
    'acervo.estadao.com.br': 11,
    'educacao.estadao.com.br': 12,
    'g1.globo.com': 13,
    'datafolha.folha.uol.com.br': 14,
    'f5.folha.uol.com.br': 15,
    'sustentabilidade.estadao.com.br': 16,
    'internacional.estadao.com.br': 17,
    'economia.estadao.com.br': 18,
    'alias.estadao.com.br': 19,
    'www.diariodobrasil.org': 20,
    'www.estadao.com.br': 21,
    'opiniao.estadao.com.br': 22,
    'link.estadao.com.br': 23,
    'www.thejornalbrasil.com.br': 24,
    'blogdofred.blogfolha.uol.com.br': 25,
    'politica.estadao.com.br': 26,
    'ciencia.estadao.com.br': 27,
    'cultura.estadao.com.br': 28,
    'viagem.estadao.com.br': 29,
}


def get_files_list(path: str) -> List[str]:
    return next(os.walk(path))[2]


def get_website_domain(text: str) -> str:
    domain_url = re.search(r'https*://[\w|.-]*', text).group()
    return re.sub(r'https*://', '', domain_url)


def get_author(file_path: str) -> str:
    with open(file_path) as metadata:
        content = metadata.read()
        return get_website_domain(content)


def get_content(file_path: str) -> str:
    with open(file_path) as data:
        return data.read()


def get_base_id(file_path: str) -> int:
    file_name = re.search(r'\d*(-meta)*.txt', file_path).group()
    base_id_str = re.sub(r'(-meta)*.txt', '', file_name)

    return int(base_id_str)


def is_fake(file_path: str) -> int:
    return FAKE_METADATA in file_path or FAKE_NEWS in file_path


def is_fake_metadata(file_path: str) -> int:
    return FAKE_METADATA in file_path


def get_id(file_path: str) -> int:
    base_id = get_base_id(file_path)
    return base_id + NEWS_AMOUNT if is_fake(file_path) else base_id


def write_news_user_file():
    with open(NEWS_AUTHOR_FILE, 'w') as file:
        writer = csv.writer(file, delimiter='\t')

        for folder in [NOT_FAKE_METADATA, FAKE_METADATA]:
            news_path = os.path.join(METADATA_PATH, folder)

            files = get_files_list(news_path)

            for news_file in files:
                file_path = os.path.join(news_path, news_file)

                news_id = get_id(file_path)
                author = get_author(file_path)

                author_id = AUTHORS_IDS[author]
                writer.writerow([news_id, author_id])


def write_news_file():
    with open(NEWS_FILE, 'w') as file:
        writer = csv.writer(file, delimiter='\t')

        for folder in [NOT_FAKE_METADATA, FAKE_METADATA]:
            texts_path = os.path.join(METADATA_PATH, folder)

            files = get_files_list(texts_path)

            for news_file in files:
                file_path = os.path.join(texts_path, news_file)

                news_id = get_id(file_path)

                writer.writerow([news_id])


def write_authors_file():
    with open(AUTHORS_FILE, 'w') as file:
        writer = csv.writer(file, delimiter='\t')
        authors = set(())

        for folder in [NOT_FAKE_METADATA, FAKE_METADATA]:
            news_path = os.path.join(METADATA_PATH, folder)

            files = get_files_list(news_path)

            for news_file in files:
                file_path = os.path.join(news_path, news_file)

                author = get_author(file_path)
                authors.add(author)

        for author in authors:
            writer.writerow([author])


def write_specific_authors_file(path, destiny):
    with open(destiny, 'w') as file:
        writer = csv.writer(file, delimiter='\t')
        authors = set(())

        news_path = os.path.join(METADATA_PATH, path)

        files = get_files_list(news_path)

        for news_file in files:
            file_path = os.path.join(news_path, news_file)

            author = get_author(file_path)
            authors.add(author)

        for author in authors:
            writer.writerow([author])


if __name__ == '__main__':
    # write_news_user_file()
    write_news_file()
    # write_authors_file()
    # write_specific_authors_file(FAKE_METADATA, FAKE_AUTHORS_FILE)
    # write_specific_authors_file(NOT_FAKE_METADATA, NOT_FAKE_AUTHORS_FILE)
