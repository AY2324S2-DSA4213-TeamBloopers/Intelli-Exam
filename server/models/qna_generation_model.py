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
        self.chat_session_id = self.client.create_chat_session_on_default_collection()


    def generate(self, prompt, timeout = 70) :
        """
        Generates an open-ended question using the prompt

        Args:
        - prompt (str): LLM generates from the prompt
        - timeout (int, optional): How long it waits until timeout.

        Returns:
        - str: The generated open-ended question.

        """
        reply = None
        while not reply:
            try:
                with self.client.connect(self.chat_session_id) as session:
                    reply = session.query(prompt, timeout=timeout, rag_config={"rag_type": "llm_only"})
            except Exception as e:
                self.chat_session_id = self.client.create_chat_session_on_default_collection()
                continue

        return reply.content

    def generate_open_ended(self, context_list, count, max_tokens_per_answer=100):
        """
        Generates open-ended questions for each context in the provided list.

        Args:
        - context_list (list of str): List of contextual data for generating questions.
        - count (int): How many questions the model should generate.
        - max_tokens_per_answer (int, optional): The maximum number of tokens allowed for each generated answer. Default is 100.

        Returns:
        - str: The content of the generated questions.
        """
        # Generate prompts
        prompt = f"Generate an open ended question for each context data with answers. Each answer should be less than {max_tokens_per_answer} words. There should be a short explanation given for the answer. \n"       
        end = "You must respond in JSON with the format like this {Q1: {Question: [Question], Answer: [Answer], Explanation: [Explanation]}, Q2{Question: [Question], Answer: [Answer], Explanation: [Explanation]} ...}" 

        generates = len(context_list)

        #Split questions equally to number of contexts
        num_questions_list = [count // generates + (1 if x < count % generates else 0)  for x in range (generates)]

        collated_replies = ""

        i = 0

        for context in context_list:
            num_questions = num_questions_list[i]
            if num_questions > 0:
                i += 1
                context_prompt = prompt + self.generate_prompt_oe(context, num_questions)
                context_prompt += end

                reply = self.generate(context_prompt)

                collated_replies += reply.content

        return collated_replies

    def generate_mcq(self, context_list, count):
        """
        Generates MCQ questions for each context in the provided list.

        Args:
        - context_list (list of str): List of contextual data for generating questions.
        - count (int): How many questions the model should generate.

        Returns:
        - str: The content of the generated questions.
        """
        # Generate prompts
        prompt = "Generate MCQ open ended questions for each context data with answers. Each MCQ questions should have four choices. There should be a short explanation given for the answer. \n"
        end = "You must respond in JSON with the format like this {Q: Question:{Question:[Question], a:[Answer], b:[Answer], c:[Answer] d:[Answer]}, Answer:[Answer] , Explanation:[Explanation]}, Q: Question:{Question:[Question], a:[Answer], b:[Answer], c:[Answer] d:[Answer]}, Answer:[Answer], Explanation: [Explanation]} ...}"

        generates = len(context_list)

        num_questions_list = [count // generates + (1 if x < count % generates else 0)  for x in range (generates)]

        collated_replies = ""

        i = 0

        for context in context_list:
            num_questions = num_questions_list[i]
            if num_questions > 0:
                i += 1
                context_prompt = prompt + self.generate_prompt_mcq(context, num_questions)
                context_prompt += end

                reply = self.generate(context_prompt)

                collated_replies += reply.content

        return collated_replies

    def generate_prompt_oe(self, context, count):
        """
        Generates a prompt for generating an open-ended question using the given context.

        Args:
        - prompt (str): The initial prompt for generating the question.
        - context (str): The contextual data to be included in the prompt.

        Returns:
        - str: The generated prompt for generating an open-ended question.
        """
        prompt = f"Prompt: Give me {count} number of open ended questions form the following context"
        context = f"Contextual Data: {context}"

        return(prompt + context)

    def generate_prompt_mcq(self, context, count):
        """
        Generates a prompt for generating an open-ended question using the given context.

        Args:
        - prompt (str): The initial prompt for generating the question.
        - context (str): The contextual data to be included in the prompt.
        - count (int): The number of questions the ML should generate form this context

        Returns:
        - str: The generated prompt for generating an open-ended question.
        """
        prompt = f"Prompt: Give me {count} number of mcq questions from following context"
        context = f"Contextual Data: {context}"

        return(prompt + context)