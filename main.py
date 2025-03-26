# Dictionary containing information about Brazilian cities
# Each city has population, tourist spots, and main university
city_data = {
    "São Paulo": {
        "população": "12,33 milhões",
        "pontos_turisticos": ["Parque Ibirapuera", "Avenida Paulista", "Mercado Municipal", "Catedral da Sé"],
        "universidade": "Universidade de São Paulo (USP)"
    },
    "Rio de Janeiro": {
        "população": "6,7 milhões",
        "pontos_turisticos": ["Cristo Redentor", "Pão de Açúcar", "Praia de Copacabana"],
        "universidade": "Universidade Federal do Rio de Janeiro (UFRJ)"
    },
    "Salvador": {
        "população": "2,9 milhões",
        "pontos_turisticos": ["Pelourinho", "Elevador Lacerda", "Farol da Barra"],
        "universidade": "Universidade Federal da Bahia (UFBA)"
    },
    "Belo Horizonte": {
        "população": "2,5 milhões",
        "pontos_turisticos": ["Praça da Liberdade", "Igreja São José", "Museu de Artes e Ofícios"],
        "universidade": "Universidade Federal de Minas Gerais (UFMG)"
    },
    "Fortaleza": {
        "população": "2,7 milhões",
        "pontos_turisticos": ["Praia do Futuro", "Catedral Metropolitana", "Mercado Central"],
        "universidade": "Universidade Federal do Ceará (UFC)"
    },
    "Brasília": {
        "população": "3,1 milhões",
        "pontos_turisticos": ["Congresso Nacional", "Catedral de Brasília", "Palácio do Planalto"],
        "universidade": "Universidade de Brasília (UnB)"
    },
    "Curitiba": {
        "população": "1,9 milhões",
        "pontos_turisticos": ["Jardim Botânico", "Ópera de Arame", "Rua XV de Novembro"],
        "universidade": "Universidade Federal do Paraná (UFPR)"
    },
    "Porto Alegre": {
        "população": "1,5 milhões",
        "pontos_turisticos": ["Parque Redenção", "Caminho dos Antiquários", "Fundação Ibere Camargo"],
        "universidade": "Universidade Federal do Rio Grande do Sul (UFRGS)"
    },
    "Recife": {
        "população": "1,6 milhões",
        "pontos_turisticos": ["Praia de Boa Viagem", "Instituto Ricardo Brennand", "Marco Zero"],
        "universidade": "Universidade Federal de Pernambuco (UFPE)"
    },
    "Manaus": {
        "população": "2,1 milhões",
        "pontos_turisticos": ["Teatro Amazonas", "Encontro das Águas", "Palácio Rio Negro"],
        "universidade": "Universidade Federal do Amazonas (UFAM)"
    },
    "Natal": {
        "população": "1,4 milhões",
        "pontos_turisticos": ["Forte dos Reis Magos", "Praia de Ponta Negra", "Dunas de Genipabu"],
        "universidade": "Universidade Federal do Rio Grande do Norte (UFRN)"
    },
    "Maceió": {
        "população": "1,0 milhão",
        "pontos_turisticos": ["Praia do Francês", "Palácio Marechal Floriano Peixoto", "Igreja de São Gonçalo do Amarante"],
        "universidade": "Universidade Federal de Alagoas (UFAL)"
    },
    "Cuiabá": {
        "população": "620 mil",
        "pontos_turisticos": ["Parque Nacional de Chapada dos Guimarães", "Catedral Basílica do Senhor Bom Jesus", "Museu do Morro da Caixa D'Água"],
        "universidade": "Universidade Federal de Mato Grosso (UFMT)"
    },
    "Aracaju": {
        "população": "650 mil",
        "pontos_turisticos": ["Praia de Atalaia", "Museu Palácio Marechal Floriano Peixoto", "Mercado Municipal"],
        "universidade": "Universidade Federal de Sergipe (UFS)"
    }
}


# Class to maintain chat conversation history
class ChatMessageHistory:
    def __init__(self):
        # List to store all chat messages
        self.history = []
    
    def add_message(self, message):
        """
        Add a new message to the chat history
        message: dict containing 'role' (user/assistant) and 'content' of the message
        """
        # Store message with role, content and timestamp
        self.history.append({
            'role': message['role'],
            'content': message['content'],
            'timestamp': message.get('timestamp', None)
        })
    
    def get_history(self):
        """
        Return the complete chat history
        """
        return self.history
    
    def get_last_n_messages(self, n):
        """
        Return the last n messages from the chat history
        """
        return self.history[-n:] if n > 0 else []
    
    def clear_history(self):
        """
        Clear all messages from the chat history
        """
        self.history = []


# Class for handling message templates with dynamic placeholders
class MessagesPlaceholder:
    def __init__(self, template):
        # Store the message template with placeholders
        self.template = template
        
    def format(self, **kwargs):
        """
        Format the template by replacing placeholders with provided values
        kwargs: dictionary of key-value pairs for placeholder substitution
        """
        try:
            # Attempt to replace all placeholders with provided values
            return self.template.format(**kwargs)
        except KeyError as e:
            # Handle missing placeholder values
            return f"Error: Missing placeholder value for {str(e)}"
        except Exception as e:
            # Handle other formatting errors
            return f"Error formatting message: {str(e)}"
    
    def get_template(self):
        """
        Return the current template
        """
        return self.template
    
    def set_template(self, new_template):
        """
        Update the template
        """
        self.template = new_template


# Class to handle ChatGroq configuration and message formatting
from dotenv import load_dotenv
import os
from datetime import datetime  # Add this import
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

