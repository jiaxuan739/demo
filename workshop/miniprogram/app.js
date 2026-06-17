// app.js - 车间管理系统
App({
  globalData: {
    apiBase: 'http://localhost:8000',
    userInfo: null,
    userRole: null,     // 'admin' | 'user'

    // 状态映射
    statusMap: {
      'pending':     { label: '待处理',   icon: '⏳', color: 'warning' },
      'in_progress': { label: '进行中',   icon: '🔄', color: 'progress' },
      'completed':   { label: '已完成',   icon: '✅', color: 'completed' },
    }
  },

  onLaunch() {
    console.log('🏭 车间管理系统 v1.0 启动');
  },

  // 获取状态显示信息
  getStatus(status) {
    return this.globalData.statusMap[status] || { label: status, icon: '❓', color: '' };
  },

  // API 请求封装
  request(options) {
    return new Promise((resolve, reject) => {
      wx.request({
        url: `${this.globalData.apiBase}${options.url}`,
        method: options.method || 'GET',
        data: options.data || {},
        success: (res) => resolve(res.data),
        fail: reject
      });
    });
  }
});
