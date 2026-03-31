<template>
  <div class="mall-management">
    <el-card class="header-card">
      <template #header>
        <div class="card-header">
          <span>商城管理</span>
          <el-button type="primary" @click="handleCreate">新增商品</el-button>
        </div>
      </template>
      
      <!-- 搜索表单 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="商品名称">
          <el-input v-model="searchForm.name" placeholder="请输入商品名称"></el-input>
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
        <el-form-item label="状态">
          <el-select v-model="searchForm.is_active" placeholder="请选择状态">
            <el-option label="全部" value=""></el-option>
            <el-option label="启用" value="true"></el-option>
            <el-option label="禁用" value="false"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 商品列表 -->
    <el-card class="product-list">
      <el-table 
        :data="productList" 
        v-loading="loading"
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="name" label="商品名称" width="200"></el-table-column>
        <el-table-column prop="category_name" label="分类" width="120"></el-table-column>
        <el-table-column prop="points_required" label="所需积分" width="120"></el-table-column>
        <el-table-column prop="stock_quantity" label="库存" width="100"></el-table-column>
        <el-table-column prop="max_exchange_per_user" label="限购" width="100"></el-table-column>
        <el-table-column prop="is_virtual" label="类型" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_virtual ? 'success' : 'info'">
              {{ row.is_virtual ? '虚拟' : '实物' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="validity_period_days" label="有效期" width="100">
          <template #default="{ row }">
            {{ row.validity_period_days ? row.validity_period_days + '天' : '永久' }}
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
            <el-button size="mini" @click="handleEdit(row)">编辑</el-button>
            <el-button size="mini" type="primary" @click="handleViewExchanges(row)">兑换记录</el-button>
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
      width="60%"
    >
      <el-form 
        :model="form" 
        :rules="formRules" 
        ref="formRef"
        label-width="120px"
      >
        <el-form-item label="商品名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入商品名称"></el-input>
        </el-form-item>
        
        <el-form-item label="商品描述">
          <el-input 
            type="textarea" 
            v-model="form.description"
            :rows="4"
            placeholder="请输入商品描述"
          ></el-input>
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
        
        <el-form-item label="所需积分" prop="points_required">
          <el-input-number v-model="form.points_required" :min="0"></el-input-number>
        </el-form-item>
        
        <el-form-item label="库存数量" prop="stock_quantity">
          <el-input-number v-model="form.stock_quantity" :min="0"></el-input-number>
        </el-form-item>
        
        <el-form-item label="单用户最大兑换次数">
          <el-input-number v-model="form.max_exchange_per_user" :min="0"></el-input-number>
        </el-form-item>
        
        <el-form-item label="商品类型">
          <el-radio-group v-model="form.is_virtual">
            <el-radio :label="true">虚拟商品</el-radio>
            <el-radio :label="false">实物商品</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item v-if="form.is_virtual" label="有效期天数">
          <el-input-number v-model="form.validity_period_days" :min="0" :max="3650"></el-input-number>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 兑换记录模态框 -->
    <el-dialog 
      title="兑换记录" 
      v-model="exchangeDialogVisible"
      width="80%"
    >
      <el-table 
        :data="exchangeRecords" 
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="user_id" label="用户ID" width="100"></el-table-column>
        <el-table-column prop="exchange_code" label="兑换码" width="150"></el-table-column>
        <el-table-column prop="points_deducted" label="扣除积分" width="120"></el-table-column>
        <el-table-column prop="quantity" label="数量" width="80"></el-table-column>
        <el-table-column prop="exchange_time" label="兑换时间" width="180"></el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="validity_end_date" label="有效期至" width="120"></el-table-column>
      </el-table>
      
      <el-pagination
        @size-change="handleExchangeSizeChange"
        @current-change="handleExchangeCurrentChange"
        :current-page="exchangePagination.currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="exchangePagination.pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="exchangePagination.total"
        style="margin-top: 20px;"
      >
      </el-pagination>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { mallApi } from '@/api/modules/mall'

export default {
  name: 'MallManagement',
  
  setup() {
    // 响应式数据
    const loading = ref(false)
    const dialogVisible = ref(false)
    const exchangeDialogVisible = ref(false)
    const dialogTitle = ref('')
    const isEdit = ref(false)
    
    // 搜索表单
    const searchForm = reactive({
      name: '',
      category_id: '',
      is_active: ''
    })
    
    // 分页信息
    const pagination = reactive({
      currentPage: 1,
      pageSize: 10,
      total: 0
    })
    
    // 兌换记录分页信息
    const exchangePagination = reactive({
      currentPage: 1,
      pageSize: 10,
      total: 0
    })
    
    // 表单数据
    const form = reactive({
      id: null,
      name: '',
      description: '',
      category_id: null,
      points_required: 0,
      stock_quantity: 0,
      max_exchange_per_user: 0,
      is_virtual: false,
      validity_period_days: 30
    })
    
    // 表单验证规则
    const formRules = {
      name: [{ required: true, message: '请输入商品名称', trigger: 'blur' }],
      category_id: [{ required: true, message: '请选择分类', trigger: 'change' }],
      points_required: [{ required: true, message: '请输入所需积分', trigger: 'blur' }],
      stock_quantity: [{ required: true, message: '请输入库存数量', trigger: 'blur' }]
    }
    
    // 数据列表
    const productList = ref([])
    const categories = ref([])
    const exchangeRecords = ref([])
    const currentProductId = ref(null)
    
    // 方法
    const loadProductList = async () => {
      loading.value = true
      try {
        const response = await mallApi.getList({
          ...searchForm,
          page: pagination.currentPage,
          page_size: pagination.pageSize
        })
        
        productList.value = response.data.products || response.data
        pagination.total = response.data.total || response.data.length
      } catch (error) {
        ElMessage.error('加载商品列表失败')
      } finally {
        loading.value = false
      }
    }
    
    const loadCategories = async () => {
      try {
        const response = await mallApi.getCategories()
        categories.value = response.data.categories || response.data
      } catch (error) {
        ElMessage.error('加载分类失败')
      }
    }
    
    const handleSearch = () => {
      pagination.currentPage = 1
      loadProductList()
    }
    
    const resetSearch = () => {
      Object.keys(searchForm).forEach(key => {
        searchForm[key] = ''
      })
      handleSearch()
    }
    
    const handleCreate = () => {
      isEdit.value = false
      dialogTitle.value = '新增商品'
      Object.keys(form).forEach(key => {
        if (key !== 'id') {
          form[key] = key === 'is_virtual' ? false : key === 'validity_period_days' ? 30 : 0
        }
      })
      dialogVisible.value = true
    }
    
    const handleEdit = (row) => {
      isEdit.value = true
      dialogTitle.value = '编辑商品'
      Object.assign(form, row)
      dialogVisible.value = true
    }
    
    const handleChangeStatus = async (row) => {
      try {
        await mallApi.update(row.id, {
          is_active: !row.is_active
        })
        ElMessage.success('状态更新成功')
        loadProductList()
      } catch (error) {
        ElMessage.error('状态更新失败')
      }
    }
    
    const handleDelete = async (id) => {
      try {
        await ElMessageBox.confirm('确定要删除这个商品吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        await mallApi.delete(id)
        ElMessage.success('删除成功')
        loadProductList()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除失败')
        }
      }
    }
    
    const handleSubmit = async () => {
      try {
        if (isEdit.value) {
          await mallApi.update(form.id, form)
          ElMessage.success('更新成功')
        } else {
          await mallApi.create(form)
          ElMessage.success('创建成功')
        }
        
        dialogVisible.value = false
        loadProductList()
      } catch (error) {
        ElMessage.error('操作失败')
      }
    }
    
    const handleViewExchanges = async (product) => {
      currentProductId.value = product.id
      try {
        const response = await mallApi.getExchangeRecords({
          product_id: product.id,
          page: exchangePagination.currentPage,
          page_size: exchangePagination.pageSize
        })
        
        exchangeRecords.value = response.data.records || response.data
        exchangePagination.total = response.data.total || response.data.length
        exchangeDialogVisible.value = true
      } catch (error) {
        ElMessage.error('加载兑换记录失败')
      }
    }
    
    const handleSizeChange = (val) => {
      pagination.pageSize = val
      loadProductList()
    }
    
    const handleCurrentChange = (val) => {
      pagination.currentPage = val
      loadProductList()
    }
    
    const handleExchangeSizeChange = (val) => {
      exchangePagination.pageSize = val
      handleViewExchanges({ id: currentProductId.value })
    }
    
    const handleExchangeCurrentChange = (val) => {
      exchangePagination.currentPage = val
      handleViewExchanges({ id: currentProductId.value })
    }
    
    const getStatusType = (status) => {
      const typeMap = {
        'pending': 'info',
        'confirmed': 'primary',
        'used': 'success',
        'cancelled': 'danger'
      }
      return typeMap[status] || 'info'
    }
    
    const getStatusText = (status) => {
      const textMap = {
        'pending': '待使用',
        'confirmed': '已确认',
        'used': '已使用',
        'cancelled': '已取消'
      }
      return textMap[status] || status
    }
    
    // 生命周期
    onMounted(() => {
      loadProductList()
      loadCategories()
    })
    
    return {
      loading,
      dialogVisible,
      exchangeDialogVisible,
      dialogTitle,
      searchForm,
      pagination,
      exchangePagination,
      form,
      formRules,
      productList,
      categories,
      exchangeRecords,
      loadProductList,
      loadCategories,
      handleSearch,
      resetSearch,
      handleCreate,
      handleEdit,
      handleChangeStatus,
      handleDelete,
      handleSubmit,
      handleViewExchanges,
      handleSizeChange,
      handleCurrentChange,
      handleExchangeSizeChange,
      handleExchangeCurrentChange,
      getStatusType,
      getStatusText
    }
  }
}
</script>

<style scoped>
.mall-management {
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

.product-list {
  margin-bottom: 20px;
}
</style>
