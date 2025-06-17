
from sentence_transformers import SentenceTransformer

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import nltk
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class Scorer:

    DEF_ROLES = ["Cuoco", "Poeta", "Insegnante", "Consulente"]
    DEF_MODEL_NAME  = 'nickprock/sentence-bert-base-italian-uncased'

    def __init__(self, roles: list = DEF_ROLES, model_name: str = DEF_MODEL_NAME):
        """
        Initialize the Scorer with a pre-trained SentenceTransformer model.
        :param roles: List of roles to set for the Scorer.
        :param model_name: Name of the pre-trained SentenceTransformer model.
        :raises ValueError: If roles is not a non-empty list of valid strings.
        """

        self.__stemmer = SnowballStemmer("italian")
        self._model = SentenceTransformer(model_name)
        self.set_roles(roles)

    def is_valid_role(self, role: str) -> bool:
        """
        Check if the role is valid.
        A valid role should not be empty and should not contain only whitespace.
        :param role: The role to check.
        :return: True if the role is valid, False otherwise.
        """
        return bool(role and role.strip())
    
    def set_roles(self, roles: list):
        """
        Set the roles for the Scorer.
        :param roles: List of roles to set.
        :raises ValueError: If roles is not a non-empty list of valid strings.
        """

        if not roles or not all([self.is_valid_role(role) for role in roles]):
            raise ValueError("Roles must be a non-empty list of valid strings.")
        self.roles = roles


    def is_valid_prompt(self, prompt: str) -> bool:
        """
        Check if the prompt is valid in relation to the given role
        A valid prompt should not be empty and should not contain only whitespace.
        :param prompt: The prompt to check.
        :return: True if the prompt is valid, False otherwise.
        """

        return bool(prompt and prompt.strip())

    def get_most_similar_role(self, prompt, threshold = 0.4) -> str:
        """
        Return the most similar role based on the given prompt.
        If similarity is below threshold, return None.
        :param prompt: The prompt to check.
        :return: most similar role based on the prompt.
        """

        # Create a list of sentences with roles and prompt coupled together
        sentences = [[role,prompt] for role in self.roles]

        # Encode the sentences using the model by extracting the embeddings
        embeddings = [self._model.encode(sentence) for sentence in sentences]
        
        # Calculate the similarity between the embeddings 
        similarities =  [self._model.similarity(embedding[0], embedding[1]) for embedding in embeddings]

        # Print index of max similarity
        max_similarity = max(similarities)
        max_index = similarities.index(max_similarity)

        # Check if the max similarity is above the threshold
        if max_similarity >= threshold:
            return self.roles[max_index]
        else:
            return None

    def __preprocess_text(self, text):
        '''
        Preprocess the text by tokenizing, removing stopwords, and stemming.
        :param text: The text to preprocess.
        :return: Preprocessed text as a string.
        '''
        tokens = word_tokenize(text.lower()) # Tokenize the text
        stop_words = set(stopwords.words('italian')) # Remove stopwords
        tokens = [token for token in tokens if token not in stop_words]
        tokens = [self.__stemmer.stem(token) for token in tokens]
        return ' '.join(tokens)

    def bow_similarity(self, prompt1, prompt2):
        '''
        Compute the Bag-of-Words (BoW) similarity between two prompts.
        :param prompt1: The first prompt.
        :param prompt2: The second prompt.
        :return: Cosine similarity score between the two prompts.
        '''
        # Preprocess the prompts
        processed_prompt1 = self.__preprocess_text(prompt1)
        processed_prompt2 = self.__preprocess_text(prompt2)

        # Create bag-of-words representation
        vectorizer = CountVectorizer()
        bow_representation = vectorizer.fit_transform([processed_prompt1, processed_prompt2])

        # Compute cosine similarity
        similarity = cosine_similarity(bow_representation[0:1], bow_representation[1:2])

        return similarity[0][0]
    
    def get_prompt_score(self, prompt: str, ideal_prompt: str, l_w=0.9) -> float:
        """
        Return the score of the prompt based on the roles.
        :param prompt: The prompt to check.
        :param ideal_prompt: The ideal prompt to compare against.
        :raises ValueError: If the prompt is not a non-empty string.
        :return: Score of the prompt based on the roles. It ranges from 0 to 1, where 1 is the best score.
        """
        # Check if the prompt is valid
        if not self.is_valid_prompt(prompt):
            raise ValueError("Prompt must be a non-empty string.")
        # Check if the ideal prompt is valid
        if not self.is_valid_prompt(ideal_prompt):
            raise ValueError("Ideal prompt must be a non-empty string.")
        
        #Check if the ideal prompt has the valid role 
        #Check if get_most_similar_role returns None
        ideal_role = self.get_most_similar_role(ideal_prompt)   
        if ideal_role is None:
            result = 0.1
            return result 
        
        else:
            # Compute embeddings for the ideal prompt and the prompt and then score them
            ideal_embedding,prompt_embedding = self._model.encode([ideal_prompt, prompt])
            semantic_similarity = self._model.similarity(ideal_embedding, prompt_embedding)

            # Normalize the semantic similarity score to be between 0 and 1
            semantic_similarity = (semantic_similarity + 1) / 2

            # Compute the Bag-of-Words similarity between the ideal prompt and the prompt
            lexical_similarity = self.bow_similarity(ideal_prompt, prompt)

            # Normalize the semantic similarity score to be between 0 and 1
            lexical_similarity = (lexical_similarity + 1) / 2

            # Combine the semantic and lexical similarity scores using the weight l_w
            result = ((1-l_w)*semantic_similarity + l_w*lexical_similarity).squeeze().item()
            
            return result


    