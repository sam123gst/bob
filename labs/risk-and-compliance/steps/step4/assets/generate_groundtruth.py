

# imports
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set USER_AGENT for HTTP requests
os.environ.setdefault('USER_AGENT', 'ai-governance-bootcamp/1.0')

from langchain_ibm import WatsonxEmbeddings, WatsonxLLM
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_core.tools import render_text_description_and_args
from langchain_core.output_parsers import BaseOutputParser, JsonOutputParser
from langchain.agents.agent import AgentExecutor
from langchain_core.exceptions import OutputParserException

# Custom JSON Agent Output Parser that converts JSON to AgentAction/AgentFinish
class CustomJSONAgentOutputParser(BaseOutputParser):
    def parse(self, text: str):
        try:
            json_parser = JsonOutputParser()
            parsed = json_parser.parse(text)
            
            if parsed.get("action") == "Final Answer":
                from langchain_core.agents import AgentFinish
                return AgentFinish(
                    return_values={"output": parsed.get("action_input", "")},
                    log=text
                )
            else:
                from langchain_core.agents import AgentAction
                return AgentAction(
                    tool=parsed.get("action"),
                    tool_input=parsed.get("action_input", {}),
                    log=text
                )
        except Exception as e:
            raise OutputParserException(f"Could not parse JSON: {e}\nText: {text}")

JSONAgentOutputParser = CustomJSONAgentOutputParser

def format_log_to_str(logs):
    return str(logs)

try:
    from langchain.memory import ConversationBufferMemory
except ImportError:
    from langchain_community.chat_message_histories import ChatMessageHistory
    ConversationBufferMemory = ChatMessageHistory
from langchain_core.runnables import RunnablePassthrough
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import EmbeddingTypes

IAM_URL = "https://iam.cloud.ibm.com"
DATAPLATFORM_URL = "https://api.dataplatform.cloud.ibm.com"
FACTSHEET_URL = "https://dataplatform.cloud.ibm.com"
SERVICE_URL = "https://aiopenscale.cloud.ibm.com"

CLOUD_API_KEY = os.getenv("WATSONX_API_KEY")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

credentials = {
    "url": "https://us-south.ml.cloud.ibm.com",
    "apikey": CLOUD_API_KEY,
}
CREDENTIALS = credentials
project_id = PROJECT_ID

# model_id="ibm/granite-3-8b-instruct", 
llm = WatsonxLLM(
    model_id="ibm/granite-4-h-small", 
    url=credentials.get("url"),
    apikey=credentials.get("apikey"),
    project_id=project_id,
    params={
        GenParams.DECODING_METHOD: "greedy",
        GenParams.TEMPERATURE: 0,
        GenParams.MIN_NEW_TOKENS: 5,
        GenParams.MAX_NEW_TOKENS: 250,
        GenParams.STOP_SEQUENCES: ["Human:", "Observation"],
    },
)



# slate-30m-english-rtrvr-v2
def get_embeddings():
    embeddings = WatsonxEmbeddings(
        model_id="ibm/slate-30m-english-rtrvr-v2", #    EmbeddingTypes.IBM_SLATE_30M_ENG.value,
        url=credentials["url"],
        apikey=credentials["apikey"],
        project_id=project_id,
    )
    return embeddings




def get_text_splitter():
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=250, chunk_overlap=0
    )
    return text_splitter





hr_faq_urls = [
    'https://www.jpmorganchase.com/content/dam/jpmc/jpmorgan-chase-and-co/documents/code-of-conduct.pdf'
]

ai_act_urls = [
    'https://artificialintelligenceact.eu/high-level-summary/'
]



def get_retriever(urls, collection_name):
    docs = []
    
    for url in urls:
        if url.endswith('.pdf'):
            # Handle PDF files
            try:
                loader = PyPDFLoader(url)
                docs.extend(loader.load())
                print(f"✓ Loaded PDF: {url}")
            except Exception as e:
                print(f"✗ Error loading PDF {url}: {str(e)}")
        else:
            # Handle web URLs
            try:
                loader = WebBaseLoader(url)
                docs.extend(loader.load())
                print(f"✓ Loaded web page: {url}")
            except Exception as e:
                print(f"✗ Error loading {url}: {str(e)}")
    
    if not docs:
        print(f"⚠ Warning: No documents loaded for {collection_name}!")
        return None
    
    text_splitter = get_text_splitter()
    doc_splits = text_splitter.split_documents(docs)
    print(f"✓ Split into {len(doc_splits)} chunks for {collection_name}")
    
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name=collection_name,
        embedding=get_embeddings(),
    )
    retriever = vectorstore.as_retriever()
    return retriever


