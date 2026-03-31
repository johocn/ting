<template>
  <div class="points-management">
    <el-card class="header-card">
      <template #header>
        <div class="card-header">
          <span>积分管理</span>
          <el-button type="primary" @click="handleCreateTransaction">创建积分流水</el-button>
        </div>
      </template>
      
      <!-- 搜索表单 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="用户ID">
          <el-input v-model="searchForm.user_id" placeholder="请输入用户ID"></el-input>
        </el-form-item>
        <el-form-item label="操作类型">
          <el-select v-model="searchForm.operation_type" placeholder="请选择操作类型">
            <el-option label="全部" value=""></el-option>
            <el-option label="观看视频" value="watch_video"></el-option>
            <el-option label="答题奖励" value="answer_quiz"></el-option>
            <el-option label="兑换商品" value="exchange"></el-option>
            <el-option label="购买商品" value="purchase"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 积分统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-item">
            <div class="stat-icon bg-blue">
              <el-icon><Coin /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ stats.total_points }}</div>
              <div class="stat-label">总积分</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-item">
            <div class="stat-icon bg-green">
              <el-icon><TrendCharts /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ stats.today_earned }}</div>
              <div class="stat-label">今日获取</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-item">
            <div class="stat-icon bg-orange">
              <el-icon><ShoppingCart /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ stats.today_spent }}</div>
              <div class="stat-label">今日消耗</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-item">
            <div class="stat-icon bg-red">
              <el-icon><Warning /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ stats.expiring_points }}</div>
              <div class="stat-label">即将过期</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 积分流水列表 -->
    <el-card class="transaction-list">
      <el-table 
        :data="transactionList" 
        v-loading="loading"
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="user_id" label="用户ID" width="100"></el-table-column>
        <el-table-column prop="transaction_type" label="交易类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getTransactionTypeTag(row.transaction_type)">
              {{ getTransactionTypeText(row.transaction_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="operation_type" label="操作类型" width="120"></el-table-column>
        <el-table-column prop="points_change" label="积分变化" width="100">
          <template #default="{ row }">
            <span :class="row.points_change > 0 ? 'positive' : 'negative'">
              {{ row.points_change > 0 ? '+' : '' }}{{ row.points_change }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="balance_before" label="变动前" width="100"></el-table-column>
        <el-table-column prop="balance_after" label="变动后" width="100"></el-table-column>
        <el-table-column prop="description" label="描述"></el-table-column>
        <el-table-column prop="created_at" label="时间" width="180"></el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="pagination.currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pagination.pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="pagination.total"
        style="margin-top: 20px;"
      >
      </el-pagination>
    </el-card>

    <!-- 创建积分流水模态框 -->
    <el-dialog 
      title="创建积分流水" 
      v-model="dialogVisible"
      width="50%"
    >
      <el-form 
        :model="form" 
        :rules="formRules" 
        ref="formRef"
        label-width="120px"
      >
        <el-form-item label="用户ID" prop="user_id">
          <el-input v-model.number="form.user_id" placeholder="请输入用户ID"></el-input>
        </el-form-item>
        
        <el-form-item label="交易类型" prop="transaction_type">
          <el-select v-model="form.transaction_type">
            <el-option label="获取积分" value="earn"></el-option>
            <el-option label="消耗积分" value="spend"></el-option>
            <el-option label="冻结积分" value="freeze"></el-option>
            <el-option label="解冻积分" value="thaw"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="操作类型" prop="operation_type">
          <el-select v-model="form.operation_type">
            <el-option label="观看视频" value="watch_video"></el-option>
            <el-option label="答题奖励" value="answer_quiz"></el-option>
            <el-option label="兑换商品" value="exchange"></el-option>
            <el-option label="购买商品" value="purchase"></el-option>
            <el-option label="推荐奖励" value="referral"></el-option>
            <el-option label="每日签到" value="daily_checkin"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="积分变化量" prop="points_change">
          <el-input-number 
            v-model="form.points_change" 
            :min="-10000" 
            :max="10000"
            :step="1"
          ></el-input-number>
        </el-form-item>
        
        <el-form-item label="相关ID">
          <el-input v-model.number="form.related_id" placeholder="相关记录ID"></el-input>
        </el-form-item>
        
        <el-form-item label="描述">
          <el-input 
            type="textarea" 
            v-model="form.description"
            :rows="3"
            placeholder="请输入描述"
          ></el-input>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { pointsApi } from '@/api/modules/points'

export default {
  name: 'PointsManagement',
  
  setup() {
    // 响应式数据
    const loading = ref(false)
    const dialogVisible = ref(false)
    
    // 搜索表单
    const searchForm = reactive({
      user_id: '',
      operation_type: ''
    })
    
    // 分页信息
    const pagination = reactive({
      currentPage: 1,
      pageSize: 10,
      total: 0
    })
    
    // 统计数据
    const stats = reactive({
      total_points: 0,
      today_earned: 0,
      today_spent: 0,
      expiring_points: 0
    })
    
    // 表单数据
    const form = reactive({
      user_id: null,
      transaction_type: 'earn',
      operation_type: 'watch_video',
      points_change: 0,
      related_id: null,
      description: ''
    })
    
    // 表单验证规则
    const formRules = {
      user_id: [{ required: true, message: '请输入用户ID', trigger: 'blur' }],
      transaction_type: [{ required: true, message: '请选择交易类型', trigger: 'change' }],
      operation_type: [{ required: true, message: '请选择操作类型', trigger: 'change' }],
      points_change: [{ required: true, message: '请输入积分变化量', trigger: 'blur' }]
    }
    
    // 数据列表
    const transactionList = ref([])
    
    // 方法
    const loadTransactionList = async () => {
      loading.value = true
      try {
        const response = await pointsApi.getTransactions({
          ...searchForm,
          page: pagination.currentPage,
          page_size: pagination.pageSize
        })
        
        transactionList.value = response.data.transactions || response.data
        pagination.total = response.data.total || response.data.length
      } catch (error) {
        ElMessage.error('加载积分流水失败')
      } finally {
        loading.value = false
      }
    }
    
    const loadStats = async () => {
      try {
        // 加载统计信息
        const account = await pointsApi.getAccount()
        stats.total_points = account.total_points || 0
        
        // 这里应该有具体的统计API，为演示使用模拟数据
        stats.today_earned = 1250
        stats.today_spent = 800
        stats.expiring_points = 500
      } catch (error) {
        console.error('加载统计信息失败:', error)
      }
    }
    
    const handleSearch = () => {
      pagination.currentPage = 1
      loadTransactionList()
    }
    
    const resetSearch = () => {
      Object.keys(searchForm).forEach(key => {
        searchForm[key] = ''
      })
      handleSearch()
    }
    
    const handleCreateTransaction = () => {
      Object.keys(form).forEach(key => {
        form[key] = key === 'transaction_type' ? 'earn' : key === 'operation_type' ? 'watch_video' : null
      })
      dialogVisible.value = true
    }
    
    const handleSubmit = async () => {
      try {
        await pointsApi.createTransaction(form)
        ElMessage.success('积分流水创建成功')
        
        dialogVisible.value = false
        loadTransactionList()
      } catch (error) {
        ElMessage.error('创建失败')
      }
    }
    
    const handleSizeChange = (val) => {
      pagination.pageSize = val
      loadTransactionList()
    }
    
    const handleCurrentChange = (val) => {
      pagination.currentPage = val
      loadTransactionList()
    }
    
    const getTransactionTypeTag = (type) => {
      const tagMap = {
        'earn': 'success',
        'spend': 'danger',
        'freeze': 'warning',
        'thaw': 'primary'
      }
      return tagMap[type] || 'info'
    }
    
    const getTransactionTypeText = (type) => {
      const textMap = {
        'earn': '获取',
        'spend': '消耗',
        'freeze': '冻结',
        'thaw': '解冻'
      }
      return textMap[type] || type
    }
    
    // 生命周期
    onMounted(() => {
      loadTransactionList()
      loadStats()
    })
    
    return {
      loading,
      dialogVisible,
      searchForm,
      pagination,
      stats,
      form,
      formRules,
      transactionList,
      loadTransactionList,
      loadStats,
      handleSearch,
      resetSearch,
      handleCreateTransaction,
      handleSubmit,
      handleSizeChange,
      handleCurrentChange,
      getTransactionTypeTag,
      getTransactionTypeText
    }
  }
}
</script>

<style scoped>
.points-management {
  padding: 20px;
}

.header-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-form {
  margin-bottom: 0;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  height: 100px;
}

.stat-item {
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  color: white;
}

.bg-blue {
  background-color: #409eff;
}

.bg-green {
  background-color: #67c23a;
}

.bg-orange {
  background-color: #e6a23c;
}

.bg-red {
  background-color: #f56c6c;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.transaction-list {
  margin-bottom: 20px;
}

.positive {
  color: #67c23a;
  font-weight: bold;
}

.negative {
  color: #f56c6c;
  font-weight: bold;
}
</style>
