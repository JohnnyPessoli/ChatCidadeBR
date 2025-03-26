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

# Load environment variables
load_dotenv()

class ChatGroqConfig:
    def __init__(self):
        # Add chat history initialization
        self.chat_history = ChatMessageHistory()
        
        # Load API key from environment variable
        self.api_key = os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        # Define the base system prompt that sets the chatbot's role
        self.base_prompt = {
            "role": "system",
            "content": (
                "Você é um chatbot especialista em cidades brasileiras. "
                "Forneça informações precisas e objetivas, sempre em português. "
                "Base suas respostas apenas nos dados fornecidos."
            )
        }
        
        # Define different templates for various types of responses
        self.prompt_templates = {
            # Template for general city information
            "city_info": (
                "Utilize as informações a seguir para responder à pergunta do usuário.\n"
                "Cidade: {cidade}\n"
                "População: {populacao}\n"
                "Pontos turísticos: {pontos_turisticos}\n"
                "Universidade: {universidade}\n"
                "Pergunta do usuário: {user_question}\n"
                "Responda de forma clara e objetiva em português."
            ),
            # Template for tourist information
            "tourist_guide": (
                "Você é um guia turístico virtual de {cidade}. "
                "Os principais pontos turísticos são: {pontos_turisticos}. "
                "Forneça informações interessantes sobre estes locais."
            ),
            # Template for university information
            "university_info": (
                "Sobre a educação superior em {cidade}, "
                "a principal instituição é {universidade}. "
                "Forneça informações sobre esta universidade."
            )
        }

    def format_message(self, template_name, **kwargs):
        """
        Format a specific template with provided data
        """
        # Verify if the requested template exists
        if template_name not in self.prompt_templates:
            raise ValueError(f"Template '{template_name}' not found")
        
        # Create placeholder and format the message    
        placeholder = MessagesPlaceholder(self.prompt_templates[template_name])
        return placeholder.format(**kwargs)

    def create_chat_messages(self, city_name, template_name, user_question):
        """
        Create a complete message array for ChatGroq
        """
        # Check if the requested city exists in our database
        if city_name not in city_data:
            return [self.base_prompt, {
                "role": "assistant",
                "content": f"Desculpe, não tenho informações sobre a cidade {city_name}."
            }]

        # Get city information and format the message
        city_info = city_data[city_name]
        formatted_prompt = self.format_message(
            template_name,
            cidade=city_name,
            populacao=city_info["população"],
            pontos_turisticos=", ".join(city_info["pontos_turisticos"]),
            universidade=city_info["universidade"],
            user_question=user_question
        )

        # Return the complete message array for ChatGroq
        return [
            self.base_prompt,
            {
                "role": "user",
                "content": formatted_prompt
            }
        ]

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
                "content": f"{cidade} tem uma população de {city_info['população']}, " \
                          f"possui atrações turísticas como {', '.join(city_info['pontos_turisticos'])}, " \
                          f"e sua principal universidade é a {city_info['universidade']}."
            }

        # Determine the type of information being requested
        template_name = "city_info"  # default template
        if any(word in pergunta.lower() for word in ["turístico", "turismo", "visitar", "conhecer"]):
            template_name = "tourist_guide"
        elif any(word in pergunta.lower() for word in ["universidade", "faculdade", "estudar"]):
            template_name = "university_info"

        # Create formatted message using appropriate template
        messages = self.create_chat_messages(cidade, template_name, pergunta)
        
        return messages[-1]  # Return the last message (user query with context)

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