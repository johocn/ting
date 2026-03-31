<template>
  <div class="channel-management">
    <el-card class="header-card">
      <template #header>
        <div class="card-header">
          <span>渠道管理</span>
          <el-button type="primary" @click="handleCreate">新增渠道</el-button>
        </div>
      </template>
      
      <!-- 搜索表单 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="渠道名称">
          <el-input v-model="searchForm.name" placeholder="请输入渠道名称"></el-input>
        </el-form-item>
        <el-form-item label="渠道类型">
          <el-select v-model="searchForm.type_id" placeholder="请选择渠道类型">
            <el-option label="全部" value=""></el-option>
            <el-option 
              v-for="type in channelTypes" 
              :key="type.id" 
              :label="type.name" 
              :value="type.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 渠道列表 -->
    <el-card class="channel-list">
      <el-table 
        :data="channelList" 
        v-loading="loading"
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="name" label="渠道名称" width="150"></el-table-column>
        <el-table-column prop="code" label="邀请码" width="120"></el-table-column>
        <el-table-column prop="type_name" label="渠道类型" width="120"></el-table-column>
        <el-table-column prop="commission_rate" label="佣金率(%)" width="120"></el-table-column>
        <el-table-column prop="stats" label="统计" width="150">
          <template #default="{ row }">
            <div>注册: {{ row.stats?.registered_users || 0 }}</div>
            <div>活跃: {{ row.stats?.active_users || 0 }}</div>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180"></el-table-column>
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'">
              {{ row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250">
          <template #default="{ row }">
            <el-button size="mini" @click="handleView(row)">查看</el-button>
            <el-button size="mini" @click="handleEdit(row)">编辑</el-button>
            <el-button 
              size="mini" 
              :type="row.is_active ? 'warning' : 'success'"
              @click="handleChangeStatus(row)"
            >
              {{ row.is_active ? '禁用' : '启用' }}
            </el-button>
            <el-button size="mini" type="primary" @click="handleViewStats(row)">统计</el-button>
          </template>
        </el-table-column>
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

    <!-- 编辑/创建模态框 -->
    <el-dialog 
      :title="dialogTitle" 
      v-model="dialogVisible"
      width="60%"
    >
      <el-form 
        :model="form" 
        :rules="formRules" 
        ref="formRef"
        label-width="120px"
      >
        <el-form-item label="渠道名称" prop="name">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        
        <el-form-item label="渠道类型" prop="type_id">
          <el-select v-model="form.type_id">
            <el-option 
              v-for="type in channelTypes" 
              :key="type.id" 
              :label="type.name" 
              :value="type.id"
            ></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="上级渠道">
          <el-select v-model="form.parent_channel_id">
            <el-option label="无上级渠道" :value="null"></el-option>
            <el-option 
              v-for="channel in allChannels" 
              :key="channel.id" 
              :label="channel.name" 
              :value="channel.id"
            ></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="佣金率(%)" prop="commission_rate">
          <el-input-number v-model="form.commission_rate" :min="0" :max="100" :precision="2"></el-input-number>
        </el-form-item>
        
        <el-form-item label="描述">
          <el-input 
            type="textarea" 
            v-model="form.description"
            :rows="4"
          ></el-input>
        </el-form-item>
        
        <el-form-item label="设置">
          <el-checkbox v-model="form.settings.allow_invite" label="允许邀请"></el-checkbox>
          <el-checkbox v-model="form.settings.allow_exchange" label="允许兑换"></el-checkbox>
          <el-checkbox v-model="form.settings.allow_verification" label="允许核销"></el-checkbox>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 渠道统计模态框 -->
    <el-dialog 
      title="渠道统计" 
      v-model="statsDialogVisible"
      width="70%"
    >
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-item">
              <div class="stat-icon bg-blue">
                <el-icon><User /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ currentStats.registered_users }}</div>
                <div class="stat-label">注册用户</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-item">
              <div class="stat-icon bg-green">
                <el-icon><UserFilled /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ currentStats.active_users }}</div>
                <div class="stat-label">活跃用户</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-item">
              <div class="stat-icon bg-orange">
                <el-icon><Coin /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ currentStats.earned_points }}</div>
                <div class="stat-label">获取积分</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-item">
              <div class="stat-icon bg-red">
                <el-icon><ShoppingCart /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ currentStats.spent_points }}</div>
                <div class="stat-label">消耗积分</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
      
      <el-table 
        :data="currentStats.daily_stats" 
        style="width: 100%; margin-top: 20px;"
      >
        <el-table-column prop="date" label="日期" width="120"></el-table-column>
        <el-table-column prop="registered_users" label="注册用户" width="120"></el-table-column>
        <el-table-column prop="active_users" label="活跃用户" width="120"></el-table-column>
        <el-table-column prop="earned_points" label="获取积分" width="120"></el-table-column>
        <el-table-column prop="spent_points" label="消耗积分" width="120"></el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { channelApi } from '@/api/modules/channel'

