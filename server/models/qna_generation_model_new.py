from h2ogpte import H2OGPTE
import inflect
import random

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

    def generate_questions(self, contents, num_qns, open_ended=False, mcq=False, complimentary_info=None, formatting=None, max_tokens_per_answer=50):
        if open_ended and mcq:
            raise TypeError("Only one of open_ended or mcq must be set as True for question generation.")

        if not (open_ended or mcq):
            raise TypeError("Either open_ended or mcq must be set as True for question generation.")
        
        if complimentary_info and formatting:
            raise TypeError("Both complimentary info and fomatting is provided. Please only provide one of the two.")
        
        if not (complimentary_info or formatting):
            raise TypeError("Neither complimentary info and fomatting is provided. Please provide one of the two.")

        if open_ended:
            scenario_prompt = "Generate open ended questions for each content data with answers.\n"
            rules_prompt = f"Each answer should be less than {max_tokens_per_answer} words. There should be a short explanation given for the answer.\n"       
            format_prompt = "You must strictly respond in JSON with the format like this {Output:[{Question: [Question], Answer: [Answer], Explanation: [Explanation]},{Question: [Question], Answer: [Answer], Explanation: [Explanation]}, ...]}" 

        if mcq:
            scenario_prompt = "Generate multiple choice questions for each content data with answers.\n"
            rules_prompt = "Each Multiple Choice Question must have four choices. There should be a short explanation given for the answer.\n"
            format_prompt = "You must strictly respond in JSON with the format like this {Output:[{Question:[Question], Choices:{a:[Answer1], b:[Answer2], c:[Answer3] d:[Answer4]}, Answer:[Answer] , Explanation:[Explanation]},{Question:[Question], Choices:{a:[Answer1], b:[Answer2], c:[Answer3] d:[Answer4]}, Answer:[Answer] , Explanation:[Explanation]} ...]}"

        num_content = len(contents)
        num_qns_per_content = [num_qns // num_content + (1 if x < num_qns % num_content else 0)  for x in range (num_content)]

        generated_questions = []
        if complimentary_info:
            for content, comp, qn_count in zip(contents, complimentary_info, num_qns_per_content):
                if qn_count == 0:
                    break
                full_prompt = scenario_prompt + rules_prompt + self.create_complimentary_info_prompt(content, comp, qn_count) + format_prompt
                generated_question = self.generate(full_prompt, timeout = 90 + qn_count*20)
                generated_questions.append(generated_question)
        
        if formatting:
            random.shuffle(contents) # To make things exciting
            for content, qn_count in zip(contents, num_qns_per_content):
                if qn_count == 0:
                    break
                full_prompt = scenario_prompt + rules_prompt + self.create_formatting_prompt(content, formatting, qn_count) + format_prompt
                generated_question = self.generate(full_prompt, timeout = 90 + qn_count*20)
                generated_questions.append(generated_question)

        return generated_questions

    def create_complimentary_info_prompt(self, content, info, qn_count):
        prompt = f"Generate exactly {inflector.number_to_words(qn_count)} questions. The questions must ask about the CONTENT and use the INFORMATION for context only. \nCONTENT: {content}\nINFORMATION: {info}\n"
        return prompt
    
    def create_formatting_prompt(self, content, format, qn_count):
        prompt = f"Generate exactly {inflector.number_to_words(qn_count)} questions. The questions must ask about the CONTENT and the structure of the question must follow the FORMAT of questions that can be identified within. \nCONTENT: {content}\nFORMAT: {format}\n"
        return prompt
