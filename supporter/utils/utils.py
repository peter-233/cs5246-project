from __future__ import annotations
import re
import nltk
import requests
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn

RESOURCE_DATA_ROOT = "resources/data"
nltk.download('wordnet', download_dir=RESOURCE_DATA_ROOT)
nltk.data.path.append(RESOURCE_DATA_ROOT)


class POSConverter2:
    NLTK_FORMAT = 1
    SPACY_FORMAT = 2
    WORDNET_FORMAT = 3
    COCA_FORMAT = 4

    NLTK_ENCODE_MAP = {
        "NOUN": "n",
        "VERB": "v",
        "ADJ": "a",
        "ADV": "r",
        "ADJ_SAT": "s"
    }
    NLTK_DECODE_MAP = {v: k for k, v in NLTK_ENCODE_MAP.items()}

    SPACY_ENCODE_MAP = {
        "NOUN": "NOUN",
        "VERB": "VERB",
        "ADJ": "ADJ",
        "ADV": "ADV",
        "ADJ_SAT": "ADJ",
    }
    SPACY_DECODE_MAP = {v: k for k, v in SPACY_ENCODE_MAP.items() if k != "ADJ_SAT"}

    WORDNET_ENCODE_MAP = {
        "NOUN": wn.NOUN,
        "VERB": wn.VERB,
        "ADJ": wn.ADJ,
        "ADV": wn.ADV,
        "ADJ_SAT": wn.ADJ_SAT,
    }
    WORDNET_DECODE_MAP = {v: k for k, v in WORDNET_ENCODE_MAP.items()}

    COCA_ENCODE_MAP = {
        "NOUN": "N",
        "VERB": "V",
        "ADJ": "J",
        "ADV": "R",
    }
    COCA_DECODE_MAP = {v: k for k, v in COCA_ENCODE_MAP.items()}

    @staticmethod
    def convert(pos: str, src_fmt: int, dst_fmt: int) -> str:
        pos_root = None
        if src_fmt == POSConverter2.NLTK_FORMAT:
            pos_root = POSConverter2.NLTK_DECODE_MAP[pos]
        elif src_fmt == POSConverter2.SPACY_FORMAT:
            pos_root = POSConverter2.SPACY_DECODE_MAP[pos]
        elif src_fmt == POSConverter2.WORDNET_FORMAT:
            pos_root = POSConverter2.WORDNET_DECODE_MAP[pos]
        elif src_fmt == POSConverter2.COCA_FORMAT:
            pos_root = POSConverter2.COCA_DECODE_MAP[pos]
        else:
            raise ValueError(f"Invalid format: {src_fmt}")

        if dst_fmt == POSConverter2.NLTK_FORMAT:
            pos_ret = POSConverter2.NLTK_ENCODE_MAP[pos_root]
        elif dst_fmt == POSConverter2.SPACY_FORMAT:
            pos_ret = POSConverter2.SPACY_ENCODE_MAP[pos_root]
        elif dst_fmt == POSConverter2.WORDNET_FORMAT:
            pos_ret = POSConverter2.WORDNET_ENCODE_MAP[pos_root]
        elif dst_fmt == POSConverter2.COCA_FORMAT:
            pos_ret = POSConverter2.COCA_ENCODE_MAP[pos_root]
        else:
            raise ValueError(f"Invalid format: {dst_fmt}")
        return pos_ret


def extract_sentence_by_word_position(article: str, start_pos: int, end_pos: int) -> tuple[int, int]:
    """
    extract the sentence containing the given word positions from the article

    Args:
        article: text of full article
        start_pos: word start position (inclusive)
        end_pos: word end position (exclusive)

    Returns:
        sentence start position (inclusive), sentence end position (exclusive)
    """
    if start_pos < 0 or end_pos > len(article) or start_pos >= end_pos:
        raise ValueError("Invalid word positions")

    sentence_endings = ['.', '!', '?']

    sentence_start = start_pos
    while sentence_start > 0:
        if article[sentence_start - 1] in sentence_endings and (
                sentence_start == len(article) or
                article[sentence_start] == ' ' or
                article[sentence_start] == '\n'
        ):
            break
        sentence_start -= 1

    sentence_end = end_pos
    while sentence_end < len(article):
        if article[sentence_end] in sentence_endings:
            sentence_end += 1
            break
        sentence_end += 1

    return sentence_start, sentence_end


def fetch_article(url: str) -> str:
    """
    fetch the article from the given url
    Args:
        url: the target url
    Returns:
        the article text
    """

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}  # Be polite
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.text, 'html.parser')

        # --- CNA Specific Extraction ---

        # --- Part 1: Extract Title ---
        title_tag = soup.find('h1', class_='h1--page-title')
        title = title_tag.get_text(strip=True) if title_tag else "Title not found"
        # --- End Part 1 ---

        # --- Part 2: Extract Subtitle ---
        subtitle_div = soup.find('div', class_='content-detail__description')
        # Check if the div exists and contains a <p> tag
        subtitle = subtitle_div.find('p').get_text(strip=True) if subtitle_div and subtitle_div.find(
            'p') else "Subtitle not found"
        # --- End Part 2 ---

        # --- Part 3: Extract Main Body ---
        # Find the main content area which seems to contain the relevant text blocks
        main_content_section = soup.find('section', class_='block-field-blocknodearticlefield-content')

        paragraphs_text = []
        if main_content_section:
            # Find all 'text-long' divs within that section
            text_long_divs = main_content_section.find_all('div', class_='text-long')
            for div in text_long_divs:
                # Extract text primarily from <p> tags within text-long divs
                p_tags = div.find_all('p')
                for p in p_tags:
                    paragraph = p.get_text(strip=True)
                    # Basic filtering (optional): remove very short paragraphs or specific unwanted text
                    if paragraph and len(
                            paragraph) > 10 and "audio is generated by an AI tool" not in paragraph.lower():
                        paragraphs_text.append(paragraph)
                # Include text from bullet points <ul><li> if any exist directly under text-long
                ul_tags = div.find_all('ul', recursive=False)  # Find direct children <ul>
                for ul in ul_tags:
                    list_items = ul.find_all('li')
                    for li in list_items:
                        item_text = li.get_text(strip=True)
                        if item_text:
                            paragraphs_text.append(f"- {item_text}")  # Add bullet point marker

        if not paragraphs_text:
            print(
                f"Warning: Could not extract text using CNA selectors for {url}. Falling back to generic <p> tag search.")
            # Fallback to generic <p> search if specific selectors fail
            paragraphs = soup.find_all('p')
            paragraphs_text = [p.get_text(strip=True) for p in paragraphs if
                               p.get_text(strip=True) and len(p.get_text(strip=True)) > 20]  # Basic length filter

        full_text = "\n\n".join(paragraphs_text)

        # Clean up extra whitespace that might result from joining
        full_text = re.sub(r'\n{3,}', '\n\n', full_text).strip()

        if not full_text:
            print(f"Warning: Could not extract significant text content for {url}")
        # --- End Part 3 ---

        # --- Part 4: Structure Return Dictionary ---
        article_data = {
            'title': title,
            'subtitle': subtitle,
            'body': full_text  # Including body in the example dict structure
        }
        # --- End Part 4 ---

        return article_data['body']

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        raise e
    except Exception as e:
        print(f"Error parsing HTML from {url}: {e}")
        raise e
