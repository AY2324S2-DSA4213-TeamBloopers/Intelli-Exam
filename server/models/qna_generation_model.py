from h2ogpte import H2OGPTE

class QNAGenerationModel:
    """
    A class for generating open-ended questions using H2OGPTE API.

    Attributes:
    - client(H2OGPTE): An instance of H2OGPTE used for connecting to the API.
    - chat_session_id(str): ID of the chat session used for generating questions.
    """
    
    def __init__(self, api_key):
        """
        Initializes the QNAGenerationModel by connecting to the H2OGPTE client and setting up a chat session.

        Args:
        - api_key (str): The API key required for connecting to the H2OGPTE client.
        """

        #Connect to client, requires API_KEY in .env
        self.client = H2OGPTE(
            address='https://h2ogpte.genai.h2o.ai',
            api_key=api_key,
        )

        #Set up chat session
        self.chat_session_id = self.client.create_chat_session_on_default_collection()

    def generate(self, context, max_new_tokens = 100) :
        """
        Generates an open-ended question using the provided context.

        Args:   
        - context (str): The contextual data to be used for generating the question.
        - max_new_tokens (int): The maximum number of tokens allowed for the generated question.

        Returns:
        - str: The generated open-ended question.

        """
        prompt = self.generate_prompt(prompt = "Give me an open ended question", context=context, max_new_tokens=max_new_tokens)
        
        #Connect with chat_session and query
        with self.client.connect(self.chat_session_id) as session:
            reply = session.query(prompt)
            
        return reply.content

    def generate_prompt(self, prompt, context, max_new_tokens):
        """
        Generates a prompt for generating an open-ended question using the given context.

        Args:
        - prompt (str): The initial prompt for generating the question.
        - context (str): The contextual data to be included in the prompt.
        - max_new_tokens (int): The maximum number of tokens allowed for the generated question.

        Returns:
        - str: The generated prompt for generating an open-ended question.

        """
        start = "Generate an open ended question using source and context data with answers. There should be a short explanation given for the answer. \n"
        prompt = f"Prompt: {prompt}"
        context = f"Contextual Data: {context}"
        end = f"The answer should be less than {max_new_tokens} words. And in the format:  Question: [Question] \\n Answer: [Answer] \\n Explanation: [Explanation]"
        return(start + prompt + context + end)
