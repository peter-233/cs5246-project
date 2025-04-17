import re

import nltk
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from gensim import corpora, models
from nltk import word_tokenize, sent_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords

from supporter.summarizer.base_summarizer import BaseSummarizer


class LDASummarizer(BaseSummarizer):
    RESOURCE_DATA_ROOT = "resources/data"

    def __init__(self, num_sentences=3, num_topics=10):
        self.num_sentences = num_sentences
        self.num_topics = num_topics
        nltk.download('punkt', download_dir=self.RESOURCE_DATA_ROOT)
        nltk.download('stopwords', download_dir=self.RESOURCE_DATA_ROOT)
        nltk.data.path.append(self.RESOURCE_DATA_ROOT)

    def __process_news_articles(self, news_article: str) -> str:
        """
        Processes news article by removing copyright notices and hyperlinks.

        Args:
            news_article (str): The news article text.

        Returns:
            str: The processed news article text.
        """
        tokens = word_tokenize(news_article)
        split_index = -1
        for i, token in enumerate(tokens[:10]):
            if token == '--':
                split_index = i
                break

        if 0 <= split_index < 10:  # only split if '--' is found in the first 10 tokens
            article_processed = news_article.split("--", 1)[1].strip()
        else:
            article_processed = news_article.strip()

        # Remove news notices (ignore case)
        article_processed = re.sub(r"copyright.*?\.", "", article_processed, flags=re.IGNORECASE)
        article_processed = re.sub(r"all rights reserved\.", "", article_processed, flags=re.IGNORECASE)
        article_processed = re.sub(r"this material may not be published, broadcast, rewritten, or redistributed\.", "",
                                   article_processed, flags=re.IGNORECASE)
        article_processed = re.sub(r"e-mail to a friend\s*\.", "", article_processed, flags=re.IGNORECASE)

        # Remove hyperlinks e.g. Watch Bush criticize the Iraqi government » .
        article_processed = re.sub(r"Watch.*»\s*\.", "", article_processed)

        return article_processed

    def __extractive_summarization_lda(self, text: str) -> str:
        """
        Performs extractive summarization using Latent Dirichlet Allocation (LDA).
        The number of topics is dynamically determined based on the article length.

        Args:
            text (str): The input text to summarize.
            num_sentences (int): The desired number of sentences in the summary (default is 4).

        Returns:
            str: The generated extractive summary.
        """
        sentences = sent_tokenize(text)
        if not sentences:
            return ""

        # Dynamically determine the number of topics based on article length, ranging from 2 to 15
        article_length = len(word_tokenize(text))
        num_topics = max(2, min(15, article_length // 100))

        # Stopwords removal
        # Normalize and tokenize sentences
        # Only keep alphanumeric tokens
        stop_words = set(stopwords.words('english'))
        tokenized_sentences = [
            [word.lower() for word in word_tokenize(sent) if word.isalnum() and word not in stop_words]
            for sent in sentences]
        # lemmatization
        lemmatizer = WordNetLemmatizer()
        tokenized_sentences = [[lemmatizer.lemmatize(word) for word in sent] for sent in tokenized_sentences]

        # Create dictionary
        dictionary = corpora.Dictionary(tokenized_sentences)

        # Create document-term matrix
        corpus = [dictionary.doc2bow(tokens) for tokens in tokenized_sentences]

        # Apply LDA model
        lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary)
        # print(f"\nLDA Topics (for article length {article_length}, num_topics={num_topics}):", lda_model.print_topics())

        # Get topic distribution for each sentence
        sentence_topic_vectors = []
        for sent_corpus in corpus:
            topic_distribution = lda_model[sent_corpus]
            # Convert topic distribution to a fixed-length vector
            topic_vector = np.zeros(num_topics)
            for topic_id, probability in topic_distribution:
                topic_vector[topic_id] = probability
            sentence_topic_vectors.append(topic_vector)

        # Calculate similarity between sentence vectors
        similarity_matrix = cosine_similarity(np.array(sentence_topic_vectors))

        # Score sentences based on the sum of their similarities with other sentences
        sentence_scores = np.sum(similarity_matrix, axis=1)

        # Get the top N scoring sentences
        ranked_sentences = sorted(((score, index) for index, score in enumerate(sentence_scores)),
                                  key=lambda s: s[0], reverse=True)

        # Extract summary sentences and sort them by their original order
        summary_indices = sorted([index for score, index in ranked_sentences[:self.num_sentences]])
        summary_sentences = [sentences[i] for i in summary_indices]

        # Join the summary sentences
        summary = " ".join(summary_sentences)
        return summary

    def summarize(self, article: str) -> str:
        cleaned_article = self.__process_news_articles(article)
        return self.__extractive_summarization_lda(cleaned_article)