export default {
  name: 'ChannelManagement',
  
  setup() {
    // 响应式数据
    const loading = ref(false)
    const dialogVisible = ref(false)
    const statsDialogVisible = ref(false)
    const dialogTitle = ref('')
    const isEdit = ref(false)
    
    // 搜索表单
    const searchForm = reactive({
      name: '',
      type_id: ''
    })
    
    // 分页信息
    const pagination = reactive({
      currentPage: 1,
      pageSize: 10,
      total: 0
    })
    
    // 表单数据
    const form = reactive({
      id: null,
      name: '',
      type_id: null,
      parent_channel_id: null,
      commission_rate: 0,
      description: '',
      settings: {
        allow_invite: true,
        allow_exchange: true,
        allow_verification: true
      }
    })
    
    // 统计数据
    const currentStats = reactive({
      registered_users: 0,
      active_users: 0,
      earned_points: 0,
      spent_points: 0,
      daily_stats: []
    })
    
    // 表单验证规则
    const formRules = {
      name: [{ required: true, message: '请输入渠道名称', trigger: 'blur' }],
      type_id: [{ required: true, message: '请选择渠道类型', trigger: 'change' }]
    }
    
    // 数据列表
    const channelList = ref([])
    const channelTypes = ref([])
    const allChannels = ref([])
    
    // 方法
    const loadChannelList = async () => {
      loading.value = true
      try {
        const response = await channelApi.getList({
          ...searchForm,
          page: pagination.currentPage,
          page_size: pagination.pageSize
        })
        
        channelList.value = response.data.channels || response.data
        pagination.total = response.data.total || response.data.length
      } catch (error) {
        ElMessage.error('加载渠道列表失败')
      } finally {
        loading.value = false
      }
    }
    
    const loadChannelTypes = async () => {
      try {
        const response = await channelApi.getTypes()
        channelTypes.value = response.data.types || response.data
      } catch (error) {
        ElMessage.error('加载渠道类型失败')
      }
    }
    
    const loadAllChannels = async () => {
      try {
        const response = await channelApi.getList({})
        allChannels.value = response.data.channels || response.data
      } catch (error) {
        console.error('加载所有渠道失败:', error)
      }
    }
    
    const handleSearch = () => {
      pagination.currentPage = 1
      loadChannelList()
    }
    
    const resetSearch = () => {
      Object.keys(searchForm).forEach(key => {
        searchForm[key] = ''
      })
      handleSearch()
    }
    
    const handleCreate = () => {
      isEdit.value = false
      dialogTitle.value = '新增渠道'
      Object.keys(form).forEach(key => {
        if (key !== 'id') {
          form[key] = key === 'settings' ? {
            allow_invite: true,
            allow_exchange: true,
            allow_verification: true
          } : key === 'commission_rate' ? 0 : null
        }
      })
      dialogVisible.value = true
    }
    
    const handleEdit = (row) => {
      isEdit.value = true
      dialogTitle.value = '编辑渠道'
      Object.assign(form, row)
      dialogVisible.value = true
    }
    
    const handleView = (row) => {
      // 查看渠道详情，可以跳转到详情页
      console.log('View channel:', row)
    }
    
    const handleChangeStatus = async (row) => {
      try {
        await channelApi.update(row.id, {
          is_active: !row.is_active
        })
        ElMessage.success('状态更新成功')
        loadChannelList()
      } catch (error) {
        ElMessage.error('状态更新失败')
      }
    }
    
    const handleViewStats = async (row) => {
      try {
        const response = await channelApi.getStatistics(row.id, {})
        Object.assign(currentStats, response.data)
        statsDialogVisible.value = true
      } catch (error) {
        ElMessage.error('加载统计信息失败')
      }
    }
    
    const handleSubmit = async () => {
      try {
        if (isEdit.value) {
          await channelApi.update(form.id, form)
          ElMessage.success('更新成功')
        } else {
          await channelApi.create(form)
          ElMessage.success('创建成功')
        }
        
        dialogVisible.value = false
        loadChannelList()
      } catch (error) {
        ElMessage.error('操作失败')
      }
    }
    
    const handleSizeChange = (val) => {
      pagination.pageSize = val
      loadChannelList()
    }
    
    const handleCurrentChange = (val) => {
      pagination.currentPage = val
      loadChannelList()
    }
    
    // 生命周期
    onMounted(() => {
      loadChannelList()
      loadChannelTypes()
      loadAllChannels()
    })
    
    return {
      loading,
      dialogVisible,
      statsDialogVisible,
      dialogTitle,
      searchForm,
      pagination,
      form,
      formRules,
      currentStats,
      channelList,
      channelTypes,
      allChannels,
      loadChannelList,
      loadChannelTypes,
      loadAllChannels,
      handleSearch,
      resetSearch,
      handleCreate,
      handleEdit,
      handleView,
      handleChangeStatus,
      handleViewStats,
      handleSubmit,
      handleSizeChange,
      handleCurrentChange
    }
  }
}
</script>

<style scoped>
.channel-management {
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

.channel-list {
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
</style>
