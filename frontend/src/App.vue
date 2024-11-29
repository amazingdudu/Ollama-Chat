<template>
  <div class="app-container">
    <el-container>
      <el-aside width="250px" class="sidebar">
        <!-- 模型选择 -->
        <div class="model-select">
          <el-select v-model="selectedModel" placeholder="选择模型" @change="handleModelChange">
            <el-option
              v-for="model in availableModels"
              :key="model.name"
              :label="model.name"
              :value="model.name"
            />
          </el-select>
        </div>

        <!-- 参数设置 -->
        <div class="model-params">
          <h3>模型参数</h3>
          <el-form>
            <el-form-item label="Temperature">
              <el-slider v-model="modelParams.temperature" :min="0" :max="1" :step="0.1" />
            </el-form-item>
            <el-form-item label="Top P">
              <el-slider v-model="modelParams.top_p" :min="0" :max="1" :step="0.1" />
            </el-form-item>
            <el-form-item label="Max Tokens">
              <el-input-number v-model="modelParams.max_tokens" :min="1" :max="2000" />
            </el-form-item>
          </el-form>
        </div>

        <!-- 会话列表 -->
        <div class="conversations">
          <h3>会话列表</h3>
          <el-menu
            :default-active="currentConversationId"
            @select="handleConversationSelect"
          >
            <el-menu-item
              v-for="id in conversations"
              :key="id"
              :index="id"
            >
              会话 {{ id }}
            </el-menu-item>
          </el-menu>
          <el-button type="primary" @click="createNewConversation">新建会话</el-button>
        </div>
      </el-aside>

      <el-main>
        <!-- 聊天界面 -->
        <div class="chat-container">
          <div class="messages" ref="messagesContainer">
            <div
              v-for="(message, index) in currentHistory"
              :key="index"
              :class="['message', message.role === 'user' ? 'user-message' : 'assistant-message']"
            >
              <div class="message-content">
                <div class="message-role">{{ message.role === 'user' ? '你' : 'AI' }}</div>
                <div class="message-text">{{ message.content }}</div>
              </div>
            </div>
          </div>

          <!-- 输入框 -->
          <div class="input-container">
            <el-input
              v-model="userInput"
              type="textarea"
              :rows="3"
              placeholder="输入消息..."
              @keyup.enter.ctrl="sendMessage"
            />
            <el-button type="primary" @click="sendMessage" :loading="loading">
              发送
            </el-button>
          </div>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

// 状态变量
const userInput = ref('')
const loading = ref(false)
const availableModels = ref([])
const selectedModel = ref('llama2')
const conversations = ref(['default'])
const currentConversationId = ref('default')
const currentHistory = ref([])
const messagesContainer = ref(null)

// 模型参数
const modelParams = ref({
  temperature: 0.7,
  top_p: 0.9,
  max_tokens: 500
})

// 获取可用模型列表
async function fetchModels() {
  try {
    const response = await axios.get('/api/models')
    availableModels.value = response.data.models
  } catch (error) {
    ElMessage.error('获取模型列表失败')
  }
}

// 获取会话历史
async function fetchHistory(conversationId) {
  try {
    const response = await axios.get(`/api/history/${conversationId}`)
    currentHistory.value = response.data.history
    await nextTick()
    scrollToBottom()
  } catch (error) {
    ElMessage.error('获取会话历史失败')
  }
}

// 发送消息
async function sendMessage() {
  if (!userInput.value.trim()) return

  loading.value = true
  try {
    const response = await axios.post('/api/chat', {
      message: userInput.value,
      conversation_id: currentConversationId.value,
      model_params: {
        model: selectedModel.value,
        ...modelParams.value
      }
    })

    currentHistory.value = response.data.history
    userInput.value = ''
    await nextTick()
    scrollToBottom()
  } catch (error) {
    ElMessage.error('发送消息失败')
  } finally {
    loading.value = false
  }
}

// 创建新会话
function createNewConversation() {
  const newId = `conv-${Date.now()}`
  conversations.value.push(newId)
  currentConversationId.value = newId
  currentHistory.value = []
}

// 切换会话
function handleConversationSelect(id) {
  currentConversationId.value = id
  fetchHistory(id)
}

// 切换模型
function handleModelChange(model) {
  selectedModel.value = model
}

// 滚动到底部
function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// 组件挂载时初始化
onMounted(() => {
  fetchModels()
  fetchHistory(currentConversationId.value)
})
</script>

<style scoped>
.app-container {
  height: 100vh;
  width: 100vw;
}

.sidebar {
  padding: 20px;
  background-color: #f5f7fa;
  border-right: 1px solid #e6e6e6;
}

.model-select,
.model-params,
.conversations {
  margin-bottom: 20px;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.messages {
  flex-grow: 1;
  overflow-y: auto;
  padding: 20px;
}

.message {
  margin-bottom: 20px;
  padding: 10px;
  border-radius: 8px;
}

.user-message {
  background-color: #e3f2fd;
  margin-left: 20%;
}

.assistant-message {
  background-color: #f5f5f5;
  margin-right: 20%;
}

.message-content {
  display: flex;
  flex-direction: column;
}

.message-role {
  font-weight: bold;
  margin-bottom: 5px;
}

.input-container {
  padding: 20px;
  border-top: 1px solid #e6e6e6;
  display: flex;
  gap: 10px;
}

.el-button {
  align-self: flex-end;
}
</style>