class ChatGroqConfig:
    def __init__(self):
        # Load environment variables first
        load_dotenv()
        
        # Verify API key is loaded
        self.api_key = os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
            
        self.chat_history = ChatMessageHistory()
        
        # Initialize LangChain components with verified API key
        self.llm = ChatGroq(
            api_key=self.api_key,
            model_name="mixtral-8x7b-32768"
        )
        
        # Initialize message store
        self.message_store = {}
        
        # Enhanced system message
        self.system_message = SystemMessage(content=(
            "Você é um chatbot especialista em cidades brasileiras que mantém o contexto da conversa. "
            "Use o histórico para contextualizar respostas e fazer referências a interações anteriores. "
            "Base suas respostas apenas nos dados fornecidos sobre as cidades."
        ))
        
        # Initialize chat prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            self.system_message,
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        # Initialize conversation with memory
        self.memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="history",
            human_prefix="Usuário",
            ai_prefix="Assistente"
        )
        
        # Create conversation chain with memory
        self.conversation = ConversationChain(
            llm=self.llm,
            prompt=self.prompt_template,
            memory=self.memory,
            verbose=True
        )

    def processar_interacao(self, pergunta):
        cidade = self.extrair_nome_cidade(pergunta)
        timestamp = datetime.now().isoformat()

        # Add context about the city if present
        if cidade and cidade in city_data:
            city_info = city_data[cidade]
            context = (
                f"\nInformações disponíveis sobre {cidade}:\n"
                f"População: {city_info['população']}\n"
                f"Pontos turísticos: {', '.join(city_info['pontos_turisticos'])}\n"
                f"Universidade: {city_info['universidade']}\n"
            )
            pergunta = context + "\n" + pergunta

        # Process the interaction with memory
        response = self.conversation.predict(input=pergunta)

        # Store in custom history
        self.chat_history.add_message({
            'role': 'user',
            'content': pergunta,
            'timestamp': timestamp
        })
        
        self.chat_history.add_message({
            'role': 'assistant',
            'content': response,
            'timestamp': timestamp
        })

        return {
            "role": "assistant",
            "content": response
        }

    def extrair_nome_cidade(self, pergunta):
        """
        Extract city name from user question
        Returns the city name if found, None otherwise
        """
        # Check each city name in the database
        for cidade in city_data.keys():
            # Case-insensitive search for city name in the question
            if cidade.lower() in pergunta.lower():
                return cidade
        return None

    def responder_pergunta(self, pergunta):
        """
        Process user question and return appropriate response
        """
        cidade = self.extrair_nome_cidade(pergunta)
        
        if not cidade:
            return {
                "role": "assistant",
                "content": "Desculpe, não identifiquei nenhuma cidade na sua pergunta. Por favor, mencione uma cidade específica."
            }

        if cidade not in city_data:
            return {
                "role": "assistant",
                "content": f"Desculpe, não possuo dados sobre a cidade {cidade}."
            }

        # Get city information
        city_info = city_data[cidade]

        # Generate natural responses based on question type
        if any(word in pergunta.lower() for word in ["população", "habitantes", "pessoas", "mora"]):
            return {
                "role": "assistant",
                "content": f"A população de {cidade} é de {city_info['população']}."
            }
        elif any(word in pergunta.lower() for word in ["turístico", "turismo", "visitar", "conhecer"]):
            return {
                "role": "assistant",
                "content": f"Em {cidade}, você pode visitar diversos pontos turísticos interessantes, como: {', '.join(city_info['pontos_turisticos'])}."
            }
        elif any(word in pergunta.lower() for word in ["universidade", "faculdade", "estudar"]):
            return {
                "role": "assistant",
                "content": f"A principal instituição de ensino superior em {cidade} é a {city_info['universidade']}."
            }
        else:
            return {
                "role": "assistant",
                "content": "Desculpe, não tenho informações específicas para responder essa pergunta. Posso informar sobre população, pontos turísticos ou universidades da cidade."
            }

    def processar_interacao(self, pergunta):
        """
        Process user interaction and store in history
        """
        # Add user question to history
        self.chat_history.add_message({
            'role': 'user',
            'content': pergunta,
            'timestamp': datetime.now().isoformat()
        })

        # Get response using existing logic
        response = self.responder_pergunta(pergunta)

        # Add response to history
        self.chat_history.add_message({
            'role': 'assistant',
            'content': response['content'],
            'timestamp': datetime.now().isoformat()
        })

        return response

    def get_chat_history(self):
        """
        Return the complete chat history
        """
        return self.chat_history.get_history()

# Initialize ChatGroq configuration
chatgroq = ChatGroqConfig()

def test_chatbot():
    """
    Test function to demonstrate chatbot capabilities
    """
    perguntas = [
        "Qual é a população de São Paulo?",
        "Quais são os pontos turísticos de Fortaleza?",
        "Qual é a principal universidade de Recife?",
        "Me fale sobre os lugares para visitar em Salvador",
        "Onde posso estudar em Curitiba?",
        "O que você sabe sobre a cidade de Campinas?",  # City not in database
        "Qual é o clima hoje?",  # Question without city mention
    ]

    print("=== Iniciando teste do ChatBot Cidades BR ===\n")
    
    for pergunta in perguntas:
        print("Pergunta:", pergunta)
        response = chatgroq.processar_interacao(pergunta)
        print("Resposta:", response['content'])
        print("-" * 50 + "\n")
    
    print("\n=== Histórico completo da conversa ===")
    history = chatgroq.get_chat_history()
    for idx, message in enumerate(history, 1):
        print(f"\nMensagem {idx}:")
        print(f"Papel: {message['role']}")
        print(f"Conteúdo: {message['content']}")
        print(f"Timestamp: {message['timestamp']}")
        print("-" * 30)

if __name__ == "__main__":
    test_chatbot()