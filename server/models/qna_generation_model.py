from h2ogpte import H2OGPTE
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

    def generate_open_ended(self, context_list, count, max_tokens_per_answer=50, question_style = None):
        """
        Generates open-ended questions for each context in the provided list.

        Args:
        - context_list (list of str): List of contextual data for generating questions.
        - count (int): How many questions the model should generate.
        - max_tokens_per_answer (int, optional): The maximum number of tokens allowed for each generated answer. Default is 50.
        - question_style (string, optional): Prompts LLM to follow style of question.

        Returns:
        - list of str: list of chunks of content as str in json format
        """
        # Generate prompts
        prompt = f"You are an educator. Generate an open ended question for each context data with answers. Each answer should be less than {max_tokens_per_answer} words. There should be a short explanation given for the answer. \n"       
        end = "You must strictly respond in JSON with the format like this {Output:[{Question: [Question], Answer: [Answer], Explanation: [Explanation]},{Question: [Question], Answer: [Answer], Explanation: [Explanation]}, ...]}" 

        generates = len(context_list)

        #Split questions equally to number of contexts
        num_questions_list = [count // generates + (1 if x < count % generates else 0)  for x in range (generates)]

        collated_replies = []

        i = 0

        for context in context_list:
            num_questions = num_questions_list[i]
            if num_questions > 0:
                i += 1
                context_prompt = prompt + self.generate_prompt_mcq(context, num_questions)
                if (question_style):
                    context_prompt += f"Please construct your question simlar to this style {question_style}"
                context_prompt += end
                collated_replies.append(self.generate(context_prompt, timeout = 90 + num_questions*20))

        return collated_replies

    def generate_mcq(self, context_list, count, question_style = None):
        """
        Generates MCQ questions for each context in the provided list.

        Args:
        - context_list (list of str): List of contextual data for generating questions.
        - count (int): How many questions the model should generate.
        - question_style (string, optional): Prompts LLM to follow style of question.

        Returns:
        - list of str: list of chunks of content as str in json format
        """
        # Generate prompts
        prompt = "You are an educator. Generate Multiple Choice Questions for each context data with answers. Each Multiple Choice Question should have four choices. There should be a short explanation given for the answer. \n"
        end = "You must strictly respond in JSON with the format like this {Output:[{Question:[Question], Choices:{a:[Answer1], b:[Answer2], c:[Answer3] d:[Answer4]}, Answer:[Answer] , Explanation:[Explanation]},{Question:[Question], Choices:{a:[Answer1], b:[Answer2], c:[Answer3] d:[Answer4]}, Answer:[Answer] , Explanation:[Explanation]} ...]}"

        generates = len(context_list)

        num_questions_list = [count // generates + (1 if x < count % generates else 0)  for x in range (generates)]

        collated_replies = []

        i = 0

        for context in context_list:
            num_questions = num_questions_list[i]
            if num_questions > 0:
                i += 1
                context_prompt = prompt + self.generate_prompt_mcq(context, num_questions)
                if (question_style):
                    context_prompt += f"Please construct your question simlar to this style {question_style}"
                context_prompt += end
                collated_replies.append(self.generate(context_prompt, timeout= 70 + num_questions*10))

        return collated_replies

    def generate_mcq_new_context(self, context_list, out_of_scope_list, count, question_style = None):
        """
        Generates MCQ questions for each context in the provided list. Includes out of scope list.

        Args:
        - context_list (list of str): List of contextual data for generating questions.
        - out_of_syllabus_list (list of str): List of contextual out of scope data that will be used to generate questions
        - count (int): How many questions the model should generate.
        - question_style (string, optional): Prompts LLM to follow style of question.

        Returns:
        - list of str: list of chunks of content as str in json format
        """
        # Generate prompts
        prompt = "You are an educator. Generate Multiple Choice Questions for each context data with answers. Each Multiple Choice Question should have four choices. There should be a short explanation given for the answer. Can you generate questions related to out of scope data, but the question's content should be those that are in context?  \n"
        end = "You must strictly respond in JSON with the format like this {Output:[{Question:[Question], Choices:{a:[Answer1], b:[Answer2], c:[Answer3] d:[Answer4]}, Answer:[Answer] , Explanation:[Explanation]},{Question:[Question], Choices:{a:[Answer1], b:[Answer2], c:[Answer3] d:[Answer4]}, Answer:[Answer] , Explanation:[Explanation]} ...]}"

        generates = len(context_list)

        num_questions_list = [count // generates + (1 if x < count % generates else 0)  for x in range (generates)]

        collated_replies = []

        i = 0

        for context in context_list:
            num_questions = num_questions_list[i]
            out_of_scope_context = out_of_scope_list[i]
            if num_questions > 0:
                context_prompt = prompt + self.generate_prompt_mcq(context, num_questions, out_of_scope=out_of_scope_context)
                if (question_style):
                    context_prompt += f"Please construct your question simlar to this style {question_style}"
                context_prompt += end
                collated_replies.append(self.generate(context_prompt, timeout= 70 + num_questions*10))
            i += 1

        return collated_replies
    
    def generate_open_ended_new_context(self, context_list, out_of_scope_list, count, max_tokens_per_answer=50, question_style = None):
        """
        Generates open-ended questions for each context in the provided list. Includes out of scope list.

        Args:
        - context_list (list of str): List of contextual data for generating questions.
        - out_of_scope_list (list of str): List of contextual out of scope data that will be used to generate questions
        - count (int): How many questions the model should generate.
        - max_tokens_per_answer (int, optional): The maximum number of tokens allowed for each generated answer. Default is 50.
        - question_style (string, optional): Prompts LLM to follow style of question.

        Returns:
        - list of str: list of chunks of content as str in json format
        """
        # Generate prompts
        prompt = f"You are an educator. Generate an open ended question for each context data with answers. Each answer should be less than {max_tokens_per_answer} words. There should be a short explanation given for the answer. Can you generate questions related to out of scope data, but the question's content should be those that are in context?\n"       
        end = "You must strictly respond in JSON with the format like this {Output:[{Question: [Question], Answer: [Answer], Explanation: [Explanation]},{Question: [Question], Answer: [Answer], Explanation: [Explanation]}, ...]}" 

        generates = len(context_list)

        #Split questions equally to number of contexts
        num_questions_list = [count // generates + (1 if x < count % generates else 0)  for x in range (generates)]

        collated_replies = []

        i = 0

        for context in context_list:
            num_questions = num_questions_list[i]
            out_of_scope_context = out_of_scope_list[i]
            if num_questions > 0:
                
                context_prompt = prompt + self.generate_prompt_mcq(context, num_questions, out_of_scope=out_of_scope_context)
                if (question_style):
                    context_prompt += f"Please construct your question simlar to this style {question_style}"
                context_prompt += end
                collated_replies.append(self.generate(context_prompt, timeout = 90 + num_questions*20))
            i += 1

        return collated_replies

    def generate_prompt_oe(self, context, count, out_of_scope = None):
        """
        Generates a prompt for generating an open-ended question using the given context.

        Args:
        - prompt (str): The initial prompt for generating the question.
        - context (str): The contextual data to be included in the prompt.
        - count (int): The number of questions the ML should generate from this context.
        - out_of_scope (string, optional): Out of scope data for prompt context.

        Returns:
        - str: The generated prompt for generating an open-ended question.
        """

        count = inflector.number_to_words(count)

        prompt = f"Prompt: Give me strictly {count} open ended questions from the following context"
        if (out_of_scope):
            prompt += f"Out Of Scope: {out_of_scope}"
        context = f"Contextual Data: {context}"

        return(prompt + context)

    def generate_prompt_mcq(self, context, count, out_of_scope = None):
        """
        Generates a prompt for generating an open-ended question using the given context.

        Args:
        - prompt (str): The initial prompt for generating the question.
        - context (str): The contextual data to be included in the prompt.
        - count (int): The number of questions the ML should generate from this context
        - out_of_scope (string, optional): Out of scope data for prompt context.

        Returns:
        - str: The generated prompt for generating an open-ended question.
        """

        count = inflector.number_to_words(count)

        prompt = f"Prompt: Give me strictly {count} multiple choice questions from following context"
        if (out_of_scope):
            prompt += f"Out Of Scope: {out_of_scope}"
        context = f"Contextual Data: {context}"

        return(prompt + context)