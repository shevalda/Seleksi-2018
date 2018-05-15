import re

content_filter = [
    'baca juga',
    'saksikan video pilihan berikut ini',
    'untuk memberikan komentar',
    'copyright',
    '\xa0'
]

def is_news_content(text):
    """
    menentukan apakah suatu kata adalah konten berita
    :param text: text yang akan diperiksa
    :return: True jika benar isi berita, False jika bukan
    """
    if re.search(r'[(].{3}[\/].{3}[)]', text) != None:
        return False
    for filter in content_filter:
        if filter in text.lower():
            return False
    return True

def format_datetime(datetime):
    """
    mengolah tanggal waktu berita dipost ke website
    :param str: string berisi tanggal dan waktu
    :return: tanggal dan waktu yang sudah diformat
    """
    temp = datetime.split()
    date = {
        'day': int(temp[2]),
        'month': temp[3],
        'year': int(temp[4][:4])
    }
    time = {
        'clock': temp[5],
        'timezone': temp[6]
    }
    return date, time

def format_link(link):
    """
    cleaning link
    """
    return re.sub(r'[?].*', '', link)

def format_news(paragraphs):
    """
    mengolah isi yang memang isi berita
    :param paragraphs: konten mentah dari html
    :return: konten berita yang sebenarnya, dipisah per paragraf
    """
    clean_paragraph = []
    for paragraph in paragraphs:
        p_temp = paragraph.text
        if is_news_content(p_temp):
            clean_paragraph.append(p_temp)
    return clean_paragraph