# Initialize retrievers with error handling
print("Initializing retrievers...")
hr_faqs_retriever = get_retriever(urls=hr_faq_urls, collection_name='hr_faqs')
ai_act_retriever = get_retriever(urls=ai_act_urls, collection_name='ai_act')

# Check if retrievers loaded successfully
if hr_faqs_retriever is None:
    print("⚠ HR FAQ retriever failed to load. This tool may not work properly.")
if ai_act_retriever is None:
    print("⚠ AI Act retriever failed to load. This tool may not work properly.")



hr_faqs_context = ""
ai_act_context = ""

@tool
def get_HR_FAQs_Context(question: str):
    """Get context from Hr documents related Frequently asked questions."""
    global hr_faqs_context
    if hr_faqs_retriever is None:
        return "HR FAQ retriever is not available. Unable to retrieve context."
    hr_faqs_context = hr_faqs_retriever.invoke(question)
    return hr_faqs_context

@tool
def get_AI_Act_Summary_Context(question: str):
    """Get context from High-level summary of the AI Act."""
    global ai_act_context
    if ai_act_retriever is None:
        return "AI Act retriever is not available. Unable to retrieve context."
    ai_act_context = ai_act_retriever.invoke(question)
    return ai_act_context

tools = [get_HR_FAQs_Context]

system_prompt = """Respond to the human as helpfully and accurately as possible. You have access to the following tools: {tools}
Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).
Valid "action" values: "Final Answer" or {tool_names}
Provide only ONE action per $JSON_BLOB, as shown:"
```
{{
  "action": $TOOL_NAME,
  "action_input": $INPUT
}}
```
Follow this format:
Question: input question to answer
Thought: consider previous and subsequent steps
Action:
```
$JSON_BLOB
```
Observation: action result
... (repeat Thought/Action/Observation N times)
Thought: I know what to respond
Action:
```
{{
  "action": "Final Answer",
  "action_input": "Final response to human"
}}
Begin! Reminder to ALWAYS respond with a valid json blob of a single action.
Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation"""

human_prompt = """{input}
{agent_scratchpad}
(reminder to always respond in a JSON blob)"""



prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", human_prompt),
    ]
)




prompt = prompt.partial(
    tools=render_text_description_and_args(list(tools)),
    tool_names=", ".join([t.name for t in tools]),
)



memory = ConversationBufferMemory()




prompt_input = prompt.messages[0].prompt.template + '\n\n' + prompt.messages[2].prompt.template

chain = (
    RunnablePassthrough.assign(
        agent_scratchpad=lambda x: format_log_to_str(x["intermediate_steps"]),
        chat_history=lambda x: [],
    )
    | prompt
    | llm
    | JSONAgentOutputParser()
)

agent_executor = AgentExecutor(
    agent=chain, tools=tools, handle_parsing_errors=True, verbose=True
)



def construct_context(relevant_context):
    context_str = ''
    for doc in relevant_context:
        context_str = context_str + doc.page_content + '\n\n'
    return context_str    



# Load queries and responses from CSV
import pandas as pd

csv_path = os.path.join(
    os.path.dirname(__file__),
    'Queries_and_Responses.csv'
)

queries_df = pd.read_csv(csv_path)

# Store the complete the context
complete_content = []

# Iterate through first 10 queries
for idx, row in queries_df.head(10).iterrows():
    query = row['query']
    reference = row['response']
    
    print(f"\nProcessing query {idx + 1}/10: {query[:50]}...")
    
    try:
        # Invoke the agent with the query
        response = agent_executor.invoke({"input": query})
        
        # Build the result object
        prompt_result = {
            'query': query,
            'reference': response['output'], # reference,
            'generated_text': response['output'],
            'context': construct_context(hr_faqs_context)
        }
        complete_content.append(prompt_result)
        print(f"✓ Query {idx + 1} completed successfully")
    except Exception as e:
        print(f"✗ Error processing query {idx + 1}: {str(e)}")
        continue

# Create dataframe from collected data
llm_data = pd.DataFrame(complete_content)

# Save to CSV
output_csv_path = os.path.join(
    os.path.dirname(__file__),
    'hr_queries_with_ground_truth.csv'
)

llm_data.to_csv(output_csv_path, index=False)
print(f"\n✓ Results saved to: {output_csv_path}")
print(f"Total queries processed: {len(llm_data)}")
print("\nDataframe preview:")
print(llm_data.head())