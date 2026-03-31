<template>
  <div class="content-management">
    <el-card class="header-card">
      <template #header>
        <div class="card-header">
          <span>内容管理</span>
          <el-button type="primary" @click="handleCreate">新增内容</el-button>
        </div>
      </template>
      
      <!-- 搜索表单 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="标题">
          <el-input v-model="searchForm.title" placeholder="请输入标题"></el-input>
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="searchForm.category_id" placeholder="请选择分类">
            <el-option label="全部" value=""></el-option>
            <el-option 
              v-for="category in categories" 
              :key="category.id" 
              :label="category.name" 
              :value="category.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 内容列表 -->
    <el-card class="content-list">
      <el-table 
        :data="contentList" 
        v-loading="loading"
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="title" label="标题" width="200"></el-table-column>
        <el-table-column prop="category" label="分类" width="120"></el-table-column>
        <el-table-column prop="duration" label="时长" width="100">
          <template #default="{ row }">
            {{ formatDuration(row.duration) }}
          </template>
        </el-table-column>
        <el-table-column prop="play_count" label="播放量" width="100"></el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'danger'">
              {{ row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button size="mini" @click="handleEdit(row)">编辑</el-button>
            <el-button 
              size="mini" 
              :type="row.status === 1 ? 'warning' : 'success'"
              @click="handleChangeStatus(row)"
            >
              {{ row.status === 1 ? '禁用' : '启用' }}
            </el-button>
            <el-button size="mini" type="danger" @click="handleDelete(row.id)">删除</el-button>
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
        label-width="100px"
      >
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title"></el-input>
        </el-form-item>
        
        <el-form-item label="分类" prop="category_id">
          <el-select v-model="form.category_id" placeholder="请选择分类">
            <el-option 
              v-for="category in categories" 
              :key="category.id" 
              :label="category.name" 
              :value="category.id"
            ></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="类型" prop="type">
          <el-radio-group v-model="form.type">
            <el-radio label="video">视频</el-radio>
            <el-radio label="audio">音频</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="时长" prop="duration">
          <el-input-number v-model="form.duration" :min="0"></el-input-number>
        </el-form-item>
        
        <el-form-item label="试看时长" prop="preview_duration">
          <el-input-number v-model="form.preview_duration" :min="0" :max="300"></el-input-number>
        </el-form-item>
        
        <el-form-item label="解锁方式" prop="unlock_mode">
          <el-select v-model="form.unlock_mode">
            <el-option label="免费" value="free"></el-option>
            <el-option label="积分解锁" value="points"></el-option>
            <el-option label="付费购买" value="paid"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item v-if="form.unlock_mode === 'points'" label="所需积分">
          <el-input-number v-model="form.required_points" :min="0"></el-input-number>
        </el-form-item>
        
        <el-form-item v-if="form.unlock_mode === 'paid'" label="价格">
          <el-input-number v-model="form.price" :precision="2" :min="0"></el-input-number>
        </el-form-item>
        
        <el-form-item label="描述">
          <el-input 
            type="textarea" 
            v-model="form.description"
            :rows="4"
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
import { ElMessage, ElMessageBox } from 'element-plus'
import { contentApi } from '@/api/modules/content'

export default {
  name: 'ContentManagement',
  
  setup() {
    // 响应式数据
    const loading = ref(false)
    const dialogVisible = ref(false)
    const dialogTitle = ref('')
    const isEdit = ref(false)
    
    // 搜索表单
    const searchForm = reactive({
      title: '',
      category_id: '',
      status: ''
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
      title: '',
      category_id: '',
      type: 'video',
      duration: 0,
      preview_duration: 30,
      unlock_mode: 'free',
      required_points: 0,
      price: 0,
      description: ''
    })
    
    // 表单验证规则
    const formRules = {
      title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
      category_id: [{ required: true, message: '请选择分类', trigger: 'change' }]
    }
    
    // 数据列表
    const contentList = ref([])
    const categories = ref([
      { id: 1, name: '教育' },
      { id: 2, name: '娱乐' },
      { id: 3, name: '科技' },
      { id: 4, name: '生活' }
    ])
    
    // 方法
    const loadContentList = async () => {
      loading.value = true
      try {
        const response = await contentApi.getList({
          ...searchForm,
          page: pagination.currentPage,
          page_size: pagination.pageSize
        })
        
        contentList.value = response.data.contents || response.data
        pagination.total = response.data.total || response.data.length
      } catch (error) {
        ElMessage.error('加载内容列表失败')
      } finally {
        loading.value = false
      }
    }
    
    const handleSearch = () => {
      pagination.currentPage = 1
      loadContentList()
    }
    
    const resetSearch = () => {
      Object.keys(searchForm).forEach(key => {
        searchForm[key] = ''
      })
      handleSearch()
    }
    
    const handleCreate = () => {
      isEdit.value = false
      dialogTitle.value = '新增内容'
      Object.keys(form).forEach(key => {
        if (key !== 'id') {
          form[key] = key === 'type' ? 'video' : key === 'preview_duration' ? 30 : ''
        }
      })
      dialogVisible.value = true
    }
    
    const handleEdit = (row) => {
      isEdit.value = true
      dialogTitle.value = '编辑内容'
      Object.assign(form, row)
      dialogVisible.value = true
    }
    
    const handleChangeStatus = async (row) => {
      try {
        await contentApi.update(row.id, {
          status: row.status === 1 ? 0 : 1
        })
        ElMessage.success('状态更新成功')
        loadContentList()
      } catch (error) {
        ElMessage.error('状态更新失败')
      }
    }
    
    const handleDelete = async (id) => {
      try {
        await ElMessageBox.confirm('确定要删除这条内容吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        await contentApi.delete(id)
        ElMessage.success('删除成功')
        loadContentList()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除失败')
        }
      }
    }
    
    const handleSubmit = async () => {
      try {
        if (isEdit.value) {
          await contentApi.update(form.id, form)
          ElMessage.success('更新成功')
        } else {
          await contentApi.create(form)
          ElMessage.success('创建成功')
        }
        
        dialogVisible.value = false
        loadContentList()
      } catch (error) {
        ElMessage.error('操作失败')
      }
    }
    
    const handleSizeChange = (val) => {
      pagination.pageSize = val
      loadContentList()
    }
    
    const handleCurrentChange = (val) => {
      pagination.currentPage = val
      loadContentList()
    }
    
    const formatDuration = (seconds) => {
      const h = Math.floor(seconds / 3600)
      const m = Math.floor((seconds % 3600) / 60)
      const s = seconds % 60
      return h > 0 ? `${h}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}` : `${m}:${s.toString().padStart(2, '0')}`
    }
    
    // 生命周期
    onMounted(() => {
      loadContentList()
    })
    
    return {
      loading,
      dialogVisible,
      dialogTitle,
      searchForm,
      pagination,
      form,
      formRules,
      contentList,
      categories,
      loadContentList,
      handleSearch,
      resetSearch,
      handleCreate,
      handleEdit,
      handleChangeStatus,
      handleDelete,
      handleSubmit,
      handleSizeChange,
      handleCurrentChange,
      formatDuration
    }
  }
}
</script>

<style scoped>
.content-management {
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

.content-list {
  margin-bottom: 20px;
}
</style>
