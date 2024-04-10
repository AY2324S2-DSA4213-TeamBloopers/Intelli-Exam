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

        # Connect to client, requires API_KEY in .env
        self.client = H2OGPTE(
            address='https://h2ogpte.genai.h2o.ai',
            api_key=api_key,
        )

        # Set up chat session
        

    def generate(self, context, max_tokens_per_answer=100) :
        """
        Generates an open-ended question using the provided context.

        Args:   
        - context (str): The contextual data to be used for generating the question.
        - max_tokens_per_answer (int): The maximum number of tokens allowed for the generated question.

        Returns:
        - str: The generated open-ended question.

        """
        # Generate prompt
        prompt = f"Generate an open ended question for each context data with answers. Each answer should be less than {max_tokens_per_answer} words. There should be a short explanation given for the answer. \n"
        end = "You must strictly follow the format:  {Question: [Question] \\n Answer: [Answer] \\n Explanation: [Explanation]\\n}"
        prompt += self.generate_prompt(context=context)
        prompt += end
        
        # Connect with chat_session and query

        reply = None
        while not reply:
            try: 
                chat_session_id = self.client.create_chat_session_on_default_collection()
                with self.client.connect(chat_session_id) as session:
                    reply = session.query(prompt, timeout=40, rag_config={"rag_type": "llm_only"})
            except Exception as e:
                continue
                    
        return reply.content

    def generate_all(self, context_list, max_tokens_per_answer=100):
        """
        Generates open-ended questions for each context in the provided list.

        Args:
        - context_list (list of str): List of contextual data for generating questions.
        - max_tokens_per_answer (int, optional): The maximum number of tokens allowed for each generated answer. Default is 100.

        Returns:
        - str: The content of the generated questions.
        """
        # Generate prompts
        prompt = f"Generate an open ended question for each context data with answers. Each answer should be less than {max_tokens_per_answer} words. There should be a short explanation given for the answer. \n"
        end = "You must respond in JSON with the format like this {Q1: {Question: [Question], Answer: [Answer], Explanation: [Explanation]}, Q2{Question: [Question], Answer: [Answer], Explanation: [Explanation]} ...}"

        for context in context_list:
            prompt += self.generate_prompt(context=context)
        
        prompt += end

        reply = None

        while not reply:
            try: 
                chat_session_id = self.client.create_chat_session_on_default_collection()
                with self.client.connect(chat_session_id) as session:
                    reply = session.query(prompt, timeout=70, rag_config={"rag_type": "llm_only"}, llm_args={"max_new_tokens": 2048})
            except Exception as e:
                continue
            
        return reply.content
        
        

    def generate_prompt(self, context):
        """
        Generates a prompt for generating an open-ended question using the given context.

        Args:
        - prompt (str): The initial prompt for generating the question.
        - context (str): The contextual data to be included in the prompt.

        Returns:
        - str: The generated prompt for generating an open-ended question.
        """
        prompt = "Prompt: Give me an open ended question"
        context = f"Contextual Data: {context}"
        
        return(prompt + context)