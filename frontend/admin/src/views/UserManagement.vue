<template>
  <div class="user-management">
    <el-card class="header-card">
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
          <el-button type="primary" @click="handleCreate">新增用户</el-button>
        </div>
      </template>
      
      <!-- 搜索表单 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="用户名">
          <el-input v-model="searchForm.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="searchForm.phone" placeholder="请输入手机号"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 用户列表 -->
    <el-card class="user-list">
      <el-table 
        :data="userList" 
        v-loading="loading"
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="username" label="用户名" width="150"></el-table-column>
        <el-table-column prop="phone" label="手机号" width="150"></el-table-column>
        <el-table-column prop="integral" label="积分" width="100"></el-table-column>
        <el-table-column prop="level" label="等级" width="80"></el-table-column>
        <el-table-column prop="is_member" label="会员" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_member ? 'success' : 'info'">
              {{ row.is_member ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="注册时间" width="180"></el-table-column>
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'">
              {{ row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button size="mini" @click="handleEdit(row)">编辑</el-button>
            <el-button 
              size="mini" 
              :type="row.is_active ? 'warning' : 'success'"
              @click="handleChangeStatus(row)"
            >
              {{ row.is_active ? '禁用' : '启用' }}
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
      width="50%"
    >
      <el-form 
        :model="form" 
        :rules="formRules" 
        ref="formRef"
        label-width="100px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username"></el-input>
        </el-form-item>
        
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="form.phone"></el-input>
        </el-form-item>
        
        <el-form-item label="积分" prop="integral">
          <el-input-number v-model="form.integral" :min="0"></el-input-number>
        </el-form-item>
        
        <el-form-item label="等级" prop="level">
          <el-input-number v-model="form.level" :min="1" :max="10"></el-input-number>
        </el-form-item>
        
        <el-form-item label="会员" prop="is_member">
          <el-switch v-model="form.is_member"></el-switch>
        </el-form-item>
        
        <el-form-item label="状态" prop="is_active">
          <el-switch v-model="form.is_active"></el-switch>
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
import { userApi } from '@/api/modules/user'

export default {
  name: 'UserManagement',
  
  setup() {
    // 响应式数据
    const loading = ref(false)
    const dialogVisible = ref(false)
    const dialogTitle = ref('')
    const isEdit = ref(false)
    
    // 搜索表单
    const searchForm = reactive({
      username: '',
      phone: ''
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
      username: '',
      phone: '',
      integral: 0,
      level: 1,
      is_member: false,
      is_active: true
    })
    
    // 表单验证规则
    const formRules = {
      username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
      phone: [{ required: true, message: '请输入手机号', trigger: 'blur' }]
    }
    
    // 数据列表
    const userList = ref([])
    
    // 方法
    const loadUserList = async () => {
      loading.value = true
      try {
        const response = await userApi.getList({
          ...searchForm,
          page: pagination.currentPage,
          page_size: pagination.pageSize
        })
        
        userList.value = response.data.users || response.data
        pagination.total = response.data.total || response.data.length
      } catch (error) {
        ElMessage.error('加载用户列表失败')
      } finally {
        loading.value = false
      }
    }
    
    const handleSearch = () => {
      pagination.currentPage = 1
      loadUserList()
    }
    
    const resetSearch = () => {
      Object.keys(searchForm).forEach(key => {
        searchForm[key] = ''
      })
      handleSearch()
    }
    
    const handleCreate = () => {
      isEdit.value = false
      dialogTitle.value = '新增用户'
      Object.keys(form).forEach(key => {
        if (key !== 'id') {
          form[key] = key === 'level' ? 1 : key === 'is_member' ? false : key === 'is_active' ? true : ''
        }
      })
      dialogVisible.value = true
    }
    
    const handleEdit = (row) => {
      isEdit.value = true
      dialogTitle.value = '编辑用户'
      Object.assign(form, row)
      dialogVisible.value = true
    }
    
    const handleChangeStatus = async (row) => {
      try {
        await userApi.update(row.id, {
          is_active: !row.is_active
        })
        ElMessage.success('状态更新成功')
        loadUserList()
      } catch (error) {
        ElMessage.error('状态更新失败')
      }
    }
    
    const handleDelete = async (id) => {
      try {
        await ElMessageBox.confirm('确定要删除这个用户吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        await userApi.delete(id)
        ElMessage.success('删除成功')
        loadUserList()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除失败')
        }
      }
    }
    
    const handleSubmit = async () => {
      try {
        if (isEdit.value) {
          await userApi.update(form.id, form)
          ElMessage.success('更新成功')
        } else {
          await userApi.create(form)
          ElMessage.success('创建成功')
        }
        
        dialogVisible.value = false
        loadUserList()
      } catch (error) {
        ElMessage.error('操作失败')
      }
    }
    
    const handleSizeChange = (val) => {
      pagination.pageSize = val
      loadUserList()
    }
    
    const handleCurrentChange = (val) => {
      pagination.currentPage = val
      loadUserList()
    }
    
    // 生命周期
    onMounted(() => {
      loadUserList()
    })
    
    return {
      loading,
      dialogVisible,
      dialogTitle,
      searchForm,
      pagination,
      form,
      formRules,
      userList,
      loadUserList,
      handleSearch,
      resetSearch,
      handleCreate,
      handleEdit,
      handleChangeStatus,
      handleDelete,
      handleSubmit,
      handleSizeChange,
      handleCurrentChange
    }
  }
}
</script>

<style scoped>
.user-management {
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

.user-list {
  margin-bottom: 20px;
}
</style>
