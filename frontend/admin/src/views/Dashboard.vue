<template>
  <div class="dashboard">
    <el-row :gutter="20" class="dashboard-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-item">
            <div class="stat-icon bg-blue">
              <el-icon><User /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">1,234</div>
              <div class="stat-label">总用户数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-item">
            <div class="stat-icon bg-green">
              <el-icon><VideoPlay /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">5,678</div>
              <div class="stat-label">总内容数</div>
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
              <div class="stat-number">98,765</div>
              <div class="stat-label">总积分</div>
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
              <div class="stat-number">1,234</div>
              <div class="stat-label">兑换数</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="dashboard-row">
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <span>用户增长趋势</span>
          </template>
          <div id="user-chart" style="height: 300px;"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <span>积分获取分布</span>
          </template>
          <div id="points-chart" style="height: 300px;"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="dashboard-row">
      <el-col :span="24">
        <el-card class="recent-activities">
          <template #header>
            <span>最近活动</span>
          </template>
          <el-table :data="recentActivities" style="width: 100%">
            <el-table-column prop="time" label="时间" width="180"></el-table-column>
            <el-table-column prop="user" label="用户" width="180"></el-table-column>
            <el-table-column prop="action" label="操作"></el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.status === '成功' ? 'success' : 'info'">{{ row.status }}</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { User, VideoPlay, Coin, ShoppingCart } from '@element-plus/icons-vue'

export default {
  name: 'Dashboard',
  components: {
    User, VideoPlay, Coin, ShoppingCart
  },
  setup() {
    const recentActivities = ref([
      { time: '2024-01-01 10:00', user: '张三', action: '观看视频', status: '成功' },
      { time: '2024-01-01 10:05', user: '李四', action: '答题', status: '成功' },
      { time: '2024-01-01 10:10', user: '王五', action: '兑换商品', status: '成功' },
      { time: '2024-01-01 10:15', user: '赵六', action: '签到', status: '成功' },
      { time: '2024-01-01 10:20', user: '钱七', action: '观看视频', status: '成功' }
    ])

    onMounted(() => {
      // 初始化图表
      initCharts()
    })

    const initCharts = () => {
      // 这里可以使用 ECharts 等图表库
      // 为演示目的，我们只做基本结构
      console.log('Initializing charts...')
    }

    return {
      recentActivities
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.dashboard-row {
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

.chart-card {
  height: 400px;
}

.recent-activities {
  min-height: 300px;
}
</style>
