from h2ogpte import H2OGPTE

# Used to convert numbers to numerical words, in an attempt to improve prompting
import inflect
inflector = inflect.engine()

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

        # Set up chat session, using non-collection chat session as we isolated the RAG pipeline away from h2oGPTe.
        self.chat_session_id = self.client.create_chat_session()

    def generate(self, prompt, timeout = 70) :
        """
        Generates questions with the provided prompt.

        Args:
        - prompt (str): Prompt used for QA generation
        - timeout (int, optional): How long it waits until timeout.

        Returns:
        - str: The generated open-ended question.

        """
        reply = None

        # Repetitively retrieve output from h2oGPTe as it sometimes timeout
        while not reply:
            try:
                with self.client.connect(self.chat_session_id) as session:
                    reply = session.query(prompt, timeout=timeout, rag_config={"rag_type": "llm_only"})
            except Exception as e:
                self.chat_session_id = self.client.create_chat_session_on_default_collection()
                continue

        return reply.content

    def generate_questions(self, contents, user_input, num_qns, open_ended=False, mcq=False, complimentary_info=False, formatting=False, max_tokens_per_answer=50):
        """
        Generates questions based on the provided contents and user input.

        Args:
        - contents (list): List of content data.
        - user_input (list): List of information to be used for context or formatting.
        - num_qns (int): Total number of questions to generate.
        - open_ended (bool, optional): Whether to generate open-ended questions (default: False).
        - mcq (bool, optional): Whether to generate multiple choice questions (default: False).
        - complimentary_info (bool, optional): Whether to include complimentary information (default: False).
        - formatting (bool, optional): Whether to format the questions (default: False).
        - max_tokens_per_answer (int, optional): Maximum number of tokens allowed per answer (default: 50).

        Raises:
        - TypeError: If both open_ended and mcq are set to True or neither of them are set to True.

        Returns:
        - list: Generated questions in JSON format.
        """
        if open_ended and mcq:
            raise TypeError("Only one of open_ended or mcq must be set as True for question generation.")

        if not (open_ended or mcq):
            raise TypeError("Either open_ended or mcq must be set as True for question generation.")
        
        if complimentary_info and formatting:
            raise TypeError("Both complimentary info and formatting is set as True. Please only set one of the two.")
        
        if not (complimentary_info or formatting):
            raise TypeError("Neither complimentary info and formatting is set as True. Please set one of the two for question generation.")

        if open_ended:
            scenario_prompt = "Generate open ended questions for each content data with answers.\n"
            rules_prompt = f"Each answer should be less than {max_tokens_per_answer} words. There should be a short explanation given for the answer.\n"       
            format_prompt = "You must strictly respond in JSON with the format like this {Output:[{Question: [Question], Answer: [Answer], Explanation: [Explanation]},{Question: [Question], Answer: [Answer], Explanation: [Explanation]}, ...]}" 

        if mcq:
            scenario_prompt = "Generate multiple choice questions for each content data with answers.\n"
            rules_prompt = "Each Multiple Choice Question must have four choices. There should be a short explanation given for the answer.\n"
            format_prompt = "You must strictly respond in JSON with the format like this {Output:[{Question:[Question], Choices:{a:[Answer1], b:[Answer2], c:[Answer3] d:[Answer4]}, Answer:[Answer] , Explanation:[Explanation]},{Question:[Question], Choices:{a:[Answer1], b:[Answer2], c:[Answer3] d:[Answer4]}, Answer:[Answer] , Explanation:[Explanation]} ...]}"


        # This list is to equally split the number of questions to generate amongst the content chunks.
        # E.g. if there are 5 chunks of content and 7 questions to generate, the calculated list will be [2, 2, 1, 1, 1]
        num_content = len(contents)
        num_qns_per_content = [num_qns // num_content + (1 if x < num_qns % num_content else 0)  for x in range (num_content)]

        generated_questions = []
        for content, user_input, qn_count in zip(contents, user_input, num_qns_per_content):
            # If the number of questions to generate is less than the number of content, then there will be unnecessary content.
            if qn_count == 0:
                break

            if formatting:
                relevant_prompt = self.create_formatting_prompt(content, user_input, qn_count)
            if complimentary_info:
                relevant_prompt = self.create_complimentary_info_prompt(content, user_input, qn_count)

            full_prompt = scenario_prompt + rules_prompt + relevant_prompt + format_prompt
            generated_question = self.generate(full_prompt, timeout = 90 + qn_count*20)
            generated_questions.append(generated_question)

        return generated_questions


    # Functions for prompt generation. Isolated to reduce clutter.
    def create_complimentary_info_prompt(self, content, info, qn_count):
        prompt = f"Generate exactly {inflector.number_to_words(qn_count)} questions. The questions must strictly be regarding the CONTENT and use the INFORMATION for context only.\n\nCONTENT: [\n{content}\n]\nINFORMATION: [\n{info}\n]\n\n"
        return prompt
    def create_formatting_prompt(self, content, format, qn_count):
        prompt = f"Generate exactly {inflector.number_to_words(qn_count)} questions. The questions must be regarding the CONTENT and the structure of the question must follow the FORMAT of questions that can be identified within.\n\nCONTENT: [\n{content}\n]\nFORMAT: [\n{format}\n]\n\n"
        return prompt
