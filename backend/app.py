from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import ollama
import logging
import sys
import traceback
from typing import Any

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Ollama Chat API")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 存储聊天历史
chat_history: Dict[str, List[Dict]] = {}

# 定义请求和响应模型
class ChatMessage(BaseModel):
    role: str
    content: str

class ModelParams(BaseModel):
    model: str = "llama2"
    temperature: float = Field(default=0.7, ge=0, le=1)
    top_p: float = Field(default=0.9, ge=0, le=1)
    max_tokens: int = Field(default=500, gt=0)

class ChatRequest(BaseModel):
    message: str
    conversation_id: str = "default"
    model_params: Optional[ModelParams] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    history: List[ChatMessage]

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        logger.debug(f"Received chat request: {request}")
        
        # 使用默认参数如果没有提供
        model_params = request.model_params or ModelParams()
        
        # 获取或创建聊天历史
        if request.conversation_id not in chat_history:
            chat_history[request.conversation_id] = []
        
        # 添加用户消息到历史记录
        user_message = {"role": "user", "content": request.message}
        chat_history[request.conversation_id].append(user_message)
        
        try:
            # 调用 Ollama API
            logger.debug("Calling Ollama API...")
            response = ollama.chat(
                model=model_params.model,
                messages=chat_history[request.conversation_id],
                options={
                    'temperature': float(model_params.temperature),
                    'top_p': float(model_params.top_p),
                    'num_predict': int(model_params.max_tokens)
                }
            )
            logger.debug(f"Ollama API response: {response}")
            
            # 添加助手回复到历史记录
            assistant_message = {
                "role": "assistant",
                "content": response['message']['content']
            }
            chat_history[request.conversation_id].append(assistant_message)
            
            return ChatResponse(
                response=assistant_message['content'],
                conversation_id=request.conversation_id,
                history=chat_history[request.conversation_id]
            )
            
        except Exception as e:
            logger.error(f"Error calling Ollama API: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=str(e))
            
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/conversations")
async def get_conversations():
    try:
        logger.debug("Getting conversations list")
        return {"conversations": list(chat_history.keys())}
    except Exception as e:
        logger.error(f"Error getting conversations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history/{conversation_id}")
async def get_history(conversation_id: str):
    try:
        logger.debug(f"Getting history for conversation: {conversation_id}")
        if conversation_id not in chat_history:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return {"history": chat_history[conversation_id]}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/models")
async def get_models():
    try:
        logger.debug("Getting models list from Ollama")
        models = ollama.list()
        logger.debug(f"Ollama models response: {models}")
        return models
    except Exception as e:
        logger.error(f"Error getting models: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI application...")
    uvicorn.run(app, host="127.0.0.1", port=5001)
