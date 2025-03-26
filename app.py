import streamlit as st
import hashlib
import re
from datetime import datetime
from main import ChatGroqConfig, ChatMessageHistory

# Configure Streamlit with additional settings
st.set_page_config(
    page_title="ChatCidadeBR - Assistente de Cidades Brasileiras",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': 'ChatCidadeBR - Assistente Virtual para Informações sobre Cidades Brasileiras'
    }
)

# Initialize session state
if 'conversations' not in st.session_state:
    st.session_state.conversations = {}
if 'current_conversation_id' not in st.session_state:
    st.session_state.current_conversation_id = None
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = ChatGroqConfig()

def sanitize_input(text):
    """
    Sanitize user input to prevent XSS and other injection attacks
    """
    # Remove HTML tags
    text = re.sub(r'<[^>]*>', '', text)
    # Remove special characters but keep Portuguese accents
    text = re.sub(r'[^\w\s\-áéíóúâêîôûãõçÁÉÍÓÚÂÊÎÔÛÃÕÇ?!.,]', '', text)
    return text.strip()

def create_conversation_id():
    """
    Generate a unique conversation ID based on timestamp
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return hashlib.md5(timestamp.encode()).hexdigest()[:8]

def get_conversation_history(conv_id):
    """
    Retrieve conversation history for given ID
    """
    return st.session_state.conversations.get(conv_id, [])

def add_message_to_history(conv_id, role, content):
    """
    Add a new message to conversation history
    """
    if conv_id not in st.session_state.conversations:
        st.session_state.conversations[conv_id] = []
    
    st.session_state.conversations[conv_id].append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    })

def main():
    st.title("💬 ChatCidadeBR - Assistente de Cidades Brasileiras")
    
    # Sidebar for conversation management
    with st.sidebar:
        st.header("Conversas")
        
        # New conversation button with key
        if st.button("Nova Conversa", key="new_chat"):
            new_conv_id = create_conversation_id()
            st.session_state.current_conversation_id = new_conv_id
            st.session_state.conversations[new_conv_id] = []
            st.rerun()
        
        # List existing conversations with container
        st.subheader("Histórico de Conversas")
        conv_container = st.container()
        
        with conv_container:
            for conv_id in st.session_state.conversations.keys():
                col1, col2 = st.columns([4, 1])
                with col1:
                    if st.button(f"Conversa {conv_id}", key=f"select_{conv_id}"):
                        st.session_state.current_conversation_id = conv_id
                        st.rerun()
                with col2:
                    if st.button("🗑️", key=f"delete_{conv_id}"):
                        del st.session_state.conversations[conv_id]
                        if st.session_state.current_conversation_id == conv_id:
                            st.session_state.current_conversation_id = None
                        st.rerun()

    # Main chat interface
    if st.session_state.current_conversation_id:
        # Display current conversation ID
        st.caption(f"Conversa atual: {st.session_state.current_conversation_id}")
        
        # Display conversation history
        for message in get_conversation_history(st.session_state.current_conversation_id):
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Digite sua pergunta sobre alguma cidade brasileira...", key="chat_input"):
            # Process message and update UI
            with st.spinner("Processando..."):
                sanitized_prompt = sanitize_input(prompt)
                # Use chatbot from session state instead of undefined chatgroq
                response = st.session_state.chatbot.processar_interacao(sanitized_prompt)
                
                # Add messages to conversation history
                add_message_to_history(
                    st.session_state.current_conversation_id,
                    "user",
                    sanitized_prompt
                )
                add_message_to_history(
                    st.session_state.current_conversation_id,
                    "assistant",
                    response["content"]
                )
                
                st.rerun()
    else:
        # Welcome message
        st.info("""
        👋 Bem-vindo ao ChatCidadeBR!
        
        Este é um assistente especializado em informações sobre cidades brasileiras.
        Para começar, clique em "Nova Conversa" no menu lateral.
        
        Você pode perguntar sobre:
        - População das cidades
        - Pontos turísticos
        - Universidades
        
        Exemplo: "Qual é a população de São Paulo?"
        """)

if __name__ == "__main__":
    main()